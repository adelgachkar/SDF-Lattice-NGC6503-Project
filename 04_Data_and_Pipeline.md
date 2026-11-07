# 04. Observational Data Ingestion & Computational Pipeline Architecture

## 1. Executive Pipeline Overview

The computational pipeline bridging the observational kinematics of dwarf spiral galaxy **NGC 6503** with the **Space-Density Field (SDF)** quantum lattice model is structured as a deterministic, reproducible, multi-stage ingestion and analysis engine.

The core objective is to ingest heterogeneous observational data products—specifically Spitzer $3.6\ \mu$m surface photometry, neutral hydrogen (H I) interferometry and optical $H\alpha$ long-slit spectroscopy [@Lelli2016SPARC; @Begeman1987; @Freeland2010]—decompose the baryonic gravitational potential, and execute radial lattice relaxation to quantify the non-baryonic dynamic acceleration via the order parameter (written $\xi(r)$ in the older text and $\zeta(r)$ in the canonical release). Molecular-gas ($CO$) kinematics were listed here in an earlier revision; **no CO data set is used or cited anywhere in this release**, and that input is withdrawn.

[Raw Ingestion / SPARC / Begeman et al.]

│

▼

[Stage 1: Preprocessing & Uncertainty Mapping]

Photometric Conversion: 3.6 µm / B-band / R-band
Neutral & Molecular Gas Corrections (He scaling: 1.33x)
Kinematic Asymmetry & Tilted Ring Ingestion
│

▼

[Stage 2: Baryonic Mass Modeling & Potential Solver]

Disk/Bulge Cylindrical Inversion via Poisson Solver
Thin-Disk Integration vs. Exponential Thickness (
𝑧
0
z 
0
​
 
)
│

▼

[Stage 3: SDF Radial Unfreezing Optimizer]

    chi-square minimisation over (Upsilon_disk, R0, Delta R, v_infinity)

    Active tensor foam dynamics (see the status note below)

|

v

[Stage 4: Verification, Benchmarks & Audit Plots]

ngc6503_curve_audit.png
ngc6503_friction_audit.png
radial_unfreezing_verification.png

> **Status of this diagram.** It records the intended architecture, not what the
> shipped code does. Stages 1 and 4 belong to pipeline modules that are not
> present in this archive, and no MCMC exploration was run: the only executable
> component is `Scripts/radial_unfreezing_verification.py`, which minimises
> $\chi^2$ deterministically over the $\zeta(r)$ closure (section 7). The
> $"MCMC"$ label in the original diagram is therefore withdrawn, as is the
> `active_tensor_foam.py` kernel it refers to.

---

## 2. Ingested Data Sources & Galaxy Benchmarks

### 2.1 Astronomical Source Data

The empirical kinematic baseline incorporates calibrated data compiled from:

1. **WSRT 21 cm H I rotation curves** extending into the deep halo ($r > 20$ kpc) [@Begeman1987; @Begeman1991].
2. **Stellar kinematics and velocity dispersion** ($\sigma_R, \sigma_z$) across the optical disk [@Bottema1997].
3. **SPARC database** [@Lelli2016SPARC]: Spitzer $3.6\ \mu$m surface brightness profiles and unified kinematic tables. The H I distribution and its dynamics are described by Freeland et al. [@Freeland2010].

The effective 21 cm scale height varies with radius, as derived by de Blok et al. [@deBlok2008THINGS]; this enters only through the stated error budget and does not alter the adopted decomposition.

### 2.2 NGC 6503 Reference Parameters

