"""E2.3b: admissible tensor structures of <F_{mu nu} F_{rho sigma}>.

Checks the finite-dimensional linear algebra behind notes/E2b_tensor_classification.tex.
The starting point is the most general Hermitian 6x6 matrix on 2-form components;
F = dA is never assumed. Covariance and the Bianchi identity are imposed as linear
equations and the surviving structures are counted. Positivity and CPT enter only
afterwards, as conditions on the coefficients.

What this does NOT check: the measure-theoretic steps of the note (that the Fourier
transform is a matrix-valued measure, and its covariant disintegration over orbits).
Those are proved or cited in the note, not here.

Conventions: metric diag(+,-,-,-); lower-index components ordered
E1,E2,E3 = F01,F02,F03 and B1,B2,B3 = F23,F31,F12.
"""

import itertools

import sympy as sp

G = sp.diag(1, -1, -1, -1)
PAIRS = [(0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2)]


def pair_index(m, n):
    for k, (a, b) in enumerate(PAIRS):
        if (a, b) == (m, n):
            return k, 1
        if (a, b) == (n, m):
            return k, -1
    return None, 0


def lorentz_generators():
    """Basis of so(1,3) acting on contravariant vectors."""
    out = []
    for a, b in itertools.combinations(range(4), 2):
        X = sp.zeros(4)
        for nu in range(4):
            X[a, nu] += G[b, nu]
            X[b, nu] -= G[a, nu]
        out.append(X)
    return out


def on_two_forms(Xcov):
    """Induced action of a covector generator on lower-index 2-form components."""
    d = sp.zeros(6)
    for A, (m, n) in enumerate(PAIRS):
        for al in range(4):
            k, s = pair_index(al, n)
            if k is not None:
                d[A, k] += Xcov[m, al] * s
            k, s = pair_index(m, al)
            if k is not None:
                d[A, k] += Xcov[n, al] * s
    return d


def general_hermitian():
    syms = sp.symbols("w0:36", real=True)
    it = iter(syms)
    W = sp.zeros(6)
    for i in range(6):
        W[i, i] = next(it)
    for i in range(6):
        for j in range(i + 1, 6):
            re, im = next(it), next(it)
            W[i, j] = re + sp.I * im
            W[j, i] = re - sp.I * im
    return W, list(syms)


def entry(W, m, n, r, s):
    A, sa = pair_index(m, n)
    B, sb = pair_index(r, s)
    if A is None or B is None:
        return 0
    return sa * sb * W[A, B]


def bianchi(W, p_low, slot="first"):
    """Cyclic sum p_[lambda W_{mu nu]},rho sigma (or on the second pair)."""
    eqs = []
    for lam, mu, nu in itertools.combinations(range(4), 3):
        for r, s in PAIRS:
            if slot == "first":
                f = lambda a, b: entry(W, a, b, r, s)
            else:
                f = lambda a, b: entry(W, r, s, a, b)
            eqs.append(p_low[lam] * f(mu, nu) + p_low[mu] * f(nu, lam) + p_low[nu] * f(lam, mu))
    return eqs


def stabilizer(p_up):
    c = sp.symbols("c0:6")
    X = sum((ci * Xi for ci, Xi in zip(c, lorentz_generators())), sp.zeros(4))
    sol = sp.solve(list(X * p_up), c, dict=True)
    Xs = X.subs(sol[0]) if sol else X
    free = sorted(Xs.free_symbols & set(c), key=str)
    return [Xs.subs({h: int(h == f) for h in free}) for f in free]


def invariance(W, generators):
    eqs = []
    for X in generators:
        d = on_two_forms(G * X * G)
        eqs += list(d * W + W * d.T)
    return eqs


def nullspace(eqs, W, syms):
    real = []
    for e in eqs:
        e = sp.expand(e)
        real += [sp.re(e), sp.im(e)]
    real = [e for e in real if e != 0]
    A, _ = sp.linear_eq_to_matrix(real, syms)
    return [W.subs(dict(zip(syms, v))) for v in A.nullspace()]


def structures(p_up, use_bianchi):
    W, syms = general_hermitian()
    eqs = invariance(W, stabilizer(p_up))
    if use_bianchi:
        p_low = list(G * p_up)
        eqs += bianchi(W, p_low, "first") + bianchi(W, p_low, "second")
    return nullspace(eqs, W, syms)


