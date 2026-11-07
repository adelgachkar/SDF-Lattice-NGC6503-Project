"""Shared kernels for the SDF-Lattice NGC 6503 analysis.

Everything here is standard-library only. Units are fixed throughout:

* radius        kpc
* velocity      km/s
* mass          Msun
* acceleration  (km/s)^2 / kpc      (so ``G`` below is in kpc (km/s)^2 / Msun)

Three rotation-curve models live here so that they can be fitted to one table,
with one stellar mass-to-light ratio and one definition of ``p``:

``sdf_velocity``
    The canonical radial-unfreezing closure,
    ``v^2 = v_bar^2 + (v_inf^2 - v_bar^2) * zeta(r)``.
``nfw_velocity``
    A Navarro-Frenk-White halo added in quadrature to the same baryons.
``mond_velocity``
    Milgrom's law with a fixed or fitted ``a0`` and one of two standard
    interpolation functions.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

# --------------------------------------------------------------------------- #
# Units and constants
# --------------------------------------------------------------------------- #
KPC_TO_M = 3.0857e19            # metres per kpc
G_KPC_KM2_MSUN = 4.300917e-6    # kpc (km/s)^2 / Msun
A0_SI = 1.2e-10                 # m / s^2, Milgrom's acceleration scale
# 1 (km/s)^2/kpc == 3.2408e-14 m/s^2, hence:
A0_KPC = A0_SI * KPC_TO_M / 1e6  # ~3702.8 (km/s)^2/kpc
A0_ERR_KPC = 0.2e-10 * KPC_TO_M / 1e6  # placeholder unless a0 is fitted

DEFAULT_R0_KPC = 1.83
DEFAULT_DELTA_R_KPC = 0.46
DEFAULT_V_INF_KMS = 116.2
DEFAULT_UPSILON_DISK = 0.62

MODEL_NAMES = ("sdf", "nfw", "mond_simple", "mond_standard")


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
def load_rotmod(path: str | Path) -> Tuple[List[Dict[str, float]], float | None]:
    """Parse a SPARC ``Rotmod_LTG`` file into rows plus the distance in its header."""
    rows: List[Dict[str, float]] = []
    distance = None
    with Path(path).open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            if text.startswith("#"):
                if "Distance" in text and "=" in text:
                    try:
                        distance = float(text.split("=")[1].split()[0])
                    except (IndexError, ValueError):
                        pass
                continue
            cells = text.split()
            if len(cells) < 6:
                continue
            try:
                values = [float(cell) for cell in cells[:8]]
            except ValueError:
                continue
            while len(values) < 8:
                values.append(0.0)
            rows.append({"r": values[0], "v_obs": values[1], "err": values[2],
                         "v_gas": values[3], "v_disk": values[4], "v_bul": values[5],
                         "sb_disk": values[6], "sb_bul": values[7]})
    if not rows:
        raise ValueError(f"no data rows parsed from {path}")
    return rows, distance


def baryonic_squared(row: Dict[str, float], ups_disk: float = DEFAULT_UPSILON_DISK,
                     ups_bul: float = 0.0) -> float:
    """SPARC baryonic speed squared; the gas term keeps its sign."""
    if ups_disk < 0 or ups_bul < 0:
        raise ValueError("mass-to-light ratios must be non-negative")
    return row["v_gas"] * abs(row["v_gas"]) + ups_disk * row["v_disk"] ** 2 + ups_bul * row["v_bul"] ** 2


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #
def zeta(r_kpc: float, r0: float = DEFAULT_R0_KPC, dr: float = DEFAULT_DELTA_R_KPC) -> float:
    """Canonical smooth transition, dimensionless in (0, 1)."""
    if r_kpc < 0:
        raise ValueError("radius must be non-negative")
    if dr <= 0:
        raise ValueError("transition width must be positive")
    return 0.5 * (1.0 + math.tanh((r_kpc - r0) / dr))


def sdf_velocity(r_kpc: float, v_bar_kms: float, v_inf_kms: float = DEFAULT_V_INF_KMS,
                 r0: float = DEFAULT_R0_KPC, dr: float = DEFAULT_DELTA_R_KPC) -> float:
    """Canonical closure: v^2 = v_bar^2 + (v_inf^2 - v_bar^2) * zeta(r)."""
    if r_kpc <= 0:
        raise ValueError("radius must be positive")
    if v_bar_kms < 0:
        raise ValueError("baryonic speed must be non-negative")
    v_bar2 = v_bar_kms * v_bar_kms
    excess = max(0.0, v_inf_kms * v_inf_kms - v_bar2)
    return math.sqrt(max(v_bar2 + excess * zeta(r_kpc, r0, dr), 1e-12))


def nfw_velocity_squared(r_kpc: float, rho_s: float, r_s: float) -> float:
    """NFW halo contribution, ``4 pi G rho_s r_s^3 / r * [ln(1+x) - x/(1+x)]``."""
    if r_kpc <= 0:
        raise ValueError("radius must be positive")
    if rho_s <= 0 or r_s <= 0:
        raise ValueError("NFW parameters must be positive")
    x = r_kpc / r_s
    return 4.0 * math.pi * G_KPC_KM2_MSUN * rho_s * r_s ** 3 / r_kpc * (
        math.log1p(x) - x / (1.0 + x))


def nfw_velocity(r_kpc: float, v_bar_kms: float, rho_s: float, r_s: float) -> float:
    """Total speed with an NFW halo added in quadrature to the same baryons."""
    if v_bar_kms < 0:
        raise ValueError("baryonic speed must be non-negative")
    total = v_bar_kms ** 2 + nfw_velocity_squared(r_kpc, rho_s, r_s)
    return math.sqrt(max(total, 1e-12))


def mond_nu(y: float, interpolation: str = "simple") -> float:
    """Boost factor nu(y) with y = g_bar / a0.

    ``simple``   nu = 1/2 + sqrt(1/4 + 1/y)
    ``standard`` nu = sqrt(1/2 + sqrt(1/4 + 1/y^2))

    Both reduce to ``1 + 1/(2y)`` at large y and to ``1/sqrt(y)`` in the
    deep-MOND limit, i.e. ``v^4 = G M a0``.
    """
    if y <= 0:
        raise ValueError("y = g_bar/a0 must be positive")
    if interpolation == "simple":
        return 0.5 + math.sqrt(0.25 + 1.0 / y)
    if interpolation == "standard":
        return math.sqrt(0.5 + math.sqrt(0.25 + 1.0 / y ** 2))
    raise ValueError("interpolation must be 'simple' or 'standard'")


def mond_velocity(r_kpc: float, v_bar_kms: float, a0_kpc: float = A0_KPC,
                  interpolation: str = "simple") -> float:
    """Milgrom's law applied to the baryonic acceleration of each point."""
    if r_kpc <= 0:
        raise ValueError("radius must be positive")
    if v_bar_kms < 0:
        raise ValueError("baryonic speed must be non-negative")
    if a0_kpc <= 0:
        raise ValueError("a0 must be positive")
    g_bar = v_bar_kms ** 2 / r_kpc
    return v_bar_kms * math.sqrt(mond_nu(g_bar / a0_kpc, interpolation))


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #
def chi_squared(observed: Sequence[float], predicted: Sequence[float],
                sigma: Sequence[float], n_parameters: int = 0) -> Tuple[float, int]:
    """Weighted chi-square and dof = N - p, with p counted on the same points."""
    n = len(observed)
    if n == 0 or len(predicted) != n or len(sigma) != n:
        raise ValueError("arrays must have equal nonzero length")
    dof = n - n_parameters
    if dof <= 0:
        raise ValueError("degrees of freedom N-p must be positive")
    if any(not math.isfinite(value) for array in (observed, predicted, sigma) for value in array):
        raise ValueError("non-finite input")
    if any(s <= 0 for s in sigma):
        raise ValueError("all uncertainties must be positive")
    total = sum(((o - m) / s) ** 2 for o, m, s in zip(observed, predicted, sigma))
    return total, dof


