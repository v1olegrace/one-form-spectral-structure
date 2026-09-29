"""Independent recheck of saved inference and its binding to the saved data.

Three separate obligations, all enforced here:

  binding      every stored record is recomputed from the declared inputs and
               the inputs themselves are tied to configuration.json;
  completeness the comparison table covers datasets x degrees x cutoffs, the
               certificate indices are a bijection, and every provenance
               counter in summary.json is recomputed.  Presence alone is not
               enough: a silently dropped row must be refused;
  provenance   repeated sources are deduplicated by full parameters and every
               occurrence is compared, not only the first.

--reintegrate also repeats every distinct Arb source enclosure and benchmark.
Pure rational verification alone is available in spectral_weight_certificates.py
with python -S (no third-party libraries).
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

from one_loop_certified import (certify_sample, certify_weight, cutoff_enclosure,
                                upper_mass_from_ratio, sample_input_key)
from run_one_loop_certificates import (pair,quadratic_interval,observational_boxes,
                                       moment_weight_baseline)
from spectral_weight_certificates import verify_certificate


def verify(out,reintegrate=False,write_result=True):
    # This verifier uses assertions for proof/data binding. Never allow -O to
    # disable them while still emitting PASS.
    if not __debug__:
        raise RuntimeError("Verification requires assertions; do not use python -O")
    def load(name):
        return json.loads((out/name).read_text(encoding='utf-8'))
    config=load('configuration.json')
    datasets=load('datasets.json')
    rows=load('comparison.json')
    certificates=load('weight_certificates.json')
    summary=load('summary.json')
    assert hashlib.sha256((out/'configuration.json').read_bytes()).hexdigest()==summary['configuration_sha256']
    byid={d['id']:d for d in datasets}
    assert len(byid)==len(datasets)
    reintegrated=set()
    sources={}
    source_records={}
    benchmark_records={}
    benchmark_reruns={}
    for d in datasets:
        assert d['kind'] in config['models']
        assert d['r0'] in config['reference_radii']
        assert F(d['spacing']) == F(config['spacing'])
        assert d['noise'] in config['raw_absolute_error_relative_to_reference']
        assert len(d['samples']) == config['sample_count']
        assert set(d['direct_weight_benchmarks']) == set(config['mass_cutoffs'])
        for j,s in enumerate(d['samples']):
            assert s['kind'] == d['kind']
            assert F(s['radius']) == F(d['r0']) + j*F(d['spacing'])
            for field in ('mass','coupling2','charge','t_max'):
                assert F(s[field]) == F(config[field])
            assert s['bits'] == config['bits']
            assert F(s['tolerance_goal']) == F(config['quadrature_tolerance'])
            identity=sample_input_key(s)
            if identity in source_records:
                assert source_records[identity] == s, "Conflicting repeated source enclosure"
            source_records[identity]=s
            if reintegrate:
                if identity not in sources:
                    sources[identity]=certify_sample(s['kind'],s['radius'],mass=s['mass'],
                        coupling2=s['coupling2'],charge=s['charge'],t_max=s['t_max'],
                        bits=s['bits'],tolerance=s['tolerance_goal'],
                        max_relative_width=config['max_raw_relative_width'])
                # Check every occurrence, including datasets differing only in noise.
                assert sources[identity] == s, "Source re-integration mismatch"
        observed,boxes=observational_boxes(d['samples'],d['noise'])
        assert observed==d['observations']
        assert boxes==[pair(x) for x in d['moment_intervals']]
        key=(d['kind'],d['r0'])
        for cutoff,truth in d['direct_weight_benchmarks'].items():
            identity=(sample_input_key(d['samples'][0]), F(cutoff))
            if identity in benchmark_records:
                assert benchmark_records[identity] == truth, "Conflicting repeated weight benchmark"
            benchmark_records[identity]=truth
            if reintegrate:
                if identity not in benchmark_reruns:
                    benchmark_reruns[identity]=certify_weight(d['kind'],d['r0'],cutoff,
                        bits=config['bits'],denominator=d['samples'][0])
                assert benchmark_reruns[identity] == truth
        assert {c['j'] for c in d['independent_checks']} == set(range(config['sample_count']))
        assert all(c['inside_enclosure'] for c in d['independent_checks'])
        if reintegrate:
            reintegrated.add(key)

    # --- cardinalities and completeness -----------------------------------
    # Binding what is present is not enough: a silently dropped comparison row
    # or a certificate referenced twice must also be refused.
    groups = {(d['kind'], d['r0']) for d in datasets}
    cutoffs_integrated = sum(F(c) > 2*F(config['mass']) for c in config['mass_cutoffs'])
    assert summary['datasets'] == len(datasets)
    assert summary['distinct_source_enclosures'] == len(source_records)
    assert summary['source_enclosure_evaluations'] == len(groups)*config['sample_count']
    assert summary['independent_quadrature_checks'] == len(groups)*config['sample_count']
    assert summary['weight_benchmark_evaluations'] == len(groups)*len(config['mass_cutoffs'])
    assert summary['weight_benchmark_integrals'] == len(groups)*cutoffs_integrated
    assert summary['distinct_weight_benchmarks'] == len(benchmark_records)
    assert summary['comparison_rows'] == len(rows)
    assert summary['exact_weight_certificates'] == len(certificates)
    assert len(datasets) == len(groups)*len(config['raw_absolute_error_relative_to_reference'])
    assert {(r['dataset_id'], r['degree'], r['mass_cutoff']) for r in rows} == {
        (d['id'], g, c) for d in datasets
        for g in config['degrees'] for c in config['mass_cutoffs']}, "Comparison table is incomplete"
    assert len(rows) == len(datasets)*len(config['degrees'])*len(config['mass_cutoffs'])
    assert len(certificates) == 2*len(rows)
    used = sorted([r['lower_certificate_index'] for r in rows]
                  + [r['upper_certificate_index'] for r in rows])
    assert used == list(range(len(certificates))), \
        "Certificate indices are not a bijection onto the stored certificates"
    assert summary['positive_weight_lower_rows'] == sum(F(x['weight_lower']) > 0 for x in rows)
    assert summary['hierarchy_no_bound_rows'] == sum(
        x['sampled_hierarchy']['status'] == 'NO_BOUND' for x in rows)

    for record in certificates:
        verify_certificate(record)
    for row in rows:
        d=byid[row['dataset_id']]
        boxes=[pair(x) for x in d['moment_intervals'][:row['available_samples']]]
        zlo,zhi=cutoff_enclosure(row['mass_cutoff'],d['spacing'],bits=config['bits'])
        stored_zlo,stored_zhi=pair(row['cutoff_y'])
        assert stored_zlo <= zlo <= zhi <= stored_zhi
        for kind,cutoff in [('lower',stored_zhi),('upper',stored_zlo)]:
            record=certificates[row[f'{kind}_certificate_index']]
            assert record['kind']==kind and record['degree']==row['degree']
            assert F(record['cutoff'])==cutoff
            assert [pair(x) for x in record['moment_intervals']]==boxes
            assert record['bound']==row[f'weight_{kind}']
        assert row['truth']==d['direct_weight_benchmarks'][row['mass_cutoff']]
        assert F(row['weight_lower']) <= F(row['truth']['lower']) <= F(row['truth']['upper']) <= F(row['weight_upper'])
        assert row['moment_weight_baseline']==moment_weight_baseline(boxes,stored_zlo,stored_zhi)
        for record in row['hierarchy_all_orders']:
            if 'vector' not in record:
                assert record['status']=='NO_BOUND'
                continue
            vector=[F(x) for x in record['vector']]
            num=quadratic_interval(vector,boxes,1)
            den=quadratic_interval(vector,boxes)
            assert num==pair(record['numerator']) and den==pair(record['denominator'])
            if record['status']=='CERTIFIED_UPPER_BOUND':
                assert num[0]>0 and den[0]>0
                ratio=num[0]/den[1]
                assert F(record['ratio_lower'])==ratio
                assert F(record['upper_mass'])==upper_mass_from_ratio(ratio,d['spacing'])
        successful=[x for x in row['hierarchy_all_orders'] if x['status']=='CERTIFIED_UPPER_BOUND']
        best=min(successful,key=lambda x:F(x['upper_mass'])) if successful else None
        assert best==row['hierarchy_best_available']
        for record in row['effective_mass']['pairs']:
            if record['status']=='CERTIFIED_UPPER_BOUND':
                j=record['j']
                ratio=boxes[j+1][0]/boxes[j][1]
                assert F(record['ratio_lower'])==ratio
                assert F(record['upper_mass'])==upper_mass_from_ratio(ratio,d['spacing'])
    result={'status':'PASS','data_sets_checked':len(datasets),'weight_certificates_checked':len(certificates),
            'comparison_rows_checked':len(rows),'source_pairs_reintegrated':len(reintegrated),
            'distinct_source_samples_checked':len(source_records),
            'source_samples_reintegrated':len(sources),
            'distinct_weight_benchmarks_checked':len(benchmark_records),
            'weight_benchmarks_reintegrated':len(benchmark_reruns),
            'cardinalities_checked':True,
            'comparison_table_complete':True,
            'certificate_index_bijection':True,
            'scope':'exact proof/data binding; Arb quadrature if requested; not general QED certification'}
    print(json.dumps(result,indent=2))
    if write_result:
        (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1]/'output'/'certified_one_loop')
    parser.add_argument('--reintegrate',action='store_true')
    parser.add_argument('--no-write',action='store_true',help='Read-only audit; do not rewrite verification.json')
    args=parser.parse_args()
    verify(args.out,args.reintegrate,write_result=not args.no_write)
