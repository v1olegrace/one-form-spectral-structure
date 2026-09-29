"""Generate the data tables plotted in paper/paper.tex (pgfplots).

Only NumPy is required, so the figures can be rebuilt on a machine where the
high-precision stack (mpmath) is unavailable.  Both quantities plotted here
are well conditioned in double precision:

* the hidden-threshold model has a closed-form Laplace transform, and
* the Dirac edge law is evaluated by quadrature after the substitution
  x = 2m cosh(u), with the common factor exp(-2 m r) removed analytically.

Status vocabulary follows README.md: everything produced here is CHECKED
(double-precision numerics cross-checked against closed forms or asymptotic
series), never CERTIFIED.

Usage::

    python reproducibility/figure_data.py          # writes paper/figures/*.dat
    python reproducibility/figure_data.py --check  # also asserts the values
                                                   # quoted in the paper text
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"

# Hidden-threshold model (paper, Section "Numerical validation"):
#   dnu = EPS * delta(x - M_EDGE) + (x - M_CONT)^{1/2} e^{-(x - M_CONT)} dx
EPS: float = 1e-12
M_EDGE: float = 2.0
M_CONT: float = 3.0
C_CONT: float = math.gamma(1.5)


def hidden_gamma(r: NDArray[np.float64]) -> NDArray[np.float64]:
    """Gamma(r) = -d log Phi / dr for the hidden-threshold model.

    Phi(r) = EPS e^{-2r} + Gamma(3/2) (1+r)^{-3/2} e^{-3r}.  The common factor
    e^{-2r} is divided out so that no underflow occurs for large r.
    """
    cont = C_CONT * (1.0 + r) ** -1.5 * np.exp(-(M_CONT - M_EDGE) * r)
    dcont = cont * (M_CONT + 1.5 / (1.0 + r))
    return (EPS * M_EDGE + dcont) / (EPS + cont)


def hidden_crossover() -> float:
    """Radius at which the two components of Phi have equal amplitude.

    Solves EPS e^{-2r} = Gamma(3/2) (1+r)^{-3/2} e^{-3r} by fixed-point
    iteration.  This is a property of this specific model; it is NOT the
    t_x of Theorem H, which refers to the two-exponential family used there.
    """
    r = 25.0
    for _ in range(200):
        r = math.log(C_CONT / EPS) - 1.5 * math.log1p(r)
    return r


def dirac_gamma(r_values: NDArray[np.float64], m: float = 1.0,
                n_nodes: int = 400_001, u_max: float = 12.0
                ) -> NDArray[np.float64]:
    """Gamma(r) for one Dirac species, dnu/dx ~ x (1 + 2m^2/x^2) sqrt(1-4m^2/x^2).

    The overall normalisation cancels in Gamma.  With x = 2m cosh(u) the
    square-root edge singularity is removed; the integrand is smooth and
    decays like exp(-2 m r (cosh u - 1)), so the trapezoidal rule on a fine
    uniform grid converges rapidly.
    """
    u = np.linspace(0.0, u_max, n_nodes)
    x = 2.0 * m * np.cosh(u)
    jac = 2.0 * m * np.sinh(u)
    dens = x * (1.0 + 2.0 * m**2 / x**2) * np.sqrt(
        np.clip(1.0 - 4.0 * m**2 / x**2, 0.0, None)) * jac
    out = np.empty_like(r_values)
    for i, r in enumerate(r_values):
        w = dens * np.exp(-r * (x - 2.0 * m))
        out[i] = 2.0 * m + np.trapezoid((x - 2.0 * m) * w, u) / np.trapezoid(w, u)
    return out


def dirac_series(r: NDArray[np.float64], m: float = 1.0) -> NDArray[np.float64]:
    """Edge-law asymptotics r(Gamma - 2m) = 3/2 - 5/(16 m r) + 45/(32 m^2 r^2)."""
    return 1.5 - 5.0 / (16.0 * m * r) + 45.0 / (32.0 * m**2 * r**2)


def write_table(path: Path, header: str, cols: list[NDArray[np.float64]]) -> None:
    data = np.column_stack(cols)
    np.savetxt(path, data, header=header, comments="", fmt="%.10e")


def signed_measure_values() -> dict[str, float]:
    """Moments of dnu = delta_1 - (1/2) delta_2 at r = 1, raw and rescaled.

    a_n(r) = e^{-r} - (1/2) 2^n e^{-2r}.  The rescaled moments are
    e^{r} a_n(r); det H_0 is for the 2x2 pencil (K = 1).
    """
    r = 1.0

    def a(n: int) -> float:
        return math.exp(-r) - 0.5 * 2**n * math.exp(-2 * r)

    det = a(0) * a(2) - a(1) ** 2
    return {"a3": a(3), "a3_rescaled": math.exp(r) * a(3),
            "detH0": det, "detH0_rescaled": math.exp(2 * r) * det}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="assert the numbers quoted in the paper")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    r_h = np.linspace(0.5, 40.0, 400)
    write_table(OUT / "hidden_threshold.dat", "r Gamma",
                [r_h, hidden_gamma(r_h)])

    r_d = np.geomspace(5.0, 300.0, 60)
    g_d = dirac_gamma(r_d)
    write_table(OUT / "dirac_edge_law.dat", "r rGm series",
                [r_d, r_d * (g_d - 2.0), dirac_series(r_d)])

    rx = hidden_crossover()
    sm = signed_measure_values()
    print(f"hidden-threshold crossover r_x = {rx:.4f}")
    for r in (10.0, 20.0, rx, 30.0):
        print(f"  Gamma({r:.2f}) = {hidden_gamma(np.array([r]))[0]:.4f}")
    print("signed measure at r=1:", {k: round(v, 4) for k, v in sm.items()})

    if args.check:
        assert abs(rx - 22.7583) < 1e-3
        quoted = {10.0: 3.136, 20.0: 3.018, rx: 2.532, 30.0: 2.0005}
        for r, v in quoted.items():
            got = hidden_gamma(np.array([r]))[0]
            assert abs(got - v) < 5e-4, (r, got, v)
        assert abs(sm["a3"] + 0.1735) < 1e-4
        assert abs(sm["a3_rescaled"] + 0.4715) < 1e-4
        assert abs(sm["detH0"] + 0.0249) < 1e-4
        assert abs(sm["detH0_rescaled"] + 0.1839) < 1e-4
        # Added audit counterexample: positive H0 but indefinite H1.
        # det(H1-lambda H0) = .855 lambda^2 - 1.341 lambda - .09.
        a0, a1, a2, a3 = 1.999, 2.99, 4.9, 8.0
        assert abs(a0*a2-a1*a1-0.855) < 1e-12
        assert abs(a1*a3-a2*a2+0.09) < 1e-12
        invalid_bound = (1.341-math.sqrt(1.341**2+4*0.855*0.09))/(2*0.855)
        assert abs(invalid_bound+0.0644645) < 1e-7
        big = dirac_gamma(np.array([80.0]))[0]
        assert abs(80.0 * (big - 2.0) - dirac_series(np.array([80.0]))[0]) < 1e-4
        print("all quoted values reproduced")


if __name__ == "__main__":
    main()
