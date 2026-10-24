# Scientific audit, final round — 22–23 October 2026 (task P14)

**Candidate:** paper v0.5.4. The tree is uncommitted and rests on HEAD
`78b637cb6a2cf4d92691a3eb7e31312baf23ef32`.

**Plan:** `.agent/plan.yaml`, tasks P0–P14. Codex executed P0–P4. It stopped
at its usage limit at 00:11 on 23 October, and Claude executed P5–P14 and
closed the P1/P2 records. Each task has a report in `.agent/reports/`, and
command evidence is in `.agent/evidence/`.

No commit, push or publication was made. Every reading and review below was
done by automated agents; no human expert has reviewed this round.

## 1. What changed scientifically

| Claim | Before | After | Evidence |
|---|---|---|---|
| Generic RPA Prop. 4 ("upper atom iff Z₃>0") | PROVED | RETRACTED for arbitrary positive densities; PROVED_CONDITIONALLY with a positive edge value | exact witness ρ=(10−s)1_[4,10], g²=1/100 |
| Generic "no other atom" completeness | PROVED | RETRACTED; Dirac density only | exact witness: atom at s=7, weight 3/7, Z₃=0 |
| 𝒢 Stieltjes for Z₃>0 | via unread SSV duality | PROVED directly (atomic approximation, then truncation and Helly) | RPA note §4 |
| Near-threshold RPA atom | wrong value (1.9%/5.0%) reported RESOLVED | CHECKED against 60/90-digit reference at identical inputs | P2 |
| Saved-output verifier | accepted forged summaries and missing groups | rejects them; full Arb reintegration PASS | P3 |
| Static-line field (Prop. 7) | used δ(p₀)/(p₁−i0) "made well defined by the regulator" | PROVED_CONDITIONALLY as a conserved-current limit; sharp half-plane equality OPEN | E2c §12; P6 |
| Tensor classification of ⟨FF⟩ (E2b) | presented as the project's | CLASSICAL in substance: Benedetti–Casini–Magán §3 | P5, P8 |
| Hankel determinant as Stieltjes falsifier | novelty 4/10 | 2/10: Masjuan–Peris eqs. (12)–(14) | P8 |
| Finite probes (new) | — | exterior lemma PROVED_CONDITIONALLY; Gaussian Γ<M* CHECKED | E3 §11.1–11.2 |
| Matched EH crossovers (Dirac measure) | massive-atom placeholder | CHECKED: 55.91/m (Gaussian), 20.48/m (ball), 18.95/m (smooth compact) | E3 §11.2–11.3 |
| First-order EH energy, arbitrary sources | radial only | PROVED two-sided bound (local theory); V(r) window 4.56×10⁴/m | E3 §11.4 |

## 2. Hostile referees

### Referee A — quantum field theory

| # | Objection | Class | Response and evidence |
|---|---|---|---|
| A1 | H3 is assumed, not derived. Prop. 7 needs an assumed Euclidean ⟨FF⟩ representation whose Wightman derivation is unverified. | MAJOR | Stated as a hypothesis in the abstract, §3 and App. A. The tensor form is now credited to BCM. The measure-theoretic steps and the continuation remain unread and OPEN. Not fatal, because no claim exceeds the hypothesis. |
| A2 | In full QED the three-photon cut starts at s=0, so M* is zero and the bounds are trivial. | MAJOR | "The first threshold need not be charged" says this, and Theorem C returns the coupled edge. The window where 2m dominates over the multi-photon tail is not computed (OPEN). It limits physical reach, not correctness. |
| A3 | The point Wilson line is not constructed; the half-plane product was formal. | MAJOR → reduced | The field is now a stated limit of smooth conserved currents. Equality with sharp half-plane extensions and an interacting line operator remain OPEN (`T-LINE-SHARP`). |
| A4 | A real heavy probe is extended; its tails could fake or hide the threshold. | MAJOR → fixed | New "Finite probes": exterior lemma for compact support. For a Gaussian tail, Γ(50/m)=0.932m<2m (CHECKED, two routes). |
| A5 | At finite probe charge the profile is not completely monotone. | MINOR | The paper restricts to the linear coefficient. E3 §7 and §11 quantify the crossover. |
| A6 | Bianchi on the time-ordered product hides two-point locality. | MINOR | Explicit since v0.5.3; E2c §11. |
| A7 | The RPA atom is a hard-cutoff artefact. | NOT_VALID as an objection to a claim | The paper scopes the RPA as a model, and the atom's existence is now tied to the edge value. |
| A8 | Gauge invariance. | NOT_VALID | Only ⟨FF⟩ and closed Wilson loops are used; the paper avoids gauge propagators explicitly. |

