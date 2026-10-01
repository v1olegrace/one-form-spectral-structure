# Audit report — paper v0.4

29 September 2026. Starting point: `6672fdb` on `main`. The previous report of
this name, dated 11 September, is at
[`reports/history/FINAL_REPORT_2026-09-11.md`](reports/history/FINAL_REPORT_2026-09-11.md).

This report records what changed, why, and how each change was checked. Where
something could not be checked with the resources at hand it is marked
`PENDING_VERIFICATION` rather than guessed.

## 1. What changed

### Code: the RPA kernel analysis

A patch developed in a separate audit worktree was reviewed line by line and
applied, not merged blind. It closed four gaps in the
uncertainty discipline that the previous round claimed to have closed:
`ghost_root()` still branched on the point value of Z₃ and bracketed from
10⁻⁶; `kernel_diagnostic()` duplicated the decision path; the polarization
quadrature's convergence message was discarded; and the continuum density
returned the Dirac formula above the cutoff, where the regulator removed it.

The edge integral and its derivative were moved to closed form. With
s = 4/(1 − v²),

    I(d) = ∫₄^{L²} ρ(s)/(L² + d − s) ds
         = C [ a(1+2/t) log(t L² (a+v)²/(4d)) − log(L²(1+v)²/4) − 4v/t ],

with t = L² + d, v = √(1 − 4/L²), a = √(1 − 4/t), C = 1/12π², and I′(d)
follows from d/dt[a(1+2/t)] = 12/(t³a). Both were checked against 50-digit
tanh-sinh quadrature for L² ∈ {10, 10⁶} and d from 10⁻³⁰ to 10⁸: agreement
10⁻⁴¹ to 10⁻⁵¹. In binary64 the error is about 10⁻¹⁶ for d ≤ 10³ L² and grows by
cancellation to 4 × 10⁻¹³ at d = 100 L², so the quadrature takes over beyond
that. The logarithm is taken as a sum, so d = 10⁻³⁰⁰ does not overflow.

Effect on the atom above the cutoff, against the independent multiprecision
reference in `reports/h3_ghost_2026-09-29/reference_mp.py`:

| g²/g²_c | quantity | before | after |
|---|---|---|---|
| 0.5 | log₁₀(edge distance) | 1.2 × 10⁻⁶ | 1.9 × 10⁻¹⁵ |
| 0.5 | weight | 2.0 × 10⁻⁶ | 2.7 × 10⁻¹⁵ |
| 0.1 | log₁₀(edge distance) | 2.1 × 10⁻⁸ | 3.4 × 10⁻¹⁶ |
| 0.1 | weight | 2.0 × 10⁻⁶ | 3.3 × 10⁻¹⁴ |

The 3.3 × 10⁻¹⁴ floor at g²/g²_c = 0.1 is intrinsic: the edge distance there is
3.3 × 10⁻⁴², reached through its logarithm, and converting amplifies the error
by |log₁₀ d| ln 10 ≈ 95. Part of the old residual was `brentq`'s default
`xtol = 2e-12`, which is absolute; it is now set explicitly. The old 2 × 10⁻⁶ came
entirely from the located root: the quadrature route for the weight, fed the
accurate root, lands near 10⁻¹¹. The status for g²/g²_c = 0.5 is now `RESOLVED`
because nothing in the chain fails to converge, not because a label changed.

### Manuscript

Version 0.3 → 0.4. Appendix A gains a paragraph on the resummed bubble chain.
The v0.3 text ended the leading-order discussion by saying the O(g_R⁶) remainder
is not asserted positive; that is still true at fixed order, and the paragraph
now shows why, then states what the resummed chain gives: H3 holds for Z₃ > 0,
fails for Z₃ < 0 through a spacelike pole of negative residue, and fails at
Z₃ = 0 through an additive constant when the total mass is finite. Two
consequences are stated there: the continuum density is non-negative for every
coupling, so continuum-moment tests cannot see the failure; and a hard cutoff
with a density nonzero at the edge produces an atom of positive weight above
the cutoff. That mechanism is attributed to Giacosa and Wolkanowski (2012),
where it appears in a different physical setting. The scope section now says,
in the main text, that passing the finite-moment tests does not rule out a
failure of the hypothesis located off the continuum. One sentence opening with
"Moreover" was rewritten; no other prose was changed, because it did not need
to be.