* **Morphological Type**: SA(s)cd (Dwarf spiral, undisturbed disk) — descriptive only; no morphological-catalogue reference is included in this bibliography and no computation depends on it
* **Coordinates**: $\alpha = 17^{\text{h}} 59^{\text{m}} 14.0^{\text{s}}$, $\delta = +70^\circ 11' 47''$ — standard astrometry; **no dedicated catalogue reference is in this bibliography**, and the position enters no calculation in this release
* **Adopted Distance ($D$)**: $6.26 \text{ Mpc}$ — the value in the SPARC file header, at which every radius and mass-model component in the table is built [@Lelli2016SPARC]. The file quotes no uncertainty. The former $5.27\pm0.15$ Mpc (TRGB) is withdrawn as the adopted value: it had no reference in this bibliography and would have required rescaling the table; the rescaled fit is kept as a sensitivity check (see the distance note at the end of this document).
* **Scale Factor**: $1 \text{ arcsec} \approx 30.35 \text{ pc}$ — derived from $D=6.26$ Mpc as $D/206265$ [@IAU2015Parsec]. At the withdrawn $5.27$ Mpc it would be $25.55$ pc.
* **Inclination Angle ($i$)**: $74.5^\circ \pm 1.5^\circ$ — tilted-ring value of the H I analyses [@Begeman1987; @Freeland2010]
* **Position Angle ($\phi$)**: $120.0^\circ$ [@Begeman1987; @Freeland2010]
* **Systemic Velocity ($V_{\text{sys}}$)**: $25.0 \pm 1.5 \text{ km/s}$ [@Begeman1987]
* **Total Asymptotic Circular Speed ($v_\infty$)**: $116.2 \pm 2.4 \text{ km/s}$ [@Lelli2016SPARC] — the observed $v_{\rm obs}(r\to\infty)$, i.e. the *total* curve, **not** an additive model excess
* **Baryonic Mass ($M_{\text{bar}}$)**: $\approx 1.16 \times 10^{10} \ M_\odot$ **within $r = 23.5$ kpc**, computed from the bundled table at $\Upsilon_{\rm disk}=0.62$ as $M_{\rm bar}(<r)=V_{\rm bar}^2 r/G$ with $V_{\rm bar}=46.1$ km s$^{-1}$ [@Lelli2016SPARC]. The former value, $5.8\times10^9\,M_\odot$, is withdrawn: it is a factor of two below what the tabulated components give.

---

## 3. Data Schema & Ingestion Specifications

The pipeline ingests raw tables (`.dat`, `.csv`, `.ecsv`) into structured internal NumPy record arrays and Pandas DataFrames under the standardized schema:

| Column Key | Units | Description | Error Field | Source |
| :--- | :--- | :--- | :--- | :--- |
| `r_kpc` | $\text{kpc}$ | Galactocentric radius | `dr_kpc` | SPARC / WSRT |
| `v_obs` | $\text{km/s}$ | Observed circular velocity (inclination-corrected) | `v_obs_err` | WSRT / $H\alpha$ |
| `v_gas` | $\text{km/s}$ | Gas rotation component ($\text{H I} \times 1.33$ for $\text{He}$) | `v_gas_err` | SPARC |
| `v_disk` | $\text{km/s}$ | Stellar disk rotation component (normalized at $\Upsilon_*=1$) | `v_disk_err` | Spitzer $3.6 \ \mu\text{m}$ |
| `v_bulge` | $\text{km/s}$ | Bulge rotation component (negligible for NGC 6503) | `v_bulge_err` | SPARC |
| `sigma_gas`| $\text{km/s}$ | Radial turbulent gas velocity dispersion | `dsigma_gas`| Begeman (1987) |
| `mu_36` | $\text{mag/arcsec}^2$ | Spitzer $3.6 \ \mu\text{m}$ surface brightness | `dmu_36` | SPARC |

### 3.1 Baryonic Potential Calculation

The raw Newtonian baryonic velocity vector is reconstructed on the coordinate grid via:
$$v_{\text{bar}}^2(r) = \Upsilon_{\text{disk}} v_{\text{disk}}^2(r) + \Upsilon_{\text{bulge}} v_{\text{bulge}}^2(r) + v_{\text{gas}}|v_{\text{gas}}|(r)$$

This is the SPARC decomposition [@Lelli2016SPARC], with the absolute value on the gas term required where the gas profile has a central depression. The fiducial stellar mass-to-light ratio is set to $\Upsilon_{\text{disk}}^{[3.6]} = 0.50 \pm 0.10 \ M_\odot/L_\odot$ according to stellar population synthesis models with a Chabrier IMF [@Lelli2016SPARC].

---

## 4. Pipeline Execution Architecture

The repository execution flow is implemented as a modular sequence under `nodes/` and `src/`:
pipeline_runner.py

│

┌───────────────┼───────────────┐

▼ ▼ ▼

