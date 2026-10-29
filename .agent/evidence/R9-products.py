"""R9: the Dalitz-integrated amplitude products M[a, b] for K = 22 (exact rules: feyn_n = 13, dal_n = 12)."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "reproducibility"))
import numpy as np
import three_photon_amplitude as tpa

K, FEYN, DAL = 22, 13, 12
t0 = time.time()
M, worst = tpa.amplitude_products(K, FEYN, DAL)
orders = list(range(4, K + 1, 2))
series = [sum(M[a, b] for a in orders for b in orders if a + b == 8 + 2 * n) for n in range(6)]
out = dict(K=K, feyn_n=FEYN, dal_n=DAL, seconds=round(time.time() - t0, 1), worst_forbidden=worst,
           orders=orders, M={f"{a},{b}": repr(float(M[a, b])) for a in orders for b in orders if a <= b},
           series_from_products=[repr(float(c)) for c in series],
           series_stored=[repr(c) for c in tpa.SERIES],
           relative_difference=[float(abs(c / d - 1)) for c, d in zip(series, tpa.SERIES)])
Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("seconds", "worst_forbidden", "relative_difference")}))