def T_tensor(p_low):
    return {(m, n, r, s): p_low[m] * p_low[r] * G[n, s] - p_low[n] * p_low[r] * G[m, s]
            - p_low[m] * p_low[s] * G[n, r] + p_low[n] * p_low[s] * G[m, r]
            for m, n, r, s in itertools.product(range(4), repeat=4)}


def dual_second(t):
    out = {}
    for m, n, r, s in itertools.product(range(4), repeat=4):
        v = 0
        for a, b in itertools.permutations(range(4), 2):
            e = sp.LeviCivita(r, s, a, b)
            if e:
                v += sp.Rational(1, 2) * e * G[a, a] * G[b, b] * t[m, n, a, b]
        out[m, n, r, s] = v
    return out


def dual_first(t):
    out = {}
    for m, n, r, s in itertools.product(range(4), repeat=4):
        v = 0
        for a, b in itertools.permutations(range(4), 2):
            e = sp.LeviCivita(m, n, a, b)
            if e:
                v += sp.Rational(1, 2) * e * G[a, a] * G[b, b] * t[a, b, r, s]
        out[m, n, r, s] = v
    return out


def as6(t):
    return sp.Matrix(6, 6, lambda A, B: t[PAIRS[A] + PAIRS[B]])


def span_equal(found, expected):
    """Same real span, compared as vectors in R^72 (real and imaginary parts)."""
    vec = lambda M: [sp.re(x) for x in M] + [sp.im(x) for x in M]
    a = sp.Matrix([vec(M) for M in found])
    b = sp.Matrix([vec(M) for M in expected])
    return a.rank() == b.rank() == sp.Matrix.vstack(a, b).rank()


REST = sp.Matrix([1, 0, 0, 0])
BOOSTED = sp.Matrix([9, 2, 3, 6])   # s = 32. At rest, or with momentum in a coordinate
                                   # plane, some cyclic Bianchi terms vanish identically
                                   # and an implementation error there goes unseen.
NULL = sp.Matrix([1, 0, 0, 1])


# ---------------------------------------------------------------- massive sector

def test_massive_without_bianchi_admits_dual_structures():
    # Discriminating twin: covariance alone leaves EE, BB and two EB structures.
    assert len(structures(REST, use_bianchi=False)) == 4


def test_massive_with_bianchi_leaves_only_minus_T():
    found = structures(REST, use_bianchi=True)
    assert len(found) == 1
    assert span_equal(found, [-as6(T_tensor(list(G * REST)))])


def test_boosted_massive_momentum_also_leaves_only_minus_T():
    found = structures(BOOSTED, use_bianchi=True)
    assert len(found) == 1
    assert span_equal(found, [-as6(T_tensor(list(G * BOOSTED)))])


def test_minus_T_is_positive_for_a_boosted_massive_momentum():
    p_up = sp.Matrix([5, 3, 0, 0])            # s = 16, not at rest
    M = -as6(T_tensor(list(G * p_up))) / 16
    assert all(ev >= 0 for ev in M.eigenvals())
    assert M.rank() == 3


# ---------------------------------------------------------------- massless sector

def test_null_stabilizer_contains_null_translations():
    gens = stabilizer(NULL)
    assert len(gens) == 3
    boosts = [X for X in gens if any(X[0, i] != 0 for i in range(1, 4))]
    assert len(boosts) == 2      # the two null translations mix time and space


def test_null_with_bianchi_leaves_minus_T_and_its_dual():
    found = structures(NULL, use_bianchi=True)
    assert len(found) == 2
    t = T_tensor(list(G * NULL))
    assert span_equal(found, [-as6(t), sp.I * as6(dual_second(t))])


def test_null_positivity_bounds_but_does_not_remove_the_dual():
    t = T_tensor(list(G * NULL))
    a, ap = sp.symbols("alpha alphap", real=True)
    M = a * (-as6(t)) + ap * (sp.I * as6(dual_second(t)))
    assert M.eigenvals() == {2 * a + 2 * ap: 1, 2 * a - 2 * ap: 1, 0: 4}


def test_cpt_reality_removes_the_null_dual():
    # CPT for a Hermitian rank-2 tensor field: W_AB(p) = W_BA(p); with Hermiticity
    # the matrix is real symmetric. The dual structure is imaginary antisymmetric.
    t = T_tensor(list(G * NULL))
    odd = sp.I * as6(dual_second(t))
    assert odd.T == -odd and odd != sp.zeros(6)
    even = -as6(t)
    assert even.T == even and all(x.is_real for x in even)


