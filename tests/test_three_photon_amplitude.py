"""The full one-loop gamma* -> 3 gamma amplitude and the O(alpha^4) window (note E4, Section 9)."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import nonlinear_probe_eh as nl  # noqa: E402
import three_photon_amplitude as tpa  # noqa: E402
import three_photon_window as tpw  # noqa: E402

ALPHA = 1.0 / 137.035999
RULE = tpa.simplex_rule(8)


def _decay(s=0.6, y=(0.31, 0.27, 0.42)):
    return tpa.decay_kinematics(s, y)


def test_ward_identity_on_every_leg_including_the_virtual_one():
    """Exact for the series (polynomial integrands); quadrature-limited for the full amplitude."""
    p, pols = _decay()
    for leg in range(4):
        pl = [list(x) for x in pols]
        pl[leg] = [p[leg]]                       # polarization replaced by the momentum
        assert np.abs(tpa.box(p, pl, RULE, kmax=8)[..., 1:]).max() < 1e-13
    scale = np.abs(tpa.box(p, pols, RULE, full=True)).max()            # about 1e-2 here
    pl = [[p[0]]] + [list(x) for x in pols[1:]]
    coarse = np.abs(tpa.box(p, pl, RULE, full=True)).max()
    fine = np.abs(tpa.box(p, pl, tpa.simplex_rule(11), full=True)).max()
    assert coarse < 1e-8 * scale and fine < coarse / 10


def test_bose_symmetry_and_forbidden_orders():
    p, pols = _decay()
    J = tpa.box(p, pols, RULE, kmax=8)
    swapped = tpa.box([p[0], p[2], p[1], p[3]], [pols[0], pols[2], pols[1], pols[3]], RULE, kmax=8)
    assert np.abs(J - np.swapaxes(swapped, 1, 2)).max() < 1e-13
    assert np.abs(J[..., [1, 2, 3, 5, 7]]).max() < 1e-13          # odd orders and lambda^2 vanish
    # the lambda^0 constant is the dropped regularization constant: it does not depend on momenta
    p2, _ = _decay(2.3, (0.2, 0.5, 0.3))
    J2 = tpa.box(p2, pols, RULE, kmax=0)
    assert np.abs(J[..., 0] - J2[..., 0]).max() < 1e-13 and np.abs(J[..., 0]).max() > 0.1


def test_euler_heisenberg_limit_with_absolute_normalization():
    """lambda^4 term = -(2/15) Q(k^eps, ...), Q the quartic form of route A; m = 1."""
    p, pols = _decay()
    J = tpa.box(p, pols, RULE, kmax=4).real[..., 4]
    for idx in np.ndindex(J.shape):
        eps = [pols[leg][idx[leg]] for leg in range(4)]
        Q = tpw.quartic_form([tpw.wedge([Fraction(c).limit_denominator(10 ** 15) for c in p[leg]],
                                        [Fraction(c).limit_denominator(10 ** 15) for c in eps[leg]])
                              for leg in range(4)])
        assert J[idx] == pytest.approx(-2 / 15 * float(Q), abs=1e-12)


def test_on_shell_expansion_matches_dicus_kao_repko_at_omega4_and_omega6():
    """hep-ph/9709415, Table II and eq. (11): 139 (3+z^2)^2 and 160 (1-z^2)(3+z^2)."""
    rule = tpa.simplex_rule(7)
    for z in (-0.6, 0.0, 0.35, 0.9):
        p, pols = tpa.scattering_kinematics(z)
        J = tpa.box(p, pols, rule, kmax=6).real
        norm = 32400 / 1024
        assert norm * (J[..., 4] ** 2).sum() == pytest.approx(139 * (3 + z * z) ** 2, rel=1e-12)
        assert norm * (2 * J[..., 4] * J[..., 6]).sum() == pytest.approx(160 * (1 - z * z) * (3 + z * z), rel=1e-12)


def test_density_series_low_orders():
    """Numerical expansion: c0 matches route A; c1/c0 agrees with 335/714; c2 matches stored data."""
    c, worst = tpa.density_series_coefficients(12, 8, 4)
    assert worst < 1e-12
    assert c[0] == pytest.approx(17 / 11664000, rel=1e-12)
    assert c[1] / c[0] == pytest.approx(335 / 714, rel=1e-11)
    assert c[2] == pytest.approx(tpa.SERIES[2], rel=1e-10)
    assert all(x > 0 for x in tpa.SERIES)


def test_kallen_sabry_density_limits():
    a = mp.mpf(ALPHA)
    with mp.workdps(40):
        thr = tpa.kallen_sabry_density(4 / (1 - mp.mpf("1e-12")), a)   # v = 1e-6
        assert abs(thr / (a * a / 4) - 1) < 1e-5                         # first Coulomb term
        high = tpa.kallen_sabry_density(mp.mpf(10) ** 14, a)
        assert abs(high / ((a / mp.pi) ** 2 / 4) - 1) < 1e-6
        # two loops / (one loop * pi alpha / 2v) -> 1 linearly in v
        dev = []
        for v in (mp.mpf("1e-2"), mp.mpf("1e-3")):
            s = 4 / (1 - v * v)
            one = a / (3 * mp.pi) * (1 + 2 / s) * v
            dev.append(abs(tpa.kallen_sabry_density(s, a) / (one * mp.pi * a / (2 * v)) - 1))
        assert dev[1] < dev[0] / 5 and dev[1] < 2e-3


def _brackets(r_x, r_g, delta=mp.mpf("1e-4"), **kw):
    """Signs of Phi_pair - Phi_3gamma and Gamma - 2m on either side of the stored roots."""
    out = []
    for r in (r_x - delta, r_x + delta):
        pair, three = tpa.profile_moments(r, ALPHA, 0, **kw)
        out.append(pair > three)
    for r in (r_g - delta, r_g + delta):
        p0, t0 = tpa.profile_moments(r, ALPHA, 0, **kw)
        p1, t1 = tpa.profile_moments(r, ALPHA, 1, **kw)
        out.append((p1 + t1) / (p0 + t0) > 2)
    return out


def test_window_with_the_full_density():
    """Point probe: series to s^9 for the three-photon density, two-loop pair."""
    with mp.workdps(30):
        assert _brackets(mp.mpf("22.56747377"), mp.mpf("20.64902588")) == [True, False, True, False]
        # leading terms only: the radii of three_photon_window.window
        assert _brackets(mp.mpf("22.60069102"), mp.mpf("20.70248284"), pair_loops=1, nterms=1) == [True, False, True, False]
        r = mp.mpf(20)
        pair, three = tpa.profile_moments(r, ALPHA, 0, pair_loops=1, nterms=1)
        # the density is used up to s = 4m^2 only: the leading term then gives gamma(10, 2r), not Gamma(10)
        upto2 = tpw.phi_three_photon(r, ALPHA) * mp.gammainc(10, 0, 2 * r) / mp.gamma(10)
        assert abs(three / upto2 - 1) < 1e-15
        assert 0 < 1 - three / tpw.phi_three_photon(r, ALPHA) < 1e-8
        assert abs(pair / tpw.phi_pair_moment(r, ALPHA, 0) - 1) < 1e-15
        # the series has converged: four terms against six, and the enhancement over the leading term
        six = tpa.profile_moments(mp.mpf("20.649"), ALPHA, 0)[1]
        four = tpa.profile_moments(mp.mpf("20.649"), ALPHA, 0, nterms=4)[1]
        five = tpa.profile_moments(mp.mpf("20.649"), ALPHA, 0, nterms=5)[1]
        lead = tpa.profile_moments(mp.mpf("20.649"), ALPHA, 0, nterms=1)[1]
        assert abs(four / six - 1) < 1e-3 and abs(five / six - 1) < abs(four / six - 1) / 2
        assert 1.13 < six / lead < 1.15


def test_compact_probe_windows_with_the_full_factor():
    with mp.workdps(30):
        assert _brackets(mp.mpf("30.7413392"), mp.mpf("28.8837986"), factor=nl.ball_exterior_factor, a=10) == [True, False, True, False]
        assert _brackets(mp.mpf("29.4081048"), mp.mpf("27.5754252"), factor=nl.polynomial2_exterior_factor, a=10) == [True, False, True, False]


def test_windows_with_the_two_loop_leading_term():
    """Note E4, Section 11.4: every radius moves in by 0.0125-0.0130/m."""
    with mp.workdps(30):
        assert _brackets(mp.mpf("22.55444897"), mp.mpf("20.63638512"),
                         three_photon_loops=2) == [True, False, True, False]
        assert _brackets(mp.mpf("30.7284344"), mp.mpf("28.8712788"), factor=nl.ball_exterior_factor, a=10,
                         three_photon_loops=2) == [True, False, True, False]
        assert _brackets(mp.mpf("29.3952351"), mp.mpf("27.5629497"), factor=nl.polynomial2_exterior_factor, a=10,
                         three_photon_loops=2) == [True, False, True, False]


def test_two_loop_factor_acts_on_the_leading_coefficient_only():
    """three_photon_loops=2 adds (1555/153)(alpha/pi) times the leading-term profile, nothing else."""
    assert Fraction(*tpa.KAPPA_2) == Fraction(1555, 153)
    kappa = mp.mpf(tpa.KAPPA_2[0]) / tpa.KAPPA_2[1]
    with mp.workdps(30):
        for k in (0, 1):
            one = tpa.profile_moments(mp.mpf(21), ALPHA, k)
            two = tpa.profile_moments(mp.mpf(21), ALPHA, k, three_photon_loops=2)
            lead = tpa.profile_moments(mp.mpf(21), ALPHA, k, nterms=1)[1]
            assert two[0] == one[0]
            assert abs((two[1] - one[1]) / (kappa * mp.mpf(ALPHA) / mp.pi * lead) - 1) < 1e-12
        assert tpa.density_series(mp.mpf("0.5"), 1, 3) == 3 * mp.mpf(tpa.SERIES[0]) * mp.mpf("0.5") ** 4


def test_dicus_kao_repko_effective_lagrangians_against_the_box():
    """Their eqs. (13) and (14) give our omega^4 and omega^6 amplitudes exactly; eq. (15),
    quoted as L_{4,4} by Heinzl-King-Mercuri-Baron (arXiv:2510.19921), gives twice our
    omega^8 amplitudes, as their Table II does (note E4, Section 10.1)."""
    rule = tpa.simplex_rule(9)
    for z in (0.3, -0.55):
        p, pols = tpa.scattering_kinematics(z)
        J = tpa.box(p, pols, rule, kmax=8).real
        for idx in [(0, 0, 0, 0), (0, 1, 0, 1), (1, 0, 0, 1), (1, 1, 1, 1)]:
            M = tpa.lagrangian_amplitudes(p, [pols[leg][idx[leg]] for leg in range(4)])
            a4, a6, a8 = J[idx + (4,)], J[idx + (6,)], J[idx + (8,)]
            assert abs(a4) > 1e-6 and abs(M[0] / a4 - 1) < 1e-10
            assert abs(M[1] - a6) < 1e-10 * max(abs(a6), abs(a4))
            assert abs(M[2] - 2 * a8) < 1e-10 * max(abs(a8), abs(a4))


def _published_low_energy_amplitudes(s, t, u):
    """Abdul Hameed-Chaubey-Shao, arXiv:2604.00099, ancillary anc/Amp1L_LE.wl (one loop, fermion,
    prefactor -Nc Qf^4 alpha^2 taken out), by power of x = s/m^2: (++++, -+++, --++, +-+-, +--+)."""
    S2, P = s*s + t*t + u*u, s*t*u
    pppp = {2: -S2/15, 3: -2*P/63, 4: -S2**2/945, 5: -P*S2/990,
            6: -(109*P*P + Fraction(75, 8)*S2**3)/450450, 7: -3*P*S2**2/100100}
    mppp = {3: -P/315, 5: -P*S2/41580, 6: -2*P*P/225225, 7: -P*S2**2/3603600}

    def mmpp(a, b, c):
        return {2: Fraction(11, 45)*a*a, 3: Fraction(4, 315)*a**3, 4: a*a*(91*a*a - 50*b*c)/18900,
                5: a**3*(48*a*a + 49*b*c)/103950,
                6: a*a*(3420*a**4 + 3577*a*a*(b*b + c*c) + 2394*a*(b**3 + c**3) + 1197*(b**4 + c**4))/37837800,
                7: a**3*(1197*a**4 - 967*a*a*(b*b + c*c) - 980*a*(b**3 + c**3) - 490*(b**4 + c**4))/37837800}
    return pppp, mppp, mmpp(s, t, u), mmpp(u, t, s), mmpp(t, s, u)


def test_box_equals_the_published_one_loop_expansion_to_omega14():
    """Independent benchmark: polarization sums are basis independent, so the bilinears of the
    lambda^4 ... lambda^14 coefficients must equal sum over the 16 helicities of theirs. This
    includes omega^8, where Dicus-Kao-Repko's Table II is twice ours."""
    rule = tpa.simplex_rule(9)
    orders = [2, 3, 4, 5, 6, 7]
    for z in (Fraction(-3, 5), Fraction(3, 10)):
        p, pols = tpa.scattering_kinematics(float(z))
        J = tpa.box(p, pols, rule, kmax=14).real.reshape(-1, 15)
        s, t, u = Fraction(4), -2 * (1 - z), -2 * (1 + z)
        weighted = list(zip((2, 8, 2, 2, 2), _published_low_energy_amplitudes(s, t, u)))
        for a in orders:
            for b in orders:
                ours = (J[:, 2 * a] * J[:, 2 * b]).sum()
                theirs = sum(w * float(amp.get(a, 0) * amp.get(b, 0)) for w, amp in weighted)
                assert abs(ours - theirs) <= 1e-13 * max(1.0, abs(theirs)), (z, a, b, ours, theirs)


def test_full_cross_section_against_dicus_kao_repko_table3():
    """omega/m = 0.65: R1 = sigma_EH/sigma_full = 0.8035 (DKR 0.799); doubling the omega^8 terms would give about 0.74."""
    rule = tpa.simplex_rule(9)
    zt, zw = np.polynomial.legendre.leggauss(8)
    full = lead = 0.0
    for z, wz in zip(zt, zw):
        p, pols = tpa.scattering_kinematics(z, 0.65)
        F = tpa.box(p, pols, rule, full=True).real
        S = tpa.box(p, pols, rule, kmax=4).real
        full += wz * (F ** 2).sum()
        lead += wz * (S[..., 4] ** 2).sum()
    assert full / lead == pytest.approx(1.244615, abs=2e-5)        # converged value (16^3 nodes, 16 angles)
    assert abs(lead / full - 0.799) < 0.006
