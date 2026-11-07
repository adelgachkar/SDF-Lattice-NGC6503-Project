# 02. Introduction: Foundational Discrepancies in Galactic Dynamics & The SDF Vacuum Paradigm

## 1. Introduction: Galactic Rotational Discrepancies and the Vacuum Dielectric Transition

The contemporary description of galactic rotation curves relies predominantly on two competing paradigms:

1. **ΛCDM Cosmological Model**, which postulates massive, dissipationless Cold Dark Matter (CDM) halos governed by density profiles such as the Navarro-Frenk-White (NFW) model [@NFW1996; @NFW1997]:
   $$\rho_{\text{NFW}}(r) = \frac{\rho_0}{\left(\frac{r}{r_s}\right)\left(1 + \frac{r}{r_s}\right)^2}$$
   Cored alternatives — Burkert [@Burkert1995] and Einasto [@Einasto1965] — are the standard empirical alternatives when the NFW cusp is disfavoured.
2. **Modified Newtonian Dynamics (MOND)** and its relativistic extensions (TeVeS/AQUAL) [@Milgrom1983a; @Milgrom1983b; @Famaey2012MOND], which modify the low-acceleration Poisson regime below $a_0 \approx 1.2 \times 10^{-10}\,\mathrm{m/s}^2$ using phenomenological interpolation functions $\mu(a/a_0)$.

While ΛCDM succeeds on cosmological scales, it faces severe galactic-scale tensions:

- **Core-Cusp Problem:** Simulated NFW halos predict steep inner cusps ($\rho \propto r^{-1}$), whereas observations consistently reveal constant-density flat cores ($\rho \propto r^0$) [@deBlok2010CoreCusp; @deBlok2008THINGS].
- **Diversity Problem:** Rotation curves of galaxies with identical baryonic mass display kinematic variety that rigid NFW profile fits fail to capture [@Bullock2017SmallScale].
- **Baryonic Tully-Fisher Relation (BTFR):** The tight empirical relation $M_b \propto v_f^4$ has an intrinsic scatter smaller than stochastic dark matter accretion histories predict [@Lelli2016SPARC]. The same regularity appears as the Radial Acceleration Relation (RAR), a tight correlation between observed and baryonic acceleration spanning roughly five decades [@McGaugh2016RAR].

Conversely, MOND succeeds phenomenologically in matching galactic rotation curves but lacks a self-consistent, microphysical field-theoretic justification rooted in the quantum vacuum [@Famaey2012MOND].

### 1.1 The Prototype Laboratory: Dwarf Spiral Galaxy NGC 6503

To rigorously test microphysical alternatives, we select **NGC 6503** as our primary observational benchmark. Characterized as an isolated, late-type spiral galaxy ($\mathrm{SA(s)cd}$) with a well-mapped rotation curve from WSRT H I 21-cm interferometry [@Begeman1987; @Begeman1991] and optical H$\alpha$ spectroscopy [@Begeman1991], NGC 6503 features an acceleration profile $a_{\text{bar}}(r)$ that smoothly traverses the critical scale $a_0$ from its inner stellar disc ($r < 2.0\,\mathrm{kpc}$) to its gas-dominated outer boundary ($r \approx 15.0\,\mathrm{kpc}$), where $M_{\mathrm{HI}}(r) > M_\star(r)$ [@Freeland2010]. Its asymptotic rotation velocity reaches $v_{\text{obs}} \approx 116.2 \pm 2.4\,\mathrm{km/s}$. That figure is the **total** asymptotic circular speed and is the quantity denoted $v_\infty$ throughout this manuscript: an observable of the galaxy, not a term added to the model, and the closure of §03 is built so that $v_{\rm model}\to v_\infty$ exactly. Under Newtonian dynamics the visible mass cannot supply that speed: at $9.1$ kpc the SPARC decomposition with $\Upsilon_{\rm disk}=0.62$ gives $V_{\rm bar}=67.1$ km s$^{-1}$ against $V_{\rm obs}=115$ km s$^{-1}$, so the baryonic terms account for only $\approx 34\%$ of $v_{\rm obs}^2$ [@Lelli2016SPARC]. That deficit is the anomaly this paper addresses; it is not a statement about any unseen mass fraction beyond that radius.