def test_null_without_bianchi_is_larger():
    assert len(structures(NULL, use_bianchi=False)) == 4


# ---------------------------------------------------------------- p = 0

def test_lorentz_invariants_at_zero_momentum_are_indefinite():
    W, syms = general_hermitian()
    found = nullspace(invariance(W, lorentz_generators()), W, syms)
    assert len(found) == 2
    x, y = sp.symbols("x y", real=True)
    M = x * found[0] + y * found[1]
    evs = [sp.simplify(e) for e in M.eigenvals()]
    # every nonzero combination has eigenvalues of both signs
    assert sorted(evs, key=str) == sorted([sp.sqrt(x**2 + y**2), -sp.sqrt(x**2 + y**2)], key=str)


# ---------------------------------------------------------------- local terms

def test_bianchi_compatible_covariant_polynomials_are_multiples_of_T():
    p = sp.symbols("p0:4")
    p_low = list(G * sp.Matrix(p))
    s = sum(G[i, i] * p[i] ** 2 for i in range(4))
    gg = {(m, n, r, q): G[m, r] * G[n, q] - G[m, q] * G[n, r]
          for m, n, r, q in itertools.product(range(4), repeat=4)}
    eps = {k: sp.LeviCivita(*k) for k in itertools.product(range(4), repeat=4)}
    t = T_tensor(p_low)
    basis = [gg, eps, t, dual_second(t), dual_first(t),
             {k: s * v for k, v in gg.items()}, {k: s * v for k, v in eps.items()}]
    c = sp.symbols("k0:7")
    Pm = sp.zeros(6)
    for ci, b in zip(c, basis):
        Pm += ci * as6(b)
    eqs = bianchi(Pm, p_low, "first") + bianchi(Pm, p_low, "second")
    coeff_eqs = []
    for e in eqs:
        coeff_eqs += sp.Poly(sp.expand(e), *p).coeffs()
    sol = sp.solve(coeff_eqs, c, dict=True)[0]
    general = Pm.subs(sol)
    free = sorted(general.free_symbols & set(c), key=str)
    survivors = [general.subs({h: int(h == f) for h in free}) for f in free]
    survivors = [M for M in survivors if M != sp.zeros(6)]
    # The ansatz is linearly dependent (*T + T* = p^2 eps), so compare spans,
    # not free coefficients: the surviving tensors must all be multiples of T(p).
    assert survivors
    Tm = as6(t)
    for M in survivors:
        ratio = {sp.simplify(M[i, j] / Tm[i, j]) for i in range(6) for j in range(6) if Tm[i, j] != 0}
        zeros_match = all(sp.simplify(M[i, j]) == 0 for i in range(6) for j in range(6) if Tm[i, j] == 0)
        assert len(ratio) == 1 and zeros_match


def test_dual_identity_used_above():
    p = sp.symbols("p0:4")
    p_low = list(G * sp.Matrix(p))
    s = sum(G[i, i] * p[i] ** 2 for i in range(4))
    t = T_tensor(p_low)
    eps = {k: sp.LeviCivita(*k) for k in itertools.product(range(4), repeat=4)}
    lhs = as6(dual_first(t)) + as6(dual_second(t))
    assert sp.simplify(lhs - s * as6(eps)) == sp.zeros(6)


# ---------------------------------------------------------------- next-step link (not E2.3b)

def test_current_relation_under_maxwell_equation():
    # With the ADDITIONAL hypothesis d^mu F_{mu nu} = j_nu, W = -T a/s gives
    # <j_nu j_beta> = a (p_nu p_beta - s g_{nu beta}): the massive density of F
    # is the current density. Recorded for the next E2 step only.
    p_up = sp.Matrix([5, 3, 0, 0])
    p_low = list(G * p_up)
    s = 16
    t = T_tensor(p_low)
    J = sp.Matrix(4, 4, lambda nu, be: sum(p_up[m] * p_up[al] * (-t[m, nu, al, be])
                                          for m in range(4) for al in range(4)) / s)
    assert J == sp.Matrix(4, 4, lambda nu, be: p_low[nu] * p_low[be] - s * G[nu, be])