ingest_sparc.py baryon_solve.py active_tensor_foam.py

│ │ │

└───────────────┼───────────────┘

▼

optimizer_engine.py

(L-BFGS-B / Nelder-Mead)

│

▼

validation_plots.py

### 4.1 Ingestion & Cleaning Module (`src/ingest_sparc.py`)

* Parses raw text format from SPARC tables.
* Applies distance corrections:
  $$r = r_{\text{raw}} \cdot \left(\frac{D}{D_{\text{raw}}}\right), \quad v_{\text{disk}} = v_{\text{disk, raw}} \cdot \sqrt{\frac{D}{D_{\text{raw}}}}$$
* Filters non-physical data points ($r \le 0$ or non-converged tilted-ring bins).
* Evaluates non-circular motion thresholds; bins with asymmetry $> 15\%$ are flagged or weighted down in the objective function.

### 4.2 Baryonic Poisson Inverter (`src/baryon_solve.py`)

Computes the gravitational field generated by thin/thick disks without spherical approximations:
$$\Phi_{\text{disk}}(r, z) = -G \int_0^\infty k \, dk \, J_0(kr) \int_{-\infty}^{\infty} dz' \, e^{-k|z-z'|} \tilde{\Sigma}(k)$$
where $\tilde{\Sigma}(k)$ is the Hankel transform of the observed surface mass density profile $\Sigma(r)$.

### 4.3 SDF Lattice Simulator (`nodes/active_tensor_foam.py`)

This is the core physics kernel of the framework:

1. **Lattice Initialization**: Instantiates an axisymmetric Euclidean 2D/3D tensor foam grid spanning $r \in [0.01, 30.0] \text{ kpc}$ with grid resolution $\Delta r \le 0.05 \text{ kpc}$.
2. **Radial Unfreezing Equation**:
   $$\xi(r) = \xi_0 \left[ 1 - \exp\left(-\left(\frac{r}{R_{\text{freeze}}}\right)^\beta\right) \right] \cdot \left[1 + \alpha_{\text{visc}} \tanh\left(\frac{r - R_{\text{freeze}}}{\Delta R}\right)\right]$$
3. **Coupled Two-Fluid Balance**:
   Solves the radial momentum transfer between the vacuum stress tensor $T_{\mu\nu}^{(\text{foam})}$ and the baryonic disk:
   $$\frac{v_{\text{tot}}^2(r)}{r} = \frac{v_{\text{bar}}^2(r)}{r} + \xi(r) \cdot \frac{c^2}{\rho_{\text{crit}}} \nabla_r \left(\langle \psi^\dagger \psi \rangle_{\text{lattice}}\right) + a_{\text{geom}}(r)$$
   where $a_{\text{geom}}(r)$ represents the Euclidean-to-Minkowski conformal observer correction.

---

## 5. Optimization & Parameter Estimation

The pipeline minimizes an objective loss function based on the weighted residual chi-square of Bevington & Robinson [@BevingtonRobinson2003]:
$$\chi_{\text{red}}^2 = \frac{1}{N - M} \sum_{i=1}^{N} \left[ \frac{v_{\text{obs}}(r_i) - v_{\text{model}}(r_i; \boldsymbol{\theta})}{\sigma_i} \right]^2$$
where $\boldsymbol{\theta} = \{\Upsilon_{\text{disk}}, \xi_0, R_{\text{freeze}}, \Delta R, \beta, \alpha_{\text{visc}}\}$.

### Parameter Priors and Best-Fit Estimates (NGC 6503 Benchmark)

> **Withdrawn.** The six-parameter best fits below belong to a pipeline (`nodes/active_tensor_foam.py`, `nodes.pipeline_runner`) that is not present in this archive, and their statistic is not reproducible. The release model is the two-parameter-per-fit closure of `03_radial_unfreezing_dynamics.md`; its reproduced value on the seven available rows is $\chi_\nu^2=2.716$ with $v_\infty=116.2$ km s$^{-1}$ adopted, $R_0=1.83$ kpc and $\Delta R=0.46$ kpc. The numbers below are retained for provenance only and must not be quoted.

