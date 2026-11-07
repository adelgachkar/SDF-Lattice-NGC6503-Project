#!/usr/bin/env python3
"""Same-conditions comparison: SDF closure vs NFW halo vs MOND on NGC 6503.

Every model is fitted to the *same* 31-bin SPARC table, at the same distance
(6.26 Mpc), with the same baryonic decomposition, the same stellar mass-to-light
ratio policy, the same 1-sigma errors and the same definition of p:

    p = the number of parameters fitted to these same 31 points.

That definition makes the comparison honest in the one place earlier revisions
were not: ``v_inf`` is taken from the galaxy being modelled, so it counts, and
the NFW halo normalisation counts for exactly the same reason. MOND with a fixed
``a0`` and a fixed ``Upsilon`` has p = 0 - it is a genuine prediction.

Models
------
sdf    v^2 = v_bar^2 + (v_inf^2 - v_bar^2) * zeta(r),  zeta = 1/2[1+tanh((r-R0)/dR)]
nfw    v^2 = v_bar^2 + v_nfw^2(r),                      v_nfw from (rho_s, r_s)
mond   v^2 = v_bar^2 * nu(g_bar/a0),                     simple and standard nu

Usage
-----
    python Scripts/model_comparison.py                # JSON to stdout
    python Scripts/model_comparison.py --markdown     # print the report
    python Scripts/model_comparison.py --write        # rewrite MODEL_COMPARISON.md
    python Scripts/model_comparison.py --self-test    # assert the pinned numbers
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sdf_lattice import physics as P  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ROTMOD = ROOT / "data" / "NGC6503_rotmod.dat"
REPORT = ROOT / "MODEL_COMPARISON.md"

# Pinned from the fits below; --self-test fails if they drift.
PINNED = {
    "sdf_ups062_p1": 39.607277,
    "nfw_p2": 116.405493,
    "nfw_p3": 40.258636,
    "mond_standard_p0": 122.341642,
    "mond_standard_p1": 100.121575,
    "mond_standard_p2": 99.770346,
    "mond_simple_p0": 812.989349,
    "mond_simple_p2": 82.598477,
}


def build_rows(rows):
    """Fit every model and return the comparison rows."""
    out = []

    # --- Upsilon fixed at the release default ---------------------------------
    sdf = P.fit_sdf(rows, 0.62)
    out.append({"model": "SDF closure (v_inf)", "family": "sdf", "ups_policy": "0.62 fixed",
                "p": sdf["n_parameters"], "fit": sdf})
    sdf3 = P.fit_sdf(rows, 0.62, True)
    out.append({"model": "SDF closure (v_inf, R0, dR)", "family": "sdf", "ups_policy": "0.62 fixed",
                "p": sdf3["n_parameters"], "fit": sdf3,
                "warning": "Delta R runs to its lower bound: the transition degenerates to a step"})
    nfw2 = P.fit_nfw(rows, 0.62)
    out.append({"model": "NFW halo (rho_s, r_s)", "family": "nfw", "ups_policy": "0.62 fixed",
                "p": nfw2["n_parameters"], "fit": nfw2})
    for interp, label in (("simple", "MOND simple mu, a0 fixed"),
                          ("standard", "MOND standard mu, a0 fixed")):
        fit = P.fit_mond(rows, 0.62, interp)
        out.append({"model": label, "family": f"mond_{interp}", "ups_policy": "0.62 fixed",
                    "p": 0, "fit": fit})
    for interp, label in (("simple", "MOND simple mu, a0 free"),
                          ("standard", "MOND standard mu, a0 free")):
        fit = P.fit_mond(rows, 0.62, interp, free_a0=True)
        out.append({"model": label, "family": f"mond_{interp}", "ups_policy": "0.62 fixed",
                    "p": fit["n_parameters"], "fit": fit})

    # --- Upsilon free for every model ----------------------------------------
    sdf4 = P.fit_sdf(rows, 0.62, True, True)
    out.append({"model": "SDF closure (all four free)", "family": "sdf", "ups_policy": "free",
                "p": sdf4["n_parameters"], "fit": sdf4,
                "warning": "Upsilon runs to its lower bound; the stellar disk is switched off"})
    nfw3 = P.fit_nfw(rows, 0.62, True)
    out.append({"model": "NFW halo (rho_s, r_s, Upsilon)", "family": "nfw", "ups_policy": "free",
                "p": nfw3["n_parameters"], "fit": nfw3})
    for interp, label in (("simple", "MOND simple mu (a0, Upsilon free)"),
                          ("standard", "MOND standard mu (a0, Upsilon free)")):
        fit = P.fit_mond(rows, 0.62, interp, free_a0=True, free_upsilon=True)
        out.append({"model": label, "family": f"mond_{interp}", "ups_policy": "free",
                    "p": fit["n_parameters"], "fit": fit})
    return out


def _fitted_names(family, p):
    """Which parameters are actually fitted, given the model family and p."""
    if family == "sdf":
        names = ["v_inf"]
        if p >= 3:
            names += ["r0", "dr"]
        if p == 4:
            names += ["ups_disk"]
        return names
    if family == "nfw":
        return ["rho_s", "r_s"] + (["ups_disk"] if p == 3 else [])
    return (["a0"] if p >= 1 else []) + (["ups_disk"] if p == 2 else [])


def summarise(entry):
    fit = entry["fit"]
    shown = _fitted_names(entry["family"], entry["p"])
    return {
        "model": entry["model"],
        "family": entry["family"],
        "ups_policy": entry["ups_policy"],
        "p": entry["p"],
        "chi2": round(fit["chi2"], 6),
        "rmse": round(fit["rmse"], 6),
        "chi2_nu": round(fit["chi2"] / (31 - entry["p"]), 6),
        "aic": round(fit["aic"], 4),
        "bic": round(fit["bic"], 4),
        "params": {key: round(fit[key], 4) for key in shown},
        "warning": entry.get("warning"),
    }


def markdown(rows, meta):
    lines = []
    lines.append("# Same-conditions comparison: SDF vs NFW vs MOND\n")
    lines.append("Generated by `Scripts/model_comparison.py --write`; do not edit by hand.\n")
    lines.append(f"* Table: `{meta['table']}` — {meta['n_points']} bins, "
                 f"$D={meta['distance_mpc']}$ Mpc\n"
                 f"* Baryons: $v_{{\\rm bar}}^2 = V_{{\\rm gas}}|V_{{\\rm gas}}| + "
                 f"\\Upsilon_{{\\rm disk}}V_{{\\rm disk}}^2$, $\\Upsilon_{{\\rm bul}}=0$\n"
                 "* Errors: the SPARC `e_Vobs` column, unchanged\n"
                 "* RMSE is the unweighted RMS of $V_{\\rm obs}-v_{\\rm model}$; $\\chi^2$ uses "
                 "`e_Vobs` given above\n"
                 "* $p$: parameters fitted to these same points, so $v_\\infty$ and the "
                 "NFW halo normalisation both count\n"
                 "* $\\chi^2_\\nu = \\chi^2/(N-p)$, AIC $=\\chi^2+2p$, BIC $=\\chi^2+p\\ln N$\n")

    for policy, title in (("0.62 fixed", "Stellar M/L fixed at 0.62 for every model"),
                          ("free", "Stellar M/L free for every model")):
        lines.append(f"\n## {title}\n")
        lines.append("| Model | p | RMSE (km/s) | $\\chi^2$ | $\\chi^2_\\nu$ | AIC | $\\Delta$AIC | BIC | Fitted parameters |")
        lines.append("| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |")
        subset = [r for r in rows if r["ups_policy"] == policy]
        best = min(r["aic"] for r in subset)
        for row in subset:
            row["delta_aic"] = row["aic"] - best
        for row in sorted(subset, key=lambda r: r["aic"]):
            params = ", ".join(f"{k}={v:g}" for k, v in row["params"].items()) or "none (prediction)"
            flag = " ⚠️" if row["warning"] else ""
            lines.append(f"| {row['model']}{flag} | {row['p']} | {row['rmse']:.3f} | {row['chi2']:.3f} | "
                         f"{row['chi2_nu']:.3f} | {row['aic']:.2f} | {row['delta_aic']:.2f} | "
                         f"{row['bic']:.2f} | {params} |")
        lines.append("")
        for row in sorted(subset, key=lambda r: r["aic"]):
            if row.get("warning"):
                lines.append(f"* **{row['model']}** — {row['warning']}.")
        lines.append("")

    by_name = {r["model"]: r for r in rows}
    sdf1 = by_name["SDF closure (v_inf)"]
    mond1 = by_name["MOND standard mu, a0 free"]
    sdf3 = by_name["SDF closure (v_inf, R0, dR)"]
    nfw2 = by_name["NFW halo (rho_s, r_s)"]
    nfw3 = by_name["NFW halo (rho_s, r_s, Upsilon)"]
    sdf4 = by_name["SDF closure (all four free)"]

    lines.append("\n## Equal-parameter comparisons\n")
    lines.append("| Pair | $p$ | $\\Delta\\chi^2$ | $\\Delta$AIC | Reading |")
    lines.append("| :--- | :---: | ---: | ---: | :--- |")
    lines.append(f"| SDF vs MOND (standard $\\mu$, $a_0$ free) | 1 | "
                 f"{mond1['chi2'] - sdf1['chi2']:.2f} | {mond1['aic'] - sdf1['aic']:.2f} | "
                 f"SDF preferred |")
    lines.append(f"| SDF (R0, $\\Delta R$ free) vs NFW (2 halo params) | 3 | "
                 f"{nfw3['chi2'] - sdf3['chi2']:.2f} | {nfw3['aic'] - sdf3['aic']:.2f} | "
                 f"SDF preferred, but NFW keeps $\\Upsilon$ free here |")
    lines.append(f"| SDF (all four free) vs NFW (2 halo params) | 4 vs 3 | "
                 f"{nfw3['chi2'] - sdf4['chi2']:.2f} | {nfw3['aic'] - sdf4['aic']:.2f} | "
                 f"SDF preferred even with one more parameter |")
    lines.append(f"| SDF (all four free) vs MOND (a0, $\\Upsilon$ free) | 4 vs 2 | "
                 f"{by_name['MOND standard mu (a0, Upsilon free)']['chi2'] - sdf4['chi2']:.2f} | "
                 f"{by_name['MOND standard mu (a0, Upsilon free)']['aic'] - sdf4['aic']:.2f} | "
                 f"SDF preferred |")
    lines.append("")

    lines.append("\n## What this does and does not establish\n")
    lines.append(
        "* On this galaxy and this table, and under identical treatment, the "
        "$\\zeta(r)$ closure reaches a lower $\\chi^2$ than an NFW halo and than MOND "
        "at equal or fewer parameters. The earlier comparison, which gave MOND "
        "$\\chi^2_\\nu = 20.545$, is **withdrawn**: it fitted six QVEX parameters "
        "against a MOND model with no fitted $\\Upsilon$ at all.\n"
        "* MOND is not tuned here: with $a_0$ and $\\Upsilon$ fixed it has $p=0$ and "
        "still describes the curve to a few km/s. Its $\\chi^2$ is large because the "
        "SPARC errors fall to 1 km/s in the outer disk (8-13 kpc), where the "
        "standard-$\\mu$ prediction sits about 2.5 km/s low. That is a real tension "
        "for this data set, not a fitting failure.\n"
        "* One galaxy is one galaxy. NGC 6503 has a markedly declining inner "
        "$V_{\\rm disk}$ and a steep $2.28$ kpc point; the ranking may not survive a "
        "175-galaxy sample.\n"
        "* All values are point estimates from a deterministic Nelder-Mead search; no "
        "posterior, no error bars on $\\Delta$AIC, and no evidence-ratio interpretation "
        "beyond the usual rule of thumb ($\\Delta$AIC > 10 = strong).\n"
        "* Two SDF rows sit on a parameter bound ($\\Delta R$ at 0.05 kpc; "
        "$\\Upsilon_{\\rm disk}$ at 0.01). A bound is a limit, not a measurement: the "
        "step-function row and the disk-off row should be read as statements about what "
        "the data will tolerate, not as evidence for a transition or for the baryons "
        "being irrelevant.\n"
        "* The manuscript's own target statistic is still the adopted-parameter row, "
        "$\\chi^2_\\nu = 1.320$ at $p=1$ (collected together with $\\Upsilon=0.62$, "
        "$R_0=1.83$, $\\Delta R=0.46$, $v_\\infty=116.2$). The 1.198 row above is a "
        "different fit at the same $\\Upsilon$ and does not replace it.\n"
        "* NFW is one halo shape, not 'dark matter'; cored profiles (Burkert, "
        "pseudo-isothermal) are not fitted here.\n")
    return "\n".join(lines) + "\n"


def self_test():
    rows, distance = P.load_rotmod(ROTMOD)
    assert len(rows) == 31 and abs(distance - 6.26) < 1e-9

    sdf = P.fit_sdf(rows, 0.62)
    assert abs(sdf["chi2"] - PINNED["sdf_ups062_p1"]) < 5e-3, sdf["chi2"]
    nfw2 = P.fit_nfw(rows, 0.62)
    assert abs(nfw2["chi2"] - PINNED["nfw_p2"]) < 5e-3, nfw2["chi2"]
    nfw3 = P.fit_nfw(rows, 0.62, True)
    assert abs(nfw3["chi2"] - PINNED["nfw_p3"]) < 5e-3, nfw3["chi2"]
    for key, kwargs, interp in (
        ("mond_standard_p0", {}, "standard"),
        ("mond_standard_p1", {"free_a0": True}, "standard"),
        ("mond_standard_p2", {"free_a0": True, "free_upsilon": True}, "standard"),
        ("mond_simple_p0", {}, "simple"),
        ("mond_simple_p2", {"free_a0": True, "free_upsilon": True}, "simple"),
    ):
        fit = P.fit_mond(rows, 0.62, interp, **kwargs)
        assert abs(fit["chi2"] - PINNED[key]) < 5e-3, (key, fit["chi2"])

    # MOND's fixed-a0 row really is a zero-parameter prediction.
    fixed = P.fit_mond(rows, 0.62, "standard")
    assert fixed["n_parameters"] == 0 and fixed["aic"] == fixed["chi2"]
    # The ordering that the report claims must actually hold.
    assert sdf["chi2"] < nfw3["chi2"] < P.fit_mond(rows, 0.62, "standard", free_a0=True)["chi2"]
    # chi2_nu uses N-p with p counted on these points.
    assert abs(sdf["chi2_nu"] - sdf["chi2"] / 30.0) < 1e-12
    assert abs(nfw3["chi2_nu"] - nfw3["chi2"] / 28.0) < 1e-12
    return {"status": "PASS", "pinned": PINNED}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sparc", type=Path, default=ROTMOD)
    parser.add_argument("--markdown", action="store_true", help="print the markdown report")
    parser.add_argument("--write", action="store_true", help="rewrite MODEL_COMPARISON.md")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args(argv)

    if args.self_test:
        result = self_test()
    else:
        rows, distance = P.load_rotmod(args.sparc)
        entries = build_rows(rows)
        table = [summarise(entry) for entry in entries]
        try:
            table_name = str(Path(args.sparc).resolve().relative_to(ROOT)).replace("\\", "/")
        except ValueError:
            table_name = str(args.sparc).replace("\\", "/")
        meta = {"table": table_name, "n_points": len(rows), "distance_mpc": distance}
        text = markdown(table, meta)
        if args.write:
            REPORT.write_text(text, encoding="utf-8")
        if args.markdown:
            print(text)
            return 0
        result = {"table": meta["table"], "distance_mpc": distance,
                  "n_points": len(rows), "rows": table,
                  "report": str(REPORT) if args.write else None}

    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output_json:
        args.output_json.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
