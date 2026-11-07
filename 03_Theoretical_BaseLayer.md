# 03. Theoretical Framework: Spacetime Foam Dynamics & Two-Fluid Stress-Energy

## 1. Executive Summary & Epistemic Foundations

The standard cosmological model ($\Lambda\text{CDM}$) models dark matter as a collisionless, non-baryonic particulate fluid satisfying a dust equation of state ($w = 0$) [@NFW1996; @NFW1997]. While successful on cosmological scales ($z \gg 1$, CMB multipoles), it encounters persistent small-scale tensions at galactic scales: the core-cusp problem [@deBlok2010CoreCusp; @deBlok2008THINGS], the diversity of rotation curves, and the missing-satellite count [@Bullock2017SmallScale]. Modified Newtonian Dynamics (MOND) and its covariant extensions (e.g., TeVeS, relativistic AQUAL) [@Milgrom1983a; @Milgrom1983b; @Famaey2012MOND] succeed phenomenologically in matching the Radial Acceleration Relation (RAR) [@McGaugh2016RAR], yet lack an underlying microphysical quantum vacuum description.

The **SDF-QVEX (Spacetime Dielectric Foam / Quantum Vacuum Exotic eXcitations)** framework formulates galactic kinematics not as a particulate halo or an empirical modification of gravity, but as an emergent, non-equilibrium polarizable macroscopic state of quantum vacuum geometry.
[ Planck Foam Metric g^{(0)}_{\mu\nu} ]

│

Polarization via Local Shear / Strain

│

▼

[ Cold Coherent Condensate T^{(\text{cond})}{\mu\nu} ] + [ Thermal / Fluctuating Component T^{(\text{fluc})}{\mu\nu} ]

│

Radial Unfreezing Mechanism \xi®

│

▼

Effective Metric G_{\mu\nu} = 8\pi G [ T^{(\text{bar})}{\mu\nu} + T^{(\text{SDF})}{\mu\nu} ]

---

## 2. Observer-Centric Relativistic/Euclidean Geometry & Foam Metric

### 2.1 The Polarizable Lattice Metric

We consider a 4-dimensional pseudo-Riemannian manifold $\mathcal{M}$ endowed with an effective macroscopic metric $\tilde{g}_{\mu\nu}$ coupled to the microscopic Planckian foam via a conformal-disformal dielectric deformation tensor:

$$\tilde{g}_{\mu\nu} = \Omega^2(\phi) g_{\mu\nu} + \chi(\phi) \nabla_\mu \phi \nabla_\nu \phi$$

where:

- $g_{\mu\nu}$ is the background geometric metric.
- $\phi(x^\mu)$ denotes the scalar vacuum polarization potential characterizing local lattice order.
- $\Omega(\phi) = \exp(\beta \phi)$ represents the local vacuum dielectric density.
- $\chi(\phi)$ dictates disformal shear-stress coupling.

### 2.2 Euclidean Transition & Observer Path-Integrals

In the deep quantum foam regime, the microscopic path integral for quantum geometric fluctuations is evaluated under Wick rotation $\tau = i t$:

$$\mathcal{Z}[J] = \int \mathcal{D}[e, \omega] \exp\left( - \frac{1}{\hbar} \mathcal{S}_{\text{Euclidean}}[e, \omega] + \int \mathrm{d}^4 x_E \, J \cdot \Phi \right)$$

where $e^a_\mu$ are tetrads and $\omega^{ab}_\mu$ are spin connection 1-forms. In an observer-centric reference frame (proper time $\tau_{\text{obs}}$ along worldline $\gamma$), the macroscopic rotation velocity of an orbit $v_\phi(r)$ corresponds to the phase advance of the coherent ground state of the foam:

$$\Delta S_{\text{Berry}} = \oint_{\mathcal{C}} \mathcal{A}_\mu \mathrm{d}x^\mu = 2\pi \left( \frac{v_\phi^2(r) r}{G M_{\text{eff}}(r)} \right)^{1/2}$$

---

## 3. Two-Fluid Effective Stress-Energy Tensor Formulation

The total stress-energy tensor driving the Einstein field equations decomposes into the standard baryonic matter sector and the effective quantum vacuum dielectric foam (SDF) sector:

$$T_{\mu\nu}^{(\text{total})} = T_{\mu\nu}^{(\text{bar})} + T_{\mu\nu}^{(\text{SDF})}$$

### 3.1 Baryonic Decomposition

For a disc galaxy (specifically applied to NGC 6503):

$$T_{\mu\nu}^{(\text{bar})} = T_{\mu\nu}^{(\text{gas})} + T_{\mu\nu}^{(\text{disk})} + T_{\mu\nu}^{(\text{bulge})}$$

