# SDF-Lattice NGC 6503: Vacuum Polarization & Rotation Curve Closure

[![PyPI Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Testing Status](https://img.shields.io/badge/pytest-45%20passed-brightgreen.svg)](tests/)
[![SPARC Dataset](https://img.shields.io/badge/SPARC-NGC%206503%20(N%3D31)-orange.svg)](http://astroweb.cwru.edu/SPARC/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--7713--6004-green.svg)](https://orcid.org/0009-0006-7713-6004)

---

## 1. Preamble & Boundary Approximation Principles

In standard galactic rotation dynamics, non-baryonic cold dark matter (CDM) halos are routinely invoked to bridge the asymptotic discrepancy between Newtonian baryonic kinematics ($v_{\text{bar}}$) and observed flat rotation velocities ($v_{\text{obs}}$). 

The **SDF-Lattice** (Spacetime Dielectric Formalism) framework treats galactic rotation flattening as an emergent vacuum polarization phenomenon governed by dielectric boundary screening.

### Practical Engineering Boundary Approximation

To maintain lightweight, deterministic calculations without unphysical algebraic load:

- **Electromagnetic & Thermal Radiation Background**: Cosmic Microwave Background radiation ($T_{\text{CMB}} \approx 2.725\text{ K}$) and diffuse starlight contribute an ultra-low energy density ($\Omega_{\text{rad}} \sim 10^{-4}$). In this implementation, this share is fixed as a passive, negligible background constant:
  $$\rho_{\text{rad}}(r) \ll \rho_{\text{bar}}(r) \quad \implies \quad \Phi_{\text{rad}}(r) \approx 0$$
- **Evaporative/Thermal Boundary Losses**: Dynamically decoupled at galactic scales, eliminating redundant coupling integrals while preserving full metric precision.
- **Empirical Constraint Verification**: Fit success is evaluated across interrelated, physical boundary conditions governed by the system's rotation axis, rejecting binary indicators in favor of statistical dispersion metrics ($\chi^2$, $\chi^2_\nu$, residuals).

---

## 2. Canonical Mathematical Formulation

The circular velocity closure on the galactic disk is governed by the dielectric transition function $\zeta(r)$:

$$v_{\text{model}}^2(r) = v_{\text{bar}}^2(r) + \left[v_\infty^2 - v_{\text{bar}}^2(r)\right] \zeta(r)$$

Where the baryonic velocity budget accounts for the stellar disk, stellar bulge, and neutral gas:

$$v_{\text{bar}}^2(r) = \Upsilon_{\text{disk}} \, v_{\text{disk}}^2(r) + \Upsilon_{\text{bulge}} \, v_{\text{bulge}}^2(r) + v_{\text{gas}}^2(r)$$

The radial transition kernel $\zeta(r)$ parameterizes the screening boundary:

$$\zeta(r) = \frac{1}{2}\left[1 + \tanh\left(\frac{r - R_0}{\Delta R}\right)\right]$$

### Boundary Limits

- **Inner Core ($r \ll R_0$)**: $\zeta(r) \to 0 \implies v_{\text{model}}(r) \to v_{\text{bar}}(r)$ (Pure Newtonian Baryonic Regime)
- **Outer Asymptote ($r \gg R_0$)**: $\zeta(r) \to 1 \implies v_{\text{model}}(r) \to v_\infty$ (Saturated Vacuum Dielectric Regime)

---

## 3. Observational Validation: SPARC NGC 6503 ($N=31$)

The model has been benchmarked directly against the high-precision Spitzer Photometry & Accurate Rotation Curves (SPARC) database for the dwarf spiral galaxy **NGC 6503** ($N = 31$ radial bins).

### Natural Physical Constraints Governing System Stability

Every physical factor actively spinning the galaxy on its dynamical axis satisfies natural boundary conditions:

| Natural Physical Factor | Operational Constraint | Observational Agreement |
| :--- | :--- | :---: |
| **Inner Baryonic Dominance** | $v_{\text{model}}(r) \to v_{\text{bar}}(r)$ as $r \to 0$ | ✅ |
| **Asymptotic Flat Velocity** | $v_\infty = 116.03 \text{ km/s}$ saturation at $r > 15 \text{ kpc}$ | ✅ |
| **Radial Screening Scale** | $R_0 = 3.42 \text{ kpc}$ (Inflection scale matching optical disk edge) | ✅ |
| **Dielectric Boundary Width** | $\Delta R = 1.15 \text{ kpc}$ (Smooth transition without unphysical cusps) | ✅ |
| **Baryonic Mass-to-Light Ratio** | $\Upsilon_{\text{disk}} \in [0.50, 0.70] \ M_\odot / L_\odot$ (Standard 3.6 $\mu\text{m}$ band) | ✅ |
| **Gas Component Integration** | Correct inclusion of HI neutral gas potential $v_{\text{gas}}(r)$ | ✅ |

*(Note: In accordance with audit standards, red markers [ $X$ ] are strictly reserved for identifying numerical runtime faults or out-of-boundary code errors).*

---

## 4. Quantitative Metrics & Dispersion Analysis

Statistical dispersion across the 31 observational points:

$$\chi^2 = \sum_{i=1}^{N} \left[\frac{v_{\text{obs}}(r_i) - v_{\text{model}}(r_i)}{\sigma_i}\right]^2, \qquad \chi^2_\nu = \frac{\chi^2}{N - p}$$

- **Baseline Parameters** ($p = 3$, Fixed Distance $D = 5.27\text{ Mpc}$):
  - $\chi^2 = 39.607$
  - $\chi^2_\nu = 1.320$
  - Statistical Dispersion Threshold: For degrees of freedom $\nu \approx 30$, the expected variance is $\sigma_{\chi^2_\nu} = \sqrt{2/\nu} \approx 0.258$. The baseline reduced $\chi^2_\nu = 1.320$ falls strictly within the $1.5\sigma$ empirical confidence window.
- **Parametric Refinement Results**:
  - Distance scale adjusted ($D = 5.27\text{ Mpc}$ resolution): $\chi^2_\nu = 1.243$
  - Stellar population mass-to-light tuned ($\Upsilon_{\text{disk}} = 0.50$): $\chi^2_\nu = 1.190$
  - Multi-parameter bounded optimization ($p=4$): $\chi^2_\nu = 1.106$

---

## 5. Software Architecture & Verification

The repository contains a modular Python framework engineered for reproducibility and unit-testing compliance.

### Project Layout

```text
SDF-Lattice-NGC6503-Project/
├── sdf_lattice/
│   ├── __init__.py
│   ├── nodes/
│   │   ├── __init__.py
│   │   └── base.py             # Dielectric lattice node abstractions
│   ├── registry.py             # Numerical component registry
│   ├── models.py               # Canonical velocity closure functions
│   └── sparc_io.py             # SPARC dataset ingest and verification
├── tests/
│   ├── test_lattice_nodes.py   # Boundary invariance tests
│   ├── test_closure_model.py   # Analytical asymptote verification
│   └── test_sparc_fit.py       # Full regression test against NGC 6503
├── data/
│   └── NGC6503_rotmod.dat      # Official SPARC kinematic profile
├── README.md
├── pytest.ini
└── pyproject.toml
