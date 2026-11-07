# SDF-Lattice-NGC6503 — Consolidated manuscript and verification status

## Data

The rotation curve is the **real** SPARC mass-model table for NGC 6503 [@Lelli2016SPARC], filed verbatim as `data/NGC6503_rotmod.dat`: 31 radial bins, $0.76$–$23.50$ kpc, MD5 `a9e481e375d7ed7d430342f406e917b1`. Provenance, both retrieval sources and the column schema are in `data/PROVENANCE.md`; a tidy named-column copy is `data/ngc6503_sparc.csv`.

**Distance: 6.26 Mpc, resolved.** The SPARC file adopts $D=6.26$ Mpc and its radii and mass-model components are built at that distance [@Lelli2016SPARC], so this release fits the table at 6.26 Mpc and every reported statistic belongs to it. The manuscript's earlier $5.27\pm0.15$ Mpc (quoted as TRGB) is **withdrawn as the adopted value**: it carries no reference in this bibliography, and using it requires rescaling the table ($r\propto D$, mass-model components $\propto\sqrt{D}$, $V_{\rm obs}$ unchanged). That rescale was run as a sensitivity check and moves the adopted-parameter statistic from $\chi^2_\nu=1.320$ to $1.243$ — across the $<1.25$ threshold. See *Distance sensitivity* below.

## Scope and canonical release values

**Definition (binding).** $v_\infty$ is the **total** asymptotic circular speed, $v_{\rm obs}(r\to\infty)$. It is an observable of the galaxy, **not** an additive component of the model.

**Canonical closure.** The adopted values ($R_0=1.83$ kpc, $\Delta R=0.46$ kpc, $v_\infty=116.2$ km s$^{-1}$, $\Upsilon_{\rm disk}=0.62$) are those of the project specification [@SDFRadialUnfreezing2026]; the SPARC convention for $v_{\rm bar}$ and the stellar mass-to-light ratios are from [@Lelli2016SPARC].

$$v_{\rm model}^2(r)=v_{\rm bar}^2(r)+\left[v_\infty^2-v_{\rm bar}^2(r)\right]\zeta(r),\qquad
\zeta(r)=\tfrac12\left[1+\tanh\frac{r-R_0}{\Delta R}\right]$$

with $v_{\rm bar}^2=V_{\rm gas}\lvert V_{\rm gas}\rvert+\Upsilon_{\rm disk}V_{\rm disk}^2$ (SPARC convention) and $1$ kpc $=3.0857\times10^{19}$ m.

The limits are correct by construction: $r\to0$ gives $v\to v_{\rm bar}$ (the residual core boost is $+0.05$ km s$^{-1}$ at $v_{\rm bar}=35.8$, since $\zeta(0)=3.3\times10^{-4}$ rather than $0$), and $r\to\infty$ gives $v\to v_\infty$ exactly, with no overshoot.

## Reproduced statistics

Computed by `Scripts/radial_unfreezing_verification.py` from the 31 SPARC bins [@Lelli2016SPARC], with $\chi_\nu^2$ defined as in [@BevingtonRobinson2003].

| Model | $p$ | $\Upsilon_{\rm disk}$ | $v_\infty$ | $R_0$ | $\Delta R$ | $\chi^2$ | $\chi^2_\nu$ |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Adopted values | 1 | 0.62 | 116.20 | 1.83 | 0.46 | 39.607 | **1.320** |
| $\Upsilon_{\rm disk}=0.5$ fixed, rest free | 3 | 0.50 | 116.27 | 1.583 | 1.036 | 33.326 | **1.190** |
| All four free | 4 | 0.010 ⚠️ | 116.28 | 0.985 | 1.042 | 29.864 | 1.106 |

The first row is the manuscript's own parameter set [@SDFRadialUnfreezing2026] and is the number that should be quoted against the $\chi_\nu^2<1.25$ target: it **fails**, at 1.320.

The third row carries a warning. $\Upsilon_{\rm disk}$ runs to its lower bound of 0.01, i.e. the fit prefers to switch the stellar disk off entirely and reproduce the curve from $v_\infty\zeta(r)$ alone. That is not a baryon-driven model; it is a two-parameter smooth step dressed as one.

$v_\infty$ is counted as a fitted parameter throughout, because it is taken from the same galaxy it is compared against.

**Outer slope.** The model saturates: $\zeta=1$ to within $10^{-6}$ beyond $r\approx6$ kpc, so the computed OLS slope for $r\geq8$ kpc is $+2\times10^{-6}$ km s$^{-1}$ kpc$^{-1}$. The model is exactly flat there by construction, and an outer slope is not a diagnostic of this closure.

**Residual structure.** With the adopted values the largest deviations are $+2.03\sigma$ at 0.76 kpc, $-2.89\sigma$ at 2.28 kpc, $+2.40\sigma$ at 3.79 and 4.55 kpc. All four sit inside or at the transition, which is where the ansatz is least constrained; the outer curve is fit almost perfectly because it is imposed.

