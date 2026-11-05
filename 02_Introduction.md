# 02. Introduction: Foundational Discrepancies in Galactic Dynamics & The SDF Vacuum Paradigm

## 1. Introduction: Galactic Rotational Discrepancies and the Vacuum Dielectric Transition

The contemporary description of galactic rotation curves relies predominantly on two competing paradigms:

1. **ΛCDM Cosmological Model**, which postulates massive, dissipationless Cold Dark Matter (CDM) halos governed by density profiles such as the Navarro-Frenk-White (NFW) model:
   $$\rho_{\text{NFW}}(r) = \frac{\rho_0}{\left(\frac{r}{r_s}\right)\left(1 + \frac{r}{r_s}\right)^2}$$
2. **Modified Newtonian Dynamics (MOND)** and its relativistic extensions (TeVeS/AQUAL), which modify the low-acceleration Poisson regime below $a_0 \approx 1.2 \times 10^{-10}\,\mathrm{m/s}^2$ using phenomenological interpolation functions $\mu(a/a_0)$.

While ΛCDM succeeds on cosmological scales, it faces severe galactic-scale tensions:

- **Core-Cusp Problem:** Simulated NFW halos predict steep inner cusps ($\rho \propto r^{-1}$), whereas observations consistently reveal constant-density flat cores ($\rho \propto r^0$).
- **Diversity Problem:** Rotation curves of galaxies with identical baryonic mass display vast kinematic variety that rigid NFW profile fits fail to capture.
- **Baryonic Tully-Fisher Relation (BTFR):** The tight empirical relation $M_b \propto v_f^4$ exhibits an intrinsic scatter smaller than stochastic dark matter accretion histories predict.

Conversely, MOND succeeds phenomenologically in matching galactic rotation curves but lacks a self-consistent, microphysical field-theoretic justification rooted in the quantum vacuum.

### 1.1 The Prototype Laboratory: Dwarf Spiral Galaxy NGC 6503

To rigorously test microphysical alternatives, we select **NGC 6503** as our primary observational benchmark. Characterized as an isolated, late-type spiral galaxy ($\mathrm{SA(s)cd}$) with a well-mapped rotation curve from H I 21-cm interferometry and H$\alpha$ spectroscopy, NGC 6503 features an acceleration profile $a_{\text{bar}}(r)$ that smoothly traverses the critical scale $a_0$ from its inner stellar disc ($r < 2.0\,\mathrm{kpc}$) to its gas-dominated outer boundary ($r \approx 15.0\,\mathrm{kpc}$), where $M_{\mathrm{HI}}(r) > M_\star(r)$. Its asymptotic rotation velocity reaches $v_{\text{obs}} \approx 116.2 \pm 2.4\,\mathrm{km/s}$. Under Newtonian dynamics, reproducing this velocity requires an invisible halo encompassing over $85\%$ of the total gravitational potential.

### 1.2 The Spacetime Dielectric Foam (SDF) Paradigm

We propose the **Spacetime Dielectric Foam / Quantum Vacuum Exotic eXcitations (QVEX)** framework. In this approach, spacetime is not an inert vacuum, but an active tensor network possessing intrinsic macroscopic shear viscosity $\eta_{\text{SDF}}$ and dielectric susceptibility $\chi_v$.

#### 1.2.1 Core Hypotheses of SDF

1. **Dynamic Lattice Elasticity:** Spacetime is modeled as a 5-tetrahedral vacuum lattice network.
2. **Topological Unfreezing Threshold:** At high accelerations ($|\nabla\Phi| \gg a_0$), lattice degrees of freedom are frozen, yielding standard general relativity ($T^{\mu\nu}_{\text{total}} \approx T^{\mu\nu}_{\text{bar}}$).
3. **Low-Field Polarization & Two-Fluid Coupling:** Below $|\nabla\Phi| \le a_0$, reduced kinematic gradients unfreeze collective lattice polarization modes, generating an effective gravitational polarization density $P^{\mu\nu}$ such that $T^{\mu\nu}_{\text{total}} = T^{\mu\nu}_{\text{bar}} + T^{\mu\nu}_{\text{SDF}}$.

Thus, the gravitational excess attributed to dark matter is identified as the **gravitational dielectric polarization of the quantum vacuum lattice** induced by the baryonic mass distribution.

### 1.3 Scope and Structure of this Investigation

The remainder of this paper is structured as follows:

- **[[03_Theoretical_BaseLayer]]** formulates the two-fluid stress-energy tensor, metric deformations, and radial unfreezing mechanics $\xi(r)$.
- **[[04_Data_and_Pipeline]]** details the SPARC observational data ingestion and Python solver pipeline.
- **[[05_Empirical_Audits]]** presents the 28-bin radial audits and kinematic verification.
- **[[06_Discussion_Comparative]]** evaluates comparative fits against ΛCDM and MOND.
- **[[07_Conclusion]]** summarizes physical implications and future outlook.
