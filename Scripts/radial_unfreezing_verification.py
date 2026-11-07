#!/usr/bin/env python3
"""Radial-unfreezing verification for the SDF-Lattice NGC 6503 project.

CANONICAL DEFINITION
--------------------
``v_inf`` is the *total* asymptotic circular speed, v_obs(r -> infinity). It is
an observable of the galaxy, not an additive excess term. The foam supplies
only the deficit between the baryonic curve and that total, gated by zeta(r):

    v_model^2(r) = v_bar^2(r) + [ v_inf^2 - v_bar^2(r) ] * zeta(r)
    zeta(r)      = 1/2 * [ 1 + tanh( (r - R0) / DeltaR ) ]

Limits are correct by construction: r -> 0 gives v -> v_bar and r -> infinity
gives v -> v_inf exactly, with no overshoot. The superseded closure
``v_bar^2 + v_inf^2 * zeta`` treated v_inf as an additive component, overshot
the observed outer curve by up to ~33 km/s, and is retained only as
``legacy_model_velocity`` so the regression test can assert it stays rejected.

DATA
----
``data/NGC6503_rotmod.dat`` is the verbatim SPARC mass-model file (Lelli,
McGaugh & Schombert 2016, AJ 152, 157): 31 radial bins, 0.76-23.50 kpc, at an
adopted distance of 6.26 Mpc. See ``data/PROVENANCE.md`` for the two
byte-identical sources used to retrieve it and for its MD5.

DISTANCE
--------
6.26 Mpc is the distance the table was built for and the canonical choice here.
``--distance-mpc`` rescales the table before fitting (r ~ D, mass-model
components ~ sqrt(D), V_obs and its errors unchanged) so an alternative distance
can be tested. Rescaling to 5.27 Mpc moves the adopted-parameter statistic from
chi2_nu = 1.320 to 1.243, i.e. across the project's < 1.25 threshold; that
sensitivity is asserted in --self-test and must be quoted with the verdict.

Baryonic speed follows the SPARC convention

    v_bar^2 = Vgas*|Vgas| + Upsilon_disk * Vdisk^2 + Upsilon_bul * Vbul^2

where ``Vdisk`` and ``Vbul`` are normalised to Upsilon = 1.

Standard-library only: the least-squares fit uses a bounded Nelder-Mead
implementation below, so no numpy/scipy is required.
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path
from typing import Sequence

KPC_TO_M = 3.0857e19
R0_KPC = 1.83
DELTA_R_KPC = 0.46
V_INF_KMS = 116.2
V_INF_ERR_KMS = 2.4
UPSILON_DISK = 0.62
UPSILON_BUL = 0.0

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ROTMOD = DATA_DIR / "NGC6503_rotmod.dat"

# Retracted manuscript benchmarks, kept for the regression test only.
REPORTED_CHI2_NU = 0.942
REPORTED_OUTER_SLOPE = -0.018

# Reproduced from data/NGC6503_rotmod.dat in this release.
REPRODUCED_CHI2_ADOPTED = 39.607430     # Upsilon=0.62, R0=1.83, dR=0.46, v_inf=116.2, p=1
REPRODUCED_CHINU_ADOPTED = 1.320248
REPRODUCED_CHI2_FIT = 33.325790         # Upsilon=0.5 fixed, v_inf/R0/dR free, p=3
REPRODUCED_CHINU_FIT = 1.190207
# Same closure on the table rescaled to 5.27 Mpc (sensitivity check only).
REPRODUCED_CHI2_AT_527 = 37.298976     # adopted params, table rescaled 6.26 -> 5.27 Mpc
REPRODUCED_CHINU_AT_527 = 1.243299
FIT_V_INF = 116.2656
FIT_R0 = 1.5832
FIT_DR = 1.0362

# Distance the SPARC file itself was built for, and the alternative checked in
# the sensitivity test below (the value the manuscript used to quote).
FILE_DISTANCE_MPC = 6.26
ALT_DISTANCE_MPC = 5.27


# --------------------------------------------------------------------------- #
# Canonical kernel and closure
# --------------------------------------------------------------------------- #
def zeta(r_kpc: float, r0: float = R0_KPC, dr: float = DELTA_R_KPC) -> float:
    """Canonical smooth unfreezing activation, dimensionless in (0, 1)."""
    if r_kpc < 0:
        raise ValueError("radius must be non-negative")
    if dr <= 0:
        raise ValueError("transition width must be positive")
    return 0.5 * (1.0 + math.tanh((r_kpc - r0) / dr))


def baryonic_squared(v_gas: float, v_disk: float, v_bul: float,
                     ups_disk: float = UPSILON_DISK, ups_bul: float = UPSILON_BUL) -> float:
    """SPARC baryonic speed squared; the gas term keeps its sign."""
    if ups_disk < 0 or ups_bul < 0:
        raise ValueError("mass-to-light ratios must be non-negative")
    return v_gas * abs(v_gas) + ups_disk * v_disk * v_disk + ups_bul * v_bul * v_bul


def model_velocity(r_kpc: float, v_bar_kms: float, v_inf_kms: float = V_INF_KMS,
                   r0: float = R0_KPC, dr: float = DELTA_R_KPC) -> float:
    """Canonical closure: v^2 = v_bar^2 + (v_inf^2 - v_bar^2) * zeta(r)."""
    if r_kpc <= 0:
        raise ValueError("radius must be positive")
    if v_bar_kms < 0:
        raise ValueError("baryonic speed must be non-negative")
    excess = max(0.0, v_inf_kms * v_inf_kms - v_bar_kms * v_bar_kms)
    return math.sqrt(max(v_bar_kms * v_bar_kms + excess * zeta(r_kpc, r0, dr), 1e-12))


def legacy_model_velocity(r_kpc: float, v_bar_kms: float, v_inf_kms: float = V_INF_KMS) -> float:
    """RETRACTED additive closure, kept only for the regression test."""
    if r_kpc <= 0:
        raise ValueError("radius must be positive")
    if v_bar_kms < 0:
        raise ValueError("baryonic speed must be non-negative")
    return math.sqrt(v_bar_kms * v_bar_kms + v_inf_kms * v_inf_kms * zeta(r_kpc))


def sparc_model(r_kpc: float, row: dict, ups_disk: float, ups_bul: float,
                v_inf: float, r0: float, dr: float) -> float:
    """Model speed for one SPARC row."""
    b2 = max(baryonic_squared(row["v_gas"], row["v_disk"], row["v_bul"], ups_disk, ups_bul), 0.0)
    excess = max(0.0, v_inf * v_inf - b2)
    return math.sqrt(max(b2 + excess * zeta(r_kpc, r0, dr), 1e-12))


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #
def chi_squared(observed: Sequence[float], predicted: Sequence[float],
                sigma: Sequence[float], n_parameters: int = 0):
    n = len(observed)
    if n == 0 or len(predicted) != n or len(sigma) != n:
        raise ValueError("arrays must have equal nonzero length")
    dof = n - n_parameters
    if dof <= 0:
        raise ValueError("degrees of freedom N-p must be positive")
    if any(not math.isfinite(x) for arr in (observed, predicted, sigma) for x in arr):
        raise ValueError("non-finite input")
    if any(s <= 0 for s in sigma):
        raise ValueError("all uncertainties must be positive")
    chi = sum(((o - m) / s) ** 2 for o, m, s in zip(observed, predicted, sigma))
    return chi, dof


def reduced_chi_squared(observed, predicted, sigma, n_parameters=0) -> float:
    chi, dof = chi_squared(observed, predicted, sigma, n_parameters)
    return chi / dof


def linear_slope(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("slope requires >=2 paired points")
    xm = sum(x) / len(x)
    ym = sum(y) / len(y)
    den = sum((a - xm) ** 2 for a in x)
    if den == 0:
        raise ValueError("radii must not all be identical")
    return sum((a - xm) * (b - ym) for a, b in zip(x, y)) / den


# --------------------------------------------------------------------------- #
# Bounded Nelder-Mead (no third-party dependency)
# --------------------------------------------------------------------------- #
def nelder_mead(f, x0, steps, lo, hi, tol=1e-12, max_iter=4000):
    """Minimise f on a box. Returns (x_best, f_best)."""

    def bounded(p):
        return [min(max(v, l), h) for v, l, h in zip(p, lo, hi)]

    n = len(x0)
    pts = [bounded(list(x0))]
    for i in range(n):
        p = list(pts[0])
        p[i] = min(max(p[i] + steps[i], lo[i]), hi[i])
        if p[i] == pts[0][i]:
            p[i] = min(max(p[i] - steps[i], lo[i]), hi[i])
        pts.append(p)
    vals = [f(p) for p in pts]

    for _ in range(max_iter):
        order = sorted(range(n + 1), key=lambda k: vals[k])
        pts = [pts[k] for k in order]
        vals = [vals[k] for k in order]
        if abs(vals[-1] - vals[0]) <= tol * (abs(vals[0]) + tol):
            break
        centroid = [sum(pts[k][i] for k in range(n)) / n for i in range(n)]
        worst = pts[-1]
        xr = bounded([centroid[i] + (centroid[i] - worst[i]) for i in range(n)])
        fr = f(xr)
        if fr < vals[0]:
            xe = bounded([centroid[i] + 2.0 * (centroid[i] - worst[i]) for i in range(n)])
            fe = f(xe)
            if fe < fr:
                pts[-1], vals[-1] = xe, fe
            else:
                pts[-1], vals[-1] = xr, fr
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = bounded([centroid[i] + 0.5 * (worst[i] - centroid[i]) for i in range(n)])
            fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                for k in range(1, n + 1):
                    pts[k] = bounded([pts[0][i] + 0.5 * (pts[k][i] - pts[0][i]) for i in range(n)])
                    vals[k] = f(pts[k])

    best = min(range(n + 1), key=lambda k: vals[k])
    return pts[best], vals[best]


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def load_rotmod(path: Path):
    """Parse a SPARC Rotmod_LTG file. Returns (rows, distance_mpc)."""
    rows, distance = [], None
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                if "Distance" in s and "=" in s:
                    try:
                        distance = float(s.split("=")[1].split()[0])
                    except (IndexError, ValueError):
                        pass
                continue
            c = s.split()
            if len(c) < 6:
                continue
            try:
                vals = [float(x) for x in c[:8]]
            except ValueError:
                continue
            while len(vals) < 8:
                vals.append(0.0)
            rows.append({"r": vals[0], "v_obs": vals[1], "err": vals[2], "v_gas": vals[3],
                         "v_disk": vals[4], "v_bul": vals[5], "sb_disk": vals[6], "sb_bul": vals[7]})
    if not rows:
        raise ValueError(f"no data rows parsed from {path}")
    return rows, distance


def rescale_to_distance(rows, target_mpc: float, file_mpc: float):
    """Rescale a SPARC table from its own adopted distance to ``target_mpc``.

    A SPARC mass model is built at one distance: radii are angular sizes and the
    tabulated gas/disk/bulge velocities are mass-model predictions. For a target
    distance D' against the file's D:

        r'       = r * (D'/D)                  angular size
        V_comp'  = V_comp * sqrt(D'/D)         V^2 = G M(<r)/r, M ~ D^2, r ~ D
        V_obs    unchanged                     a measured velocity
        sigma    unchanged                     measurement error

    Rescaling is offered so that an alternative distance can be tested; the
    canonical release fits the table at its own distance (see ``--distance-mpc``).
    """
    if target_mpc <= 0 or file_mpc <= 0:
        raise ValueError("distances must be strictly positive")
    ratio = target_mpc / file_mpc
    scale_v = math.sqrt(ratio)
    out = []
    for x in rows:
        y = dict(x)
        y["r"] = x["r"] * ratio
        for key in ("v_gas", "v_disk", "v_bul"):
            y[key] = x[key] * scale_v
        out.append(y)
    return out


def load_csv(path: Path):
    """Legacy CSV schema: r_kpc,v_obs_kms,v_bar_kms,sigma_kms."""
    required = {"r_kpc", "v_obs_kms", "v_bar_kms", "sigma_kms"}
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must include: " + ", ".join(sorted(required)))
        rows = [{k: float(row[k]) for k in required} for row in reader]
    if not rows:
        raise ValueError("CSV contains no data rows")
    return rows


def export_csv(path: Path, rows):
    """Write the tidy named-column copy of the rotmod table."""
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["r_kpc", "v_obs_kms", "err_v_kms", "v_gas_kms", "v_disk_kms",
                    "v_bul_kms", "sb_disk_lsun_pc2", "sb_bul_lsun_pc2"])
        for x in rows:
            w.writerow([x["r"], x["v_obs"], x["err"], x["v_gas"], x["v_disk"],
                        x["v_bul"], x["sb_disk"], x["sb_bul"]])


# --------------------------------------------------------------------------- #
# Fitting
# --------------------------------------------------------------------------- #
def _sparc_chi2(rows, ups_disk, ups_bul, v_inf, r0, dr):
    total = 0.0
    for x in rows:
        m = sparc_model(x["r"], x, ups_disk, ups_bul, v_inf, r0, dr)
        total += ((x["v_obs"] - m) / x["err"]) ** 2
    return total


def fit_sparc(rows, ups_disk_fixed=None, free=("v_inf", "r0", "dr")):
    """Bounded least squares over a subset of {ups_disk, v_inf, r0, dr}."""
    names = list(free)
    lo = {"ups_disk": 0.01, "v_inf": 80.0, "r0": 0.05, "dr": 0.05}
    hi = {"ups_disk": 2.0, "v_inf": 200.0, "r0": 12.0, "dr": 6.0}
    start = {"ups_disk": 0.5, "v_inf": 116.2, "r0": 1.83, "dr": 0.46}
    step = {"ups_disk": 0.2, "v_inf": 2.0, "r0": 0.3, "dr": 0.2}

    def unpack(x):
        p = dict(start)
        p.update(dict(zip(names, x)))
        if ups_disk_fixed is not None:
            p["ups_disk"] = ups_disk_fixed
        return p

    def objective(x):
        p = unpack(x)
        if p["dr"] <= 0:
            return float("inf")
        return _sparc_chi2(rows, p["ups_disk"], UPSILON_BUL, p["v_inf"], p["r0"], p["dr"])

    best = None
    for seed in (start, {"ups_disk": 0.6, "v_inf": 110.0, "r0": 1.0, "dr": 1.2},
                 {"ups_disk": 0.4, "v_inf": 125.0, "r0": 3.0, "dr": 0.3}):
        x0 = [seed[n] for n in names]
        x, fx = nelder_mead(objective, x0, [step[n] for n in names],
                            [lo[n] for n in names], [hi[n] for n in names])
        if best is None or fx < best[1]:
            best = (x, fx)
    p = unpack(best[0])
    p["chi2"] = best[1]
    p["chi2_nu"] = best[1] / (len(rows) - len(names))
    p["n_parameters"] = len(names)
    return p


# --------------------------------------------------------------------------- #
# Self test
# --------------------------------------------------------------------------- #
def self_test():
    assert abs(KPC_TO_M - 3.0857e19) < 1e5

    # Activation kernel.
    assert zeta(0.0) < 1e-3
    assert abs(zeta(R0_KPC) - 0.5) < 1e-15
    assert all(1.0 - zeta(r) < 1e-6 for r in (6.0, 8.2, 11.48, 15.58))
    assert all(zeta(a) < zeta(b) for a, b in zip([x / 4 for x in range(0, 24)],
                                                 [x / 4 for x in range(1, 25)]))

    # DEFINITION TEST: canonical limits, and the legacy additive form rejected.
    v_bar = 35.8
    assert abs(model_velocity(2000.0, v_bar) - V_INF_KMS) < 1e-9
    core = model_velocity(1e-9, v_bar)
    assert core > v_bar and (core - v_bar) / v_bar < 5e-3
    assert legacy_model_velocity(2000.0, v_bar) > V_INF_KMS + 3.0
    assert all(model_velocity(r, v_bar) <= V_INF_KMS + 1e-9 for r in (1, 3, 5, 8, 15, 30))

    # DATA TEST: the bundled file must be the real SPARC table.
    assert ROTMOD.exists(), f"missing {ROTMOD}"
    rows, distance = load_rotmod(ROTMOD)
    assert len(rows) == 31, len(rows)
    assert abs(distance - 6.26) < 1e-9, distance
    assert abs(rows[0]["r"] - 0.76) < 1e-9 and abs(rows[0]["v_obs"] - 77.0) < 1e-9
    assert abs(rows[-1]["r"] - 23.50) < 1e-9 and abs(rows[-1]["v_obs"] - 115.0) < 1e-9
    assert all(x["err"] > 0 for x in rows)

    # DISTANCE TEST: rescaling to the file's own distance is the identity, and
    # the 5.27 Mpc alternative reproduces the recorded sensitivity numbers.
    same = rescale_to_distance(rows, FILE_DISTANCE_MPC, FILE_DISTANCE_MPC)
    assert all(abs(a["r"] - b["r"]) < 1e-12 and abs(a["v_gas"] - b["v_gas"]) < 1e-12
               for a, b in zip(same, rows))
    alt = rescale_to_distance(rows, ALT_DISTANCE_MPC, FILE_DISTANCE_MPC)
    ratio = ALT_DISTANCE_MPC / FILE_DISTANCE_MPC
    assert abs(alt[-1]["r"] - rows[-1]["r"] * ratio) < 1e-12
    assert abs(alt[-1]["v_disk"] - rows[-1]["v_disk"] * math.sqrt(ratio)) < 1e-12
    assert alt[-1]["v_obs"] == rows[-1]["v_obs"]
    alt_pred = [sparc_model(x["r"], x, UPSILON_DISK, UPSILON_BUL, V_INF_KMS, R0_KPC, DELTA_R_KPC)
                for x in alt]
    alt_chi, _ = chi_squared([x["v_obs"] for x in alt], alt_pred, [x["err"] for x in alt], 1)
    assert abs(alt_chi - REPRODUCED_CHI2_AT_527) < 5e-3, alt_chi
    assert abs(alt_chi / 30.0 - REPRODUCED_CHINU_AT_527) < 1e-4
    # The headline verdict is distance-sensitive and must be reported as such:
    # 6.26 Mpc fails the < 1.25 target, 5.27 Mpc squeaks past it.
    assert alt_chi / 30.0 < 1.25 < REPRODUCED_CHINU_ADOPTED

    # REPRODUCTION TEST (adopted parameters, deterministic, no optimiser).
    pred = [sparc_model(x["r"], x, UPSILON_DISK, UPSILON_BUL, V_INF_KMS, R0_KPC, DELTA_R_KPC)
            for x in rows]
    chi, _ = chi_squared([x["v_obs"] for x in rows], pred, [x["err"] for x in rows], 1)
    assert abs(chi - REPRODUCED_CHI2_ADOPTED) < 5e-3, chi
    assert abs(chi / 30.0 - REPRODUCED_CHINU_ADOPTED) < 1e-4

    # The retracted values must not be reproducible from real data either.
    assert abs(chi / 30.0 - REPORTED_CHI2_NU) > 0.2
    outer = [(x["r"], p) for x, p in zip(rows, pred) if x["r"] >= 8.0]
    slope = linear_slope([q[0] for q in outer], [q[1] for q in outer])
    assert abs(slope) < 1e-4, slope
    assert abs(slope - REPORTED_OUTER_SLOPE) > 1e-3

    # FIT TEST: the optimiser must reach the published optimum or better.
    best = fit_sparc(rows, ups_disk_fixed=0.5)
    assert best["chi2"] <= REPRODUCED_CHI2_FIT + 0.5, best["chi2"]
    assert abs(best["v_inf"] - FIT_V_INF) < 0.5, best["v_inf"]
    assert abs(best["r0"] - FIT_R0) < 0.1, best["r0"]
    assert abs(best["dr"] - FIT_DR) < 0.1, best["dr"]

    # Statistics helpers.
    assert abs(reduced_chi_squared([2.0], [0.0], [1.0], 0) - 4.0) < 1e-12
    xs = [10.0, 15.0, 20.0]
    ys = [120.0 + REPORTED_OUTER_SLOPE * x for x in xs]
    assert abs(linear_slope(xs, ys) - REPORTED_OUTER_SLOPE) < 1e-12

    return {
        "status": "PASS",
        "checks": [
            "kpc conversion",
            "activation kernel limits, midpoint, monotonicity, saturation",
            "v_inf is the TOTAL asymptote (legacy additive form rejected)",
            "no overshoot above v_inf",
            "bundled data is the 31-row SPARC table at 6.26 Mpc",
            "chi2 recomputed from data/NGC6503_rotmod.dat",
            "retracted chi2_nu=0.942 is not reproducible",
            "retracted outer slope is unreachable (model exactly flat)",
            "Nelder-Mead reaches the published optimum",
            "chi-square and OLS-slope identities",
        ],
        "reproduced": {
            "adopted": {"chi2": REPRODUCED_CHI2_ADOPTED, "chi2_nu": REPRODUCED_CHINU_ADOPTED,
                        "n_parameters": 1, "n_points": 31,
                        "params": {"Upsilon_disk": UPSILON_DISK, "v_inf_kms": V_INF_KMS,
                                   "R0_kpc": R0_KPC, "DeltaR_kpc": DELTA_R_KPC}},
            "fitted": {"chi2": round(best["chi2"], 6), "chi2_nu": round(best["chi2_nu"], 6),
                       "n_parameters": 3,
                       "params": {"Upsilon_disk": 0.5, "v_inf_kms": round(best["v_inf"], 4),
                                  "R0_kpc": round(best["r0"], 4), "DeltaR_kpc": round(best["dr"], 4)}},
        },
        "note": "Computed from the real 31-bin SPARC rotation curve (Lelli et al. 2016).",
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sparc", type=Path, default=ROTMOD,
                    help="SPARC rotmod file (default: data/NGC6503_rotmod.dat)")
    ap.add_argument("--input", type=Path, help="legacy CSV: r_kpc,v_obs_kms,v_bar_kms,sigma_kms")
    ap.add_argument("--n-parameters", type=int, default=1,
                    help="parameters estimated from these points (default 1: v_inf)")
    ap.add_argument("--outer-min-kpc", type=float, default=8.0)
    ap.add_argument("--v-inf", type=float, default=V_INF_KMS)
    ap.add_argument("--upsilon", type=float, default=UPSILON_DISK, help="stellar disk M/L")
    ap.add_argument("--R0", type=float, default=R0_KPC, dest="r0")
    ap.add_argument("--DeltaR", type=float, default=DELTA_R_KPC, dest="dr")
    ap.add_argument("--distance-mpc", type=float,
                    help=("rescale the table to this distance before fitting "
                          "(r ~ D, mass-model components ~ sqrt(D); V_obs unchanged). "
                          "Default: use the table's own distance, 6.26 Mpc."))
    ap.add_argument("--fit", action="store_true", help="fit the closure to the SPARC table")
    ap.add_argument("--export-csv", type=Path, help="write a tidy named-column CSV of the table")
    ap.add_argument("--output-json", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    def load_table():
        """Load the SPARC table, optionally rescaled to --distance-mpc."""
        rows, distance = load_rotmod(args.sparc)
        if args.distance_mpc is None:
            return rows, distance
        return rescale_to_distance(rows, args.distance_mpc, distance), args.distance_mpc

    if args.self_test:
        result = self_test()
    elif args.export_csv:
        rows, distance = load_rotmod(args.sparc)
        export_csv(args.export_csv, rows)
        result = {"status": "EXPORTED", "path": str(args.export_csv),
                  "rows": len(rows), "distance_mpc": distance}
    elif args.fit:
        rows, distance = load_table()
        adopted = _sparc_chi2(rows, args.upsilon, UPSILON_BUL, args.v_inf, args.r0, args.dr)
        ladder = [{
            "model": "adopted parameters (Upsilon as given, v_inf/R0/DeltaR as given)",
            "n_parameters": 1,
            "params": {"Upsilon_disk": args.upsilon, "v_inf_kms": args.v_inf,
                       "R0_kpc": args.r0, "DeltaR_kpc": args.dr},
            "chi2": round(adopted, 6), "chi2_nu": round(adopted / (len(rows) - 1), 6),
        }]
        for ups_fixed, free, label in (
            (0.5, ("v_inf", "r0", "dr"), "Upsilon_disk=0.5 fixed; v_inf, R0, DeltaR free"),
            (None, ("ups_disk", "v_inf", "r0", "dr"), "all four free"),
        ):
            f = fit_sparc(rows, ups_disk_fixed=ups_fixed, free=free)
            entry = {"model": label, "n_parameters": f["n_parameters"],
                     "params": {"Upsilon_disk": round(f["ups_disk"], 4),
                                "v_inf_kms": round(f["v_inf"], 4),
                                "R0_kpc": round(f["r0"], 4),
                                "DeltaR_kpc": round(f["dr"], 4)},
                     "chi2": round(f["chi2"], 6), "chi2_nu": round(f["chi2_nu"], 6)}
            if ups_fixed is None and f["ups_disk"] < 0.15:
                entry["warning"] = ("Upsilon_disk runs to its lower bound: the fit suppresses the "
                                    "stellar disk entirely, so this is not a baryon-driven model")
            ladder.append(entry)
        result = {"table": str(args.sparc), "distance_mpc": distance, "n_points": len(rows),
                  "ladder": ladder,
                  "retracted": {"chi2_nu": REPORTED_CHI2_NU,
                                "outer_slope": REPORTED_OUTER_SLOPE,
                                "status": "not reproducible from the canonical closure"}}
    elif args.input:
        rows = load_csv(args.input)
        obs = [x["v_obs_kms"] for x in rows]
        sig = [x["sigma_kms"] for x in rows]
        pred = [model_velocity(x["r_kpc"], x["v_bar_kms"], args.v_inf, args.r0, args.dr) for x in rows]
        chi, dof = chi_squared(obs, pred, sig, args.n_parameters)
        outer = [(x["r_kpc"], p) for x, p in zip(rows, pred) if x["r_kpc"] >= args.outer_min_kpc]
        result = {"n_points": len(rows), "n_parameters": args.n_parameters, "dof": dof,
                  "chi2": chi, "chi2_nu": chi / dof,
                  "outer_model_slope_kms_per_kpc":
                      linear_slope([q[0] for q in outer], [q[1] for q in outer])
                      if len(outer) >= 2 else None,
                  "outer_min_kpc": args.outer_min_kpc,
                  "model": "sqrt(v_bar^2 + (v_inf^2 - v_bar^2)*zeta(r))"}
    else:
        rows, distance = load_table()
        pred = [sparc_model(x["r"], x, args.upsilon, UPSILON_BUL, args.v_inf, args.r0, args.dr)
                for x in rows]
        chi, dof = chi_squared([x["v_obs"] for x in rows], pred, [x["err"] for x in rows],
                               args.n_parameters)
        result = {
            "status": "READY",
            "table": str(args.sparc), "distance_mpc": distance, "n_points": len(rows),
            "canonical_closure": "v_model^2 = v_bar^2 + (v_inf^2 - v_bar^2)*zeta(r)",
            "v_inf_definition": "TOTAL asymptotic circular speed, v_obs(r -> infinity)",
            "chi2": chi, "chi2_nu": chi / dof, "n_parameters": args.n_parameters, "dof": dof,
            "parameters": {"Upsilon_disk": args.upsilon, "v_inf_kms": args.v_inf,
                           "R0_kpc": args.r0, "DeltaR_kpc": args.dr},
            "retracted": {"chi2_nu": REPORTED_CHI2_NU, "outer_slope": REPORTED_OUTER_SLOPE},
        }

    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.output_json:
        args.output_json.write_text(text + "\n", encoding="utf8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
