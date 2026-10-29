"""Reject inputs outside the declared exterior, truncated-series model."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'reproducibility'))
import three_photon_amplitude as tpa


@pytest.mark.parametrize('kw', [dict(r=0), dict(r=2, a=2), dict(a=-1),
    dict(r=float('inf')), dict(alpha=float('nan')), dict(alpha=0),
    dict(nterms=0), dict(nterms=7), dict(nterms=2.5), dict(pair_loops=3),
    dict(three_photon_loops=0), dict(three_photon_loops=3), dict(three_photon_loops=True),
    dict(smax=0), dict(smax=5), dict(k=-1), dict(k=True)])
def test_invalid_domain_fails_before_quadrature(kw, monkeypatch):
    import nonlinear_probe_eh as nl
    def no_quadrature(*a, **k):
        pytest.fail('invalid domain reached quadrature')
    monkeypatch.setattr(nl, 'quad_relative', no_quadrature)
    args = dict(r=20, alpha=1/137.035999)
    args.update(kw)
    with pytest.raises(ValueError):
        tpa.profile_moments(**args)
