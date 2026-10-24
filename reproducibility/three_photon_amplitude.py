"""The full one-loop gamma* -> 3 gamma amplitude and the O(alpha^4) three-photon density (note E4, Section 9).

The 1PI four-photon vertex of a Dirac loop of mass m (= 1 here) is

    Gamma = -(e^4/16 pi^2) sum over the six orderings of J,
    J = int_simplex d^3x [N0/Delta^2 - N2/(2 Delta) - N4 log(Delta)/4],

from Feynman parameters x_j, the shifted loop momentum, and the four-dimensional
tensor integrals. The trace runs Tr[e0 S(l-p0) ea S(l+pb+pc) eb S(l+pc) ec S(l)]
with every momentum incoming. N0, N2 and N4 collect zero, two and four loop
momenta. The slots are m + lambda*vslash_j(x), and v_j = sum_i (delta_ji - x_i) K_i
is linear in fixed vectors K_i, so every Dirac trace is computed once and does
not depend on x.

The momentum-independent constant (zero external momenta) comes from the
regularization constants dropped with the l^4 terms. Gauge invariance makes the
true constant zero, so it is subtracted. The Ward identity on every leg, the
Euler-Heisenberg limit with the absolute normalization -2/15 Q, and the on-shell
expansion of Dicus, Kao and Repko (hep-ph/9709415, Table II at orders omega^4
and omega^6) are checks of this, not inputs.

    rho_Pi = (alpha/pi)^4 / 4608 * int_{Dalitz simplex} sum_pol |sum J|^2 dy1 dy2.

All values are CHECKED by quadrature; nothing here is interval-certified.
"""
from __future__ import annotations

import itertools
import math
from numbers import Integral

import mpmath as mp
import numpy as np

import nonlinear_probe_eh as nl

ETA = np.array([1.0, -1.0, -1.0, -1.0])
_I2, _Z2 = np.eye(2), np.zeros((2, 2))
_SIG = (np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex))
G = np.array([np.block([[_I2, _Z2], [_Z2, -_I2]]).astype(complex)]
             + [np.block([[_Z2, s], [-s, _Z2]]) for s in _SIG])          # gamma^mu
GL = np.array([ETA[a] * G[a] for a in range(4)])                        # gamma_mu
ONE = np.eye(4, dtype=complex)

# rho_Pi/(alpha/pi)^4 = sum_n SERIES[n] s^(4+n), m = 1. Computed by
# density_series_coefficients(18, 11, 9) on 23 October 2026 (661 s); c0 = 17/11664000
# and c1 = (335/714) c0 to 15 digits. The tests recompute c0..c2 at lower resolution.
SERIES = (1.4574759945130315e-06, 6.838297733359467e-07, 2.2381382577853135e-07,
          6.360593981058841e-08, 1.6854097101958432e-08, 4.295553129190592e-09)

# The O(alpha^5) term of the leading coefficient: SERIES[0] -> SERIES[0] (1 + KAPPA_2 alpha/pi),
# with KAPPA_2 = 1555/153 from the two-loop Euler-Heisenberg coefficients
# (three_photon_window.three_photon_two_loop; note E4, Section 11). The later
# terms have no computed O(alpha^5) part.
KAPPA_2 = (1555, 153)


def slash(v):
    """v_mu gamma^mu for upper-index v of shape (..., 4)."""
    return np.einsum("...m,mij->...ij", np.asarray(v) * ETA, G)


# --- quadrature ----------------------------------------------------------------
def simplex_rule(n):
    """Collapsed Gauss-Legendre rule on the 3-simplex (volume 1/6): barycentric x (N, 4), w (N,).

    Exact for polynomials of degree <= 2n - 3 in x.
    """
    t, wt = np.polynomial.legendre.leggauss(n)
    t, wt = (t + 1) / 2, wt / 2
    u, v, z = np.meshgrid(t, t, t, indexing="ij")
    wu, wv, wz = np.meshgrid(wt, wt, wt, indexing="ij")
    x1, x2, x3 = u, (1 - u) * v, (1 - u) * (1 - v) * z
    x = np.stack([1 - x1 - x2 - x3, x1, x2, x3], -1).reshape(-1, 4)
    return x, (wu * wv * wz * (1 - u) ** 2 * (1 - v)).ravel()


