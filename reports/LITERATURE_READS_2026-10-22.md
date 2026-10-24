# Primary-source reads, 22–23 October 2026 (task P8)

The Codex session of 22–23 October downloaded the sources below; it stopped
at its usage limit before writing this record. Claude re-read each cited
location in the downloaded file on 23 October and records here only what it
checked itself. Files, URLs and SHA-256 hashes:
`tmp/scientific_execution_2026-10-22/literature/download_manifest.json` and
`primary_access_attempts_2026-10-23.json` (local, not tracked).

Reading depth uses the master-prompt scale. Relation to this project:
IDENTICAL, SAME_MATHEMATICS_DIFFERENT_OBSERVABLE, ANALOGOUS, BACKGROUND,
CHALLENGES_NOVELTY, CHALLENGES_ASSUMPTION or NOT_RELEVANT.

## Summary

| Source | Depth | Locations checked | Relation | Affects |
|---|---|---|---|---|
| Benedetti, Casini, Magán, JHEP06(2023)095, arXiv:2212.11291 | EQUATION_LEVEL_READ | §3.1 (3.2), (3.6), (3.10), (3.14), (3.17)–(3.20) and the paragraph after (3.20); §3.3 (3.24)–(3.25) | IDENTICAL (tensor structure and Källén–Lehmann form of a closed two-form); CHALLENGES_NOVELTY of E2b | C10, E2b |
| Masjuan, Peris, PLB (2010), arXiv:0903.0294 | EQUATION_LEVEL_READ | p. 5, eqs. (11)–(14) | SAME_MATHEMATICS_DIFFERENT_OBSERVABLE; CHALLENGES_NOVELTY of the "Hankel hierarchy as falsifier" framing | C1, C3, C7 |
| Giacosa, Wolkanowski, arXiv:1209.2332 | EQUATION_LEVEL_READ | p. 2, eqs. (6)–(8) and the normalisation sentence | ANALOGOUS (resummation creates a first-sheet pole outside the input continuum; positive residue; sum rule) | C9 |
| Lawrence, arXiv:2408.11766 | ABSTRACT_READ (+ pp. 1–2 introduction) | abstract | BACKGROUND, as the paper cites it | C4 |
| Mutzel, Tilloy, arXiv:2512.19594 | EQUATION_LEVEL_READ | eqs. (2)–(4), p. 1; "Bootstrapping the mass gap", p. 4 | ANALOGOUS; also BACKGROUND, as cited | C4, C7 |
| Schilling, Song, Vondraček, *Bernstein Functions*, 2nd ed. (2012) | TITLE_ONLY (table of contents and author errata list) | contents pages (OCR); errata of 2 December 2022 | BACKGROUND; theorem statement and numbering UNRESOLVED | appendix duality sentence |
| Brown, Weisberger, PRD 20, 3239 (1979) | ABSTRACT_READ (INSPIRE record only) | none: APS 403, APS harvest 401, ADS scan 403 | UNRESOLVED | static-potential formalism |

## Notes per source

**Benedetti–Casini–Magán.**

- §3.1 classifies conserved biform two-point functions. (3.6) is the unique
  bi-closed structure $p\wedge g^{(k-1)}\wedge p$. Its normalisation (3.14)
  gives, for $d=4$, $k=2$, our $T$ up to sign.
- (3.10) is the Källén–Lehmann form $(a_F\delta(s)+\rho_F(s))$ times that
  structure.
- For $k=q=d/2$, (3.17)–(3.20) add a light-cone term $b_F(P^{(k)}\tilde*)$.
  The sentence after (3.20) reads "Combining this with spatial commutativity
  requires that $b_F, b_G = 0$ if $k$ is even".
- §3.3: positivity gives $\rho_F\ge0$ and $a_F\ge0$.

This is Theorem E2b and its locality qualification, at the physics level of
tensor structures. The note's measure-theoretic statements, Bochner–Schwartz
and covariant disintegration, are not in BCM and remain UNRESOLVED. **Action:**
credit BCM in the appendix sentence on the tensor classification; remove any
implication that the classification is ours.

**Masjuan–Peris.** Eq. (12) defines the Hankel determinant $D(m,n)$ of
Taylor coefficients. The text states "A Stieltjes function must satisfy
$D(m,n) > 0$". Eqs. (13)–(14) give $D(0,1)=-0.0226376<0$ for the
$O(\alpha_s^2)$ heavy-quark term. They conclude that the individual function
$\Pi^{(2)}$ is not Stieltjes although the full $\Pi$ is.

This uses a Hankel determinant to falsify the Stieltjes property of a
fixed-order term. It parallels the appendix's $O(g_R^6)$ statement, and it
weakens the "positivity gate as model check" framing in
`WHAT_IS_ACTUALLY_NEW.md`. **Action:** the abstract already cites them for
threshold extraction; also credit the determinant falsifier where the paper
discusses fixed-order failure.

**Giacosa–Wolkanowski.**

- (6): for $g\ge g^*$, a pole $z_I=\tilde M-i\varepsilon$ appears on the
  first sheet below threshold.
- (7): $dS=Z\delta(x-\tilde M)+d_{a.t.}$.
- (8): $Z=[1+2g^2\partial\Sigma/\partial x^2]^{-1}$.
- Normalisation: $Z+\int d_{a.t.}=1$.

Their pole is below threshold; ours lies above the input cutoff. The
mechanism is the same, which the appendix already says.

**Lawrence.** The abstract confirms the paper's sentence: convex optimisation
and Lagrange duality give bounds on integrals of the spectral density from
Euclidean data. Pages 4–5 were not re-read. No theorem is attributed beyond
the abstract.

**Mutzel–Tilloy.**

- (2)–(4): Källén–Lehmann for equal-time correlators. The spatial decay
  encodes the gap; the assumed form is an atom plus a continuum from
  $4M^2$.
- p. 4: the gap is a bootstrap estimate. It scans $M$ for feasibility of a
  linear program that assumes that form, decreasing the slack until the
  interval collapses.

This is an estimate under a structural assumption, not a model-free lower
bound, so it is consistent with the paper's finite-window no-go. Extracting
the gap from the spatial decay of a static correlator is the same idea as
the paper's profile; the paper should not present it as new.

**Schilling–Song–Vondraček.** The OCR of the contents lists chapter 6
"Complete Bernstein functions" and chapter 7 "Properties of complete
Bernstein functions". No theorem text was available. The duality
"$f$ complete Bernstein $\iff 1/f$ Stieltjes" is therefore not confirmed at
theorem level. The RPA note's direct proof (finite cutoff, $Z_3>0$) makes
the paper's use independent of it in that case.

**Brown–Weisberger.** Every full-text route returned 401 or 403. The status
stays ABSTRACT_READ and nothing is attributed to it beyond the INSPIRE
metadata.

## Effect on the contribution

After these reads the narrowest defensible contribution is:

- the identification of the one-form breaking profile as a positive Laplace
  transform under the stated hypotheses (Theorem A);
- the transport of classical effective-mass and Hankel technology to it,
  credited as classical (Lüscher–Wolff, Blossier et al., Masjuan–Peris);
- explicit failure modes:
  - finite-window no-go;
  - WGC scale invariance;
  - RPA atoms and their counterexamples;
  - the probe-size condition of note E3, Section 11.

The tensor classification (E2b) is now classical in substance (BCM). The
"Hankel determinant as Stieltjes falsifier" idea has a direct precedent
(Masjuan–Peris).
