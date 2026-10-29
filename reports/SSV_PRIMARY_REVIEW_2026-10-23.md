# SSV: primary-source access and narrow uses

23 October 2026. Read-only review of the scientific repository; only this
report and source evidence under `tmp/ssv_review_2026-10-23/` were created.

## Result

An authorized public preview of the actual **second edition, 2012**, was
located and downloaded from the publisher distribution service Pageplace:

<https://api.pageplace.de/preview/DT0400.9783110269338_A19166479/preview-9783110269338_A19166479.pdf>

This is original book text, not a summary. It has 43 PDF pages. The title and
copyright pages identify the second edition, print ISBN 978-3-11-025229-3,
e-ISBN 978-3-11-026933-8, and copyright 2012. The retained file is
`tmp/ssv_review_2026-10-23/ssv_2012_publisher_preview.pdf`, SHA256
`e8a981a018288ed2701dcfa05cff8c9139bc9764f6da56b9a0a537ce246aa429`.
The download returned HTTP 200. The manifest records its URL, bytes and hash.

The previous blanket `TITLE_ONLY` description is now too weak for Chapter 2.
It remains correct that the actual statements and proofs in Chapters 6 and 7
have not been read in an authorized original full-text copy during this review.

## What was actually read

Printed pp. 16-18 (PDF pages 30-32) were extracted and inspected as images.
The following account is a paraphrase, not a transcription.

- Definition 2.1, p. 16: the Stieltjes representation includes a nonnegative
  constant, a possible atom at zero, and a positive measure satisfying the
  stated weighted integrability condition.
- Theorem 2.2, p. 17: Stieltjes functions are completely monotone, form a
  convex cone, and are closed under finite pointwise limits. Its full proof
  on that page was read, including the compactification/weak convergence step.
- The introductory paragraph on p. 16 explicitly assigns reciprocal duality
  between nontrivial Stieltjes and complete Bernstein functions to **Theorem
  7.3**. The paragraph above Theorem 2.2 on p. 17 assigns the analytic
  half-plane characterization to **Corollary 7.4**. These are different results.

Thus the theorem-number ambiguity is resolved by original second-edition
cross-references, but the exact Chapter 7 theorem hypotheses and proof have
**not** been verified. Read depth: `EQUATION_LEVEL_READ` for Definition 2.1
and Theorem 2.2, including the latter's complete proof. For 7.3/7.4 only
the original cross-references were read; the exact statements and proofs
of Theorem 6.2 and the Chapter 7 results remain `UNRESOLVED`.

The author's two-page errata dated 2 December 2022 was read in full and
retained as `tmp/ssv_review_2026-10-23/ssv_2012_author_errata.pdf`:
<https://www.motapa.de/bernstein_functions/misprints-ssv-2nd.pdf>.
It lists sign corrections on pp. 73-74, in the Chapter 6 development. A
future proof-level Chapter 6 read must apply these corrections. Absence of a
listed correction is not evidence that an unread proof was checked.

## Concrete uses in this repository

These are our deductions/application suggestions, not new results claimed
by the book.

1. **Already usable with a fully read theorem.** Theorem 2.2(iii) can support
   the final passage from positive atomic approximants to the RPA Stieltjes
   kernel in `notes/H3_RPA_proof_note_2026-09-29.md`, section 7(a). Check the
   pointwise convergence and finiteness in that note; these are model-specific
   premises and are not supplied by citing SSV. The theorem alone also does
   not preserve a particular positive spectral gap without support control.

2. **Useful background with a precise locator now available.** The appendix
   can identify reciprocal duality as Theorem 7.3 and analytic characterization
   as Corollary 7.4, while retaining the direct RPA proof. A source ledger
   should say that their statements are referenced on original pp. 16-17,
   rather than claiming their full proofs were read.

3. **Short alternative proof to complete later.** With
   `W(z)=Z3+g^2 integral rho(s)/(z+s) ds`, form
   `H(z)=z W(z)/g^2=(Z3/g^2)z+integral z/(z+s) rho(s) ds`.
   Its displayed positive representation is the expected complete Bernstein
   representation for `Z3>=0`. Reciprocal duality would give `G=1/H` in the
   Stieltjes class. Under `Z3>0`, the elementary bound
   `G(x)<=g^2/(Z3 x)` excludes a constant term. Before presenting this as a
   book-based proof, read the actual representation theorem (6.2) and 7.3,
   with their nonzero and integrability hypotheses. The existing direct proof
   should continue to carry the result in the meantime.

4. **Keep the book's class distinct from H3.** The allowed constant in
   Definition 2.1 explains why ordinary membership in the Stieltjes class
   does not by itself establish the contact-term-free version of H3. Neither
   the book nor reciprocal duality proves the full QED kernel, the Wilson
   transport construction, a positive gap, or nonlinear probe control.

No bibliography, paper, claim catalog or scientific note was edited.

## Access boundaries and remaining work

The author book homepage is
<https://www.motapa.de/bernstein_functions/>. The publisher metadata record
is <https://doi.org/10.1515/9783110269338>. The publisher's series page also
lists a third edition in 2026, DOI
<https://doi.org/10.1515/9783111295121>; no theorem numbering from that edition
was imported into the 2012 citation.

The main publisher landing page and an attempted Chapter 7 page returned
405 through the browsing tool. Google Books did not provide a readable
Chapter 7 page. A public Dokumen mirror initially exposed matching
second-edition front matter and OCR, but follow-up requests returned 403;
its distribution authority was not established. No full mirror PDF was
downloaded and no theorem-proof verification is based on that mirror.
A search-index result from a first-edition mirror displayed text from printed
p. 63, but it was not counted as a full-page primary read or used to upgrade
the second-edition proof status.

The useful deliverable is therefore the actual 2012 publisher preview and a
verified Chapter 2 result, with a bounded remaining request for original
printed pp. 69-79 and 92-94 through an authorized library/publisher copy.