### Referee B — mathematical physics and inverse problems

| # | Objection | Class | Response and evidence |
|---|---|---|---|
| B1 | Stieltjes versus Stieltjes plus a constant. | NOT_VALID | Z₃=0 is treated separately (constant 1/μ). |
| B2 | The SSV duality is cited without a theorem-level read. | MINOR → fixed | The argument no longer depends on it. The citation is background only, and its statement remains UNRESOLVED (TITLE_ONLY). |
| B3 | Everything is classical. | MAJOR (novelty) | The paper concedes this and now also credits BCM and Masjuan–Peris. The surviving contribution is narrow (P8 report). It is an honest narrow contribution, not a fatal flaw. |
| B4 | The finite-window no-go (Theorem H) is elementary. | MINOR | The paper states this. |
| B5 | Edge convergence of the Hankel hierarchy. | NOT_VALID | App. B uses density of polynomials in L²(ω) with an exponential moment; Carleman is used only for determinacy. |
| B6 | The exterior lemma is Newton's shell theorem. | MINOR | No priority claimed; novelty UNRESOLVED (no targeted search). |
| B7 | The ordered limits in Prop. 7 are not uniform. | MINOR | Stated: T→∞ first, then the regulator; the 1/T rate is not uniform. |

### Referee C — numerics and reproducibility

| # | Objection | Class | Response and evidence |
|---|---|---|---|
| C1 | The RPA atom was silently wrong near threshold. | MINOR → fixed | P2: independent reference at identical inputs; route-disagreement guard; switch boundary probed (≤1.9×10⁻¹²). |
| C2 | The verifier's PASS did not bind its headlines. | MINOR → fixed | P3. |
| C3 | The new CI `git diff --exit-code` guards could fail because of platform or version differences. | MAJOR for readiness → partly fixed | Confirmed. The first clean room (fresh venv: numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2) drifted byte-wise in eight rendered figures and in `extended_verification.json`: package versions and two QUADPACK error estimates in the 9th digit. No scientific value changed. The guard now excludes those two categories, on that evidence. The remaining guarded files reproduced byte-identically on Windows; on Ubuntu this is untested (P13, P4 addendum). |
| C4 | Headline numbers are not certified. | NOT_VALID | Labelled CHECKED throughout; only the one-loop Arb benchmark is CERTIFIED. |
| C5 | Oscillatory quadrature can fail silently. | MINOR | Found this round: `mp.quadosc` is wrong at 30 digits on the ball route. The default is now 40, and the route is tested against an independent one to 10⁻³⁰. |
| C6 | Remote CI does not cover the candidate. | MAJOR for readiness | The last green run, 37331435402, is at `78b637c`. The candidate is uncommitted. |
| C7 | Clean-room reproduction. | — | See §3. |

**No FATAL objection was found.**

## 3. Reproduction

- **Local tree.** `pytest tests -q -rs` with the repository-local Tectonic
  on PATH: 466 passed, 0 skipped. `make.py numerics` and `make.py audit`
  produced no drift. `make.py bib` is offline and idempotent.
- **Falsification suite.** 21 cases; FATAL=0, FAIL=0.
- **PDF.** v0.5.4, 16 pages, structural QA PASS, no LaTeX warnings. Changed
  pages were inspected as images.
- **Clean-room.** Run on a snapshot of the 498 candidate files with a fresh
  venv from the documented requirements (numpy 2.5.4, scipy 1.18.1,
  matplotlib 3.11.2). check, bib, numerics, audit, test (469 passed),
  certified, pdf and the Arb reintegration all exited 0, as did the corrected
  CI guards. Byte drift occurred only in the rendered figures and
  `extended_verification.json`, which the guard now excludes on that
  evidence. Details and gaps are in `.agent/reports/P13.md`.

## 4. Readiness