All radii and velocities used here are taken from the SPARC mass model for this galaxy [@Lelli2016SPARC], whose stellar mass-to-light ratios follow the same photometric decomposition; the maximum-rotation and mass scale are as discussed by Bottema [@Bottema1997].

### 1.2 The Spacetime Dielectric Foam (SDF) Paradigm

We propose the **Spacetime Dielectric Foam / Quantum Vacuum Exotic eXcitations (QVEX)** framework [@Gachkar2026SDF]. In this approach, spacetime is not an inert vacuum, but an active tensor network possessing intrinsic macroscopic shear viscosity $\eta_{\text{SDF}}$ and dielectric susceptibility $\chi_v$.

#### 1.2.1 Core Hypotheses of SDF

1. **Dynamic Lattice Elasticity:** Spacetime is modeled as a 5-tetrahedral vacuum lattice network.
2. **Topological Unfreezing Threshold:** At high accelerations ($|\nabla\Phi| \gg a_0$), lattice degrees of freedom are frozen, yielding standard general relativity ($T^{\mu\nu}_{\text{total}} \approx T^{\mu\nu}_{\text{bar}}$).
3. **Low-Field Polarization & Two-Fluid Coupling:** Below $|\nabla\Phi| \le a_0$, reduced kinematic gradients unfreeze collective lattice polarization modes, generating an effective gravitational polarization density $P^{\mu\nu}$ such that $T^{\mu\nu}_{\text{total}} = T^{\mu\nu}_{\text{bar}} + T^{\mu\nu}_{\text{SDF}}$.

Thus, the gravitational excess attributed to dark matter is identified as the **gravitational dielectric polarization of the quantum vacuum lattice** induced by the baryonic mass distribution.

### 1.3 Intellectual lineage

The idea that geometry itself carries the microscopic degrees of freedom has a long history. Wheeler's geometrodynamics and geon programme treated spacetime as a dynamical medium with structure at the Planck scale [@Wheeler1957Geons; @Wheeler1962Geometrodynamics]. Discrete or pre-geometric substrata have been explored as causal sets [@Bombelli1987CausalSets] and as loop-space quantum geometry [@Rovelli1990LoopSpace]. A parallel line derives gravity from thermodynamics, either from horizon entropy and equipartition [@Padmanabhan2010Emergent; @Padmanabhan2012Emergence] or from entanglement entropy in de Sitter space [@Verlinde2011Entropic], the latter extended to a candidate explanation of galactic dark phenomena [@Verlinde2017EmergentDM].

The specific machinery used here — a medium whose elastic and torsional defects are the gravitational sources — is the continuum theory of defects. Volterra distortions, disclinations and dislocations in an elastic continuum map onto torsion and curvature [@Kroener1981Continuum; @Puntigam1997Volterra], the three-dimensional case is worked out in detail [@Katanaev1992Defects; @Kleinert1989GaugeFields], and the coupling of spin to torsion gives the Einstein–Cartan class of theories [@Hehl1976MAG]. The multivalued-field formalism supplies the mathematical language for the phase winding that this work assigns to the lattice order parameter [@Kleinert2008Multivalued].

SDF differs from these in one testable respect: it does not modify the field equations of general relativity, but proposes that the *effective source* responds to acceleration, so that the same baryonic mass produces a different gravitational field in the frozen and unfrozen regimes.

### 1.4 Scope and Structure of this Investigation

The remainder of this paper is structured as follows:

- **[[03_Theoretical_BaseLayer]]** formulates the two-fluid stress-energy tensor, metric deformations, and radial unfreezing mechanics $\zeta(r)$.
- **[[04_Data_and_Pipeline]]** details the SPARC observational data ingestion and Python solver pipeline.
- **[[05_Empirical_Audits]]** presents the radial audits and kinematic verification on the full 31-bin SPARC curve.
- **[[06_Discussion_Comparative]]** evaluates comparative fits against ΛCDM and MOND [@Famaey2012MOND; @McGaugh2016RAR].
- **[[07_Conclusion]]** summarizes physical implications and future outlook.
