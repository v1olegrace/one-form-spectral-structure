"""Matched-data experiment: continuum samples, weight certificates, gap bounds.

Run from any directory. Configuration is saved before computing observations.
Inference functions receive only moment boxes, h and declared cuts, never the
spectral density, true support edge, or direct-integral benchmark values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path

import flint
import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import eigh

from one_loop_certified import (certify_sample, certify_weight, cutoff_enclosure,
                                interval_record, upper_mass_from_ratio)
from spectral_weight_certificates import (normalize_sample_intervals,
                                          propose_certificate, verify_certificate)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "output" / "certified_one_loop"
CONFIG = {
    "models": ["dirac", "scalar"], "mass": "1", "coupling2": "1", "charge": "1",
    "reference_radii": ["1", "2"], "spacing": "1/4", "sample_count": 10,
    "degrees": [3, 5, 7, 9], "mass_cutoffs": ["5/2", "3", "4"],
    "raw_absolute_error_relative_to_reference": ["0", "1e-6", "1e-3"],
    "bits": 160, "t_max": "8", "quadrature_tolerance": "1e-28",
    "max_raw_relative_width": "1e-20", "bernstein_subdivisions_per_side": 8,
    "cutoff_rounding_denominator": 10**12,
    "noise": "deterministic alternating half-envelope shift; no statistical coverage claim",
    "selection": "configuration fixed before first benchmark; no scan to choose favorable cuts",
}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pair(record):
    return F(record["lower"]), F(record["upper"])


def linear_interval(coefficients, intervals):
    lo, hi = F(0), F(0)
    for c, (left, right) in zip(coefficients, intervals):
        lo += c * (left if c >= 0 else right)
        hi += c * (right if c >= 0 else left)
    return lo, hi


def quadratic_interval(v, intervals, shift=0):
    # Aggregate identical moments first: p(y)^2 = sum_l c_l y^l.
    coefficients = [F(0)]*(2*len(v)-1)
    for i, vi in enumerate(v):
        for j, vj in enumerate(v):
            coefficients[i+j] += vi*vj
    return linear_interval(coefficients, intervals[shift:])


def sampled_gap_bound(intervals, h, order):
    n = order+1
    if len(intervals) != 2*n:
        raise ValueError("K requires exactly 2K+2 shared samples")
    mids = [float((a+b)/2) for a,b in intervals]
    c0 = np.array([[mids[i+j] for j in range(n)] for i in range(n)])
    c1 = np.array([[mids[i+j+1] for j in range(n)] for i in range(n)])
    try:
        values, vectors = eigh(c1, c0)
    except np.linalg.LinAlgError:
        return {"status": "NO_BOUND", "reason": "midpoint pencil not positive definite"}
    vfloat = vectors[:,-1]
    vfloat = vfloat/np.max(np.abs(vfloat))
    v = [F(str(float(x))) for x in vfloat]  # now exact, arbitrary test vector
    num = quadratic_interval(v, intervals, 1)
    den = quadratic_interval(v, intervals, 0)
    result = {
        "vector": [str(x) for x in v], "numerator": interval_record(num),
        "denominator": interval_record(den), "nominal_eigenvalue": float(values[-1]),
        "order": order, "status": "NO_BOUND",
    }
    if num[0] <= 0 or den[0] <= 0:
        return dict(result, reason="uncertainty does not certify positive numerator and denominator")
    ell = num[0]/den[1]
    if not 0 < ell <= 1:
        return dict(result, reason="ratio outside valid range")
    result.update(status="CERTIFIED_UPPER_BOUND", ratio_lower=str(ell),
                  upper_mass=str(upper_mass_from_ratio(ell, h)),
                  scope="one-sided support-edge upper bound from a fixed rational test vector")
    return result


def effective_mass_bounds(intervals, h):
    bounds=[]
    for j in range(len(intervals)-1):
        a,b=intervals[j],intervals[j+1]
        if a[0] <= 0 or b[0] <= 0:
            bounds.append({"j":j,"status":"NO_BOUND","reason":"nonpositive sample lower endpoint"})
            continue
        ell=b[0]/a[1]
        if not 0 < ell <= 1:
            bounds.append({"j":j,"status":"NO_BOUND","reason":"ratio outside valid range"})
            continue
        bounds.append({"j":j,"status":"CERTIFIED_UPPER_BOUND", "ratio_lower":str(ell),
                       "upper_mass":str(upper_mass_from_ratio(ell,h))})
    valid=[F(x['upper_mass']) for x in bounds if 'upper_mass' in x]
    return {"pairs":bounds,"best_upper_mass":str(min(valid)) if valid else None}


def moment_weight_baseline(intervals,z_lower,z_upper):
    lower,upper=F(0),F(1)
    for j,(lo,hi) in enumerate(intervals[1:],1):
        lower=max(lower,(lo-z_upper**j)/(1-z_upper**j))
        upper=min(upper,hi/z_lower**j)
    return {"lower":str(lower),"upper":str(upper)}


def observational_boxes(samples, eta):
    """Raw quadrature error + known deterministic observational envelope.

    observation = midpoint + (-1)^j delta/2.  Valid error radius is delta
    plus quadrature radius; delta = eta times midpoint of raw reference.
    The truth therefore belongs to every emitted box. Normalization propagates
    uncertainty in the same reference observation and retains b0 exactly one.
    """
    exact_boxes=[pair(x['raw']) for x in samples]
    delta=F(eta)*sum(exact_boxes[0])/2
    rows,boxes=[],[]
    for j,(lo,hi) in enumerate(exact_boxes):
        mid=(lo+hi)/2
        shift=((-1)**j)*delta/2
        observed=mid+shift
        error=delta+(hi-lo)/2
        obs=(max(F(0),observed-error),observed+error)
        assert obs[0] <= lo <= hi <= obs[1]
        boxes.append(obs)
        rows.append({"observation":str(observed),"numerical_radius":str((hi-lo)/2),
                     "declared_observation_error":str(delta), "box":interval_record(obs)})
    return rows, normalize_sample_intervals(boxes)


def main(out):
    start=datetime.now(timezone.utc).isoformat()
    tic=time.perf_counter()
    out.mkdir(parents=True,exist_ok=True)
    save(out/'configuration.json',CONFIG)  # before observations
    config_hash=hashlib.sha256((out/'configuration.json').read_bytes()).hexdigest()
    h=F(CONFIG['spacing'])
    cuts={}
    for cut in CONFIG['mass_cutoffs']:
        lo,hi=cutoff_enclosure(cut,h,bits=CONFIG['bits'])
        scale=CONFIG['cutoff_rounding_denominator']
        lo=F((lo*scale).__floor__(),scale)
        hi=F((hi*scale).__ceil__(),scale)
        cuts[cut]=(lo,hi)
    datasets=[]
    records=[]
    rows=[]
    mp.mp.dps=70
    from spectral_models import build_models
    legacy=build_models()
    for kind in CONFIG['models']:
        for r0text in CONFIG['reference_radii']:
            r0=F(r0text)
            samples=[certify_sample(kind,r0+j*h,bits=CONFIG['bits'],
                      t_max=CONFIG['t_max'],tolerance=CONFIG['quadrature_tolerance'],
                      max_relative_width=CONFIG['max_raw_relative_width'])
                     for j in range(CONFIG['sample_count'])]
            direct={cut:certify_weight(kind,r0,cut,bits=CONFIG['bits'],denominator=samples[0])
                    for cut in CONFIG['mass_cutoffs']}
            # Independent high-precision check; a check, not the certificate source.
            legacy_model=legacy['D_dirac' if kind=='dirac' else 'E_scalar']
            checks=[]
            for j,sample in enumerate(samples):
                rr=mp.mpf(str(r0.numerator))/r0.denominator + j*mp.mpf(h.numerator)/h.denominator
                value=legacy_model.Phi_scaled(rr)*mp.exp(-2*rr)
                lo,hi=pair(sample['raw'])
                passed=mp.mpf(lo.numerator)/lo.denominator <= value <= mp.mpf(hi.numerator)/hi.denominator
                if not passed:
                    raise AssertionError('Independent quadrature outside validated enclosure')
                checks.append({'j':j,'status':'CHECKED','legacy_value':mp.nstr(value,45),'inside_enclosure':True})
            for eta in CONFIG['raw_absolute_error_relative_to_reference']:
                obs,intervals=observational_boxes(samples,eta)
                dataid=f'{kind}_r{r0text}_noise{eta}'
                dataset={'id':dataid,'kind':kind,'r0':r0text,'spacing':str(h),'noise':eta,
                         'samples':samples,'observations':obs,'moment_intervals':[interval_record(x) for x in intervals],
                         'direct_weight_benchmarks':direct,'independent_checks':checks}
                datasets.append(dataset)
                for degree in CONFIG['degrees']:
                    available=intervals[:degree+1]
                    # All methods have exactly the same available prefix.
                    effective=effective_mass_bounds(available,h)
                    hierarchy=sampled_gap_bound(available,h,(degree-1)//2)
                    order_scan=[sampled_gap_bound(available[:2*k+2],h,k)
                                for k in range((degree-1)//2+1)]
                    successful=[x for x in order_scan if x['status']=='CERTIFIED_UPPER_BOUND']
                    best_hierarchy=min(successful,key=lambda x:F(x['upper_mass'])) if successful else None
                    for cut in CONFIG['mass_cutoffs']:
                        zlo,zhi=cuts[cut]
                        lower=propose_certificate(available,zhi,degree,kind='lower')
                        upper=propose_certificate(available,zlo,degree,kind='upper')
                        for rec in (lower,upper):
                            verify_certificate(rec)
                            records.append(rec)
                        truth_lo,truth_hi=pair(direct[cut])
                        lower_q,upper_q=F(lower['bound']),F(upper['bound'])
                        # Stronger than midpoint inclusion: the entire truth enclosure fits.
                        if not lower_q <= truth_lo <= truth_hi <= upper_q:
                            raise AssertionError('Weight certificate fails against validated benchmark')
                        if hierarchy['status']=='CERTIFIED_UPPER_BOUND':
                            assert F(hierarchy['upper_mass']) >= 2
                        if effective['best_upper_mass'] is not None:
                            assert F(effective['best_upper_mass']) >= 2
                        rows.append({'dataset_id':dataid,'degree':degree,'available_samples':degree+1,
                                     'mass_cutoff':cut,'cutoff_y':interval_record((zlo,zhi)),
                                     'lower_certificate_index':len(records)-2,'upper_certificate_index':len(records)-1,
                                     'weight_lower':str(lower_q),'weight_upper':str(upper_q),
                                     'truth':direct[cut], 'weight_width':str(upper_q-lower_q),
                                     'moment_weight_baseline':moment_weight_baseline(available,zlo,zhi),
                                     'effective_mass':effective,'sampled_hierarchy':hierarchy,
                                     'hierarchy_all_orders':order_scan,
                                     'hierarchy_best_available':best_hierarchy})
                print(f'{dataid}: completed {len(CONFIG["degrees"])*len(CONFIG["mass_cutoffs"])*2} certificates',flush=True)
    save(out/'datasets.json',datasets)
    save(out/'weight_certificates.json',records)
    save(out/'comparison.json',rows)
    summary={
        'start_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),
        'seconds':time.perf_counter()-tic,'configuration_sha256':config_hash,
        'datasets':len(datasets),'unique_raw_integrals':40,'comparison_rows':len(rows),
        'exact_weight_certificates':len(records),'all_certificates_verified':True,
        'all_direct_weight_enclosures_contained':True,
        'python':sys.version,'platform':platform.platform(),
        'versions':{'python_flint':flint.__version__,'scipy':scipy.__version__,
                    'numpy':np.__version__,'mpmath':mp.__version__},
        'positive_weight_lower_rows':sum(F(x['weight_lower'])>0 for x in rows),
        'hierarchy_no_bound_rows':sum(x['sampled_hierarchy']['status']=='NO_BOUND' for x in rows),
        'scope':'fixed one-loop models; deterministic error envelopes; no statistical coverage or QED truncation bound',
    }
    save(out/'summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=DEFAULT_OUT)
    args=parser.parse_args()
    main(args.out)
