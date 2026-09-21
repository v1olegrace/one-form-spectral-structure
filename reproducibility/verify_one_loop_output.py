"""Independent recheck of saved inference and its binding to the saved data.

--reintegrate also repeats every distinct Arb source enclosure and benchmark.
Pure rational verification alone is available in spectral_weight_certificates.py
with python -S (no third-party libraries).
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

from one_loop_certified import certify_sample, certify_weight, cutoff_enclosure, upper_mass_from_ratio
from run_one_loop_certificates import (pair,quadratic_interval,observational_boxes,
                                       moment_weight_baseline)
from spectral_weight_certificates import verify_certificate


def verify(out,reintegrate=False):
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
    for d in datasets:
        observed,boxes=observational_boxes(d['samples'],d['noise'])
        assert observed==d['observations']
        assert boxes==[pair(x) for x in d['moment_intervals']]
        key=(d['kind'],d['r0'])
        if reintegrate and key not in reintegrated:
            for s in d['samples']:
                rerun=certify_sample(s['kind'],s['radius'],mass=s['mass'],coupling2=s['coupling2'],
                                    charge=s['charge'],t_max=s['t_max'],bits=s['bits'],
                                    tolerance=s['tolerance_goal'],
                                    max_relative_width=config['max_raw_relative_width'])
                assert rerun==s
            for cutoff,truth in d['direct_weight_benchmarks'].items():
                assert certify_weight(d['kind'],d['r0'],cutoff,bits=config['bits'],
                                      denominator=d['samples'][0])==truth
            reintegrated.add(key)
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
            'scope':'exact proof/data binding; Arb quadrature if requested; not general QED certification'}
    print(json.dumps(result,indent=2))
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1]/'output'/'certified_one_loop')
    parser.add_argument('--reintegrate',action='store_true')
    args=parser.parse_args()
    verify(args.out,args.reintegrate)
