# SOFTWARE AUDIT

Generated 2026-09-11.

**Star counts are metadata, not quality evidence.** They are recorded
because they are cheap to record, and ignored in the recommendation.

## What we actually need, and what exists

| Need | Our current implementation | Best external candidate |
|---|---|---|
| arbitrary precision | `mpmath` (dps up to 200) | mpmath; `python-flint`/Arb is faster and has rigorous balls |
| interval arithmetic | `mpmath.iv` | **Arb via python-flint** — ball arithmetic is the standard, and `mp.iv` lacks its rigorous special functions |
| generalized eigenproblem | `mp.cholesky` + `mp.eigsy` | Arb's `arb_mat` eigen routines, for certified enclosures |
| moment / SOS hierarchy | none | `GloptiPoly`, `SumOfSquares.jl`, `ncpol2sdpa` |
| Prony / matrix pencil | none | see cluster H repositories below |
| inverse Laplace | none | `CONTIN`-family and NNLS implementations |

**The one concrete recommendation:** move the certified path from
`mpmath.iv` to **Arb (python-flint)**. The wide-dynamic-range model
needed ~86 digits where float64 has 16, and `mp.iv` has no rigorous
special-function support; Arb's ball arithmetic is designed for exactly
this and would let the `CERTIFIED` label cover more of the pipeline.

## Repositories discovered

* **KarpelesLab/puremp** (Rust, MIT, ★4, updated 2026-07-12) — Pure-Rust, clean-room arbitrary-precision arithmetic: integers, rationals, MPFR-class floats, decimals, complex, polynom
* **mrlhansen/rmsd** (C, no license, ★2, updated 2024-08-27) — Reconstruction of smeared spectral densities from lattice QCD correlators
* **34j/numpy-flint-arb** (Python, MIT, ★1, updated 2026-09-11) — Arbitrary precision floating / ball arithmetic (interval arithmetic) dtype in NumPy / array API
* **lituus-lab/UniMath** (Nim, Apache-2.0, ★1, updated 2026-09-09) — Multi-precision arithmetic engine: arbitrary-precision integers, fixed-point, big floats, rationals, intervals and compl
* **hottorch/Python-tools-for-Deep-Level-Transient-Spectroscopy-analysis** (Python, Unlicense, ★0, updated 2025-07-03) — A part of the supplimentary information of the paper: Comparison of Five DLTS Analysis Methods on a SiC Schottky Diode: 
* **LoopyNoodle/axial-form-factors** (Jupyter Notebook, no license, ★0, updated 2023-11-13) — Exploring the phenomenological applications of rational approximations, such as Padé approximants, to estimate axial mas
* **buividovich/static_lattice_QCD** (C++, no license, ★0, updated 2025-12-28) — Code for hamiltonian-based lattice QCD simulations. Implements numerical methods described in the paper "Spectral recons
* **epi13/mncs-math** (Python, Apache-2.0, ★0, updated 2026-09-08) — Machine-native scientific mathematics for MNCS, including linear algebra, arbitrary precision, tensors, autodiff, interv
* **thiagomassensini/finite-native-carry-operator** (Python, Apache-2.0, ★0, updated 2026-08-05) — Numerical and formal study of finite native-carry operators over R², including multibase CPU/CUDA scanning, arbitrary-pr

## Archived research records (Zenodo)

* Layered-column vertical scattering and tomographic resolution analysis for L-band radar so — <p>A horizontally layered snow, sea ice, slush and seawater column is built from field-derived param
* erdc/proteus: 1.9.0 — <h1>Contributors</h1>
<ul>
<li>Chris Kees @cekees</li>
<li>Arnob Barua @abarua-ce</li>
<li>Darsh Nat
* Reproducibility archive for conditioning-controlled retrieval of broadband land surface te — <p>This archive provides the frozen Version 12b scientific reproducibility materials associated with
* Code for "Quantifying the responses of AI precipitation forecast errors to reanalysis erro — <p>This repository archives the code supporting the manuscript &ldquo;Quantifying the responses of A
* radio-astro-tools/tutorials: 2026.09.10 — <h2>What's Changed</h2>
<ul>
<li>add spectral-cube reprojection example by @keflavich in https://git
* music: extreme-fidelity synthesis of musical elements — Extreme-fidelity synthesis of musical elements, based on the MASS framework: psychophysical descript
* fabtwin: learned generative process twins for yield-aware inverse design of multilayer opt — <p>Real-data release: the pipeline the paper names as its essential next step -- a process twin trai
* Reproducibility code for Prognostic Drift in Survival Risk Sets — <p>Reproducibility code for the manuscript &ldquo;Prognostic Drift in Survival Risk Sets: Structure,
* Data and software for estimating electron density enhancements caused by solar flares usin — Reproducibility package containing the code, curated notebooks, observational and synthetic data pro
* nvrecon: physics-informed magnetization reconstruction from NV magnetometry maps — <p>Python package nvrecon: physics-informed reconstruction of a thin-film magnetization from a singl
* ramansep: two-mode separation of strain and carrier density in 2D-material Raman maps — <p>Calibration release: the package's no-shipped-coefficients policy finally comes with the tool tha
* OpenPBEE/Functional-Recovery-Python — <p>This release brings the component library up to the current ATC-138 fragility set, raises the saf
