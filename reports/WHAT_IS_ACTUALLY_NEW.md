# WHAT IS ACTUALLY NEW

Generated 2026-09-11. No flattering language. Where novelty confidence is
low, it is stated as low.

## The finding that reorganises the paper

Raman's 2026 lecture notes (arXiv:2603.28454), read at equation level,
establish two things that the manuscript currently presents as its own
analytic contributions:

1. **eq. (119)-(120):** *If Π(Q²) is the vacuum polarization function
   then −Π(Q²)/Q² is a Stieltjes function.* Derived from the
   once-subtracted Källén–Lehmann dispersion relation with ρ(s) ≥ 0.
   This is the analytic content of Corollary A1.
2. **eq. (19)-(22):** complete monotonicity ⟺ positive semidefiniteness
   of the Hankel matrices of derivatives,
   (H₀)ᵢⱼ = (−1)^{i+j} f^{(i+j)}(x), (H₁)ᵢⱼ = (−1)^{i+j+1} f^{(i+j+1)}(x).
   This is the construction underlying Theorems B and E.

Both are presented there as **review material**. Neither can be claimed.

Equally important is what those notes do *not* contain: no static
potential, no Wilson loop, no position-space potential, and no
extraction of inf supp μ from the function. The threshold-recovery step
is absent.

## Per-result classification

| Result | Classification | Basis |
|---|---|---|
| Corollary A1 (Stieltjes VP) | **PREVIOUSLY_KNOWN** | Raman eq. (120) |
| Theorem B (CM as H3 falsifier) | **CLASSICAL_APPLICATION** | Raman eq. (19)–(22); Bernstein–Widder |
| Theorem C (Γ(r) bounds M_*) | **CLASSICAL_APPLICATION** | E = −lim t⁻¹ log Z_t is textbook; lattice effective mass |
| Theorem E (Hankel pencil → M_*) | **NEW_COMPUTATIONAL_APPLICATION** | pencil objects classical; λ_min(H₁,H₀) → inf supp not found in the QFT literature |
| Theorem D (edge law) | **UNCERTAIN_PRIORITY** | Watson's lemma is classical; Hinrichs–Polzer 2025 studies exactly this edge behaviour |
| Theorem F/G (sampled hierarchy, envelope) | **NEW_ASSEMBLY** | no precedent found for the sampled, differentiation-free form with a deterministic envelope |
| Theorem H (finite-window non-identifiability) | **NEW_ASSEMBLY** | concept known (Cover 2008); closed-form crossover not found |
| Claim J (one-form symmetry reading) | **NEW_INTERPRETATION** | the observable is not in the CM/QFT literature |

## The smallest scientifically defensible novelty claim

Strip everything that the literature already owns and this survives:

> For the reduced one-form symmetry-breaking profile Φ(r) = δ(r)/r²,
> the classical Laplace–Stieltjes positivity hierarchy becomes an
> *operational model-check on a physical hypothesis*: the same Hankel
> data that bound the threshold also **falsify H3 itself**, and the
> falsification is sharp enough to reject a signed measure that is
> indistinguishable from screening at the level of Φ > 0 and −Φ′ > 0.

That claim is defensible because it is about neither the mathematics
(classical) nor the threshold extraction (done better elsewhere), but
about what the positivity hierarchy *means* when the measure's
positivity is a physical hypothesis rather than a standing assumption.

### Correction — an earlier draft overclaimed here, and the overclaim mattered

This section previously asserted that *in every other setting found —
amplitudes, Feynman integrals, lattice correlators — positivity is
guaranteed, so the hierarchy can only ever confirm.* **That is false.**

Violation of reflection positivity in the Landau-gauge gluon propagator
is a standard confinement diagnostic: one computes the temporal
Schwinger function, observes it go negative, and concludes the gluon is
not a physical asymptotic state. There is a Phys. Rev. D paper titled
*Schwinger function, confinement, and positivity violation in pure gauge
QED* (106, L011502, 2022). Using spectral positivity as a falsifiable
hypothesis tested on a Euclidean correlator is established practice in
this exact field.

The search missed it through a vocabulary inversion that this project's
own saturation report warns about: every round searched for positivity
*constraints*, none for positivity *violation used as a diagnostic*.
Round 18 was added to repair it.

**What survives, stated narrowly.** The standard diagnostic is a single
sign check — does the Schwinger function go negative. Our gate is the
full Hankel hierarchy, and the difference is demonstrable rather than
rhetorical: the signed-measure model in the test suite satisfies Φ > 0
and −Φ′ > 0, so it **passes the standard test**, and is rejected only at
a₃ = −0.4715, det H₀ = −0.1839. The contribution is the depth of the
certificate, not the idea of testing positivity.

## Second surviving claim: spectral resolution theory

The search found no source that separates

* `M_strict` — the true inf supp ν;
* `M_detectable(T, ε)` — what is recoverable from data on a window of
  length T at precision ε;
* `M_dominant` — the edge that actually controls the observed decay,

as three distinct quantities with a quantitative relation between them.
Cover (2008) tests the *existence* of weight below a cutoff but gives no
closed-form limit; Pham Ngoc (2008) gives minimax rates for the density,
not the endpoint. The crossover r_x ≈ log(1/ε)/(M − μ), verified
numerically here (predicted 22.758, observed Γ crossing at r ≈ 22.76),
is a quantitative law for a phenomenon that is otherwise discussed
qualitatively.

**This is probably the stronger of the two claims** and is currently the
less developed one in the manuscript.

## Novelty confidence

| Axis | Score (0–10) |
|---|---|
| Novelty of the mathematics | **1** |
| Novelty of the threshold-extraction method | **2** |
| Novelty of the positivity-gate-as-model-check framing | **4** |
| Novelty of the resolution trichotomy | **6** |
| Novelty of the physical observable (one-form profile) | **7** |

Previous audit put overall novelty confidence at 3/10. This search does
not raise that for the mathematics — it lowers it further, since
Corollary A1 is now known to be textbook. It does, however, identify two
specific claims at ~6/10 that were previously buried.