def aic(chi2: float, n_parameters: int) -> float:
    """AIC for Gaussian errors with known sigma: chi^2 + 2p."""
    return chi2 + 2.0 * n_parameters


def bic(chi2: float, n_parameters: int, n_points: int) -> float:
    """BIC for Gaussian errors with known sigma: chi^2 + p ln N."""
    return chi2 + n_parameters * math.log(n_points)


# --------------------------------------------------------------------------- #
# Bounded Nelder-Mead (same routine as the verification script)
# --------------------------------------------------------------------------- #
def nelder_mead(f, x0, steps, lo, hi, tol: float = 1e-12, max_iter: int = 6000):
    """Minimise ``f`` on a box; returns ``(x_best, f_best)``."""

    def bounded(point):
        return [min(max(v, l), h) for v, l, h in zip(point, lo, hi)]

    n = len(x0)
    points = [bounded(list(x0))]
    for i in range(n):
        point = list(points[0])
        point[i] = min(max(point[i] + steps[i], lo[i]), hi[i])
        if point[i] == points[0][i]:
            point[i] = min(max(point[i] - steps[i], lo[i]), hi[i])
        points.append(point)
    values = [f(p) for p in points]

    for _ in range(max_iter):
        order = sorted(range(n + 1), key=lambda k: values[k])
        points = [points[k] for k in order]
        values = [values[k] for k in order]
        if abs(values[-1] - values[0]) <= tol * (abs(values[0]) + tol):
            break
        centroid = [sum(points[k][i] for k in range(n)) / n for i in range(n)]
        worst = points[-1]
        reflected = bounded([centroid[i] + (centroid[i] - worst[i]) for i in range(n)])
        f_reflected = f(reflected)
        if f_reflected < values[0]:
            expanded = bounded([centroid[i] + 2.0 * (centroid[i] - worst[i]) for i in range(n)])
            f_expanded = f(expanded)
            if f_expanded < f_reflected:
                points[-1], values[-1] = expanded, f_expanded
            else:
                points[-1], values[-1] = reflected, f_reflected
        elif f_reflected < values[-2]:
            points[-1], values[-1] = reflected, f_reflected
        else:
            contracted = bounded([centroid[i] + 0.5 * (worst[i] - centroid[i]) for i in range(n)])
            f_contracted = f(contracted)
            if f_contracted < values[-1]:
                points[-1], values[-1] = contracted, f_contracted
            else:
                for k in range(1, n + 1):
                    points[k] = bounded([points[0][i] + 0.5 * (points[k][i] - points[0][i])
                                         for i in range(n)])
                    values[k] = f(points[k])

    best = min(range(n + 1), key=lambda k: values[k])
    return points[best], values[best]


