# Independent adversarial review: finite probes and the local EH energy bound

Date: 23 October 2026. Read-only scientific review of the Claude takeover.
No scientific source, implementation, test, staged state, or generated artifact
was modified. This report is the only new file written by this reviewer.

Read first: `.agent/TAKEOVER_CLAUDE_2026-10-23.md` and `.agent/reports/P7.md`.
Scope: E3 Section 11, its implementation/tests, the canonical finite-probe
paragraph, and associated catalog entries. No conclusion below validates the
other P0-P14 tasks, the full-QED continuation, or remote CI.

## Finding 1 — MAJOR: positivity is missing from the canonical finite-probe statement

Locations: `paper/paper.tex:453-460`; compare the correctly qualified lemma
at `notes/E3_nonlinear_probe_EH.md:349-354`.

The inequalities `1 <= F <= sinh(xa)/(xa)` require a **nonnegative** radial
unit-total density. The canonical paragraph states radiality, total charge,
and compact support but does not explicitly state nonnegativity. These
conditions alone do not imply the displayed inequalities or preserve a
positive Laplace representation.

An exact bounded-density witness, with support radius a=1, is

    rho(u) = 12/pi                 for 0 <= u < 1/2,
             -6/(7 pi)            for 1/2 < u < 1,
              0                  otherwise.

The inner ball has charge 2 and the outer annulus charge -1, so the total is
1. Let B(z)=3(z cosh(z)-sinh(z))/z^3. Its exterior multiplier is

    F(x) = [15 B(x/2) - 8 B(x)]/7.
    F(4) = -1.2578597963643499176458835142650516... < 0.

A positive spectral atom at x=4 then yields a negative exterior profile.
Smooth signed approximations preserve this strict inequality. This does not
refute the E3 lemma, whose positivity hypothesis is explicit. Add that
hypothesis to the canonical paragraph and summaries.

The closing sentence at `paper/paper.tex:469-471` also changes a sufficient
criterion into an apparent necessary one: this review establishes an exterior
guarantee for nonnegative radial compact sources, not that every other source
must violate every threshold inequality. Replace "only" by language describing
the guarantee proved here.

## Finding 2 — MAJOR computational correctness, limited scientific effect: far-tail quadrature has an accuracy floor

Locations: `reproducibility/nonlinear_probe_eh.py:377-386`,
`notes/E3_nonlinear_probe_EH.md:416-417`,
`tests/test_e3_nonlinear_probe.py:357`.

At R=10, r=300, alpha=1/137.035999, the unscaled spectral quadrature returns
a stable wrong value even as `dps` increases through 40, 60, and 90:

    Gamma_raw(300) = 2.00755065423793887472192279537790095...

Multiplying the spectral integrand by exp(2r-100) before integrating gives

    Gamma_scaled(300) = 2.0075159041867909454418884873...

The latter number uses the same central-difference step h=1e-6; the small
last-digit difference from the exact logarithmic derivative is expected.
The unscaled profile has relative error approximately
`0.0017343921352834895`, i.e. 0.17344 percent. Increasing the precision without
rescaling does not resolve the quadrature's absolute stopping criterion.

An independent reference uses the explicit one-loop density, without the
module's density function, smeared-kernel routine, or raw quadrature:

    w(x) = exp(25(x^2-4)-300(x-2))
           * (2 alpha/(3 pi)) x (1+2/x^2) sqrt(1-4/x^2).
    Gamma = integral_2^3 x w(x) dx / integral_2^3 w(x) dx.

Here the Gaussian Yukawa error-function factors have already saturated to
their exterior values. At r=300, their corrections and the omitted x>3
contribution are far smaller than the discrepancy under review. With split
nodes 2, 2.001, 2.005, 2.01, 2.05, 2.1, 2.5, 3, this independent route gives

    dps 40: 2.007515904186790945378386875388079870083768...
    dps 60: 2.007515904186790945378386875388079870083771...
    dps 90: 2.007515904186790945378386875388079870083771...

A separate rescaled evaluation of the full exact smeared-Yukawa bracket,
including the high-x local tail, agrees to the quoted digits relevant here.
The correct five-decimal value is **2.00752**, not 2.00755. The test currently
requires agreement with the inaccurate number to absolute tolerance 1e-5.
These are independent high-precision checks, not interval certificates.

The qualitative return to the threshold from above survives. The important
Gaussian counterexample at r=50 and the three quoted crossover radii also
survive. This finding does not invalidate them.

At r=100 and r=120 the correctly rescaled slopes are approximately
1.93671796236 and 2.12221550228; their stated five-decimal values survive.
An early exploratory comparison omitted the high-x tail at these two radii;
that exploratory comparison is **not** evidence of percent-level error there.

Recommended numerical continuation: integrate a dimensionless, exponentially
normalized profile and its derivative/moment; compare against an independent
normalized route. Assert relative error after rescaling rather than relying
on raw `dps` convergence. A checked or certified truncation bound is a separate
task; do not describe a fixed three-term asymptotic tail as exact at arbitrary
working precision (`notes/E3_nonlinear_probe_EH.md:398-400`).