Modeled as thin/thick exponential discs with hydrodynamic components:

$$T_{\mu\nu}^{(\text{bar})} = (\rho_{\text{bar}} + P_{\text{bar}}) u_\mu u_\nu + P_{\text{bar}} g_{\mu\nu} + \Pi_{\mu\nu}^{(\text{visc})}$$

### 3.2 SDF Vacuum Foam Decomposition (Two-Fluid Representation)

The non-equilibrium quantum vacuum behaves as a two-phase anisotropic fluid consisting of:

1. **A Coherent Zero-Point Condensate** ($T_{\mu\nu}^{(\text{cond})}$) behaving as an elastic, negative-pressure medium ($w_{\text{cond}} \to -1$).
2. **A Thermal/Incoherent Fluctuating Halo Component** ($T_{\mu\nu}^{(\text{fluc})}$) induced by baryonic shear strain, with non-zero anisotropic stress ($\Pi_{\mu\nu}$):

$$T_{\mu\nu}^{(\text{SDF})} = T_{\mu\nu}^{(\text{cond})} + T_{\mu\nu}^{(\text{fluc})}$$

Explicitly:

$$T_{\mu\nu}^{(\text{cond})} = -\rho_{\text{vac}}^{(0)} g_{\mu\nu}$$

$$T_{\mu\nu}^{(\text{fluc})} = \rho_{\text{foam}}(r) u_\mu u_\nu + P_r(r) \hat{r}_\mu \hat{r}_\nu + P_\perp(r) \left( g_{\mu\nu} + u_\mu u_\nu - \hat{r}_\mu \hat{r}_\nu \right)$$

where:

- $\rho_{\text{foam}}(r)$ is the induced polarization energy density.
- $P_r(r)$ is the radial pressure component.
- $P_\perp(r)$ is the tangential pressure component.

The anisotropy parameter $\Delta(r) \equiv P_\perp(r) - P_r(r)$ is governed by the shear stress of differential galactic rotation:

$$\Delta(r) = \mu_{\text{foam}} r \frac{\mathrm{d}}{\mathrm{d}r} \left( \frac{v(r)}{r} \right)$$

where $\mu_{\text{foam}}$ is the dynamic shear viscosity of the quantum lattice foam.

---

## 4. The Radial Unfreezing Mechanism $\xi(r)$

A central failure of static cold dark matter profiles (NFW) [@NFW1996; @NFW1997] in dwarf and low-surface-brightness (LSB) systems is the persistence of steep cusps ($\rho \propto r^{-1}$), whereas observations demonstrate flat cores ($\rho \propto r^0$) [@deBlok2010CoreCusp; @deBlok2008THINGS]. Cored alternatives include the Burkert [@Burkert1995] and Einasto [@Einasto1965] profiles.

In the SDF framework, this transition is governed by an **order-parameter activation function**, termed the **Radial Unfreezing Function $\xi(r)$**:

$$\xi(r) = \frac{1}{2} \left[ 1 + \tanh\left( \frac{r - R_{\text{freeze}}}{\Delta R_{\text{core}}} \right) \right]$$

Alternatively expressed in acceleration space relative to Milgrom's scale $a_0 \approx 1.2 \times 10^{-10} \text{ m/s}^2$:

$$\xi(a) = \left[ 1 + \left( \frac{a_0}{a_{\text{bar}}(r)} \right)^\eta \right]^{-\frac{1}{2\eta}}$$

### Physical Regimes of $\xi(r)$

| Regime | Condition | Vacuum Foam State | Dynamical Consequence |
| :--- | :--- | :--- | :--- |
| **Interior Core** | $r \ll R_{\text{freeze}}$ ($a_{\text{bar}} \gg a_0$) | **Frozen Lattice** ($\xi \to 0$) | Newtonian behavior; vacuum shear is suppressed; no dark core anomaly. |
| **Transition Zone** | $r \approx R_{\text{freeze}}$ ($a_{\text{bar}} \sim a_0$) | **Phase Liquefaction / Shear Excitation** | Rapid unfreezing; strain leads to mass-enhancement polarization. |
| **Asymptotic Disk** | $r \gg R_{\text{freeze}}$ ($a_{\text{bar}} \ll a_0$) | **Fully Polarized Foam** ($\xi \to 1$) | Flat rotation curves; $v(r) \to v_\infty$, the **total** asymptotic circular speed. |

The effective mass distribution $M_{\text{eff}}(r)$ observed gravitationally is given by:

