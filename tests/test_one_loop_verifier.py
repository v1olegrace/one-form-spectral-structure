"""End-to-end binding, completeness, duplicate-source and read-only checks."""
from copy import deepcopy
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import shutil
import subprocess
import sys

import pytest

pytest.importorskip("flint", reason="Install reproducibility/requirements-certified.txt")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import run_one_loop_certificates as runner
from verify_one_loop_output import verify, verify_hierarchy_record, verified_effective_mass


@pytest.fixture(scope="module")
def base_output(tmp_path_factory):
    """Build the reduced benchmark once; each test mutates its own copy."""
    config = deepcopy(runner.CONFIG)
    config.update(models=['dirac'], reference_radii=['1', '2'], spacing='1',
                  sample_count=2, degrees=[1], mass_cutoffs=['3'],
                  raw_absolute_error_relative_to_reference=['0', '1e-3'])
    original, runner.CONFIG = runner.CONFIG, config
    try:
        out = tmp_path_factory.mktemp("certified_base")
        runner.main(out)
    finally:
        runner.CONFIG = original
    return out


@pytest.fixture()
def small_output(base_output, tmp_path):
    target = tmp_path / "out"
    shutil.copytree(base_output, target)
    return target


def test_overlapping_samples_counted_and_reintegrated_once(small_output):
    summary = json.loads((small_output/'summary.json').read_text())
    # 2 radii x 2 samples = 4 evaluations, of which 3 are distinct inputs.
    assert summary['source_enclosure_evaluations'] == 4
    assert summary['distinct_source_enclosures'] == 3
    # Counters that are NOT the source count: benchmark integrals and the
    # independent mpmath cross-checks are reported separately.
    assert summary['weight_benchmark_evaluations'] == 2
    assert summary['weight_benchmark_integrals'] == 2
    assert summary['distinct_weight_benchmarks'] == 2
    assert summary['independent_quadrature_checks'] == 4
    result = verify(small_output, reintegrate=True, write_result=False)
    assert result['source_samples_reintegrated'] == 3
    assert result['distinct_source_samples_checked'] == 3
    assert result['comparison_table_complete'] and result['certificate_index_bijection']
    assert not (small_output/'verification.json').exists()


def _load(path):
    return json.loads(path.read_text())


def _store(path, value):
    path.write_text(json.dumps(value), encoding='utf-8')


def test_dropped_comparison_row_is_refused(small_output):
    """A row removed together with its counter passed every earlier assertion."""
    path = small_output/'comparison.json'
    rows = _load(path)
    assert len(rows) > 1
    _store(path, rows[:-1])
    summary_path = small_output/'summary.json'
    summary = _load(summary_path)
    summary['comparison_rows'] = len(rows) - 1
    _store(summary_path, summary)
    with pytest.raises(AssertionError, match='Comparison table is incomplete'):
        verify(small_output, write_result=False)


@pytest.mark.parametrize('field', ['sampled_hierarchy', 'effective_mass'])
def test_modified_headline_mass_is_refused(small_output, field):
    path = small_output/'comparison.json'
    rows = _load(path)
    if field == 'sampled_hierarchy':
        row = next(r for r in rows if r[field]['status'] == 'CERTIFIED_UPPER_BOUND')
        row[field]['upper_mass'] = '-999'
    else:
        row = next(r for r in rows if r[field]['best_upper_mass'] is not None)
        row[field]['best_upper_mass'] = '-999'
    _store(path, rows)
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


def test_modified_weight_width_is_refused(small_output):
    path = small_output/'comparison.json'
    rows = _load(path)
    rows[0]['weight_width'] = '-999'
    _store(path, rows)
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