def triangle_rule(n):
    """Collapsed Gauss rule on y1, y2 >= 0, y1 + y2 <= 1 (area 1/2); exact to degree 2n - 2."""
    t, wt = np.polynomial.legendre.leggauss(n)
    t, wt = (t + 1) / 2, wt / 2
    u, v = np.meshgrid(t, t, indexing="ij")
    wu, wv = np.meshgrid(wt, wt, indexing="ij")
    return np.stack([u, (1 - u) * v], -1).reshape(-1, 2), (wu * wv * (1 - u)).ravel()


# --- kinematics ------------------------------------------------------------------
def _photon_pols(k):
    """Two real linear polarizations of a photon with momentum in the xy-plane."""
    kh = k[1:] / np.linalg.norm(k[1:])
    return [np.array([0, 0, 0, 1.0]), np.array([0, -kh[1], kh[0], 0.0])]


def decay_kinematics(s, y):
    """gamma*(q) -> photons k1, k2, k3 at rest, y_i = s_jk/s; incoming momenta (q, -k1, -k2, -k3).

    Returns the momenta and the physical polarizations: three for q, two per photon.
    """
    rs = np.sqrt(s)
    E = (1 - np.asarray(y, float)) * rs / 2
    c12 = 1 - s * y[2] / (2 * E[0] * E[1])
    s12 = np.sqrt(max(0.0, 1 - c12 * c12))
    k1, k2 = E[0] * np.array([1, 1, 0, 0.0]), E[1] * np.array([1, c12, s12, 0.0])
    q = np.array([rs, 0, 0, 0.0])
    k3 = q - k1 - k2
    pols = [[np.array([0, 1, 0, 0.0]), np.array([0, 0, 1, 0.0]), np.array([0, 0, 0, 1.0])]]
    pols += [_photon_pols(k) for k in (k1, k2, k3)]
    return [q, -k1, -k2, -k3], pols


def scattering_kinematics(z, omega=1.0):
    """gamma gamma -> gamma gamma in the CM frame, cos(theta) = z; incoming (k1, k2, -k3, -k4)."""
    sz = np.sqrt(1 - z * z)
    k1, k2 = omega * np.array([1, 0, 0, 1.0]), omega * np.array([1, 0, 0, -1.0])
    k3, k4 = omega * np.array([1, sz, 0, z]), omega * np.array([1, -sz, 0, -z])

    def pols(k):
        kh = k[1:] / np.linalg.norm(k[1:])
        return [np.array([0, 0, 1.0, 0]), np.array([0.0, *np.cross([0, 1.0, 0], kh)])]
    return [k1, k2, -k3, -k4], [pols(k) for k in (k1, k2, k3, k4)]


# --- the box ------------------------------------------------------------------------
def _chain_trace(E0, mats):
    """Tr[E0 M1 E1 M2 E2 M3 E3 M4] with pol axes on E's and option axes on M's.

    mats alternates slot arrays (O, 4, 4) and vertex arrays (P, 4, 4): [M1, E1, M2, E2, M3, E3, M4].
    Returns axes (P0, P1, P2, P3, O1, O2, O3, O4).
    """
    M = np.einsum("aij,ojk->aoik", E0, mats[0])
    M = np.einsum("aoij,bjk->aobik", M, mats[1])
    M = np.einsum("aobij,pjk->aobpik", M, mats[2])
    M = np.einsum("aobpij,cjk->aobpcik", M, mats[3])
    M = np.einsum("aobpcij,qjk->aobpcqik", M, mats[4])
    M = np.einsum("aobpcqij,djk->aobpcqdik", M, mats[5])
    M = np.einsum("aobpcqdij,rjk->aobpcqdrik", M, mats[6])
    return np.transpose(np.trace(M, axis1=-2, axis2=-1), (0, 2, 4, 6, 1, 3, 5, 7))