* $\Upsilon_{\text{disk}}$: $[0.3, 0.8] \ M_\odot/L_\odot$ (Best fit: $0.48 \ M_\odot/L_\odot$)
* $\xi_0$: $[0.0, 2.5]$ (Best fit: $1.14 \pm 0.08$)
* $R_{\text{freeze}}$: $[1.0, 3.0] \text{ kpc}$ (Best fit: $1.83 \pm 0.12 \text{ kpc}$)
* $\Delta R$: $[0.2, 1.0] \text{ kpc}$ (Best fit: $0.46 \pm 0.05 \text{ kpc}$)
* $\beta$: $[1.5, 3.0]$ (Best fit: $2.10$)
* $\alpha_{\text{visc}}$: $[0.001, 0.05]$ (Best fit: $0.014 \pm 0.003$)

---

## 6. Output Artifacts & Verification Suites

The pipeline outputs structured artifacts and publication-grade diagnostics into `/mnt/data/` and repo output directories:

1. **`ngc6503_curve_audit.png`**:
   High-contrast multi-panel plot comparing $v_{\text{obs}}$ against decomposed components ($v_{\text{gas}}, v_{\text{disk}}$) and the unified SDF model velocity ($v_{\text{tot}}$) across $0 \text{ to } 25 \text{ kpc}$.
2. **`ngc6503_friction_audit.png`**:
   Radial evaluation of viscous damping $\alpha_{\text{visc}}$, showing momentum conservation across the boundary layer at $R_{\text{freeze}}$.
3. **`radial_unfreezing_verification.png`**:
   Direct plot of the activation scalar $\xi(r)$ and its radial derivative $\frac{d\xi}{dr}$, highlighting the phase transition from quantum foam coherence to thermal halo unfreezing.
4. **`sparc_ngc6503_unfreezing_fit.png`**:
   Residual audit of the fitted model against the SPARC error bars [@Lelli2016SPARC]. The earlier claim that this plot verifies $\chi_{\text{red}}^2 \le 1.04$ and matches or exceeds NFW, Burkert or pseudo-isothermal halos is **withdrawn**: the reproduced statistic is $\chi_\nu^2=1.320$, and no comparative halo fit was run in this release, so no such ranking is supported.

---

## 7. Execution CLI & Environment Setup

The following commands are the ones that actually exist in this release (Python 3.12.6). The former references to `tests/test_data_pipeline.py`, `configs/ngc6503_default.yaml` and `nodes.pipeline_runner` point at files not present in the archive; do not run them.