# --------------------------------------------------------------------------- #
# Fits on a SPARC table
# --------------------------------------------------------------------------- #
def _predict(rows: Iterable[Dict[str, float]], kind: str, params: Dict[str, float],
             ups_bul: float = 0.0) -> List[float]:
    ups_disk = params["ups_disk"]
    out = []
    for row in rows:
        b2 = max(baryonic_squared(row, ups_disk, ups_bul), 0.0)
        v_bar = math.sqrt(b2)
        r = row["r"]
        if kind == "sdf":
            out.append(sdf_velocity(r, v_bar, params["v_inf"], params["r0"], params["dr"]))
        elif kind == "nfw":
            out.append(nfw_velocity(r, v_bar, 10.0 ** params["log_rho_s"], 10.0 ** params["log_r_s"]))
        elif kind in ("mond_simple", "mond_standard"):
            out.append(mond_velocity(r, v_bar, 10.0 ** params["log_a0"],
                                     "simple" if kind.endswith("simple") else "standard"))
        else:
            raise ValueError(f"unknown model {kind!r}")
    return out


def _chi2_for(rows, kind, params, ups_bul=0.0) -> float:
    predicted = _predict(rows, kind, params, ups_bul)
    total = 0.0
    for row, model in zip(rows, predicted):
        total += ((row["v_obs"] - model) / row["err"]) ** 2
    return total


def _unpack(kind: str, names: Sequence[str], x: Sequence[float], base: Dict[str, float]) -> Dict[str, float]:
    params = dict(base)
    params.update(dict(zip(names, x)))
    if "log_a0" in params:
        params["a0"] = 10.0 ** params["log_a0"]
    if "log_rho_s" in params:
        params["rho_s"] = 10.0 ** params["log_rho_s"]
    if "log_r_s" in params:
        params["r_s"] = 10.0 ** params["log_r_s"]
    return params


BOUNDS = {
    "ups_disk": (0.01, 2.0),
    "v_inf": (60.0, 200.0),
    "r0": (0.05, 12.0),
    "dr": (0.05, 6.0),
    "log_rho_s": (2.0, 14.0),
    "log_r_s": (-1.5, 2.5),
    "log_a0": (math.log10(500.0), math.log10(15000.0)),
}
STEPS = {"ups_disk": 0.2, "v_inf": 2.0, "r0": 0.3, "dr": 0.2,
         "log_rho_s": 1.0, "log_r_s": 0.3, "log_a0": 0.1}
START = {"ups_disk": 0.62, "v_inf": 116.2, "r0": 1.83, "dr": 0.46,
         "log_rho_s": 8.0, "log_r_s": 0.5, "log_a0": math.log10(A0_KPC)}