**Not `READY_FOR_EXPERT_REVIEW`.** The following gates are unmet:

1. Remote CI on the candidate. This needs a commit and push, which are not
   authorized.
2. Brown–Weisberger (1979), the static-potential precedent, is still
   unread: every full-text route returned 401 or 403.
3. Human expert review, a separate gate.

All other gates hold locally:

- tests, numerics, audit and bib pass;
- the claim graph matches the manuscript (57 reviewed claims, 32 units, none
  uncovered);
- no FATAL item remains;
- open questions are labelled;
- title and abstract do not imply H3 is proved.

## 5. Open, in order of physical importance

1. The Wightman → Euclidean step for ⟨FF⟩: measure-theoretic lemmas and
   continuation.
2. The QED window where the 2m tail dominates the massless multi-photon
   tail in Φ. This needs the low-s coefficient of the 3γ spectral function,
   which was not looked up or computed.
3. Point probes beyond the quadratic cumulant: the light-by-light kernel at
   distances of order 1/m.
4. A remainder for V(r) that decays with r beyond first order in c.
5. Equality of all sharp half-plane extensions; an interacting Wilson-line
   operator.

## Addendum, 23 October 2026, afternoon: independent review and corrections

Another agent reviewed this hand-back
(`reports/INDEPENDENT_REVIEW_CLAUDE_2026-10-23.md` and the two topic reviews
beside it). The text above is kept as written; this addendum records what
changed. Records: `.agent/reports/R0.md`, `R1.md`, `R2.md` and `R3.md`.

**Errors found in this report's candidate.**

- **Γ_Gauss(300/m) = 2.00755** (E3 §11.2) was wrong in the fifth decimal.
  The correct value is 2.00752. The cause was mpmath's absolute stopping
  rule.
- **Γ_ball(50/m) = 2.03646** (E3 §11.1) was wrong for the same reason. The
  correct value is 2.03647. The review missed this one; it was found while
  checking the fix.
- **Finite probes.** The paper's paragraph omitted ρ ≥ 0, and it presented a
  sufficient condition as necessary ("only outside"). Both are fixed.
- **"Smooth compact"** (in §1, row "Matched EH crossovers"): the polynomial
  probe is C¹, not smooth.
- **The critical case Z₃ = 0.** Positivity of G − 1/μ was asserted without
  proof. It is now Proposition 3b of the RPA note (PROVED).
- **C3.** PDF QA was not run in the clean-room environment, and
  `reproducibility/requirements-pdf.txt` does exist. P13 is corrected.

**Changed in the open list of §5.** Item 2, the QED window, is no longer
uncomputed. Note E4 gives the three-photon density for s ≪ m² as
(17/11664000)(α/π)⁴s⁴/m⁸, by two independent routes. For the linear
coefficient, the pair threshold controls Φ, with Γ ≥ 2m, only out to
r ≈ 20.7/m. This is CHECKED at leading order in each channel; higher orders
are estimated, not bounded.

**Readiness.** Still not READY_FOR_EXPERT_REVIEW. The gates are unchanged:
remote CI, Brown–Weisberger and human review.

## Addendum 2, 23 October 2026, evening: the E4 window error

A second review (`reports/NEXT_STEPS_E4_REVIEW_2026-10-23.md`) found three
problems:

- the paper did not distinguish the two window criteria;
- the uncertainty of the leading-order radii was not controlled;
- the point-probe window had been applied to extended probes.

All three are addressed in note E4, Section 10, and `.agent/reports/R5.md`:

- **Amplitude.** The full one-loop γ*→3γ amplitude replaces the leading
  term. It is checked by:
  - the Ward identity on every leg;
  - the EH limit with absolute normalization;
  - Dicus–Kao–Repko on shell (ω⁴ and ω⁶ exact; the full cross section within
    0.5%).

  Their ω⁸ column is found to be twice ours.
- **Radii.** With the pair channel at O(α²): r_Γ = 20.65/m and
  r_× = 22.57/m. The numerical error is below 0.002/m; higher orders in α
  are estimated at 0.015/m. CHECKED.
- **Probes and charge.** Compact probes shift the radii by about 8/m. A
  probe of charge e is limited by its own EH tail instead.

Readiness is unchanged: remote CI, Brown–Weisberger and human review are
still outstanding.
