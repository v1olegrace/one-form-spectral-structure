"""Failure semantics for required generators and CI regeneration checks."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ['analysis.py', 'laplace_geometry.py', 'extended_analysis.py',
           'falsification_suite.py', 'interval_bounds.py', 'figure_data.py']


@pytest.fixture
def driver(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('physics_make_driver', ROOT/'make.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    folder = tmp_path/'reproducibility'
    folder.mkdir()
    for script in SCRIPTS:
        (folder/script).touch()
    return module


@pytest.mark.parametrize('script', SCRIPTS)
def test_any_missing_required_generator_fails_before_running(driver, monkeypatch, script, capsys):
    (driver.ROOT/'reproducibility'/script).unlink()
    calls = []
    monkeypatch.setattr(driver, 'run', lambda *args, **kwargs: calls.append(args) or 0)
    assert driver.target_numerics() != 0
    assert not calls
    assert script in capsys.readouterr().out


def test_numerics_runs_each_required_generator_and_preserves_failure(driver, monkeypatch):
    calls = []
    def run(command, cwd):
        calls.append((command, cwd))
        return 7 if command[1] == 'extended_analysis.py' else 0
    monkeypatch.setattr(driver, 'run', run)
    assert driver.target_numerics() != 0
    assert [cmd[1] for cmd, cwd in calls] == SCRIPTS
    assert calls[-1][0][-1] == '--check'
    assert all(cwd == driver.ROOT/'reproducibility' for cmd, cwd in calls)


def test_ordinary_tests_report_skip_reasons(driver, monkeypatch):
    calls = []
    monkeypatch.setattr(driver, 'run', lambda command: calls.append(command) or 0)
    assert driver.target_test() == 0
    assert '-rs' in calls[0]


def test_ci_guards_regenerated_tracked_paths_and_retains_certified_no_skip():
    workflow = (ROOT/'.github/workflows/tests.yml').read_text(encoding='utf-8')
    numerical = workflow.split('- name: Numerical reproducibility', 1)[1].split('- name:', 1)[0]
    audit = workflow.split('- name: Audit ledgers rebuild cleanly', 1)[1].split('- name:', 1)[0]
    # line endings are ignored: csv writes CRLF on Linux, the committed files are LF (R6)
    assert 'git diff --ignore-cr-at-eol --exit-code --' in numerical
    guard = next(line for line in numerical.splitlines() if 'git diff --ignore-cr-at-eol --exit-code --' in line)
    for path in ('output/data', 'manuscript/numerical_results.qmd', 'paper/figures'):
        assert path in guard
    # Environment-dependent artifacts are excluded on evidence, not for convenience:
    # a fresh-venv clean room changed only these (see .agent/reports/P13.md).
    assert "':(exclude)output/data/extended_verification.json'" in guard
    assert 'output/figures' not in guard
    # The excluded files are still compared, on scientific content (R6: Windows and Ubuntu).
    for name in ('localizing_bounds.csv', 'uncertainty_summary.json', 'verification_checks.json'):
        assert f"':(exclude)output/data/{name}'" in guard and name in numerical
    assert 'git show "HEAD:output/data/$f"' in numerical
    assert 'python scripts/compare_numerical_outputs.py $args' in numerical
    assert 'git diff --ignore-cr-at-eol --exit-code --' in audit
    for path in ('data/literature_audit.csv', 'data/claims_matrix.csv', 'data/theorem_status.csv'):
        assert path in audit
    assert 'run: python -m pytest tests -q -rs' in workflow
    assert 'if grep -q "skipped" pytest.out;' in workflow


def test_numerical_output_comparator_policy(tmp_path):
    sys.path.insert(0, str(ROOT/'scripts'))
    import compare_numerical_outputs as cmp
    base = json.loads((ROOT/'output/data/extended_verification.json').read_text(encoding='utf-8'))
    assert cmp.differences(base, base) == []
    new = json.loads(json.dumps(base))
    new['environment']['scipy'] = '0.0.0'
    new['mellin'][0]['outer_quad_error_estimate'] *= 1.000001
    x = new['mellin'][0]['relative_difference']
    new['mellin'][0]['relative_difference'] = x * (1 + 2.2e-16)            # one ulp: accepted
    assert cmp.differences(base, new) == []
    new['mellin'][0]['relative_difference'] = x * (1 + 1e-13)             # 450 ulp: reported
    new['quadrature'][0]['Gamma'] += '1'                                  # strings are exact
    assert [d.split(':')[0] for d in cmp.differences(base, new)] == ['mellin[0].relative_difference',
                                                                    'quadrature[0].Gamma']
    # CSV: round-off diagnostics are skipped, other columns compared
    head = 'K,upper_bound_s0,gate_status,float64_relative_difference'
    a, b, c = tmp_path/'a.csv', tmp_path/'b.csv', tmp_path/'c.csv'
    a.write_text('\n'.join([head, '3,4.45198285022805,CHECKED_COMPATIBLE,7.06e-14', '']), encoding='utf-8')
    b.write_text('\n'.join([head, '3,4.45198285022805,CHECKED_COMPATIBLE,6.97e-14', '']), encoding='utf-8')
    c.write_text('\n'.join([head, '3,4.45198285022806,CHECKED_COMPATIBLE,7.06e-14', '']), encoding='utf-8')
    assert cmp.main([str(a), str(b)]) == 0
    assert cmp.main([str(a), str(c)]) == 1
