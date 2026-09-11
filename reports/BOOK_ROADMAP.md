# BOOK ROADMAP

Generated 2026-09-11. 12 monographs.

**Access policy.** These are copyrighted monographs. Stored here:
metadata, the exact chapter to read, and the reason. No protected full
text is downloaded or stored. Obtain through an institutional library
or the publisher.

## NOW

### Asymptotics and Special Functions

Frank W. J. Olver · AKP reissue · 1997 · A K Peters/CRC Press  
ISBN 9780429064616 · cluster C · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1201/9781439864548

**Read:** Ch. 3 (Watson's lemma and Laplace's method), Ch. 4 (error bounds for asymptotic expansions)

**Why:** Watson's lemma with RIGOROUS ERROR BOUNDS is what turns the edge law (Theorem D) from an asymptotic statement into a usable inequality. The paper currently states the expansion; Olver supplies the remainder bound.

### Bernstein Functions: Theory and Applications

Rene L. Schilling; Renming Song; Zoran Vondracek · 2nd · 2012 · De Gruyter  
ISBN 9783110252293 · cluster A · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1515/9783110269338

**Read:** Ch. 1 (complete monotonicity), Ch. 3 (Bernstein/Stieltjes functions), Ch. 7 (Stieltjes and complete Bernstein classes)

**Why:** The precise class definitions the paper depends on. Theorem B's statement must distinguish completely monotone from Stieltjes from complete Bernstein; these are DIFFERENT classes and the paper's counterexamples separating positivity, support and UV integrability live exactly here. A 3rd edition (2026, DOI 10.1515/9783111295121) exists.

### Jacobi Matrices and the Moment Problem

Aad Dijksma; et al. · 1st · 2023 · Springer Nature  
ISBN 9783031463860 · cluster B · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1007/978-3-031-46387-7

**Read:** Chapters on Jacobi operators and the spectrum; extreme eigenvalues

**Why:** Directly the machinery of Theorem E. The map from the Hankel pencil to a Jacobi operator, and the convergence of its extreme Ritz values to the endpoint of the support, is the exact theorem the paper needs to cite rather than re-derive.

### Laplace Transform (PMS-6)

David Vernon Widder · 1st · 1942 · Princeton University Press  
ISBN 9781400876457 · cluster A · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1515/9781400876457

**Read:** Ch. II (Stieltjes-Laplace transform), Ch. IV (Bernstein-Widder representation theorem), Ch. V (inversion and uniqueness)

**Why:** The Bernstein-Widder theorem is the backbone of Theorem A and B. Cite the theorem number from here, not a secondary restatement.

### Orthogonal Polynomials: Computation and Approximation

Walter Gautschi · 1st · 2004 · Oxford University Press  
ISBN 9780198506720 · cluster D · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1093/oso/9780198506720.001.0001

**Read:** Ch. 1.4 (Gauss quadrature), Ch. 2 (computing recurrence coefficients, conditioning of the moment map)

**Why:** The conditioning results matter directly: Gautschi quantifies how badly the map from moments to recurrence coefficients is conditioned, which is the mechanism behind the paper's finite-precision no-go (Theorem H) and behind the observed need for ~86 digits in the wide-dynamic-range model.

### Quantum Fields on a Lattice

Istvan Montvay; Gernot Munster · 1st · 1994 · Cambridge University Press  
ISBN 9780521404327 · cluster E · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1017/cbo9780511470783

**Read:** Ch. 3 (transfer matrix and reflection positivity), Ch. 7 (static potential and Wilson loops)

**Why:** The source for reflection positivity of the transfer matrix, which is the strongest available support for H3 at the nonperturbative level, and for the standard definition of the static potential from Wilson loops.

### The Moment Problem

Konrad Schmudgen · 1st · 2017 · Springer  
ISBN 9783319645452 · cluster B · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1007/978-3-319-64546-9

**Read:** Ch. 3 (moment problem on an interval); Ch. 9-10 (truncated Hamburger and Stieltjes problems, Hankel matrices); Ch. 16-17 (determinacy, Carleman)

**Why:** THE reference for every moment-problem statement in the paper. Needed to cite the truncated Stieltjes problem correctly and to state exactly which Hankel positivity conditions are necessary vs sufficient. Also settles determinacy language: Carleman gives determinacy ONLY, never support.

## NEXT

### An Introduction to Orthogonal Polynomials

Theodore S. Chihara · 1st · 1978 · Gordon and Breach  
**identifier unresolved** · cluster B · access: PENDING_VERIFICATION  
Route: identifier unresolved; obtain via institutional library catalogue

**Read:** Ch. I-II (moment functionals, quasi-definite case), Ch. IV (chain sequences and the true interval of orthogonality)

**Why:** NOT RESOLVED against Crossref in this session: no identifier is recorded rather than a guessed one. Chihara's chain sequences give the sharp condition for the true interval of orthogonality, which is the natural home of the signed-measure gate (a quasi-definite but not positive-definite moment functional is exactly what the gate must reject).

### Moments, Positive Polynomials and Their Applications

Jean-Bernard Lasserre · 1st · 2009 · Imperial College Press  
ISBN 9781848164451 · cluster B · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1142/p665

**Read:** Ch. 3 (moment-SOS hierarchy), Ch. 4 (localizing matrices and support constraints)

**Why:** Determines whether the paper's Hankel hierarchy is the one-dimensional specialization of the general moment-SOS hierarchy. If it is, that is a required citation and a further downgrade of Theorem E's novelty.

### Pade Approximants

George A. Baker; Peter Graves-Morris · 2nd · 1996 · Cambridge University Press  
ISBN 9780511530074 · cluster D · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1017/cbo9780511530074

**Read:** Ch. 5 (Stieltjes series and Pade), Ch. 17 (convergence for Stieltjes functions, bounds from Pade)

**Why:** Establishes that Pade approximants to a Stieltjes series give two-sided bounds converging to the function, and that poles/zeros interlace on the cut. This is the classical ancestor of threshold extraction and must be cited when claiming the Hankel hierarchy is not new mathematics.

### The Classical Moment Problem and Some Related Questions in Analysis

N. I. Akhiezer · SIAM reissue · 2020 · SIAM  
ISBN 9781611976380 · cluster B · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1137/1.9781611976397

**Read:** Ch. 1-2 (Hamburger/Stieltjes), Ch. 3 (Nevanlinna parametrization)

**Why:** The classical source. Needed for the canonical form of the truncated problem and for the extremal-measure characterization underlying the sharpness of the Hankel bound.

### The Problem of Moments

J. A. Shohat; J. D. Tamarkin · 1st · 1943 · American Mathematical Society  
ISBN 9780821815014 · cluster B · access: PAYWALLED_METADATA_ONLY  
Route: https://doi.org/10.1090/surv/001

**Read:** Ch. I-II (existence and determinacy), Ch. III (Hankel forms)

**Why:** Historical primary source for the Hankel-determinant criteria; useful for the HISTORICAL_LINEAGE report and for priority statements.

