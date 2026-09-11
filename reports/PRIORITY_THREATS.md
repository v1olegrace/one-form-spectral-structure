# PRIORITY THREATS

Generated 2026-09-11 from `data/literature.db`.

A threat is ranked by what it would cost the paper if true, not by how
similar its words are. The ranking below is therefore driven by the
equation-level and abstract-level reads recorded in
`data/claim_literature_matrix.csv`, not by the keyword score.

## Tier 1 -- established at equation level

### Claim A — SUPPORTS_ASSUMPTION (confidence 9/10)

**Lecture Notes on Positivity Properties of Scattering Amplitudes** (2026) — `arxiv:2603.28454v1`  
Locator: eq. (119)-(120) / Sec. 3.3.1  
Read level: **EQUATION_LEVEL_READ**

> States and derives: 'If Pi(Q^2) is the vacuum polarization function then -Pi(Q^2)/Q^2 is a Stieltjes function.' Derivation is the once-subtracted Kallen-Lehmann dispersion relation eq. (119) Pi(q^2) = q^2 int_{s_thr}^inf rho(s)/(s(s-q^2)) ds, followed by u=1/s, Q^2=-q^2 giving eq. (120) Pi(Q^2) = -Q^2 int_0^{1/s_thr} rho(1/u)/(1+uQ^2) du, with rho(s)>=0 for s>=s_thr guaranteed by unitarity.

**Consequence.** DECISIVE FOR P0.1. The Stieltjes property of the ABELIAN vacuum polarization -- the analytic content of Corollary A1 -- is standard and is stated as a known result in a 2026 review. H3 must therefore NOT be presented as a new analytic structure at the VP level. What remains open is H3 for the NONPERTURBATIVE GAUGE-INVARIANT STATIC RESPONSE, which this reference does not address: it contains no static potential, no Wilson loop and no position-space potential.

### Claim B — STRICTLY_STRONGER_PRIOR (confidence 9/10)

**Lecture Notes on Positivity Properties of Scattering Amplitudes** (2026) — `arxiv:2603.28454v1`  
Locator: eq. (19), (20)-(21), (22) / Sec. 2.1.2  
Read level: **EQUATION_LEVEL_READ**

> Defines exactly our Hankel hierarchy from derivatives: (H_0)_ij = (-1)^(i+j) f^(i+j)(x), (H_1)_ij = (-1)^(i+j+1) f^(i+j+1)(x), and proves PSD via sum_ij (-1)^(i+j+l) f^(i+j+l)(x) xi_i xi_j = int_0^inf dt mu(t) e^(-xt) t^l (sum_i t^i xi_i)^2 >= 0. Eq. (22) is the 2x2 log-convexity determinant.

**Consequence.** The equivalence 'complete monotonicity <=> PSD Hankel matrices of derivatives' is classical and is presented as review material. Theorem B and the H_0/H_1 construction of Theorem E are therefore CLASSICAL as mathematics. Novelty cannot be claimed for the hierarchy itself.

### Claim E — USES_SAME_MATH (confidence 9/10)

**Lecture Notes on Positivity Properties of Scattering Amplitudes** (2026) — `arxiv:2603.28454v1`  
Locator: eq. (19) / Sec. 2.1.2  
Read level: **EQUATION_LEVEL_READ**

> Same H_0, H_1 pencil objects, same positivity proof.

**Consequence.** NOT identical: the review builds the Hankel matrices to CERTIFY complete monotonicity. It never forms the generalized eigenvalue problem lambda_min(H_1,H_0) and never extracts inf supp mu. The threshold-extraction step of Theorem E is absent here.

### Claim J — CHALLENGES_ASSUMPTION (confidence 8/10)

**Lecture Notes on Positivity Properties of Scattering Amplitudes** (2026) — `arxiv:2603.28454v1`  
Locator: abstract, Sec. 3 / —  
Read level: **EQUATION_LEVEL_READ**