def test_dropped_configured_radius_group_is_refused(small_output):
    """Internally consistent remaining files cannot redefine configuration."""
    data = [d for d in _load(small_output/'datasets.json') if d['r0'] == '1']
    ids = {d['id'] for d in data}
    rows = [r for r in _load(small_output/'comparison.json') if r['dataset_id'] in ids]
    old_certificates = _load(small_output/'weight_certificates.json')
    certificates = []
    for row in rows:
        for kind in ('lower', 'upper'):
            record = old_certificates[row[f'{kind}_certificate_index']]
            row[f'{kind}_certificate_index'] = len(certificates)
            certificates.append(record)
    summary = _load(small_output/'summary.json')
    for counter in ('source_enclosure_evaluations', 'distinct_source_enclosures',
                    'weight_benchmark_evaluations', 'weight_benchmark_integrals',
                    'distinct_weight_benchmarks', 'independent_quadrature_checks'):
        summary[counter] = 2 if 'source' in counter or counter == 'independent_quadrature_checks' else 1
    summary.update(datasets=len(data), comparison_rows=len(rows),
                   exact_weight_certificates=len(certificates),
                   positive_weight_lower_rows=sum(F(r['weight_lower']) > 0 for r in rows),
                   hierarchy_no_bound_rows=sum(r['sampled_hierarchy']['status'] == 'NO_BOUND' for r in rows))
    for name, value in [('datasets', data), ('comparison', rows),
                        ('weight_certificates', certificates), ('summary', summary)]:
        _store(small_output/f'{name}.json', value)
    with pytest.raises(AssertionError, match='Configured dataset inventory'):
        verify(small_output, write_result=False)


@pytest.mark.parametrize('field,omitted', [('models', 'scalar'), ('reference_radii', '3'),
                                         ('raw_absolute_error_relative_to_reference', '1e-2')])
def test_each_configured_dataset_axis_must_be_complete(small_output, field, omitted):
    """A declared model, radius or noise level cannot have zero saved data."""
    path = small_output/'configuration.json'
    config = _load(path)
    config[field].append(omitted)
    _store(path, config)
    summary_path = small_output/'summary.json'
    summary = _load(summary_path)
    summary['configuration_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    _store(summary_path, summary)
    with pytest.raises(AssertionError, match='Configured dataset inventory'):
        verify(small_output, write_result=False)


@pytest.mark.parametrize('intervals', [
    [(F(1), F(1)), (F(0), F(1))],  # uncertain/nonpositive numerator
    [(F(1), F(1)), (F(2), F(2))],  # ratio outside the support-domain constraint
    [(F(0), F(0)), (F(1), F(1))],  # midpoint pencil cannot supply a vector
])
def test_genuine_hierarchy_refusals_and_their_reasons(intervals):
    record = runner.sampled_gap_bound(intervals, F(1), 0)
    assert record['status'] == 'NO_BOUND'
    verify_hierarchy_record(record, intervals, F(1), 0)
    record['reason'] = 'invented refusal'
    with pytest.raises(AssertionError):
        verify_hierarchy_record(record, intervals, F(1), 0)


def test_solver_failure_cannot_replace_a_successful_fixed_vector():
    intervals = [(F(1), F(1)), (F(1, 2), F(1, 2))]
    forged = {'status': 'NO_BOUND', 'reason': 'midpoint pencil not positive definite'}
    with pytest.raises(AssertionError, match='Unjustified midpoint-pencil refusal'):
        verify_hierarchy_record(forged, intervals, F(1), 0)


@pytest.mark.parametrize('intervals', [
    [(F(1), F(1)), (F(0), F(1))],
    [(F(1), F(1)), (F(2), F(2))],
    [(F(1), F(1)), (F(1, 2), F(1, 2)), (F(1, 8), F(1, 8))],
])
def test_effective_summary_keeps_all_outcomes_and_exact_minimum(intervals):
    actual = verified_effective_mass(intervals, F(1))
    assert actual == runner.effective_mass_bounds(intervals, F(1))
    assert [pair['j'] for pair in actual['pairs']] == list(range(len(intervals)-1))


@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'wrong_order', 'bad_reason'])
def test_hierarchy_inventory_and_status_are_bound(small_output, mutation):
    path = small_output/'comparison.json'
    rows = _load(path)
    scan = rows[0]['hierarchy_all_orders']
    if mutation == 'missing':
        scan.pop()
    elif mutation == 'duplicate':
        scan.append(deepcopy(scan[0]))
    elif mutation == 'wrong_order':
        scan[0]['order'] = 42
    else:
        scan[0].update(status='NO_BOUND', reason='invented refusal')
    _store(path, rows)
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'bad_reason', 'false_status'])
def test_effective_pair_inventory_and_status_are_bound(small_output, mutation):
    path = small_output/'comparison.json'
    rows = _load(path)
    pairs = rows[0]['effective_mass']['pairs']
    if mutation == 'missing':
        pairs.pop()
    elif mutation == 'duplicate':
        pairs.append(deepcopy(pairs[0]))
    elif mutation == 'bad_reason':
        pairs[0].update(status='NO_BOUND', reason='invented refusal')
    else:
        pairs[0]['status'] = 'UNKNOWN'
    _store(path, rows)
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


