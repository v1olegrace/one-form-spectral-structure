"""Reproducible checks for the symmetry-resolved positivity manuscript.

The script uses a unit-mass Dirac fermion benchmark.  It evaluates the exact
Kallen-Lehmann moments of the conserved vector current, verifies the ratio and
Hankel/localizing bounds, and runs a deterministic Monte Carlo uncertainty
study.  All outputs are regenerated from scratch under output/data and
output/figures.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "output" / "data"
FIGURE_DIR = ROOT / "output" / "figures"
SEED = 20260910
N_DRAWS = 100_000


def beta(a: float, b: float) -> float:
    """Euler beta function evaluated through log-gamma for stability."""

    return math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))


def dirac_moment(n: int, mass: float = 1.0, charge: float = 1.0) -> float:
    r"""Return c_n = integral rho(s) / s^(n+1) ds for n >= 1.

    rho(s) = q^2/(12 pi^2) (1 + 2 m^2/s) sqrt(1 - 4 m^2/s)
    for s >= 4 m^2.
    """

    if n < 1:
        raise ValueError("n must be at least 1")
    integral = beta(n, 1.5) + 0.5 * beta(n + 1, 1.5)
    return charge**2 * integral / (12.0 * math.pi**2 * (4.0 * mass**2) ** n)


def exact_ratio(n: int, mass: float = 1.0) -> float:
    """Closed form for c_n/c_(n+1)."""

    return (
        4.0
        * mass**2
        * (n + 1.0)
        * (2.0 * n + 5.0)
        / (2.0 * n * (n + 2.0))
    )


def localizing_bound(n0: int, order: int, mass: float = 1.0) -> float:
    """Return min generalized eigenvalue of H0 v = lambda H1 v.

    H0[i,j] = c_(n0+i+j), H1[i,j] = c_(n0+i+j+1).  Positivity of
    H0 - s0 H1 implies s0 <= lambda_min(H0,H1).
    """

    idx = np.arange(order + 1)
    h0 = np.array(
        [[dirac_moment(n0 + int(i + j), mass) for j in idx] for i in idx],
        dtype=float,
    )
    h1 = np.array(
        [
            [dirac_moment(n0 + int(i + j) + 1, mass) for j in idx]
            for i in idx
        ],
        dtype=float,
    )
    scale = np.sqrt(np.diag(h1))
    h0_scaled = h0 / np.outer(scale, scale)
    h1_scaled = h1 / np.outer(scale, scale)
    eigenvalues = eigh(h0_scaled, h1_scaled, eigvals_only=True)
    return float(np.min(eigenvalues))


def monte_carlo_ratio(n: int = 20, relative_sigma: float = 0.005) -> dict[str, float]:
    """Quantify ratio-estimator bias, coverage, and rejection power.

    Adjacent log-moment errors have correlation 0.7.  A lognormal observation
    model guarantees positive measured moments and is centered so that each
    moment estimate is unbiased in linear space.
    """

    rng = np.random.default_rng(SEED)
    correlation = 0.7
    covariance = relative_sigma**2 * np.array(
        [[1.0, correlation], [correlation, 1.0]], dtype=float
    )
    mean_shift = -0.5 * np.diag(covariance)
    noise = rng.multivariate_normal(mean_shift, covariance, size=N_DRAWS)
    true_pair = np.array([dirac_moment(n), dirac_moment(n + 1)])
    observed = true_pair * np.exp(noise)
    ratio_draws = observed[:, 0] / observed[:, 1]

    true_ratio = exact_ratio(n)
    sigma_log_ratio = relative_sigma * math.sqrt(2.0 * (1.0 - correlation))
    z95 = 1.6448536269514722
    upper = ratio_draws * np.exp(z95 * sigma_log_ratio)

    return {
        "seed": SEED,
        "draws": N_DRAWS,
        "moment_index_n": n,
        "relative_sigma_each_moment": relative_sigma,
        "adjacent_log_error_correlation": correlation,
        "true_threshold_s0": 4.0,
        "true_ratio_Rn": true_ratio,
        "structural_excess_fraction_Rn_over_s0": true_ratio / 4.0 - 1.0,
        "mean_ratio_estimate": float(np.mean(ratio_draws)),
        "relative_statistical_bias": float(np.mean(ratio_draws) / true_ratio - 1.0),
        "rmse_relative_to_Rn": float(
            np.sqrt(np.mean((ratio_draws - true_ratio) ** 2)) / true_ratio
        ),
        "one_sided_95_coverage_for_Rn": float(np.mean(upper >= true_ratio)),
        "one_sided_95_coverage_for_s0": float(np.mean(upper >= 4.0)),
        "power_reject_gap_ge_1p01_Rn": float(np.mean(upper < 1.01 * true_ratio)),
        "power_reject_gap_ge_1p02_Rn": float(np.mean(upper < 1.02 * true_ratio)),
        "power_reject_gap_ge_1p05_Rn": float(np.mean(upper < 1.05 * true_ratio)),
    }


def write_outputs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    ratio_rows = []
    for n in range(1, 31):
        numerical = dirac_moment(n) / dirac_moment(n + 1)
        closed = exact_ratio(n)
        ratio_rows.append(
            {
                "n": n,
                "c_n": dirac_moment(n),
                "ratio_numeric": numerical,
                "ratio_closed_form": closed,
                "ratio_over_threshold": closed / 4.0,
                "relative_formula_error": abs(numerical / closed - 1.0),
            }
        )

    with (DATA_DIR / "dirac_moment_ratios.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=ratio_rows[0].keys())
        writer.writeheader()
        writer.writerows(ratio_rows)

    localizing_rows = []
    for order in range(0, 6):
        bound = localizing_bound(n0=1, order=order)
        localizing_rows.append(
            {
                "matrix_order_K": order,
                "dimension": order + 1,
                "upper_bound_s0": bound,
                "bound_over_true_s0": bound / 4.0,
            }
        )

    with (DATA_DIR / "localizing_bounds.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=localizing_rows[0].keys())
        writer.writeheader()
        writer.writerows(localizing_rows)

    stats = monte_carlo_ratio()
    (DATA_DIR / "uncertainty_summary.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    ns = np.array([row["n"] for row in ratio_rows])
    normalized = np.array([row["ratio_over_threshold"] for row in ratio_rows])
    fig, ax = plt.subplots(figsize=(7.2, 4.3), constrained_layout=True)
    ax.plot(ns, normalized, "o-", color="#1f5f99", lw=1.8, ms=3.8)
    ax.axhline(1.0, color="#202020", ls="--", lw=1.2, label=r"limiar exato $s_0=4m^2$")
    ax.set_xlabel(r"ordem do momento $n$")
    ax.set_ylabel(r"$R_n/s_0$, com $R_n=c_n/c_{n+1}$")
    ax.set_xlim(1, 30)
    ax.set_ylim(0.98, max(normalized) * 1.03)
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    fig.savefig(FIGURE_DIR / "dirac_ratio_convergence.png", dpi=220)
    fig.savefig(FIGURE_DIR / "dirac_ratio_convergence.svg")
    plt.close(fig)

    orders = np.array([row["matrix_order_K"] for row in localizing_rows])
    bounds = np.array([row["bound_over_true_s0"] for row in localizing_rows])
    fig, ax = plt.subplots(figsize=(7.2, 4.3), constrained_layout=True)
    ax.plot(orders, bounds, "s-", color="#8b2f3f", lw=1.8, ms=5)
    ax.axhline(1.0, color="#202020", ls="--", lw=1.2, label="limiar exato")
    ax.set_xlabel(r"ordem $K$ da matriz localizadora")
    ax.set_ylabel(r"$B_{1,K}/s_0$")
    ax.set_xticks(orders)
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    fig.savefig(FIGURE_DIR / "localizing_bound_convergence.png", dpi=220)
    fig.savefig(FIGURE_DIR / "localizing_bound_convergence.svg")
    plt.close(fig)

    checks = {
        "max_relative_ratio_formula_error": max(
            row["relative_formula_error"] for row in ratio_rows
        ),
        "ratios_monotone_nonincreasing": bool(
            np.all(np.diff([row["ratio_closed_form"] for row in ratio_rows]) <= 0)
        ),
        "all_ratio_bounds_above_threshold": bool(
            np.all(np.array([row["ratio_closed_form"] for row in ratio_rows]) >= 4.0)
        ),
        "localizing_bounds_monotone_nonincreasing": bool(np.all(np.diff(bounds) <= 1e-10)),
        "all_localizing_bounds_above_threshold": bool(np.all(bounds >= 1.0 - 1e-10)),
    }
    (DATA_DIR / "verification_checks.json").write_text(
        json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not all(value for value in checks.values() if isinstance(value, bool)):
        raise RuntimeError(f"verification failed: {checks}")


if __name__ == "__main__":
    write_outputs()