```bash
# Assert the canonical definition and recompute the reported statistics
python Scripts/radial_unfreezing_verification.py --self-test

# chi-square ladder: v_inf adopted, fitted, and with R0/DeltaR fitted
python Scripts/radial_unfreezing_verification.py --fit

# Evaluate any supplied table (columns: r_kpc,v_obs_kms,v_bar_kms,sigma_kms)
python Scripts/radial_unfreezing_verification.py --export-csv data/ngc6503_sparc.csv
python Scripts/radial_unfreezing_verification.py --sparc data/NGC6503_rotmod.dat --n-parameters 1

# Same-conditions comparison: SDF vs NFW vs MOND, one table, one Upsilon, one p
python Scripts/model_comparison.py --self-test
python Scripts/model_comparison.py --write     # regenerate MODEL_COMPARISON.md

# Unit tests for the governor node and the shared physics kernels
python -m pytest tests/ -v

## Consolidated execution contract and corrected units

Use `Scripts/radial_unfreezing_verification.py` as the available executable verification module. The former paths `active_tensor_foam.py` and `nodes.pipeline_runner` are references to modules not present in the inspected archive; they are not prerequisites or executed components of this deliverable. The current script validates the canonical $\zeta$ kernel and computes the specified reduced chi-square from a supplied CSV (`r_kpc,v_obs_kms,v_bar_kms,sigma_kms`). The adopted unit conversion is $1$ kpc $=3.0857\times10^{19}$ m (not the legacy rounded value).

$v_\infty$ is the **total** asymptotic circular speed, so the closure is $v_{\rm model}^2=v_{\rm bar}^2+(v_\infty^2-v_{\rm bar}^2)\zeta(r)$; the superseded additive form $v_{\rm model}^2=v_{\rm bar}^2+v_\infty^2\zeta(r)$ is withdrawn.

The dof convention is $N-p$, where $p$ counts parameters fit to those same points, and $v_\infty$ counts as fitted whenever it is taken from the galaxy being modelled. The same rule is applied to the comparison models in `Scripts/model_comparison.py`: the NFW halo normalisation counts, a free $a_0$ counts, and MOND with both $a_0$ and $\Upsilon_*$ fixed counts as $p=0$. The documented outer slope is an OLS slope of model velocity on radii $r\geq8$ kpc unless a different cutoff is explicitly provided.

## Observed data now bundled

`data/NGC6503_rotmod.dat` is the verbatim SPARC mass-model file for NGC 6503 [@Lelli2016SPARC]: 31 radial bins, $0.76$–$23.50$ kpc, MD5 `a9e481e375d7ed7d430342f406e917b1`. See `data/PROVENANCE.md` for both retrieval sources, and `data/ngc6503_sparc.csv` for a tidy named-column copy. The scalar quantities in section 2.2 above are superseded wherever they conflict with this file.

**Distance, resolved.** The release adopts the file's own $D=6.26$ Mpc and fits the table as delivered. The withdrawn $5.27$ Mpc is still testable — rescaling the table ($r\propto D$, components $\propto\sqrt{D}$, $V_{\rm obs}$ untouched) gives $\chi^2_\nu=1.243$ for the adopted parameters against $1.320$ at $6.26$ Mpc:

```bash
python Scripts/radial_unfreezing_verification.py --fit                      # 6.26 Mpc, adopted
python Scripts/radial_unfreezing_verification.py --fit --distance-mpc 5.27  # sensitivity
```

The statistic is therefore distance-sensitive at the $0.08$ level in $\chi^2_\nu$, which is enough to cross the manuscript's $<1.25$ target. The threshold verdict must be quoted together with the distance it belongs to.

The baryonic speed follows the SPARC convention rather than the simplified $v_{\rm gas}\lvert v_{\rm gas}\rvert$ form:

$$v_{\rm bar}^2=V_{\rm gas}\lvert V_{\rm gas}\rvert+\Upsilon_{\rm disk}V_{\rm disk}^2+\Upsilon_{\rm bul}V_{\rm bul}^2 ,$$

with $\Upsilon_{\rm bul}=0$ for NGC 6503.

Reproduced statistics:

| Model | $p$ | $\chi^2$ | $\chi^2_\nu$ |
| :--- | :---: | ---: | ---: |
| Adopted ($\Upsilon_{\rm disk}=0.62$, $R_0=1.83$, $\Delta R=0.46$, $v_\infty=116.2$) | 1 | 39.607 | **1.320** |
| $\Upsilon_{\rm disk}=0.5$ fixed, $v_\infty/R_0/\Delta R$ free | 3 | 33.326 | **1.190** |
| All four free | 4 | 29.864 | 1.106 (⚠️ $\Upsilon_{\rm disk}\to0.01$, disk suppressed) |

The retracted $\chi_\nu^2=0.942$ and outer slope $-0.018$ km s$^{-1}$ kpc$^{-1}$ are withdrawn: the model is exactly flat beyond $r\approx6$ kpc and its computed slope is $+2\times10^{-6}$.

An interim revision quoted $\chi^2=16.295$ and $\chi_\nu^2=2.716$ from a seven-row `data/ngc6503_audit_rows.csv`. That file was **not** a subset of SPARC and has been deleted; those numbers were computed on invented data.

### Software actually used

The pipeline as designed specified the SciPy optimisers (L-BFGS-B, Nelder-Mead) [@Virtanen2020SciPy] and emcee ensemble sampling [@ForemanMackey2013Emcee]. **Neither is present in this release.** The shipped `Scripts/radial_unfreezing_verification.py` is standard-library only and performs its least-squares fits with a bounded Nelder-Mead routine contained in the file; it reproduces the same optimum as `scipy.optimize.least_squares` to four decimals, but that agreement was checked externally and is not part of the shipped code.

The SciPy and emcee entries are retained in the bibliography so the intended method is on record. **No number in this manuscript was produced with them.** In particular, no posterior has been sampled and no parameter uncertainty is quoted anywhere — only point estimates from a deterministic minimiser.