## Distance sensitivity

The fit is run at the distance the data were built for, 6.26 Mpc. The withdrawn
5.27 Mpc value was tested by rescaling the whole table ($r\propto D$, gas/disk/bulge
components $\propto\sqrt{D}$, $V_{\rm obs}$ and its errors untouched) and refitting:

| Distance | $p$ | Model | $v_\infty$ | $R_0$ | $\Delta R$ | $\chi^2$ | $\chi^2_\nu$ |
| :--- | :---: | :--- | ---: | ---: | ---: | ---: | ---: |
| 6.26 Mpc (adopted) | 1 | adopted parameters | 116.20 | 1.83 | 0.46 | 39.607 | **1.320** ❌ |
| 6.26 Mpc (adopted) | 3 | $\Upsilon_{\rm disk}=0.5$, rest free | 116.27 | 1.583 | 1.036 | 33.326 | 1.190 |
| 6.26 Mpc (adopted) | 4 | all four free | 116.28 | 0.985 | 1.042 | 29.864 | 1.106 |
| 5.27 Mpc (sensitivity) | 1 | adopted parameters | 116.20 | 1.83 | 0.46 | 37.299 | **1.243** |
| 5.27 Mpc (sensitivity) | 3 | $\Upsilon_{\rm disk}=0.5$, rest free | 116.27 | 1.196 | 0.893 | 32.017 | 1.143 |
| 5.27 Mpc (sensitivity) | 4 | all four free | 116.28 | 0.828 | 0.877 | 29.861 | 1.106 |

At 5.27 Mpc the adopted parameter set lands just under the $<1.25$ target ($1.243$)
instead of failing it ($1.320$). That flip is a property of the distance scale, not a
result about the galaxy: the same closure, the same parameters and the same data give
two different verdicts depending on which distance is assumed. It is exactly why the
$6.26$ Mpc of the data file is adopted here — the alternative would need a cited TRGB
measurement, not a value chosen because it passes. The all-four-free row is unchanged
in substance at either distance: $\Upsilon_{\rm disk}$ still runs to its lower bound.

Reproduce with:

```bash
python Scripts/radial_unfreezing_verification.py --fit                      # 6.26 Mpc
python Scripts/radial_unfreezing_verification.py --fit --distance-mpc 5.27  # sensitivity
```

## Retracted values and why

| Quantity | Retracted | Status |
| :--- | :--- | :--- |
| Closure | $v_{\rm bar}^2+v_\infty^2\zeta$ | **Wrong.** Treats $v_\infty$ as an additive excess, so the model asymptotes to $\sqrt{v_{\rm bar}^2+v_\infty^2}=121.6$ km s$^{-1}$ against an observed $\approx115$, overshooting by up to $+33$ km s$^{-1}$ near $r=2.46$ kpc |
| $\chi^2_\nu$ | $0.942$ | **Not reproducible** |
| $\chi^2_\nu$ | $2.716$ | **Computed on invented data.** The interim seven-row table is not a subset of SPARC; none of its radii or velocities appears in the official file |
| Outer slope | $-0.018$ km s$^{-1}$ kpc$^{-1}$ | **Unreachable.** The model is exactly flat beyond $r\approx6$ kpc |
| $\Upsilon_*$ | $0.62\,M_\odot/L_\odot$ | Now used as the adopted disk M/L in the first ladder row; not itself fitted there |
| Distance | $5.27\pm0.15$ Mpc (TRGB) | **Withdrawn as the adopted value.** No reference in this bibliography, and the table is built at 6.26 Mpc [@Lelli2016SPARC]. Retained only as a sensitivity check, which rescales to $\chi^2_\nu=1.243$ |

## Reproducibility and repository map

- Theory and conventions: `03_Theoretical_BaseLayer.md`.
- Data schema and pipeline: `04_Data_and_Pipeline.md`.
- Audit/evidence status: `05_Empirical_Audits.md`.
- Derivation: `Equations_Snippets/03_radial_unfreezing_dynamics.md`.
- Executable checks: `Scripts/radial_unfreezing_verification.py`.
- Data and provenance: `data/NGC6503_rotmod.dat`, `data/PROVENANCE.md`.
- Bibliography: `References/08_References.bib`.

The former references to `active_tensor_foam.py` and a `nodes.pipeline_runner` entry point are not supplied as executable modules in the inspected project archive. This release uses the self-contained verification script above; it does not imply those missing modules were executed.

```
python Scripts/radial_unfreezing_verification.py --self-test    # asserts the reproduced values
python Scripts/radial_unfreezing_verification.py --fit          # chi2 ladder
python Scripts/radial_unfreezing_verification.py                # adopted-parameter chi2
python Scripts/radial_unfreezing_verification.py --export-csv data/ngc6503_sparc.csv
```

The script is standard-library only; the least-squares fit uses a bounded Nelder-Mead implementation included in the file.