def test_available_prefix_cannot_be_changed(small_output):
    path = small_output/'comparison.json'
    rows = _load(path)
    rows[0]['available_samples'] -= 1
    _store(path, rows)
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


def test_duplicated_combination_is_refused(small_output):
    """Cardinality is preserved, so only the cartesian-product check catches it."""
    path = small_output/'comparison.json'
    rows = _load(path)
    assert len(rows) > 1
    rows[1] = dict(rows[0])
    _store(path, rows)
    with pytest.raises(AssertionError, match='Comparison table is incomplete'):
        verify(small_output, write_result=False)


def test_certificate_index_must_be_a_bijection(small_output):
    """Two rows pointing at one certificate survives a pure length check."""
    path = small_output/'comparison.json'
    rows = _load(path)
    assert len(rows) > 1
    rows[1]['lower_certificate_index'] = rows[0]['lower_certificate_index']
    _store(path, rows)
    with pytest.raises(AssertionError, match='not a bijection'):
        verify(small_output, write_result=False)


def test_dropped_certificate_is_refused(small_output):
    path = small_output/'weight_certificates.json'
    records = _load(path)
    _store(path, records[:-1])
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


@pytest.mark.parametrize('counter', ['source_enclosure_evaluations',
                                     'distinct_source_enclosures',
                                     'weight_benchmark_evaluations',
                                     'weight_benchmark_integrals',
                                     'distinct_weight_benchmarks',
                                     'independent_quadrature_checks',
                                     'comparison_rows',
                                     'exact_weight_certificates',
                                     'datasets',
                                     'positive_weight_lower_rows',
                                     'hierarchy_no_bound_rows'])
def test_every_provenance_counter_is_recomputed(small_output, counter):
    """Each advertised count must be rebuilt from the data, not trusted."""
    path = small_output/'summary.json'
    summary = _load(path)
    assert counter in summary, counter
    summary[counter] = summary[counter] + 1
    _store(path, summary)
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


def test_independent_check_flag_cannot_be_falsified(small_output):
    path = small_output/'datasets.json'
    data = _load(path)
    data[0]['independent_checks'][0]['inside_enclosure'] = False
    _store(path, data)
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


def test_conflicting_duplicate_is_not_skipped(small_output):
    path = small_output/'datasets.json'
    data = json.loads(path.read_text())
    # Same source in the next noise dataset: old group-level caching skipped it.
    data[1]['samples'][0]['backend'] = 'unverified replacement'
    path.write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(AssertionError, match='Conflicting repeated source'):
        verify(small_output, reintegrate=True, write_result=False)


def test_dataset_sample_must_match_declared_radius(small_output):
    path = small_output/'datasets.json'
    data = json.loads(path.read_text())
    data[0]['samples'][0]['radius'] = '5'
    path.write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(AssertionError):
        verify(small_output, write_result=False)


def test_conflicting_duplicate_weight_benchmark_is_not_skipped(small_output):
    path = small_output/'datasets.json'
    data = json.loads(path.read_text())
    data[1]['direct_weight_benchmarks']['3']['lower'] = '0'
    path.write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(AssertionError, match='Conflicting repeated weight benchmark'):
        verify(small_output, reintegrate=True, write_result=False)


def test_optimized_python_cannot_silently_disable_verification(tmp_path):
    root = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, '-O', str(root/'reproducibility/verify_one_loop_output.py'),
         '--out', str(tmp_path), '--no-write'], capture_output=True, text=True)
    assert proc.returncode != 0
    assert 'do not use python -O' in proc.stderr