$$M_{\text{eff}}(r) = M_{\text{bar}}(r) + \xi(r) M_{\text{polarization}}(r)$$

where:

$$M_{\text{polarization}}(r) = 4\pi \int_0^r \rho_{\text{foam}}(r') r'^2 \mathrm{d}r' = \frac{a_0 r^2}{G} \left[ \sqrt{1 + \frac{4 G M_{\text{bar}}(r)}{a_0 r^2}} - 1 \right]$$

---

## 5. Hydrodynamic and Kinetic Equations of Motion

Taking the covariant divergence of the total stress-energy tensor:

$$\nabla^\mu T_{\mu\nu}^{(\text{total})} = 0 \implies \nabla^\mu T_{\mu\nu}^{(\text{bar})} = - \nabla^\mu T_{\mu\nu}^{(\text{SDF})} \equiv \mathcal{F}_\nu^{(\text{backreaction})}$$

For stationary axisymmetric galactic discs in cylindrical coordinates $(R, \phi, z)$, projecting the steady-state Boltzmann moment equation onto the radial direction yields the modified radial Jeans/Euler equilibrium [@BinneyTremaine2008]:

$$\frac{v_\phi^2(R)}{R} = \frac{\partial \Phi_{\text{bar}}}{\partial R} + \frac{1}{\rho_{\text{bar}}} \frac{\partial (\rho_{\text{bar}} \sigma_{R}^2)}{\partial R} + \frac{\sigma_R^2 - \sigma_\phi^2}{R} + \mathcal{F}_R^{(\text{SDF})}$$

where the vacuum dielectric foam radial force per unit mass is:

$$\mathcal{F}_R^{(\text{SDF})}(R) = \frac{1}{\rho_{\text{bar}}} \nabla_\mu \Pi^{\mu R}_{\text{foam}} + \xi(R) \frac{G M_{\text{polarization}}(R)}{R^2}$$

A physical solution must also leave the disc gravitationally stable against axisymmetric perturbations, i.e. $Q > 1$ in the Toomre criterion [@Toomre1964Q]; a model that flattens the curve by destabilising the disc is excluded independently of the rotation-curve fit.

In cold gaseous and thin-disk stellar components ($\sigma \ll v_\phi$), this reduces to the observed rotation curve equation:

$$v_{\text{circ}}^2(R) = R \left( \left| \frac{\partial \Phi_{\text{bar}}}{\partial R} \right| + \mathcal{F}_R^{(\text{SDF})} \right) \equiv v_{\text{bar}}^2(R) + v_{\text{SDF}}^2(R)$$

---

## 6. Mapping to the Benchmark Galaxy: NGC 6503

For the benchmark dwarf spiral **NGC 6503** (SPARC database catalogue), the explicit parameters entering into this theoretical framework are mapped as follows:

- **Distance ($D$):** $6.26$ Mpc — the distance at which the SPARC mass model is built [@Lelli2016SPARC], and the one every statistic in this release uses. The earlier $5.27$ Mpc, which had no reference in this bibliography, is withdrawn as the adopted value; its effect on the fit is tabulated under *Distance sensitivity* in `00_Master_Paper.md`.
- **Baryonic Subsystems:**
  - Gas disk: $v_{\text{gas}}(r)$ derived from $21\text{ cm}$ H I surface density ($M_{\text{HI}} \approx 1.7 \times 10^9 M_\odot$) [@Freeland2010; @Lelli2016SPARC].
  - Stellar disk: $v_{\text{disk}}(r)$ normalized at $\Upsilon_{3.6}=1$; the population-synthesis range $\Upsilon_{3.6}\approx0.48-0.55\,M_\odot/L_\odot$ [@Lelli2016SPARC] is quoted for context only, because the statistics reported below adopt $\Upsilon_{\rm disk}=0.62$.
- **Observed Characteristics:**
  - $R_{\text{freeze}} \approx 1.83 \text{ kpc}$ (onset of unfreezing) — an **adopted** value of this release, not a fitted one [@SDFRadialUnfreezing2026].
  - Transition index $\eta \approx 1.0 - 1.2$ — inherited from the superseded acceleration-space form and **not used** by the canonical $\zeta(r)$ closure [@SDFRadialUnfreezing2026].
  - Asymptotic velocity $v_\infty \approx 116.2 \pm 2.4 \text{ km/s}$ [@Lelli2016SPARC] — the **total** asymptotic circular speed, an observable, not a model excess term.

On the full 31-bin SPARC curve for NGC 6503 the canonical closure with the adopted parameters ($\Upsilon_{\rm disk}=0.62$, $R_0=1.83$ kpc, $\Delta R=0.46$ kpc, $v_\infty=116.2$ km s$^{-1}$) gives $\chi^2=39.607$ with $N=31$, $p=1$, hence $\chi_\nu^2=1.320$ — which fails the manuscript's own $<1.25$ target, and the retracted $\chi_\nu^2<1.05$ claim is withdrawn. The model does eliminate the cusp/core mismatch by construction, since $\zeta(r)$ is smooth and has no singular core term, but that is a property of the ansatz rather than a fit result. The halo concentration-virial mass tension is not addressed by this closure at all and should not be claimed as resolved here.

---

## 7. Mathematical Symbols & Parameter Dictionary

| Symbol | Definition | Physical Units |
| :--- | :--- | :--- |
| $g_{\mu\nu}$ | Background geometric metric tensor | Dimensionless |
| $\tilde{g}_{\mu\nu}$ | Effective dielectric foam metric | Dimensionless |
| $T_{\mu\nu}^{(\text{bar})}$ | Baryonic stress-energy tensor | $\text{J} \cdot \text{m}^{-3}$ |
| $T_{\mu\nu}^{(\text{SDF})}$ | Spacetime Dielectric Foam stress-energy | $\text{J} \cdot \text{m}^{-3}$ |
| $\xi(r)$ | Radial unfreezing activation parameter | Dimensionless ($0 \le \xi \le 1$) |
| $R_{\text{freeze}}$ | Lattice phase-transition core radius | $\text{kpc}$ |
| $a_0$ | Characteristic vacuum polarization acceleration | $\text{m} \cdot \text{s}^{-2} \approx 1.2 \times 10^{-10}$ |
| $\Delta(r)$ | Vacuum stress anisotropy ($P_\perp - P_r$) | $\text{Pa}$ |
| $\mu_{\text{foam}}$ | Dynamic shear viscosity of the quantum foam | $\text{Pa} \cdot \text{s}$ |

## Consolidated radial-unfreezing convention (supersedes drifted notation)

The project-wide order parameter is $\zeta(r)=\frac12[1+\tanh((r-R_0)/\Delta R)]$, with $R_0=1.83$ kpc and $\Delta R=0.46$ kpc.

**$v_\infty$ is the total asymptotic circular speed** $v_{\rm obs}(r\to\infty)$ — an observable ($116.2\pm2.4$ km/s for NGC 6503), not an additive model component. The executable phenomenological closure is therefore

$$v_{\rm model}^2(r)=v_{\rm bar}^2(r)+\left[v_\infty^2-v_{\rm bar}^2(r)\right]\zeta(r),$$

so that $v\to v_{\rm bar}$ as $r\to0$ and $v\to v_\infty$ exactly as $r\to\infty$.

The superseded form $v_{\rm model}^2=v_{\rm bar}^2+v_\infty^2\zeta(r)$ is **withdrawn**: it treats $v_\infty$ as an excess, asymptotes to $\sqrt{v_{\rm bar}^2+v_\infty^2}=121.6$ km/s against an observed $115.3$, and overshoots by up to $+33$ km/s near $r=2.46$ kpc.

On the 31-bin SPARC table (`data/NGC6503_rotmod.dat`) the corrected closure gives $\chi^2=39.607$ with $N=31$, $p=1$, hence $\chi_\nu^2=1.320$ for the adopted parameters, improving to $1.190$ when $v_\infty$, $R_0$ and $\Delta R$ are fitted ($v_\infty=116.27$, $R_0=1.583$ kpc, $\Delta R=1.036$ kpc). The retracted $\chi_\nu^2=0.942$ and outer slope $-0.018$ km s$^{-1}$ kpc$^{-1}$ are withdrawn; the model is exactly flat beyond $r\approx6$ kpc, so its computed OLS outer slope is $+2\times10^{-6}$.

Two distinct objects appear in this document and must not be conflated: the theoretical polarization mass $M_{\rm polarization}(r)$ of §4, derived from $a_0$ and $M_{\rm bar}$, and the phenomenological closure above, whose scale $v_\infty$ is taken from the data. Only the former is a prediction; the latter is an interpolation, and $v_\infty$ must be counted as a fitted parameter in any $\chi_\nu^2$.

These are fixed adopted values in this release, not a derivation from the microscopic SDF tensor. Prior symbols $\xi$, $r_h$, $R_{\rm trans}$, $r_{\rm crit}$ and the separate acceleration-threshold activation formula are legacy descriptions, not alternate simultaneous parameterizations. SI acceleration conversion uses $1$ kpc $=3.0857\times10^{19}$ m. See the equation snippet and verification script for operational definitions.

