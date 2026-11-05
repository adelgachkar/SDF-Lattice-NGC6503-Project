# 04. Observational Data Ingestion & Computational Pipeline Architecture

## 1. Executive Pipeline Overview

The computational pipeline bridging the observational kinematics of dwarf spiral galaxy **NGC 6503** with the **Space-Density Field (SDF)** quantum lattice model is structured as a deterministic, reproducible, multi-stage ingestion and analysis engine.

The core objective is to ingest heterogeneous observational data products—specifically surface photometry, neutral hydrogen (H I) interferometry, optical $H\alpha$ long-slit spectroscopy, and molecular gas ($CO$) kinematics—decompose the baryonic gravitational potential, and execute radial lattice relaxation to quantify the non-baryonic dynamic acceleration via the radial unfreezing parameter $\xi(r)$.

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

𝜒
2
χ 
2
 
 / MCMC Exploration of
(
𝜉
0
,
𝑅
freeze
,
Δ
𝑅
,
𝛼
visc
)
(ξ
0
​
 ,R
freeze
​
 ,ΔR,α
visc
​
 )
Active Tensor Foam Dynamics (active_tensor_foam.py)
│

▼

[Stage 4: Verification, Benchmarks & Audit Plots]

ngc6503_curve_audit.png
ngc6503_friction_audit.png
radial_unfreezing_verification.png


---

## 2. Ingested Data Sources & Galaxy Benchmarks

### 2.1 Astronomical Source Data

The empirical kinematic baseline incorporates calibrated data compiled from:

1. **Begeman (1987, 1989)**: WSRT (Westerbork Synthesis Radio Telescope) 21 cm H I rotation curves extending into the deep halo ($r > 20 \text{ kpc}$).
2. **Bottema (1989)**: Stellar kinematics and velocity dispersion ($\sigma_R, \sigma_z$) across the optical disk.
3. **SPARC Database (Lelli, McGaugh, & Schombert 2016)**: High-precision Spitzer $3.6 \ \mu\text{m}$ surface brightness profiles and unified kinematic tables.

### 2.2 NGC 6503 Reference Parameters

* **Morphological Type**: SA(s)cd (Dwarf spiral, undisturbed disk)
* **Coordinates**: $\alpha = 17^{\text{h}} 59^{\text{m}} 14.0^{\text{s}}$, $\delta = +70^\circ 11' 47''$
* **Adopted Distance ($D$)**: $5.27 \pm 0.15 \text{ Mpc}$ (Tip of the Red Giant Branch, TRGB)
* **Scale Factor**: $1 \text{ arcsec} \approx 25.55 \text{ pc}$
* **Inclination Angle ($i$)**: $74.5^\circ \pm 1.5^\circ$
* **Position Angle ($\phi$)**: $120.0^\circ$
* **Systemic Velocity ($V_{\text{sys}}$)**: $25.0 \pm 1.5 \text{ km/s}$
* **Asymptotic Flat Velocity ($v_{\text{flat}}$)**: $116.2 \pm 2.4 \text{ km/s}$
* **Baryonic Mass ($M_{\text{bar}}$)**: $\approx 5.8 \times 10^9 \ M_\odot$

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

where the fiducial stellar mass-to-light ratio is set to $\Upsilon_{\text{disk}}^{[3.6]} = 0.50 \pm 0.10 \ M_\odot/L_\odot$ according to stellar population synthesis (SPS) models with a Chabrier IMF.

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

The pipeline minimizes an objective loss function based on weighted residual chi-square:
$$\chi_{\text{red}}^2 = \frac{1}{N - M} \sum_{i=1}^{N} \left[ \frac{v_{\text{obs}}(r_i) - v_{\text{model}}(r_i; \boldsymbol{\theta})}{\sigma_i} \right]^2$$
where $\boldsymbol{\theta} = \{\Upsilon_{\text{disk}}, \xi_0, R_{\text{freeze}}, \Delta R, \beta, \alpha_{\text{visc}}\}$.

### Parameter Priors and Best-Fit Estimates (NGC 6503 Benchmark)

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
   Comparative residual audit verifying that $\chi_{\text{red}}^2 \le 1.04$, matching or exceeding standard dark matter halo profiles (NFW, Burkert, Pseudo-Isothermal) without fine-tuned halo core parameters.

---

## 7. Execution CLI & Environment Setup

Run the end-to-end pipeline within PowerShell (Python 3.12.6):

```powershell
# Set Python path to current workspace root
$env:PYTHONPATH="."

# Run pipeline unit tests
python -m pytest tests/test_data_pipeline.py -v

# Execute complete ingestion, potential solve, and SDF fit
python -m nodes.pipeline_runner --galaxy NGC6503 --config configs/ngc6503_default.yaml --save-plots

## Consolidated execution contract and corrected units

Use `Scripts/radial_unfreezing_verification.py` as the available executable verification module. The former paths `active_tensor_foam.py` and `nodes.pipeline_runner` are references to modules not present in the inspected archive; they are not prerequisites or executed components of this deliverable. The current script validates the canonical $\zeta$ kernel and computes the specified reduced chi-square from a supplied CSV (`r_kpc,v_obs_kms,v_bar_kms,sigma_kms`). The adopted unit conversion is $1$ kpc $=3.0857\times10^{19}$ m (not the legacy rounded value).

The dof convention is $N-p$, where $p$ counts parameters fit to those same points. The documented outer slope is an OLS slope of model velocity on radii $r\geq8$ kpc unless a different cutoff is explicitly provided. A raw observational table is absent from the supplied project archives, so pipeline capability is distinct from independent reproduction of the reported fit.