def _ordering_traces(pp, Ev):
    """x-independent traces for one ordering (trace order 0, a, b, c)."""
    K = np.array([-pp[0], pp[2] + pp[3], pp[3]])                 # K_3 = 0
    X = np.array([ONE] + [slash(k) for k in K])                  # slot options: 1, K0, K1, K2
    T0 = _chain_trace(Ev[0], [X, Ev[1], X, Ev[2], X, Ev[3], X])
    T2 = {}
    for i, j in itertools.combinations(range(4), 2):
        acc = 0
        for al in range(4):
            slots = [G[al][None] if k == i else GL[al][None] if k == j else X for k in range(4)]
            acc = acc + _chain_trace(Ev[0], [slots[0], Ev[1], slots[1], Ev[2], slots[2], Ev[3], slots[3]])
        T2[(i, j)] = acc
    T4 = 0
    for pairing in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        for al in range(4):
            for be in range(4):
                mats = [None] * 4
                mats[pairing[0][0]], mats[pairing[0][1]] = G[al][None], GL[al][None]
                mats[pairing[1][0]], mats[pairing[1][1]] = G[be][None], GL[be][None]
                T4 = T4 + _chain_trace(Ev[0], [mats[0], Ev[1], mats[1], Ev[2], mats[2], Ev[3], mats[3]])[..., 0, 0, 0, 0]
    return K, T0, T2, T4