def fit_model(rows, kind: str, uns_fixed: float | None = DEFAULT_UPSILON_DISK,
              free: Sequence[str] = (), ups_bul: float = 0.0,
              starts: Sequence[Dict[str, float]] | None = None) -> Dict[str, float]:
    """Fit one model with an explicit list of free parameters.

    ``p`` is exactly ``len(free)``; ``v_inf``, ``rho_s``, ``r_s`` and ``a0`` all
    count whenever they are fitted to the same points, because every one of them
    is taken from the galaxy under study.
    """
    names = list(free)
    lo = [BOUNDS[name][0] for name in names]
    hi = [BOUNDS[name][1] for name in names]
    steps = [STEPS[name] for name in names]

    # Seed set mirrors the verification script, so that the shared implementation
    # reproduces the published ladder exactly rather than landing in a different
    # local minimum.
    ups_seed = uns_fixed if uns_fixed is not None else 0.5
    base = {"v_inf": 116.2, "r0": 1.83, "dr": 0.46,
            "log_rho_s": 8.0, "log_r_s": 0.5, "log_a0": math.log10(A0_KPC),
            "ups_disk": ups_seed}
    extras: List[Dict[str, float]] = [{}]
    if kind == "sdf":
        extras += [{"v_inf": 110.0, "r0": 1.0, "dr": 1.2, "ups_disk": 0.6},
                   {"v_inf": 125.0, "r0": 3.0, "dr": 0.3, "ups_disk": 0.4}]
    elif kind == "nfw":
        extras += [{"log_rho_s": 7.0, "log_r_s": 0.0},
                   {"log_rho_s": 9.0, "log_r_s": 1.0}]
    else:
        extras += [{"log_a0": math.log10(A0_KPC * 0.7)},
                   {"log_a0": math.log10(A0_KPC * 1.4)}]
    if starts:
        extras += list(starts)
    seeds = [{**base, **extra} for extra in extras]

    def objective(x):
        params = _unpack(kind, names, x, base)
        if params["dr"] <= 0:
            return float("inf")
        return _chi2_for(rows, kind, params, ups_bul)

    best = None
    for seed in seeds:
        x0 = [seed[name] for name in names]
        x, fx = nelder_mead(objective, x0, steps, lo, hi)
        if best is None or fx < best[1]:
            best = (x, fx)

    params = _unpack(kind, names, best[0], base)
    predicted = _predict(rows, kind, params, ups_bul)
    params["rmse"] = math.sqrt(
        sum((row["v_obs"] - model) ** 2 for row, model in zip(rows, predicted)) / len(rows))
    params["chi2"] = best[1]
    params["n_parameters"] = len(names)
    params["chi2_nu"] = best[1] / (len(rows) - len(names))
    params["aic"] = aic(best[1], len(names))
    params["bic"] = bic(best[1], len(names), len(rows))
    return params


def fit_sdf(rows, ups_disk: float = DEFAULT_UPSILON_DISK, free_transition: bool = False,
            free_upsilon: bool = False) -> Dict[str, float]:
    """SDF closure. ``free_transition`` adds R0 and Delta R; ``free_upsilon`` adds M/L."""
    free: List[str] = ["v_inf"]
    if free_transition:
        free += ["r0", "dr"]
    if free_upsilon:
        free.append("ups_disk")
    if free_upsilon and free_transition:
        # canonical all-four fit keeps v_inf, R0, DeltaR and Upsilon free
        pass
    return fit_model(rows, "sdf", ups_disk, free)


def fit_nfw(rows, ups_disk: float = DEFAULT_UPSILON_DISK, free_upsilon: bool = False) -> Dict[str, float]:
    """NFW halo plus the same baryons; p = 2, or 3 when Upsilon is also fitted."""
    free: List[str] = ["log_rho_s", "log_r_s"]
    if free_upsilon:
        free.append("ups_disk")
    return fit_model(rows, "nfw", ups_disk, free)


def fit_mond(rows, ups_disk: float = DEFAULT_UPSILON_DISK, interpolation: str = "simple",
             free_a0: bool = False, free_upsilon: bool = False) -> Dict[str, float]:
    """MOND with fixed a0 (p = 0) or a fitted a0 (p = 1), optionally with free M/L."""
    free: List[str] = []
    if free_a0:
        free.append("log_a0")
    if free_upsilon:
        free.append("ups_disk")
    return fit_model(rows, f"mond_{interpolation}", ups_disk, free)