> The programme 'CM/Stieltjes positivity as a property of QFT observables' is an established, actively reviewed research area covering the cusp anomalous dimension (eq. 99), scalar Feynman integrals (eq. 102, 114), the vacuum polarization (eq. 120) and Coulomb-branch amplitudes in N=4 SYM.

**Consequence.** Our framing cannot be presented as opening this programme. The defensible position is a NEW OBSERVABLE within an existing programme, not a new programme.

## Tier 2 -- established at abstract level only

These are recorded with relations that do NOT assert equation-level
equivalence, because their equations have not been read. The database
refuses to promote them until they are.

### Claim C — ANALOGOUS (confidence 9/10)

**Extracting quantum field theory dynamics from an approximate ground state** (2025) — `arxiv:2512.19594`  
Read level: **ABSTRACT_READ**

> Mutzel & Tilloy 2025: linear-programming extraction of the MASS GAP from a static EQUAL-TIME two-point function at spatial separation, by recasting Kallen-Lehmann inversion as convex optimization. Tested on 1+1d phi^4 with relativistic continuous matrix product states.

**Consequence.** CLOSEST PUBLISHED ANALOGUE TO THE CORE METHOD. Same input class (a static spatial correlator), same target (the mass gap / spectral edge), same hypothesis (positive Kallen-Lehmann density). Differs in algorithm (linear programming vs Hankel pencil) and in the error statement (a posteriori bound on correlator error vs our monotone deterministic bound). This is a stronger precedent than the lattice effective mass, because the geometry -- spatial separation rather than Euclidean time -- matches ours.

### Claim E — USES_SAME_MATH (confidence 8/10)

**Model-free spectral reconstruction via Lagrange duality** (2024) — `doi:10.48550/arxiv.2408.11766`  
Read level: **ABSTRACT_READ**

> Lawrence 2024: recasts spectral reconstruction from Euclidean correlators as a convex optimization problem and, via Lagrange duality, obtains bounds on arbitrary integrals of the spectral density from positivity alone. Bounds are stated to be 'information-theoretically complete': for any point within the bounds there exists a consistent spectral density.

**Consequence.** HIGH THREAT TO THEOREM E's OPTIMALITY. If the bounds are information-theoretically complete for linear functionals of the measure, no method -- ours included -- can do better on those functionals. Our edge M_* is NOT a linear functional, so it is not directly covered, but this must be addressed explicitly rather than ignored. REQUIRES EQUATION-LEVEL READ before any optimality language is used in the paper.

### Claim H — ANALOGOUS (confidence 8/10)

**A robust and reliable method for detecting signals of interest in multiexponential decays** (2007) — `doi:10.1063/1.2930799`  
Read level: **ABSTRACT_READ**

> Cover 2008: a hypothesis test in relaxation-spectrum space whose null is 'there exists a relaxation spectrum with NO signal below 40 ms consistent with the observed T2 decay'. Applied to detecting the myelin signal in brain MRI.

**Consequence.** STRUCTURALLY THE TINY-ATOM QUESTION, posed as a falsifiable test, in the NMR/MRI literature since 2008. The CONCEPT of testing for undetectable spectral weight below a threshold is therefore NOT new. No closed-form detection limit is given, so the crossover law r_x ~ log(1/eps)/(M-mu) is not preempted in closed form -- but Theorem H must be framed as supplying the quantitative law for a known qualitative phenomenon.

### Claim H — BACKGROUND_ONLY (confidence 7/10)

**Statistical minimax approach of the Hausdorff moment problem** (2007) — `doi:10.1088/0266-5611/24/4/045018`  
Read level: **ABSTRACT_READ**

> Pham Ngoc 2007/2008: minimax upper and lower bounds for estimating a compactly supported DENSITY from noisy moments (Hausdorff moment problem).

**Consequence.** DOES NOT PREEMPT THEOREM H. The estimand is the density, not the endpoint of the support. Relevant as the correct minimax framework to cite, and as evidence that the noisy Hausdorff problem has a developed statistical theory that our deterministic envelope should be compared against.

