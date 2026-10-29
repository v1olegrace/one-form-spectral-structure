"""R9: size of the crude rigorous envelope for the three-photon truncation remainder.

Per ordering, after amplitude order K (s = lambda^2, m = 1, momenta of s = 1 scaled by lambda):
  E1 <= sum_jd lambda^jd B0[jd] (n0+1) lambda^(2 n0) I(n0)/(1-s/4)^2      n0 = (K-jd)//2 + 1, jd = 0..4
      + sum_jd lambda^jd (B2[jd]/2) lambda^(2 n0) I(n0)/(1-s/4)             jd = 0..2
      + (192/4) lambda^(2 n0) I(n0)/(n0 (1-s/4))                            n0 = K//2 + 1
with I(n) = int_simplex Rbar^n, Rbar = x0 x3 + x0 x2 + x1 x3 >= R (exact Dirichlet moments),
B0[jd] = 4 C(4,jd) 4^jd, B2[jd] = 96 C(2,jd) 4^jd. The six orderings are added: E = 6 E1.
The RMS amplitude per polarization is sqrt(384 rho); |rho - rho_K| <= 2 sqrt(rho eps) + eps, eps = E^2/384.
"""
import json
import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "reproducibility"))
import mpmath as mp
import three_photon_amplitude as tpa

K = 18
B0 = [4 * math.comb(4, j) * 4 ** j for j in range(5)]
B2 = [96 * math.comb(2, j) * 4 ** j for j in range(3)]


def dirichlet(a):
    return Fr(math.prod(math.factorial(x) for x in a), math.factorial(sum(a) + 3))


def I(n):
    total = Fr(0)
    for i in range(n + 1):
        for j in range(n + 1 - i):
            k = n - i - j
            coeff = Fr(math.factorial(n), math.factorial(i) * math.factorial(j) * math.factorial(k))
            # x0^(i+j) x1^k x2^j x3^(i+k)
            total += coeff * dirichlet((i + j, k, j, i + k))
    return total


def E1(s):
    lam, u = math.sqrt(s), s / 4
    total = 0.0
    for jd in range(5):
        n0 = (K - jd) // 2 + 1
        total += lam ** jd * B0[jd] * (n0 + 1) * lam ** (2 * n0) * float(I(n0)) / (1 - u) ** 2
    for jd in range(3):
        n0 = (K - jd) // 2 + 1
        total += lam ** jd * B2[jd] / 2 * lam ** (2 * n0) * float(I(n0)) / (1 - u)
    n0 = K // 2 + 1
    total += 192 / 4 * lam ** (2 * n0) * float(I(n0)) / (n0 * (1 - u))
    return total


rows = []
for s in (0.05, 0.1, 0.19, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0):
    rho = float(tpa.density_series(s))
    E = 6 * E1(s)
    eps = E * E / 384
    rel = (2 * math.sqrt(rho * eps) + eps) / rho
    rows.append(dict(s=s, rho_series=rho, A_rms=math.sqrt(384 * rho), E_bound=E, rel_density_bound=rel))
    print(f"s={s:5.2f}  A_rms={math.sqrt(384*rho):.3e}  E_bound={E:.3e}  E/A={E/math.sqrt(384*rho):.3e}  |drho|/rho<={rel:.3e}")

# weight of the region where the bound fails, in the leading-order profile at r_Gamma
r = mp.mpf("20.636")
for s1 in (0.19, 0.3, 0.5):
    frac = mp.gammainc(10, r * mp.sqrt(s1), mp.inf) / mp.gamma(10)
    print(f"leading-order fraction of Phi_3gamma(r_Gamma) from s > {s1}: {mp.nstr(frac, 3)}")
out = dict(K=K, I={n: str(I(n)) for n in (8, 9, 10)}, rows=rows,
           note="sizes of the crude rigorous envelope; see .agent/reports/R9.md")
Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
