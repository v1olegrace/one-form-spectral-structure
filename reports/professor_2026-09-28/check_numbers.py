"""Checagem independente (27-28/09/2026) dos numeros citados em CONTENT.md.

Nao faz parte do pipeline canonico e nao grava nada fora desta pasta.
Uso: python reports/professor_2026-09-28/check_numbers.py
Gera fig_tiny_atom.csv (dados para a figura da pagina 3) nesta pasta.
"""
import csv
import os

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
mp.mp.dps = 30
W = mp.mpf("1e-12")
G32 = mp.gamma(mp.mpf(3) / 2)


def atom(r):
    return W * mp.e ** (-2 * r)


def cont(r):
    return G32 * (1 + r) ** mp.mpf(-1.5) * mp.e ** (-3 * r)


def phi(r):
    return atom(r) + cont(r)


def gam(r):
    return -mp.diff(lambda t: mp.log(phi(t)), r)


rx = mp.findroot(lambda r: mp.log(atom(r)) - mp.log(cont(r)), 22)
print("r_x (modelo do artigo) =", mp.nstr(rx, 6))
print("t_x (familia de 2 exponenciais, M-mu=1) =", mp.nstr(mp.log((1 - W) / W), 6))
for r in [3, 10, 20, rx, 25, 30, 40]:
    print("r=%-8s Gamma=%s  fracao do atomo=%s" % (mp.nstr(r, 5), mp.nstr(gam(r), 6),
                                                  mp.nstr(atom(r) / phi(r), 4)))

mp.mp.dps = 60


def a(n, r):
    c = mp.quad(lambda x: x ** n * mp.sqrt(x - 3) * mp.e ** (-(x - 3)) * mp.e ** (-r * x),
                [3, 4, 10, mp.inf])
    return W * 2 ** n * mp.e ** (-2 * r) + c


r = 3
mom = [a(n, r) for n in range(10)]
for K in range(5):
    H0 = mp.matrix(K + 1, K + 1)
    H1 = mp.matrix(K + 1, K + 1)
    for i in range(K + 1):
        for j in range(K + 1):
            H0[i, j] = mom[i + j]
            H1[i, j] = mom[i + j + 1]
    L = mp.cholesky(H0)
    Li = L ** -1
    ev = mp.eigsy(Li * H1 * Li.T)[0]
    print("r=3  B_%d = %s" % (K, mp.nstr(min(ev), 6)))

mp.mp.dps = 30
alpha = 1 / mp.mpf(137)


def g2pibar_inf(logL):
    """g_R^2 * int_{4m^2}^{Lambda^2} rho_J(s)/s ds, s = 4m^2 e^t."""
    f = lambda t: (1 / (12 * mp.pi ** 2)) * (1 + mp.e ** (-t) / 2) * mp.sqrt(1 - mp.e ** (-t))
    return 4 * mp.pi * alpha * mp.quad(f, [0, 1, 10, logL])


for label, logL in [("10", 2 * mp.log(mp.mpf(10) / 2)),
                    ("1e19", 2 * mp.log(mp.mpf(10) ** 19 / 2)),
                    ("1e100", 2 * mp.log(mp.mpf(10) ** 100 / 2)),
                    ("e^645", mp.mpf("1288.6")),
                    ("e^700", mp.mpf("1398.6"))]:
    v = g2pibar_inf(logL)
    print("Lambda/m=%-6s log=%s g2Pibar(inf)=%s Z3=%s" % (label, mp.nstr(logL, 6),
                                                         mp.nstr(v, 5), mp.nstr(1 - v, 5)))
print("Landau: log(Lambda^2/4m^2) = 3pi/alpha =", mp.nstr(3 * mp.pi / alpha, 7))

# polo unico: G = g2/(Q2 [1 - g2 Pibar]), rho_J = Z delta(s-s0), c = g2 Z/s0
g2, Z, s0, Q2 = mp.mpf("0.3"), mp.mpf("0.7"), mp.mpf("2.0"), mp.mpf("1.3")
c = g2 * Z / s0
lhs = g2 / (Q2 * (1 - g2 * Z * Q2 / (s0 * (s0 + Q2))))
rhs = g2 / Q2 + (g2 * c / (1 - c)) / (Q2 + s0 / (1 - c))
print("polo unico: |lhs-rhs| =", mp.nstr(abs(lhs - rhs), 3))

with open(os.path.join(HERE, "fig_tiny_atom.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["r", "atom_1e-12_e^-2r", "continuum_G(3/2)(1+r)^-1.5_e^-3r", "Phi", "Gamma"])
    for k in range(0, 401):
        rr = mp.mpf(k) / 10
        w.writerow([float(rr), float(atom(rr)), float(cont(rr)), float(phi(rr)), float(gam(rr))])
print("fig_tiny_atom.csv escrito")