The manuscript was not rewritten wholesale. A scan for the connectives on the
editing checklist found one occurrence in `paper.tex` and none in the appendix;
two uses of "additionally" are precise mathematical usage ("requires, in
addition to the previous condition") and were kept.

### Bibliography

Giacosa–Wolkanowski 2012 was added through the provenance pipeline: INSPIRE for
the metadata, Crossref for the page number INSPIRE lacked. The API responses are
cached under `data/api_responses/`. Schilling–Song–Vondraček, *Bernstein
Functions* (2nd ed., 2012), was added to the hand-entered monograph table with
an explicit note that its theorem numbering is `PENDING_VERIFICATION`.

### Discussion brief (pt-BR)

`paper/professor_brief.tex` still described the Z₃ criterion as an exploratory
note to be corrected, and quoted 169 tests. Page 6 was rewritten around the
three regimes, the attribution of the atom, and the blind spot of continuum
moments; pages 2 and 5 were brought up to date. Five pt-BR slips were fixed:
"o transformado de Yukawa" (the noun is feminine), and four English terms a
Brazilian physicist would write in Portuguese (blindagem, massa efetiva, feixe
de matrizes, tipo espaço).

A second reading of the rewritten page 6 found three imprecisions, fixed before
commit: the table gave the atom for Z₃ > 0 without its condition (a density
nonzero at the edge) and the failure at Z₃ = 0 without its condition (finite
total mass); page 2 folded Z₃ < 0 and Z₃ = 0 into one clause qualified by the
mass, which only the second needs; and the page used 𝒢 and μ without defining
them, although it is a backup meant to be read alone, and μ means something
else on page 3.

The author's own study sheets in `output/impressao_professor_2026-09-28/fontes_tex/`
were stale in ways that would have been said aloud: "no remote CI has run",
"171 tests" and "211 tests", "the Z₃ criterion is a working note not promoted to
the paper", an atom error of 2 × 10⁻⁶, and the atom called an artefact of the
cutoff without crediting Giacosa and Wolkanowski. The reasoning sheet also
cited "Schilling–Song–Vondraček, Thm 7.3", the very number marked
`PENDING_VERIFICATION`; it now cites the chapter and says the number is
unchecked. The speaking sheet gains a line for page 6 of the brief.

### Tests

`tests/test_text_hygiene.py` fails on any control character in the manuscript,
the bibliography, the Markdown documents, the scripts and the print-folder
sources, except a carriage return that begins a CRLF. It scans only files
tracked by git: a first version scanned whatever was on disk and counted two
private notes, so the suite reported 326 tests here and would have reported
324 in a clean checkout. Two tests let QUADPACK's roundoff warning escape into
the summary; one now requires the declared `IntegrationWarning` type, and the
other, whose subject is the returned error estimate, silences it with a
comment saying why.

### Continuous integration

Run 36543772146 at `730bdf0` failed in the `paper` job with
`! LaTeX Error: File 'lmodern.sty' not found`. The workflow installs TeX Live
with `--no-install-recommends`, and `lmodern` is a separate Debian package that
the brief needs and the paper does not. `lmodern` was added in `6672fdb`, and
run 36597424208 passed all three jobs.

The fix was then reproduced locally, in a clean `ubuntu:24.04` container using
the workflow's own `apt` line. Without `lmodern` the brief fails with exactly the
CI error; with it, the brief builds. After the v0.4 changes, the final
`pdflatex` pass reports, for both documents, zero undefined citations, zero
undefined references and zero overfull boxes: 13 pages for the paper, 6 for the
brief. The combined `latexmk` output shows 64 undefined citations for the paper,
all from the first pass before BibTeX runs; the count that matters is the last
pass.

### Ledgers and governance

`data/claims_matrix.csv` gains C9 (the bubble-chain reduction, with the
novelty verdict "NO for the atom mechanism"); `data/theorem_status.csv` gains
A-RPA. `CHANGELOG_PAPER.md`, `ROADMAP_CIENTIFICO.md` (new section E2.5 and the
v0.4 row), `CITATION.cff` and the README were brought in line.

## 2. Status of each statement

| Statement | Status | Where |
|---|---|---|
| W = Z₃ + g²∫ρ/(s+Q²), W(0) = 1, W(∞) = Z₃, strictly decreasing | proved in scope | appendix A; note Prop. 1 |
| Z₃ < 0: unique simple spacelike pole, residue < 0 | proved in scope | note Props. 1–2 |
| Z₃ > 0: contact-free Stieltjes representation, Coulomb residue g_R² | proved in scope, conditional on the Stieltjes/CBF duality | appendix A; note Prop. 3 |
| Z₃ = 0: 𝒢 → 1/μ; fails when μ < ∞ | proved in scope | note §7(b) |
| No zeros of W off the real axis | proved in scope | note Prop. 6 |
| One positive atom above a hard cutoff for Z₃ > 0 | proved for densities nonzero at the edge | note Prop. 4 |
| Two spectral sum rules | proved; checked numerically to 6 × 10⁻¹⁰ and 5 × 10⁻⁹ | note §7-quater |
| Closed form for I(d), I′(d) | derived; checked against 50-digit quadrature | this report, §1 |
| Atom position and weight to machine precision | checked numerically, not certified | §1 table |
| Continuum-moment tests cannot detect Z₃ < 0 | proved (density formula); demonstrated by a test | appendix A |
| H3 for the nonperturbative Wilson-loop kernel | open | — |
| Transport ⟨FF⟩ → Wilson loop → static kernel | open | roadmap E2.5 |
| Irreducible O(g_R⁶) contributions | open | — |
| Fate of the atom under a smooth regulator (resonance on another sheet) | open; a resonance claim was retracted | note §7-bis |
| Originality of the Z₃ reduction for this kernel | not established | claims C9 |

"Proved in scope" means within the stated model: ρ_J ≥ 0 not identically zero,
finite inverse moment, g_R² > 0, the once-subtracted Dyson form. None of it is a
statement about the interacting static response.

## 3. Verification

Run in a fresh clone of commit `dc0985b`, the last commit of this round before
this section was written, on Windows 11 with Python 3.13.7 and portable
Tectonic 0.17.0:

| Command | Result |
|---|---|
| `python -m pytest tests -q -rs` | 324 passed, 0 skipped, no warnings (55 of them scan tracked text files for control characters) |
| `python make.py numerics` | exit 0 |
| `python make.py audit` | exit 0 |
| `python make.py certified` | exit 0 |
| `python reproducibility/verify_one_loop_output.py --reintegrate --no-write` | PASS; cardinalities, complete comparison table, certificate-index bijection |
| `git status` after all of the above | empty |
| `python make.py pdf` | exit 0; 13 pages, Type0/Type1 fonts only |
| `python reproducibility/canonical_pdf_qa.py` | PASS for v0.4; `visual_review: NOT_ASSESSED_BY_SCRIPT` (needs the `.log`, which `make.py pdf` does not keep under Tectonic; built again with `--keep-logs`) |
| clean `ubuntu:24.04` container, workflow `apt` line, `paper/` of that clone | `latexmk -pdf` passes for both documents; in the last pass, 0 undefined citations, 0 undefined references, 0 overfull boxes; 13 pages and 6 pages |

The PDF QA record is the one tracked file that does not come back identical. It
stores the absolute path and SHA-256 of the PDF it inspected, and the SHA-256 of
each source file as checked out. The committed values are for LF line endings,
which is what the repository holds and what Linux CI checks out; the Windows
clone converts to CRLF, so its `paper.tex` hash differs. The README said every
generator reproduces its output byte for byte; it now names the three that do
and this exception.

Earlier in the round, before the fix, the same container showed the brief
failing without `lmodern` with exactly the CI error, and building with it.

The sign-convention test was checked by mutation rather than by reading it:
flipping the sign inside its `kernel()` makes three of its nine tests fail — the
positive measure, the detection of the flipped convention, and the ultraviolet
growth of the effective coupling. The six that still pass do not depend on the
sign.

Rendered pages of the paper were inspected for layout: all 13 on a contact
sheet, pages 6, 9 and 10 at full size. The same for pages 2 and 6 of the brief.
That is automated inspection of rendered output. It is not a human review, and
none has taken place.

## 4. Errors found in this round

The ones that bear on results are also listed in the README.

- A `quadrature_ok` flag reported `True` while six non-convergence warnings
  escaped from the same call. The flag was introduced in the previous round.
- Two tests required the code to stay imprecise. They now pin the measured
  accuracy; the historical failure is still shown on raw QUADPACK.
- `python make.py bib` does not reproduce the committed bibliography. Eight
  cited records came from outside the harvester's seed list, and re-resolution
  moves some years from publication to preprint (Masjuan–Peris 2010 → 2009).
  Running the target once during this round dropped the article count from 26
  to 19. The change was reverted before anything was committed, and the new
  record was appended to the harvest instead. The target itself is **not yet
  fixed**; CI never runs it. The committed `literature_harvest.csv` and
  `literature_harvest.json` already disagreed by the same eight records (18 rows
  against 26); the new record was appended to both, leaving that difference as
  it was.
- A carriage return replaced `\r` in `\ref` inside the manuscript, and a
  vertical tab replaced `\v` in a BibTeX author field. Both came from text
  passed through the shell command channel of the editing environment, which
  reduced `\\` to `\` before the content reached Python. Bash semantics do not
  explain it: the loss was reproduced with a quoted here-document, which bash
  passes literally. The same mechanism accounts for every escape defect earlier
  in the project's history. Files containing backslashes are now written with
  an editor, not through the shell. The control-character scan used to catch
  these whitelisted carriage returns because of CRLF line endings, so a stray
  one inside a line passed; it now flags any carriage return not immediately
  followed by a line feed.
- Two slips in preparing this round's commits, both caught before anything was
  pushed. The move of the old report to `reports/history/` had been staged
  earlier and went into the manuscript commit; it was taken out and committed
  with this report. And `literature_harvest.json` had been rewritten with a
  different indentation, so adding one record produced a 774-line diff; the file
  was rewritten in its original format, and the new record carries the `added`
  date that the other hand-appended records have.
- A statement in the theorem ledger said H3 holds "iff Z₃ > 0". That is false in
  general: at Z₃ = 0 with infinite mass it holds. Corrected before commit.
- Two README claims were broader than the facts. "Every bibliography field
  comes from an API response" ignored the six monographs and the DLMF, entered
  by hand. "`git status` is empty after running every generator" ignored the PDF
  QA record. Both now say what is true.
- The README omitted, in its account of the atom, the condition that the density
  not vanish at the cutoff. Added.

## 5. Pending

- `PENDING_VERIFICATION` — Schilling–Song–Vondraček theorem numbering. The
  errata sheet was read in full and touches none of the duality statements;
  secondary sources cite the result as Thm 7.3 or as Cor 7.4. The book has not
  been opened.
- Brown–Weisberger (1979), Phys. Rev. D 20, 3239: not read. The APS full text is
  behind a paywall.
- arXiv:1206.0176 (tachyonic contribution to the top propagator): read at
  abstract level only; not cited in the paper.
- `make.py bib` idempotence, as above.
- Human expert review of the manuscript and the brief.
- The next scientific step, with its refutation and acceptance criteria, is in
  `ROADMAP_CIENTIFICO.md`, section E2.5: a controlled case in which the
  transport from ⟨FF⟩ to the Wilson-loop static kernel can be carried out
  explicitly.

## 6. Sources examined

| Source | What was checked | Level |
|---|---|---|
| Giacosa & Wolkanowski 2012, arXiv:1209.2332 | pole on the physical sheet, outside the input support, positive residue, sum rule | full text (HTML), directed reading |
| Schilling, Song & Vondraček, *Bernstein Functions*, 2nd ed. | table of contents; errata sheet of 2022-12-02 | authors' page, primary for errata; statements secondary |
| Raman 2026, arXiv:2603.28454 | Stieltjes property of the vacuum polarization; no resummed object, no Z₃ | full text, directed reading |
| INSPIRE, Crossref, Semantic Scholar | metadata for the new record | API responses cached |
| Brown & Weisberger 1979 | — | not read |
