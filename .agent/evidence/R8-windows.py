"""R8: windows and charge thresholds with the two-loop leading three-photon coefficient."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "reproducibility"))
import mpmath as mp
import nonlinear_probe_eh as nl
import three_photon_amplitude as tpa

ALPHA = mp.mpf(1) / mp.mpf("137.035999")
PROBES = {
    "point": dict(factor=None, a=0, guess=(22.5, 20.6)),
    "ball": dict(factor=nl.ball_exterior_factor, a=10, guess=(30.7, 28.9)),
    "polynomial": dict(factor=nl.polynomial2_exterior_factor, a=10, guess=(29.4, 27.6)),
}
out = {}
mp.mp.dps = 30
for name, p in PROBES.items():
    for loops in (1, 2):
        t0 = time.time()
        r_x, r_g = tpa.window(ALPHA, factor=p["factor"], a=p["a"], guess=p["guess"], three_photon_loops=loops)
        kw = dict(factor=p["factor"], a=p["a"], three_photon_loops=loops)
        q = {}
        for label, r in (("at_r_x", r_x), ("at_r_gamma", r_g)):
            three = tpa.profile_moments(r, ALPHA, 0, **kw)[1]
            q[label] = mp.sqrt(three * 45 * mp.pi * r ** 6 / (8 * ALPHA ** 3))
        # D = M1 - 2 M0 at r_Gamma, pair and three-photon parts, and dD/dr
        p0, t0_ = tpa.profile_moments(r_g, ALPHA, 0, **kw)
        p1, t1_ = tpa.profile_moments(r_g, ALPHA, 1, **kw)
        h = mp.mpf("1e-4")
        def D(r):
            a0, b0 = tpa.profile_moments(r, ALPHA, 0, **kw)
            a1, b1 = tpa.profile_moments(r, ALPHA, 1, **kw)
            return (a1 + b1) - 2 * (a0 + b0)
        dD = (D(r_g + h) - D(r_g - h)) / (2 * h)
        out[f"{name}_loops{loops}"] = dict(
            r_x=mp.nstr(r_x, 12), r_gamma=mp.nstr(r_g, 12),
            q_max_at_r_x=mp.nstr(q["at_r_x"], 6), q_max_at_r_gamma=mp.nstr(q["at_r_gamma"], 6),
            D_pair=mp.nstr(p1 - 2 * p0, 6), D_3gamma=mp.nstr(t1_ - 2 * t0_, 6), dD_dr=mp.nstr(dD, 6),
            seconds=round(time.time() - t0, 1))
        print(name, loops, out[f"{name}_loops{loops}"], flush=True)

# sensitivity: the factor on the whole series instead of the leading term only
c0 = 1 + mp.mpf(1555) / 153 * ALPHA / mp.pi
saved = tpa.SERIES
tpa.SERIES = tuple(c * float(c0) for c in saved)
try:
    r_x, r_g = tpa.window(ALPHA, guess=(22.5, 20.6))
finally:
    tpa.SERIES = saved
out["point_whole_series_factor"] = dict(r_x=mp.nstr(r_x, 12), r_gamma=mp.nstr(r_g, 12), factor=mp.nstr(c0, 15))
print(out["point_whole_series_factor"], flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=1)
