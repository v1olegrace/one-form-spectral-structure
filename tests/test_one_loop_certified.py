"""Validated integration boundaries, independent benchmarks and refusal paths."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

import pytest
import mpmath as mp

pytest.importorskip("flint", reason="Install reproducibility/requirements-certified.txt")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"reproducibility"))
from one_loop_certified import certify_sample, certify_weight, cutoff_enclosure, upper_mass_from_ratio
from run_one_loop_certificates import observational_boxes, sampled_gap_bound, effective_mass_bounds
from spectral_models import build_models


def mpr(value):
    q=F(value)
    return mp.mpf(q.numerator)/q.denominator


@pytest.mark.parametrize('kind,key',[('dirac','D_dirac'),('scalar','E_scalar')])
@pytest.mark.parametrize('radius',['1','4'])
def test_validated_integral_encloses_independent_numerical_evaluation(kind,key,radius):
    sample=certify_sample(kind,radius)
    with mp.workdps(80):
        r=mp.mpf(radius)
        independent=build_models()[key].Phi_scaled(r)*mp.exp(-2*r)
        assert mpr(sample['raw']['lower']) < independent < mpr(sample['raw']['upper'])
    assert F(sample['raw_relative_width']) < F('1e-20')
    assert json.loads(json.dumps(sample))==sample


def test_omitted_tail_is_included_and_can_dominate_uncertainty():
    short=certify_sample('dirac','1',t_max='1',max_relative_width='100')
    long=certify_sample('dirac','1')
    assert F(short['tail_scaled_upper']) > F('1e-3')
    # The finite integral alone misses a material positive tail.
    assert F(short['finite_scaled']['upper']) < F(long['scaled']['lower'])
    assert F(short['scaled']['lower']) < F(long['scaled']['lower'])
    assert F(short['scaled']['upper']) > F(long['scaled']['upper'])
    with pytest.raises(ArithmeticError,match='width'):
        certify_sample('dirac','1',t_max='1')


@pytest.mark.parametrize('kind,key',[('dirac','D_dirac'),('scalar','E_scalar')])
def test_direct_weight_encloses_independent_truncated_integral(kind,key):
    enc=certify_weight(kind,'1','3')
    with mp.workdps(75):
        model=build_models()[key]
        density=model.branches[0][1]
        numerator=mp.quad(lambda x: mp.exp(-x)*density(x),[2,3])
        denominator=model.Phi_scaled(1)*mp.exp(-2)
        assert mpr(enc['lower']) < numerator/denominator < mpr(enc['upper'])
    assert certify_weight(kind,'1','2')=={'lower':'0','upper':'0'}


def test_amplitude_scaling_and_nondefault_mass():
    first=certify_sample('dirac','1',mass='2')
    second=certify_sample('dirac','1',mass='2',coupling2='3',charge='2')
    assert 12*F(first['raw']['lower']) <= F(second['raw']['upper'])
    assert F(second['raw']['lower']) <= 12*F(first['raw']['upper'])
    assert first['x_max']=='68'


def test_cutoff_rounding_and_log_have_outward_endpoints():
    lo,hi=cutoff_enclosure('3','1/4')
    upper=upper_mass_from_ratio(F(1,2),'1/4')
    with mp.workdps(80):
        assert mpr(lo) < mp.exp(-mp.mpf(3)/4) < mpr(hi)
        assert mpr(upper) >= 4*mp.log(2)


def test_normalization_keeps_shared_reference_exact_and_truth_inside():
    samples=[certify_sample('scalar',str(r)) for r in (1,2,3)]
    observations,normalized=observational_boxes(samples,'1e-3')
    assert normalized[0]==(F(1),F(1))
    for j in (1,2):
        true_lo=F(samples[j]['raw']['lower'])/F(samples[0]['raw']['upper'])
        true_hi=F(samples[j]['raw']['upper'])/F(samples[0]['raw']['lower'])
        assert normalized[j][0] <= true_lo <= true_hi <= normalized[j][1]
    assert F(observations[0]['declared_observation_error'])>0


def test_fixed_vector_gap_bound_and_no_bound_are_explicit():
    data=[(F(1),F(1)),(F(1,2),F(1,2))]
    result=sampled_gap_bound(data,F(1),0)
    assert result['status']=='CERTIFIED_UPPER_BOUND'
    with mp.workdps(80):
        assert mpr(result['upper_mass'])>=mp.log(2)
    bad=[(F(1),F(1)),(F(0),F(1))]
    assert sampled_gap_bound(bad,F(1),0)['status']=='NO_BOUND'
    assert effective_mass_bounds(bad,F(1))['best_upper_mass'] is None


def test_inexact_inputs_and_invalid_domains_refused():
    for kwargs in [dict(radius=1.0),dict(radius='0'),dict(radius='1',mass='-1'),
                   dict(radius='1',tolerance='-1'),dict(radius='1',charge='0')]:
        with pytest.raises(ValueError):
            certify_sample('dirac',**kwargs)


def test_legacy_random_trials_are_not_labeled_certified():
    import interval_bounds as legacy
    legacy.RESULTS.clear()
    with mp.workdps(40):
        old=mp.iv.dps
        try:
            mp.iv.dps=40
            legacy.certify_envelope()
        finally:
            mp.iv.dps=old
    assert len(legacy.RESULTS)==5
    assert all(x['kind']=='CHECKED' for x in legacy.RESULTS)
