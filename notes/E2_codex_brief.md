# E2 handoff brief — numerical/symbolic half (for Codex)

Repo: `physics of all`, branch off `remediation/priority-audit` at `97aa5c4`.
Work on a new branch **`e2/codex-numerics`**. Read `ROADMAP_CIENTIFICO.md`
section E2 and `paper/paper.tex` Theorem A (`thm:A`) + `paper/appendix.tex`
Appendix A before starting. The other half of E2 (the proof note
`notes/E2_positivity_H3.tex`, tensor-structure proof, literature) is done by
Claude in parallel — **do not create or edit that file**.

## Context in three sentences

Theorem A says: if the static response kernel is a positive Stieltjes function,
`G(Q²) = g_R²/Q² + ∫ dσ(s)/(Q²+s)` with `σ ≥ 0` (Hypothesis H3), then
`Φ(r) = δ(r)/r²` is the Laplace transform of `ν ≥ 0`, where
`∫f dν = g_R⁻² ∫ s f(√s) dσ(s)`. Stage E2 asks whether H3 follows from Wightman
positivity of `F_{μν}` in an abelian theory with electric matter only, at order
`O(q_W²)` in the probe. Your job is to build the numerical and symbolic
evidence that such a proof must be consistent with.

## House rules (non-negotiable; the test suite enforces the spirit)

1. **Every test has a discriminating twin that must fail** under the wrong
   sign/convention. A test that passes both ways is rejected.
2. Status vocabulary: `CHECKED` (numerics, no rigorous bound) vs `CERTIFIED`
   (interval enclosure / exact rational / proved). Never label a float or
   `mp.quad` result `CERTIFIED`.
3. No network at test time, fixed seeds, no new dependencies beyond
   `requirements.txt` (mpmath, numpy, scipy, sympy, matplotlib, pytest).
4. Touch **only new files** listed below. Do not edit `paper/`, `data/`,
   existing tests, or existing `reproducibility/*.py` (import them instead;
   `reproducibility/spectral_models.py` has `Model`, `dirac_density`,
   `scalar_density`).
5. `python -m pytest tests -q` must stay green (currently 86 passed, 1 skipped).

## Task C1 — E2.3c: one-loop consistency of ⟨FF⟩ (symbolic)

File: `tests/test_e2_one_loop.py`.

From Appendix A: `Π̄(Q²) = Q² ∫ ρ_J(s) ds / (s(s+Q²)) ≥ 0` and
`G(Q²) = g_R² / (Q²[1 − g_R² Π̄(Q²)])`.

Assert, with sympy:

- (a) The Euclidean photon propagator `D_E(Q²) = G(Q²)` expanded to `O(g_R⁴)`
  has Källén–Lehmann density `ρ_A(s) = g_R² δ(s) + g_R⁴ ρ_J(s)/s`, i.e. the
  `O(g_R⁴)` coefficient equals `∫ ρ_J(s) ds / (s(s+Q²))` exactly.
- (b) Build `⟨F_{μν}F_{ρσ}⟩(p) = T_{μνρσ}(p) D(p²)` with
  `T = p_μp_ρ η_{νσ} − p_νp_ρ η_{μσ} − p_μp_σ η_{νρ} + p_νp_σ η_{μρ}` from
  `F = ∂A` and the transverse propagator; verify symbolically that `T` is
  antisymmetric in (μν) and (ρσ), symmetric under pair exchange, and satisfies
  the Bianchi contraction `ε^{λμνκ} p_λ T_{μνρσ} = 0` (this is the algebraic
  fact behind "(B) eliminates the dual structure").
- (c) Static electric component: for `p = (0, **Q**)` (Euclidean),
  `⟨E_i E_j⟩ ∝ (Q_iQ_j − Q² δ_ij)·D_E(Q²)` up to sign convention — derive and
  assert the exact form.
- (d) With the one-loop Dirac density
  `ρ_J = q²/(12π²) (1 + 2m²/s) √(1 − 4m²/s)`, the resulting `dσ = g_R⁴ρ_J ds/s`
  reproduces the Uehling prefactor `2α/3π` (q=1, g_R² = 4πα).
- **Twin:** replacing `1 − g_R²Π̄` by `1 + g_R²Π̄` makes the `O(g_R⁴)` density
  negative — assert that it does.

## Task C2 — E2.3d: vector-meson toy model through the Hankel gate (numeric)

Files: `reproducibility/e2_toy_models.py`, `tests/test_e2_toy_models.py`.

**Correction to the roadmap:** a *pure* free Proca field (`G = g²/(Q²+m²)`,
no massless pole) is **not** a valid instance: `q(r) → 0` at infinity, so
`q_∞ = 0` and `δ = −r q′/q_∞` is undefined. Implement instead, and document
this in the module docstring:

- **T1 (photon + one massive vector):** `G = g_R²/Q² + w/(Q²+m²)`, `w > 0`.
  Then `σ = w δ_{m²}`, `ν` is one atom of weight `m²w/g_R²` at `x = m`, and
  `Φ(r) = (m² w/g_R²) e^{−mr}`. Compute `Φ` **from `G` numerically**
  (3D inverse Fourier → potential → Gauss-law charge → `δ` → `Φ`), not from the
  closed form, and assert agreement with the closed form.
- **T2 (photon + two massive vectors):** weights `w₁, w₂ > 0`, masses
  `m₁ < m₂`. Assert `Γ(r) = −(log Φ)′` decreases to `m₁` and the Hankel pencil
  `B_K` is exact at `K = 1`.
- **T3 — twin (ghost):** `w < 0` in T1/T2 (a negative-norm vector). Assert the
  positivity gate (`(−1)ⁿΦ⁽ⁿ⁾ > 0` for n ≤ 3 **and** `H₀ ≻ 0`) **refuses** it.
  For T2 with `w₂ < 0` small enough that `Φ > 0` and `−Φ′ > 0`, show the naive
  screening checks pass and only the full gate fails.
- **T4 — pure Proca (documenting the obstruction):** assert that `q_∞ = 0`
  numerically, and that the code raises a clear error instead of dividing by it.

Use mpmath at ≥ 40 digits for the Hankel steps; label all outputs `CHECKED`.

## Task C3 (optional, only if C1–C2 are done) — E4.1 test L

File: `tests/test_e4_noise_recovery.py`. Synthetic `Φ` samples from the T2
measure with controlled deterministic noise `|b̂_j − b_j| ≤ η`; assert the
upper bound from `interval_bounds.envelope_bound` stays `≥ m₁` for all η
tested and returns *no bound* (not a truncated value) once η is too large.

## Deliverables and handback

- One commit per task on `e2/codex-numerics`, message explaining *why*.
- Report back: test counts before/after, any formula in this brief you found
  to be wrong (say so — do not silently "fix" the physics), and the exact
  numerical tolerances you used.