## Finding 3 — MINOR: the compact polynomial source is C1, not C-infinity

Locations: `notes/E3_nonlinear_probe_EH.md:456`,
`reproducibility/nonlinear_probe_eh.py:442-450`.

The function `(1-u^2/a^2)^2` on u<a, extended by zero outside, has a nonzero
interior second derivative at the boundary and zero exterior second derivative.
It is globally C1, not C-infinity. Calling it simply "smooth compact" can
conflate this benchmark with the C-infinity conserved-current mollifiers in
the transport construction. Say "C1 compact polynomial density" or use a
separate C-infinity bump. This does not affect the exterior lemma or its
computed multiplier. It supplies no control of higher-derivative EFT errors.

## Claims surviving independent review

### Positive compact radial exterior lemma — PROVED_CONDITIONALLY

For a nonnegative radial unit-total density supported within a finite a, the
shell solution of the Yukawa equation gives exactly the stated F on r>a.
The monotonicity of sinh(z)/z gives its two-sided bound. Strict positivity of
F preserves the support edge. Exponential growth F<=exp(ax) transfers the
original Laplace moment bounds after choosing a sufficiently later reference
radius. Complete monotonicity and the spectral bounds follow on the exterior
domain. All of these statements remain at linear probe order and retain the
positive-kernel hypothesis. No claim about arbitrary signed/nonradial probes
or full QED follows.

### Gaussian counterexample and matched roots — CHECKED

The headline Gamma(50) is confirmed at 40, 60, and 90 digits by both routes:

    spectral: 0.932403168696575383423525470392116046...
    momentum: 0.932403168696575383169296139950825679...

Their difference is about 2.54e-19. The counterexample to transferring the
point-source lower-threshold bound to arbitrary noncompact source profiles
survives.

With q=0.3, R or a=10, alpha as above, repeated precision checks give

    Gaussian: 55.9067264856621765265092644207645...  (dps 50 and 70)
    ball:     20.4822190112477457766668513200270...  (dps 50)
    C1 bump:  18.9502732027310441741636333072507...  (dps 50).

Default dps30 agrees well within the stated radius tolerances. An independent
momentum-space linear profile plus the same local nonlinear term gives the
Gaussian root 55.9067264856621765399250187862233 at dps50, differing from the
spectral root by approximately 1.34e-17. These are zeros of the specified
truncated sum, **not** exact full-QED zeros or rigorously bounded crossover
intervals. The text correctly leaves derivative, nonlocal, and higher-order
errors unbounded. Their cancellation at the crossing makes this limitation
essential.

### Arbitrary-source energy bound — PROVED inside the local electric theory

Locations: `notes/E3_nonlinear_probe_EH.md:465-482`.

I independently obtain the stated inequality for c>=0. The assumptions
D0 in L2 intersect L6 imply D0 in L4, so every displayed Maxwell trial-field
integral is finite. The Legendre transform obeys the pointwise inequality

    h_c(D0) <= |D0|^2/2 - c|D0|^4 + 8c^2|D0|^6.

Using D0 as a primal admissible trial gives the upper bound. Fenchel-Young
with E0=D0 and the weak integration-by-parts identity gives the lower bound.
For a fully formal whole-space statement, specify the finite-energy affine
divergence class (the natural L2+L^(4/3) Orlicz class for c>0), use the infimum,
and justify density of compact test potentials or existence of the minimum.
The stated assumptions permit the usual approximation because E0 belongs to
L2 intersect L4. This is a functional-analytic presentation detail; I found no
counterexample to the bound.

There is no hidden curl assumption invalidating the proof: a nonradial
nonlinear minimizing displacement need not equal D0, and minimization against
divergence-free variations enforces curl-free electric field h'_c(D). The
formal second-order transverse projection in lines 484-489 is consistent with
that fact. The difference-of-remainders estimate for V follows from taking
the difference of two nonnegative bounded remainders; the max in its bound is
correct, and the bound need not decay with separation.

The grounded-grid calculation checks an edgewise scalar graph analogue, not
a continuum three-dimensional PDE discretization of the isotropic quartic
functional. The report accurately calls it a lattice check. Its role should
remain a check of the proof mechanism, not independent continuum certification.

## Verification and stopping boundary

Command executed without bytecode or pytest cache writes:

    PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_e3_nonlinear_probe.py -q -p no:cacheprovider

Result: **38 passed in 25.61 s**. Passing tests do not remove Finding 2,
because the far-tail test currently asserts the inaccurate reference.

Independent calculations were temporary Python stdin scripts; no repository
scientific file was edited or regenerated. No commit, staging, push, external
publication, or full-suite validation was performed by this reviewer.

No FATAL finding within this bounded scope. Full-QED spectral behavior,
decaying interaction remainder, controlled nonlocal light-by-light matching,
and rigorous numerical certification remain OPEN.
