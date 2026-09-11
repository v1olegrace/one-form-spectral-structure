# Search saturation report

## What this measures -- and what it does not

Saturation here means: **no new HIGH-threat work appeared under the
query families listed below**. That is a statement about the exhaustion
of *our query vocabulary*, which is strictly weaker than the exhaustion
of the literature. A predecessor that shares our mathematics but none of
our words is invisible to every keyword round, by construction.

The citation-snowball rounds (7 and 17) exist to break that circularity,
because they reach works whose vocabulary was never guessed. Round 17
specifically traverses pre-1990 HEP through INSPIRE, where OpenAlex and
Crossref coverage thins out badly.

| round | papers seen | new unique | new HIGH | new MED | families |
|---:|---:|---:|---:|---:|---|
| 1 | 908 | 783 | 0 | 30 | H3.positivity, H3.running_coupling, H3.screening, H3.static_spectral,  |
| 2 | 1200 | 1088 | 15 | 40 | CM.classical, CM.potential, INV.edge, INV.exp, INV.relax, MOM.hankel,  |
| 3 | 525 | 374 | 3 | 24 | LAT.effmass, LAT.spectral, LAT.string |
| 4 | 369 | 273 | 1 | 2 | THR.moments, THR.qcdsr |
| 5 | 450 | 357 | 0 | 9 | EFT.bootstrap, EFT.positivity, SYM.oneform, SYM.wgc |
| 6 | 375 | 335 | 2 | 4 | NOISE.cond, NOISE.minimax, NOISE.precision |
| 7 | 1059 | 886 | 1 | 0 | citation_snowball |
| 9 | 525 | 431 | 1 | 7 | PRONY.core, PRONY.recovery, PRONY.robust |
| 10 | 424 | 336 | 1 | 5 | OPT.canonical, OPT.christoffel, OPT.jacobi, OPT.lasserre |
| 11 | 408 | 291 | 1 | 2 | HID.dynamic, HID.lattice, HID.mixture, HID.window |
| 12 | 300 | 246 | 0 | 0 | TAU.classic, TAU.edge, TAU.mellin |
| 13 | 225 | 203 | 0 | 1 | TILT.stat |
| 14 | 300 | 238 | 2 | 3 | SGN.tests |
| 15 | 200 | 129 | 0 | 0 | ROB.moment, ROB.pencil |
| 16 | 303 | 219 | 0 | 2 | HIST.cm, HIST.confine, HIST.qed |
| 17 | 727 | 508 | 0 | 0 | inspire_snowball |

Totals: 8298 records examined, 6697 unique works retained.

## Saturation status, per the stated criterion

The criterion requires THREE consecutive waves with no new HIGH/FATAL
threat, <1% growth of the HIGH corpus, and no new distinct method.

Rounds 15, 16, 17 produced no new HIGH-threat work.

**Status: NOT SATURATED.** The last three rounds were thematically narrow (history, robustness, INSPIRE snowball). A quiet tail on narrow rounds is not evidence of saturation across the whole search universe; the criterion demands quiet rounds that were also BROAD.

Unfinished axes, stated explicitly so that absence of evidence is not
mistaken for evidence of absence:

* Backward references of the HIGH-threat set have not been traversed.
* No book-length source has been read; the moment-problem monographs
  (Akhiezer, Schmudgen, Chihara, Widder) are metadata-only.
* Paywalled pre-1990 primary sources (Bachas 1986, Seiler 1978,
  Brown-Weisberger 1979, Wichmann-Kroll 1956) were NOT read; their
  content is known here only through later restatements.
* Only 1 work has been read at equation level in this pass.