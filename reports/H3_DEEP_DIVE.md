# H3 DEEP DIVE (priority zero)

**Question.** Has anyone already proved a representation sufficiently
close to H3 — a positive Stieltjes representation of the gauge-invariant
static response?

## Verdict

The question splits in two, and the two halves have different answers.

### (a) H3 at the level of the abelian vacuum polarization

**Classification: YES_EXACT — previously known.**

Raman 2026 (arXiv:2603.28454) §3.3.1, eq. (119)–(120), read at equation
level, states and derives:

```
  Pi(q^2)  = q^2 * int_{s_thr}^inf  rho(s) / (s (s - q^2))  ds      (119)
  Pi(Q^2)  = -Q^2 * int_0^{1/s_thr} rho(1/u) / (1 + u Q^2) du       (120)
  =>  -Pi(Q^2)/Q^2  is a Stieltjes function.
```

with ρ(s) ≥ 0 for s ≥ s_thr guaranteed by unitarity. This is the
analytic content of Corollary A1, and it is review material.

### (b) H3 for the NONPERTURBATIVE gauge-invariant static response

**Classification: UNKNOWN_REQUIRES_READING.**

No source found in this search states a positive Stieltjes
representation for the static potential or for a Wilson-loop-derived
response. Raman's notes contain no static potential, no Wilson loop and
no position-space potential.

**This must not be read as evidence of novelty.** The decisive primary
sources are pre-1990 and paywalled, and were NOT read:

| Work | DOI | Status |
|---|---|---|
| Bachas, *Concavity of the quarkonium potential* (1986) | 10.1103/PhysRevD.33.2723 | NOT READ — paywalled |
| Seiler, *Upper bound on the color-confining potential* (1978) | 10.1103/PhysRevD.18.482 | NOT READ — paywalled |
| Brown & Weisberger, *Remarks on the static potential in QCD* (1979) | 10.1103/PhysRevD.20.3239 | NOT READ — paywalled |
| Wichmann & Kroll (1956) | 10.1103/PhysRev.101.843 | NOT READ — paywalled |

Bachas and Seiler are the two papers most likely to contain a
positivity structure for the static potential derived from reflection
positivity alone — i.e. from a *weaker* hypothesis than H3. The prior
audit already established that Bachas obtains two derivative conditions
this way. Whether either derives the full hierarchy is the single
open question that most affects the paper's standing.

## Bibliographic correction found while resolving these seeds

`paper/references.bib` entry `bachas_1986` carries
`title = {Convexity of the Quarkonium Potential}` and `year = {1985}`.
Crossref (the publisher record) returns
**"Concavity of the quarkonium potential", 1986**, Phys. Rev. D **33**,
2723. INSPIRE's title field says "Convexity" and disagrees with the
publisher. The sign word matters here — concavity and convexity are
opposite claims about the same object, and the paper cites this work
*for a sign condition*. Resolve against the published article before
submission.

Seiler (1978) is absent from `references.bib` entirely and should be
added: an upper bound on the confining potential is directly relevant to
Theorem B's territory.

## What would settle (b)

1. Read Bachas 1986 and Seiler 1978 in full (institutional access).
2. Read Montvay & Münster Ch. 3 on transfer-matrix reflection
   positivity — the strongest general route to a spectral representation
   for a Wilson-loop observable.
3. Determine whether reflection positivity yields the *full* Stieltjes
   property or only finitely many derivative conditions. If only
   finitely many, H3 is strictly stronger than anything proved, and the
   paper's conditional framing is correct and defensible.
