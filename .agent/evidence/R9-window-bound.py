"""R9: what the truncation envelope implies for the radii (point probe, two-loop leading term).

r_Gamma: |dr| <= |dD|/|dD/dr|, |dD| <= int |x - 2| w |rho - rho_6|.
r_x:     |dr| <= (|dPhi_3gamma|/Phi_3gamma)/|t1/t0 - p1/p0| (log slopes of the two parts).
Below s1 the deviation is bounded (envelope + computed cross terms beyond s^9); above s1 the
stated assumption |rho - rho_6| <= rho_6. The part above 4m^2 is not included here.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "reproducibility"))
import mpmath as mp
import numpy as np
import three_photon_amplitude as tpa

data = json.loads((HERE / "R9-products-data.json").read_text())
K = data["K"]
M = np.zeros((K + 1, K + 1))
for key, v in data["M"].items():
    a, b = map(int, key.split(","))
    M[a, b] = M[b, a] = float(v)
ALPHA = 1 / 137.035999
windows = json.loads((HERE / "R8-windows.json").read_text())["point_loops2"]
r_g, r_x = mp.mpf(windows["r_gamma"]), mp.mpf(windows["r_x"])
dDdr = abs(mp.mpf(windows["dD_dr"]))
with mp.workdps(30):
    p0, t0 = tpa.profile_moments(r_x, ALPHA, 0, three_photon_loops=2)
    p1, t1 = tpa.profile_moments(r_x, ALPHA, 1, three_photon_loops=2)
    slope = abs(t1 / t0 - p1 / p0)
table = []
with mp.workdps(20):
    for s in (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0):
        rho6, rhoK = tpa.density_series(s), tpa.density_truncated(s, M)
        env = tpa.density_envelope(s, K, M)
        table.append(dict(s=s, envelope_over_rhoK=float(env / rhoK), cross_terms_over_rho6=float((rhoK - rho6) / rho6)))
        print(f"s={s}: |rho-rho_K|/rho_K <= {float(env / rhoK):.3e}; (rho_K-rho_6)/rho_6 = {float((rhoK - rho6) / rho6):.3e}")
rows = []
for s1 in (0.75, 1.0, 1.25, 1.5, 1.75, 2.0):
    bg = tpa.truncation_moment_bounds(r_g, ALPHA, M, K, s1)
    bx = tpa.truncation_moment_bounds(r_x, ALPHA, M, K, s1)
    row = dict(s1=s1,
               r_gamma_bounded=float(bg["bounded_D"] / dDdr), r_gamma_assumed=float(bg["assumed_D"] / dDdr),
               r_x_bounded=float(bx["bounded_M0"] / bx["model_M0"] / slope),
               r_x_assumed=float(bx["assumed_M0"] / bx["model_M0"] / slope),
               share_assumed_r_gamma=float(bg["assumed_M0"] / bg["model_M0"]),
               share_bounded_dev_r_gamma=float(bg["bounded_M0"] / bg["model_M0"]))
    rows.append(row)
    print({k: (f"{v:.3e}" if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
out = dict(K=K, r_gamma=str(r_g), r_x=str(r_x), dD_dr=str(-dDdr), log_slope_difference=str(slope),
           density_table=table, rows=rows)
(HERE / "R9-window-bound.json").write_text(json.dumps(out, indent=1))