def _ordering_values(K, T0, T2, T4, x, w, kmax, full):
    N = x.shape[0]
    R = _feynman_R(K, x)
    N0, N2 = _numerators(T0, T2, x)
    pols = T0.shape[:4]
    if full:
        D = 1 - R
        return (N0.sum(-1) / D ** 2 - N2.sum(-1) / (2 * D) - T4[..., None] * np.log(D) / 4) @ w
    out = np.zeros(pols + (kmax + 1,), complex)
    for k in range(kmax + 1):
        acc = np.zeros(pols + (N,), complex)
        for jd in range(min(k, 4) + 1):
            if (k - jd) % 2 == 0:
                n = (k - jd) // 2
                acc += N0[..., jd] * ((n + 1) * R ** n)                      # 1/Delta^2
        for jd in range(min(k, 2) + 1):
            if (k - jd) % 2 == 0:
                n = (k - jd) // 2
                acc -= N2[..., jd] * (R ** n / 2)                            # -1/(2 Delta)
        if k % 2 == 0 and k > 0:
            acc += T4[..., None] * (R ** (k // 2) / (k // 2) / 4)             # -log(Delta)/4
        out[..., k] = acc @ w
    return out


def _feynman_R(K, x):
    """R(x) of Delta = m^2 - R at the barycentric nodes x, for the offsets K (K_3 = 0)."""
    Kf = np.vstack([K, np.zeros(4)])
    P = x @ Kf
    return (x * np.einsum("jm,jm,m->j", Kf, Kf, ETA)).sum(1) - np.einsum("nm,nm,m->n", P, P, ETA)


def _numerators(T0, T2, x):
    """(N0, N2): the trace numerators at the nodes x, by degree in lambda (last axis)."""
    N = x.shape[0]
    A = np.zeros((4, N, 2, 4))                                    # slot, node, lambda degree, option
    A[:, :, 0, 0] = 1.0
    for j in range(4):
        for i in range(3):
            A[j, :, 1, i + 1] = float(i == j) - x[:, i]
    pols = T0.shape[:4]
    N0 = np.zeros(pols + (N, 5), complex)
    for ds in itertools.product((0, 1), repeat=4):
        N0[..., sum(ds)] += np.einsum("PQRSabcd,na,nb,nc,nd->PQRSn", T0, A[0, :, ds[0]], A[1, :, ds[1]],
                                      A[2, :, ds[2]], A[3, :, ds[3]], optimize=True)
    N2 = np.zeros(pols + (N, 3), complex)
    for (i, j), T in T2.items():
        k, l = (m for m in range(4) if m not in (i, j))
        idx = [slice(None)] * 8
        idx[4 + i] = idx[4 + j] = 0
        Tij = T[tuple(idx)]
        for dk, dl in itertools.product((0, 1), repeat=2):
            N2[..., dk + dl] += np.einsum("PQRSab,na,nb->PQRSn", Tij, A[k, :, dk], A[l, :, dl], optimize=True)
    return N0, N2


def box(p, pols, rule, kmax=8, full=False):
    """sum over orderings of J for every polarization combination, axes in leg order.

    full=False: coefficients of lambda^k, k = 0..kmax, of the momentum scaling.
    full=True: the value at lambda = 1 with the zero-momentum constant subtracted.
    """
    x, w = rule
    Ev_leg = [np.array([slash(e) for e in pl]) for pl in pols]
    total = 0
    for perm in itertools.permutations([1, 2, 3]):
        pp = [p[0]] + [p[i] for i in perm]
        Ev = [Ev_leg[0]] + [Ev_leg[i] for i in perm]
        data = _ordering_traces(pp, Ev)
        inv = [0] + [1 + perm.index(leg) for leg in (1, 2, 3)]
        val = _ordering_values(*data, x, w, kmax, full)
        if full:
            val = val - _ordering_values(*data, x, w, 0, False)[..., 0]
        total = total + np.transpose(val, inv + ([] if full else [4]))
    return total


# --- Dicus-Kao-Repko's effective Lagrangians (hep-ph/9709415, eqs. (13)-(15)) -------------
def _lagrangian_terms(P, F):
    """Their omega^4, omega^6 and omega^8 Lagrangians for photons in slots 1-4, m = alpha = 1.

    Eq. (14) is written as Heinzl, King and Mercuri-Baron (arXiv:2510.19921) quote it in
    eq. (L.4.2), after checking it; eq. (15) is their (L.4.4). With A = e exp(-ipx),
    F -> -i(p e - e p) and d -> -ip, so the phases are 1, -1 and 1.
    """
    low = lambda T: ETA[:, None] * T * ETA[None, :]
    lowv = lambda p: ETA * p
    dot = lambda a, b: (a * ETA) @ b
    FF = lambda A, B: np.einsum("mn,mn->", low(A), B)
    chain = lambda A, B, C, D: np.einsum("mn,nl,lr,rm->", low(A), B, low(C), D)
    p1, p2, p3, p4 = P
    F1, F2, F3, F4 = F
    eta = np.diag(ETA)
    eh = 5 * FF(F1, F2) * FF(F3, F4) - 14 * chain(F1, F2, F3, F4)
    t1 = FF(F1, F2) * (lowv(p1) @ F3 @ eta @ F4 @ lowv(p1))
    w6 = -(t1 + 3 * dot(p1, p2) * FF(F1, F2) * FF(F3, F4) + 11 * dot(p1, p3) * chain(F1, F2, F3, F4))
    u1 = dot(p1, p2) * dot(p3, p4) * FF(F1, F2) * FF(F3, F4)
    u2 = dot(p1, p3) * dot(p2, p4) * FF(F1, F2) * FF(F3, F4)
    u3 = (p3 @ low(F1) @ F2 @ lowv(p3)) * (p1 @ low(F3) @ F4 @ lowv(p1))
    return np.array([eh / 180, w6 / 945, (-33 * u1 + 106 * u2 - 262 * u3) / 9450])


def lagrangian_amplitudes(p, e):
    """Matrix elements of their eqs. (13), (14), (15) for incoming momenta p and polarizations e,
    summed over the 24 assignments of the photons to the four field strengths."""
    F = [np.outer(pi, ei) - np.outer(ei, pi) for pi, ei in zip(p, e)]
    return sum(_lagrangian_terms([p[i] for i in perm], [F[i] for i in perm])
               for perm in itertools.permutations(range(4)))


# --- the three-photon density ----------------------------------------------------------
def density_series_coefficients(kmax, feyn_n, dal_n):
    """rho_Pi/(alpha/pi)^4 = sum_n c_n s^(4+n), from the exact low-energy expansion.

    The lambda^k coefficient is a polynomial of degree <= k on the simplex, and the
    order s^(4+n) is a polynomial of degree 4 + n on the Dalitz triangle, so the rules
    are exact when 2 feyn_n - 3 >= kmax and 2 dal_n - 2 >= 4 + nmax.
    Returns (c, largest coefficient at an order that must vanish).
    """
    rule = simplex_rule(feyn_n)
    nmax = (kmax - 8) // 2
    acc, worst = np.zeros(nmax + 1), 0.0
    for (y1, y2), wy in zip(*triangle_rule(dal_n)):
        p, pols = decay_kinematics(1.0, (y1, y2, 1 - y1 - y2))
        J = box(p, pols, rule, kmax).real
        worst = max(worst, np.abs(J[..., [k for k in range(1, kmax + 1) if k % 2 or k == 2]]).max())
        for n in range(nmax + 1):
            acc[n] += wy * sum((J[..., a] * J[..., 8 + 2 * n - a]).sum()
                               for a in range(4, kmax + 1, 2) if 4 <= 8 + 2 * n - a <= kmax)
    return acc / 4608.0, worst


def amplitude_products(kmax, feyn_n, dal_n):
    """M[a, b] = (1/4608) int_Dalitz sum_pol J_a J_b for even a, b in [4, kmax], at s = 1.

    The density of the amplitude truncated after lambda^kmax is
    rho_K(s)/(alpha/pi)^4 = sum_ab M[a, b] s^((a+b)/2). The lambda^k coefficient is
    a polynomial of degree <= k on the simplex, and sum_pol J_a J_b one of degree
    (a+b)/2 on the Dalitz triangle (the summed amplitude obeys the Ward identity at
    every order), so the rules are exact when 2 feyn_n - 3 >= kmax and
    2 dal_n - 2 >= kmax. Returns (M, largest coefficient at an order that must vanish).
    """
    rule = simplex_rule(feyn_n)
    orders = list(range(4, kmax + 1, 2))
    forbidden = [k for k in range(1, kmax + 1) if k % 2 or k == 2]
    M, worst = np.zeros((kmax + 1, kmax + 1)), 0.0
    for (y1, y2), wy in zip(*triangle_rule(dal_n)):
        p, pols = decay_kinematics(1.0, (y1, y2, 1 - y1 - y2))
        J = box(p, pols, rule, kmax).real.reshape(-1, kmax + 1)
        worst = max(worst, np.abs(J[:, forbidden]).max())
        M[np.ix_(orders, orders)] += wy * (J[:, orders].T @ J[:, orders])
    return M / 4608.0, worst


def density_full(s, feyn_n, dal_n):
    """rho_Pi/(alpha/pi)^4 at 0 < s < 4 from the unexpanded amplitude."""
    rule, total = simplex_rule(feyn_n), 0.0
    for (y1, y2), wy in zip(*triangle_rule(dal_n)):
        p, pols = decay_kinematics(s, (y1, y2, 1 - y1 - y2))
        total += wy * (np.abs(box(p, pols, rule, full=True)) ** 2).sum()
    return total / 4608.0


def density_series(s, nterms=len(SERIES), lead_factor=1):
    """sum_n SERIES[n] s^(4+n) to nterms terms, with SERIES[0] multiplied by lead_factor."""
    s = mp.mpf(s)
    return sum(mp.mpf(SERIES[n]) * (lead_factor if n == 0 else 1) * s ** (4 + n) for n in range(nterms))


# --- an envelope for the truncated amplitude (note E4, Section 12) ------------------
# With s = lambda^2 and the momenta of s = 1, each ordering has Delta = 1 - lambda^2 R(x),
# where R = x0 x3 + s_a x0 x2 + s_b x1 x3 and s_a + s_b <= 1 are two Dalitz invariants,
# so 0 <= R <= 1/4. A slot of degree one is K_j - sum_i x_i K_i: every K_i^0 lies in
# [-1, 0] and |K_i| <= 1/2, so its norm is at most 2. The polarizations are spatial unit
# vectors (norm 1), |gamma^a| = 1, and |Tr M| <= 4 |M| for 4x4 matrices.
SLOT_NORM = 2
N0_BOUND = tuple(4 * math.comb(4, j) * SLOT_NORM ** j for j in range(5))
N2_BOUND = tuple(6 * 4 * 4 * math.comb(2, j) * SLOT_NORM ** j for j in range(3))
T4_BOUND = 3 * 4 * 4 * 4

# M[a, b] of amplitude_products(22, 13, 12) for even 4 <= a <= b <= 22, computed on
# 24 October 2026 in 1508 s (.agent/evidence/R9-products-data.json). Its anti-diagonals
# reproduce SERIES to 2e-15; the tests check that and recompute the first entries.
PRODUCTS_K22 = {
    (4, 4): 1.4574759945130298e-06, (4, 6): 3.419148866679732e-07, (4, 8): 7.16271590940903e-08,
    (4, 10): 1.487791107561341e-08, (4, 12): 3.122393030902729e-09, (4, 14): 6.642947459846598e-10,
    (4, 16): 1.4321219593218012e-10, (4, 18): 3.124418046396148e-11, (4, 20): 6.888202258513322e-12,
    (4, 22): 1.5325730816298437e-12, (6, 6): 8.055950759035081e-08, (6, 8): 1.6925058829680756e-08,
    (6, 10): 3.522651609342559e-09, (6, 12): 7.40375568728861e-10, (6, 14): 1.5769028738624523e-10,
    (6, 16): 3.402483508925052e-11, (6, 18): 7.428150049039516e-12, (6, 20): 1.6385403271311567e-12,
    (6, 22): 3.6472904977655623e-13, (8, 8): 3.564007821467834e-09, (8, 10): 7.431062498817709e-10,
    (8, 12): 1.564002520615289e-10, (8, 14): 3.334797495405627e-11, (8, 16): 7.201892705003724e-12,
    (8, 18): 1.5734292270252193e-12, (8, 20): 3.4728488641321706e-13, (8, 22): 7.734273670780665e-14,
    (10, 10): 1.5516606845203076e-10, (10, 12): 3.269606875587014e-11, (10, 14): 6.9781968624935034e-12,
    (10, 16): 1.5082068014705765e-12, (10, 18): 3.297186591436571e-13, (10, 20): 7.281460691753358e-14,
    (10, 22): 1.6223789038956793e-14, (12, 12): 6.896314705425464e-12, (12, 14): 1.4730338285493504e-12,
    (12, 16): 3.1857997969987245e-13, (12, 18): 6.968538685222412e-14, (12, 20): 1.5396414403619623e-14,
    (12, 22): 3.431832642223813e-15, (14, 14): 3.1484569081461854e-13, (14, 16): 6.81310399990143e-14,
    (14, 18): 1.4909780998013255e-14, (14, 20): 3.2954994661023464e-15, (14, 22): 7.348097763521772e-16,
    (16, 16): 1.4750106050791702e-14, (16, 18): 3.229184382150497e-15, (16, 20): 7.13984610799263e-16,
    (16, 22): 1.5924576814316993e-16, (18, 18): 7.071900419630817e-16, (18, 20): 1.564071684909166e-16,
    (18, 22): 3.489337547599398e-17, (20, 20): 3.460063266079589e-17, (20, 22): 7.720807984091702e-18,
    (22, 22): 1.7231439476225949e-18,
}


def products_matrix(table=PRODUCTS_K22):
    """(M, K): the symmetric matrix of a products table and its truncation order K."""
    K = max(b for _, b in table)
    M = np.zeros((K + 1, K + 1))
    for (a, b), v in table.items():
        M[a, b] = M[b, a] = v
    return M, K


def envelope_integral(n):
    """n!(n+1)!/(2n+3)!, an upper bound of int over the simplex of R^n at every Dalitz point.

    R <= x0 x3 + t x0 x2 + (1-t) x1 x3 with t = s_a. The integral of its n-th power is
    convex in t, and both endpoints give int x3^n (x0+x1)^n, a Dirichlet(1, 2, 1) moment.
    """
    return math.factorial(n) * math.factorial(n + 1) / math.factorial(2 * n + 3)


def amplitude_envelope(s, K):
    """E with |A - A_K| <= E at every Dalitz point and polarization, for 0 < s < 4.

    A_K keeps the orders lambda^k, 1 <= k <= K, of the summed orderings. E adds over the
    six orderings the tails, with u = s R <= s/4:
    sum_{n>=n0} (n+1) u^n <= (n0+1) u^n0/(1-u)^2, sum u^n <= u^n0/(1-u) and
    sum u^n/n <= u^n0/(n0 (1-u)); then int u^n0 <= s^n0 envelope_integral(n0).
    """
    if not 0 < s < 4:
        raise ValueError("the envelope requires 0 < s < 4")
    lam, umax = math.sqrt(s), s / 4
    total = 0.0
    for jd, bound in enumerate(N0_BOUND):                       # N0/Delta^2
        n0 = (K - jd) // 2 + 1
        total += lam ** jd * bound * (n0 + 1) * s ** n0 * envelope_integral(n0) / (1 - umax) ** 2
    for jd, bound in enumerate(N2_BOUND):                       # -N2/(2 Delta)
        n0 = (K - jd) // 2 + 1
        total += lam ** jd * bound / 2 * s ** n0 * envelope_integral(n0) / (1 - umax)
    n0 = K // 2 + 1                                             # -T4 log(Delta)/4
    total += T4_BOUND / 4 * s ** n0 * envelope_integral(n0) / (n0 * (1 - umax))
    return 6 * total


def density_truncated(s, M):
    """rho_K/(alpha/pi)^4 = sum_ab M[a, b] s^((a+b)/2) from amplitude_products."""
    s = mp.mpf(s)
    n = M.shape[0]
    return sum(mp.mpf(float(M[a, b])) * s ** mp.mpf((a + b) / 2) for a in range(n) for b in range(n) if M[a, b])


def density_envelope(s, K, M):
    """Bound of |rho - rho_K|/(alpha/pi)^4, by Cauchy-Schwarz over the Dalitz triangle (area 1/2)
    and the 24 polarizations: rho = (1/4608) int sum_pol |A|^2, so
    |rho - rho_K| <= 2 sqrt(rho_K eps) + eps with eps = 12 E^2/4608 = E^2/384."""
    eps = mp.mpf(amplitude_envelope(float(s), K)) ** 2 / 384
    return 2 * mp.sqrt(density_truncated(s, M) * eps) + eps


def truncation_moment_bounds(r, alpha, M, K, s1, factor=None, a=0):
    """How far the three-photon parts of M0 and D = M1 - 2 M0 can move when the six-term
    model is replaced by the one-loop density below 4m^2 (m = 1; note E4, Section 12).

    For s <= s1: |rho - rho_6| <= density_envelope + |rho_K - rho_6|, an analytic bound in
    float64 plus the cross terms beyond s^9 that rho_K keeps. For s1 < s < 4: the stated
    assumption |rho - rho_6| <= rho_6. Returns a dict, (alpha/pi)^4 included.
    """
    with mp.workdps(20):                  # a bound: the envelope itself is float64
        r, a, s1 = mp.mpf(r), mp.mpf(a), mp.mpf(s1)
        if not (0 < s1 < 4 and r > a >= 0):
            raise ValueError('Require 0 < s1 < 4 and r > a >= 0')
        F = (lambda x: 1) if factor is None else (lambda x: factor(x, a))
        pref = (mp.mpf(alpha) / mp.pi) ** 4
        x1 = mp.sqrt(s1)
        w = lambda x: mp.e ** (-r * x) * F(x) * 2 * x * pref
        dev = lambda x: density_envelope(x * x, K, M) + abs(density_truncated(x * x, M) - density_series(x * x))
        scale = 2 * mp.mpf(SERIES[0]) * mp.factorial(9) / (r - a) ** 10 * pref
        low, high = [0, x1 / 4, x1 / 2, 3 * x1 / 4, x1], [x1, (x1 + 2) / 2, 2]
        quad = lambda f, cuts: nl.quad_relative(lambda x: w(x) * f(x), cuts, scale)
        rho6 = lambda x: density_series(x * x)
        return dict(model_M0=quad(rho6, [0] + high),
                    model_D=-quad(lambda x: (2 - x) * rho6(x), [0] + high),
                    bounded_M0=quad(dev, low), bounded_D=quad(lambda x: (2 - x) * dev(x), low),
                    assumed_M0=quad(rho6, high), assumed_D=quad(lambda x: (2 - x) * rho6(x), high))


# --- the pair channel at O(alpha^2) ----------------------------------------------------
def kallen_sabry_density(s, alpha):
    """Irreducible two-loop rho_Pi = Im Pi^(2)/pi, Laporta-Jentschura (arXiv:2403.07127) eq. (55).

    Tends to alpha^2/4 at threshold (the first Coulomb term) and to alpha^2/(4 pi^2) at high energy.
    """
    s, a = mp.mpf(s), mp.mpf(alpha)
    if s <= 4:
        return mp.mpf(0)
    v = mp.sqrt(1 - 4 / s)
    if 1 - v < mp.mpf("1e-20"):              # x log x -> 0 analytically, nan numerically
        return (a / mp.pi) ** 2 / 4
    xv, L = (v - 1) / (v + 1), mp.log((1 - v) / (1 + v))
    Phi = lambda n, z: mp.polylog(n, z) + 2 * mp.polylog(n, -z)
    br = ((v ** 4 - 2 * v ** 2 - 3) / 6 * (Phi(1, xv) * L - 2 * Phi(2, xv))
          + (3 * v - v ** 3) / 6 * (2 * Phi(1, xv) + 3 * L)
          + (7 * v ** 4 - 22 * v ** 2 - 33) * L / 48 + (5 * v - 3 * v ** 3) / 8)
    return (a / mp.pi) ** 2 * br


# --- the window in the six-term low-energy cutoff model ------------------------------
def _pair_dnu(alpha, loops):
    one = nl.dirac_dnu(alpha)
    if loops == 1:
        return one
    return lambda x: one(x) + 2 * x * kallen_sabry_density(x * x, alpha)


def profile_moments(r, alpha, k=0, pair_loops=2, nterms=len(SERIES), smax=4, factor=None, a=0,
                    three_photon_loops=1):
    """(pair, three-photon) parts of int x^k e^{-rx} F(x) d nu, m = 1.

    The three-photon density is the series of SERIES truncated to nterms and used up
    to s = smax (its part above 4m^2 is not included; see note E4). With
    three_photon_loops=2 its leading coefficient carries the O(alpha^5) factor
    1 + KAPPA_2 alpha/pi. factor is an exterior factor F(x, a) of note E3,
    Section 11.1, valid for r > a.
    """
    r, a = mp.mpf(r), mp.mpf(a)
    alpha, smax = mp.mpf(alpha), mp.mpf(smax)
    if not all(mp.isfinite(v) for v in (r, a, alpha, smax)):
        raise ValueError('r, a, alpha and smax must be finite')
    if a < 0 or r <= a or alpha <= 0:
        raise ValueError('Require r > a >= 0 and alpha > 0')
    if isinstance(k, bool) or not isinstance(k, Integral) or k < 0:
        raise ValueError('k must be a nonnegative integer')
    if isinstance(nterms, bool) or not isinstance(nterms, Integral) or not 1 <= nterms <= len(SERIES):
        raise ValueError('nterms must select 1..len(SERIES) stored coefficients')
    if pair_loops not in (1, 2) or isinstance(pair_loops, bool):
        raise ValueError('pair_loops must be 1 or 2')
    if three_photon_loops not in (1, 2) or isinstance(three_photon_loops, bool):
        raise ValueError('three_photon_loops must be 1 or 2')
    if not 0 < smax <= 4:
        raise ValueError('The low-energy cutoff model requires 0 < smax <= 4')
    F = (lambda x: 1) if factor is None else (lambda x: factor(x, a))
    d = r - a
    dnu = _pair_dnu(alpha, pair_loops)
    pair = nl.quad_relative(lambda x: x ** k * mp.e ** (-r * x) * F(x) * dnu(x),
                             [2, 2 + 1 / d, 2 + 4 / d, 2 + 16 / d, 3, 4, 8, mp.inf],
                             mp.e ** (-2 * r) * F(mp.mpf(2)))
    c0 = 1 if three_photon_loops == 1 else 1 + mp.mpf(KAPPA_2[0]) / KAPPA_2[1] * alpha / mp.pi
    lead = 2 * mp.mpf(SERIES[0]) * c0 * mp.factorial(9 + k) / d ** (10 + k) * (mp.mpf(alpha) / mp.pi) ** 4
    xmax = mp.sqrt(smax)
    cuts = [c for c in (0, 1 / d, 4 / d, 10 / d, 20 / d, 1, xmax) if c <= xmax]
    three = nl.quad_relative(lambda x: x ** k * mp.e ** (-r * x) * F(x) * 2 * x * (mp.mpf(alpha) / mp.pi) ** 4
                              * density_series(x * x, nterms, c0), sorted(set(cuts)), lead)
    return pair, three


def window(alpha, pair_loops=2, nterms=len(SERIES), factor=None, a=0, guess=(22.5, 20.6), dps=30,
           three_photon_loops=1):
    """(r_x, r_Gamma): pair and three-photon parts of Phi equal, and Gamma = 2m."""
    with mp.workdps(dps):
        kw = dict(pair_loops=pair_loops, nterms=nterms, factor=factor, a=a,
                  three_photon_loops=three_photon_loops)

        def log_ratio(r):
            p, t = profile_moments(r, alpha, 0, **kw)
            return mp.log(p) - mp.log(t)

        def gamma_minus_two(r):
            p0, t0 = profile_moments(r, alpha, 0, **kw)
            p1, t1 = profile_moments(r, alpha, 1, **kw)
            return (p1 + t1) / (p0 + t0) - 2
        return mp.findroot(log_ratio, guess[0]), mp.findroot(gamma_minus_two, guess[1])
