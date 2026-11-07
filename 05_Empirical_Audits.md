# 05_Empirical_Audits.md

## 1. Executive Summary & Audit Scope

This document details the rigorous empirical validation and falsification auditing pipeline for the **Space-Defect / Active Tensor-Foam Framework (SDF)** applied to the dwarf spiral galaxy **NGC 6503**. 

Standard gravity frameworks rely on postulating cold dark matter halos with NFW-like profiles [@NFW1996; @NFW1997] to reconcile the discrepancy between the observed flat rotation curves and the Keplerian decline predicted by the visible baryonic distribution. The failure of that prescription in the cores of dwarf and LSB systems is the core-cusp problem [@deBlok2010CoreCusp; @deBlok2008THINGS], one of the small-scale challenges catalogued by Bullock & Boylan-Kolchin [@Bullock2017SmallScale]; the competing MOND description [@Milgrom1983a; @Milgrom1983b; @Famaey2012MOND] is built around the Radial Acceleration Relation [@McGaugh2016RAR]. Under the SDF framework, the gravitational anomaly is modeled as an emerging topological response: radial unfreezing of underlying vacuum defects driven by the local baryonic matter density gradient.

The empirical audit focuses on four distinct physical and observational pillars:

1. **Rotation Curve Reconstruction**: Auditing the baseline Baryon vs. Observed ($v_{\text{obs}}$) curve fit against the unfreezing response profile.
2. **Dynamic Vacuum Friction & Dissipation Bounds**: Quantitative assessment of whether the moving baryonic disk experiences spurious vacuum drag or unphysical friction torque.
3. **Residual Variance & Chi-Squared Optimization**: Minimization of the metric loss $\chi^2_{\nu}$ across the radial kinematic bins of NGC 6503. The 31-bin SPARC table is bundled as `data/NGC6503_rotmod.dat` [@Lelli2016SPARC]; every statistic in this document is computed from it, and the earlier statement that only the seven selected stations were available is withdrawn.
4. **Asymptotic Convergence & Outer Halo Boundary Conditions**: Verifying that the metric recovers Minkowski flat spacetime without runaway scalar/tensor polarization at $r \to \infty$.

---

## 2. Core Mathematical Formalism Under Audit

> **Superseded.** The two formulae in this section ($\Phi_v$ with an acceleration threshold $\kappa g/a_0$, and the $\mathcal{F}_{\rm geom}$ form factor) are the legacy parameterisation. They are retained for provenance only and are **not** the canonical closure. The release uses $\zeta(r)=\tfrac12[1+\tanh((r-R_0)/\Delta R)]$ with $v_{\rm model}^2=v_{\rm bar}^2+(v_\infty^2-v_{\rm bar}^2)\zeta(r)$; see section 6 and `03_radial_unfreezing_dynamics.md`.

### 2.1. The Radial Unfreezing Order Parameter

The vacuum lattice state is modulated by the scalar order parameter $\Phi_v(r) \in [0, 1]$, describing the transition from an inactive (frozen) defect ground state to an active topological tensor excitation:

$$
\Phi_v(r) = 1 - \exp\left( - \left[ \frac{\kappa \cdot \nabla \Phi_{\text{bar}}(r)}{a_0} \right]^{\beta} \right)
$$

Where:

- $\nabla \Phi_{\text{bar}}(r) = \frac{v_{\text{bar}}^2(r)}{r} = g_{\text{bar}}(r)$ represents the Newtonian gravitational acceleration induced by baryonic matter (gas + stellar disk + bulge).
- $a_0 \approx 1.20 \times 10^{-10} \text{ m/s}^2$ is the characteristic MONDian acceleration threshold.
- $\kappa$ is the dimensionless coupling constant of the active lattice foam.
- $\beta$ is the critical exponent controlling the transition sharpness (verified empirically around $\beta \approx 1.0 - 1.2$).

### 2.2. Effective Circular Velocity

The total circular velocity predicted by the framework is governed by:

$$
v_{\text{model}}^2(r) = v_{\text{bar}}^2(r) + v_{\text{foam}}^2(r)
$$

Where the defect lattice contribution is parameterized as:

$$
v_{\text{foam}}^2(r) = \Phi_v(r) \cdot \sqrt{G M_{\text{eff}}(r) a_0} \cdot \mathcal{F}_{\text{geom}}(r/R_d)
$$

Here, $\mathcal{F}_{\text{geom}}$ is the geometric form-factor accounting for the thin-disk topology of NGC 6503 ($R_d \approx 1.72 \text{ kpc}$).

---

## 3. Audit Artifacts & Empirical Datasets

The audit suite inspects and cross-references artifacts produced during pipeline runs:

- `ngc6503_curve_audit.png`: Comparative decomposition ($v_{\text{obs}}$, $v_{\text{gas}}$, $v_{\text{disk}}$, $v_{\text{model}}$).
- `ngc6503_friction_audit.png`: Upper limits on dynamical friction and momentum loss $\tau_{\text{loss}} / \tau_{\text{Hubble}}$.
- `radial_unfreezing_verification.png`: Spatial derivative profile of $\frac{d\Phi_v}{dr}$ identifying the unfreezing front.
- `sparc_ngc6503_unfreezing_fit.png`: Normalized residual distribution against SPARC 1-sigma observational error bands.

### 3.1. The SPARC rotation curve of NGC 6503

The table below is the **real** SPARC mass-model file [@Lelli2016SPARC], `data/NGC6503_rotmod.dat`, reproduced verbatim: 31 radial bins, $0.76$–$23.50$ kpc, adopted distance $6.26$ Mpc, MD5 `a9e481e375d7ed7d430342f406e917b1`. Provenance and both retrieval sources are in `data/PROVENANCE.md`.

$V_{\rm bar}$ is built with the SPARC convention $V_{\rm bar}^2=V_{\rm gas}\lvert V_{\rm gas}\rvert+\Upsilon_{\rm disk}V_{\rm disk}^2$ at $\Upsilon_{\rm disk}=0.62$; $v_{\rm model}$ uses the canonical closure with $R_0=1.83$ kpc, $\Delta R=0.46$ kpc, $v_\infty=116.2$ km s$^{-1}$. Residuals beyond $2\sigma$ are bold.

| $r$ (kpc) | $V_{\rm obs}\pm\sigma$ | $V_{\rm gas}$ | $V_{\rm disk}$ | $V_{\rm bar}$ | $v_{\rm model}$ | $(v_{\rm obs}-v_{\rm model})/\sigma$ |
|---:|---:|---:|---:|---:|---:|---:|
| 0.76 | 77.0 $\pm$ 10.0 | 4.04 | 70.72 | 55.8 | 56.7 | **+2.03** |
| 1.52 | 100.0 $\pm$ 5.0 | 7.62 | 123.17 | 97.3 | 101.5 | -0.29 |
| 2.28 | 110.0 $\pm$ 2.0 | 9.72 | 142.64 | 112.7 | 115.8 | **-2.89** |
| 3.04 | 118.0 $\pm$ 2.0 | 12.42 | 134.42 | 106.6 | 116.2 | +0.92 |
| 3.79 | 121.0 $\pm$ 2.0 | 13.35 | 121.97 | 97.0 | 116.2 | **+2.40** |
| 4.55 | 121.0 $\pm$ 2.0 | 14.78 | 111.53 | 89.1 | 116.2 | **+2.40** |
| 5.31 | 117.0 $\pm$ 2.0 | 17.55 | 103.23 | 83.2 | 116.2 | +0.40 |
| 6.07 | 116.0 $\pm$ 2.0 | 19.20 | 96.65 | 78.5 | 116.2 | -0.10 |
| 6.83 | 116.0 $\pm$ 2.0 | 20.33 | 91.96 | 75.2 | 116.2 | -0.10 |
| 7.59 | 116.0 $\pm$ 2.0 | 21.66 | 87.62 | 72.3 | 116.2 | -0.10 |
| 8.35 | 115.0 $\pm$ 1.0 | 22.79 | 83.25 | 69.4 | 116.2 | -1.20 |
| 9.11 | 115.0 $\pm$ 1.0 | 23.92 | 79.58 | 67.1 | 116.2 | -1.20 |
| 9.86 | 116.0 $\pm$ 1.0 | 24.84 | 76.81 | 65.4 | 116.2 | -0.20 |
| 10.64 | 117.0 $\pm$ 1.0 | 25.46 | 74.18 | 63.7 | 116.2 | +0.80 |
| 11.38 | 117.0 $\pm$ 1.0 | 26.38 | 71.50 | 62.2 | 116.2 | +0.80 |
| 12.12 | 118.0 $\pm$ 1.0 | 27.20 | 69.18 | 60.9 | 116.2 | +1.80 |
| 12.86 | 117.0 $\pm$ 1.0 | 28.13 | 67.04 | 59.8 | 116.2 | +0.80 |
| 13.70 | 116.0 $\pm$ 1.0 | 28.74 | 64.84 | 58.6 | 116.2 | -0.20 |
| 14.44 | 115.0 $\pm$ 1.0 | 28.64 | 63.05 | 57.3 | 116.2 | -1.20 |
| 15.18 | 117.0 $\pm$ 1.0 | 28.33 | 61.39 | 56.0 | 116.2 | +0.80 |
| 15.91 | 116.0 $\pm$ 1.0 | 28.13 | 59.88 | 54.9 | 116.2 | -0.20 |
| 16.65 | 115.0 $\pm$ 2.0 | 28.33 | 58.45 | 54.0 | 116.2 | -0.60 |
| 17.49 | 115.0 $\pm$ 2.0 | 28.23 | 56.93 | 53.0 | 116.2 | -0.60 |
| 18.23 | 115.0 $\pm$ 2.0 | 27.82 | 55.71 | 51.9 | 116.2 | -0.60 |
| 18.97 | 114.0 $\pm$ 2.0 | 27.20 | 54.55 | 50.8 | 116.2 | -1.10 |
| 19.71 | 115.0 $\pm$ 2.0 | 26.90 | 53.46 | 50.0 | 116.2 | -0.60 |
| 20.45 | 114.0 $\pm$ 2.0 | 26.69 | 52.44 | 49.2 | 116.2 | -1.10 |
| 21.29 | 116.0 $\pm$ 2.0 | 26.49 | 51.35 | 48.3 | 116.2 | -0.10 |
| 22.03 | 115.0 $\pm$ 3.0 | 26.18 | 50.44 | 47.6 | 116.2 | -0.40 |
| 22.76 | 118.0 $\pm$ 4.0 | 25.87 | 49.61 | 46.9 | 116.2 | +0.45 |
| 23.50 | 115.0 $\pm$ 10.0 | 25.46 | 48.79 | 46.1 | 116.2 | -0.12 |

With $N=31$ and $p=1$ ($v_\infty$ is an observable of this same galaxy, so it counts as fitted):

$$\chi^2=39.607,\qquad \chi_\nu^2=1.320 .$$

That **fails** the $<1.25$ target this document sets for itself.

**Where the fit fails.** Four bins exceed $2\sigma$, and all four sit at or inside the transition: $+2.03\sigma$ at 0.76 kpc, $-2.89\sigma$ at 2.28 kpc, $+2.40\sigma$ at 3.79 and 4.55 kpc. The outer curve is reproduced almost exactly, but only because the closure imposes $v\to v_\infty$ there by construction — it is not a prediction.

**Fitted parameters.** With $\Upsilon_{\rm disk}=0.5$ held fixed and $v_\infty$, $R_0$, $\Delta R$ free ($p=3$): $v_\infty=116.27$ km s$^{-1}$, $R_0=1.583$ kpc, $\Delta R=1.036$ kpc, $\chi^2=33.326$, $\chi_\nu^2=1.190$. The data prefer a transition roughly twice as wide and slightly closer in than the adopted values.

**A degeneracy that matters.** Leaving all four parameters free drives $\Upsilon_{\rm disk}$ to its lower bound of 0.01 ($\chi_\nu^2=1.106$). The fit prefers to switch the stellar disk off and generate the entire curve from $v_\infty\zeta(r)$. A model that can discard its own baryons and still fit is not testing a baryon-driven mechanism.

**Withdrawn.** An earlier revision of this section carried seven rows at $r=0.41, 1.23, 2.46, \dots$ kpc with a $v_{\rm SDF}$ column. Those rows are **not** a subset of SPARC — none of their radii or velocities appears in the official file — and the file they came from has been deleted. The statistics derived from them ($\chi_\nu^2=2.716$, and before that $0.942$) are void.

**Distance, resolved.** The release fits the table at its own $D=6.26$ Mpc [@Lelli2016SPARC]; the $5.27\pm0.15$ Mpc quoted in earlier revisions is withdrawn as the adopted value because it had no reference in this bibliography and would have required rescaling the data. The rescale was nevertheless run as a sensitivity check ($r\propto D$, mass-model components $\propto\sqrt{D}$, $V_{\rm obs}$ unchanged): the adopted parameters then give $\chi^2=37.299$, $\chi^2_\nu=1.243$, and the transition fit gives $1.143$ with $v_\infty=116.27$, $R_0=1.196$ kpc, $\Delta R=0.893$ kpc. So the $<1.25$ verdict flips with the distance ($1.320$ at 6.26 Mpc, $1.243$ at 5.27 Mpc). That is a statement about the distance scale, not about the model, and the marginal pass at 5.27 Mpc must not be quoted as a success. Reproduce with `--distance-mpc 5.27`.

## 4. Audit Execution & Verification Scripts

The verification engine is `Scripts/radial_unfreezing_verification.py`.

The inline "audit engine snippet" that previously appeared here has been **removed**. It implemented a different kernel ($1-\exp[-(\kappa g/a_0)^{\beta}]$), injected a fixed `v_asymp = 116.2` boost, used a `dof = len(r) - 2` convention, and its `__main__` block printed `[PASS] Reduced Chi^2 target verified` without computing anything. None of that matched the canonical release.

Run the real script instead:

```bash
python Scripts/radial_unfreezing_verification.py --self-test              # asserts the reproduced values
python Scripts/radial_unfreezing_verification.py --fit                    # chi2 ladder
python Scripts/radial_unfreezing_verification.py                          # adopted-parameter chi2
python Scripts/radial_unfreezing_verification.py --export-csv data/ngc6503_sparc.csv
```

The self-test asserts the canonical definition ($v_\infty$ is the total asymptote; the legacy additive form must stay rejected; no overshoot), verifies that the bundled file really is the 31-bin SPARC table at 6.26 Mpc, **recomputes** $\chi^2=39.607$, $\chi_\nu^2=1.320$ and the zero outer slope from `data/NGC6503_rotmod.dat`, requires the optimiser to reach $\chi^2\le33.5$, and reproduces the 5.27 Mpc sensitivity value ($\chi^2=37.299$) including the fact that it crosses the $<1.25$ threshold.

The script is standard-library only: the bounded Nelder-Mead used for the fits is implemented inside it, so no numpy or scipy is needed.

## 5. Dynamical Vacuum Friction Audit

A major falsification criterion for non-standard vacuum models is anomalous orbital decay: if the vacuum lattice behaved as an imperfect fluid with non-zero shear viscosity, orbiting bodies would experience a secular drag

$$\mathbf{F}_{\text{drag}} = -\Gamma_{\text{eff}}\,\mathbf{v}.$$

**Status of this section.** The two constraints quoted here are *assumptions of the framework*, not results. Neither is derived anywhere in this archive, and no code computes them; they are recorded so that a future implementation has a stated target to be tested against. The condition $\nabla_\mu T^{\mu\nu}_{(\text{foam})}=0$ is imposed by construction in the two-fluid ansatz of `03_Theoretical_BaseLayer.md` §3 (it follows from the Bianchi identity once the foam sector is written conservatively) [@BinneyTremaine2008], and the bounds

$$\Gamma_{\text{eff}} \le 10^{-42}\ \text{s}^{-1}, \qquad \frac{\tau_{\text{decay}}}{\tau_{\text{Hubble}}} > 10^4$$

are the tolerance this project sets for itself [@SDFRadialUnfreezing2026]. The earlier wording that these bounds "prove" the absence of detectable kinematic friction on the H I disk over $13.8$ Gyr is **withdrawn**: an uncomputed bound proves nothing, and the H I kinematics of NGC 6503 are in any case consistent with no measurable drag at the precision of the existing data [@Begeman1987; @Freeland2010]. The audit row for $\Gamma_{\text{eff}}$ therefore reads UNVERIFIED, as it does in §6.

## 6. Audit Verdict & Synthesis

| Criterion | Target threshold | Audited value | Status |
| :--- | :--- | :--- | :--- |
| $\chi_\nu^2$ (NGC 6503, 31 SPARC bins, $p=1$) | $<1.25$ | $1.320$ | **FAIL** |
| $\chi_\nu^2$ with $v_\infty,R_0,\Delta R$ fitted ($p=3$) | $<1.25$ | $1.190$ | Pass, but $\Upsilon_{\rm disk}$ held fixed by hand |
| Retracted $\chi_\nu^2$ | — | $0.942$ | **WITHDRAWN — not reproducible** |
| Interim $\chi_\nu^2$ | — | $2.716$ | **WITHDRAWN — computed on invented data** |
| Outer-halo flatness slope | $\lvert dv/dr\rvert<0.05$ km s$^{-1}$ kpc$^{-1}$ | $+2\times10^{-6}$ | Pass only vacuously: the model is flat by construction |
| Core cusp at $r\to0$ | no singularity | $\zeta(r)$ smooth, $v\to v_{\rm bar}$ | Pass by construction of the ansatz |
| Stellar $\Upsilon_*$ | $[0.5,0.8]\,M_\odot/L_\odot$ | $0.62$ adopted; $0.01$ when fitted | **FAIL when fitted** |
| Vacuum drag $\Gamma_{\rm eff}$ | below detectability | not computed | **UNVERIFIED** |

**Verdict.** Judged by the weighted least-squares statistic of Bevington & Robinson [@BevingtonRobinson2003], and using the tolerance conventions of this project [@SDFRadialUnfreezing2026], the model on real data is a mediocre fit, not a good one. The adopted parameter set gives $\chi_\nu^2=1.320$ and fails the stated threshold. Fitting the transition recovers $1.190$, but only with the stellar mass-to-light ratio pinned by hand; released, the fit collapses $\Upsilon_{\rm disk}$ to 0.01 and stops being a baryonic model at all.

Two rows are passes only in a degenerate sense. The outer slope is zero because the closure forces $v\to v_\infty$; the core is smooth because $\zeta$ is a tanh. Neither is evidence about the galaxy.

The dissipation bound $\Gamma_{\rm eff}\le10^{-42}$ s$^{-1}$ and the ratio $\tau_{\rm decay}/\tau_{\rm Hubble}>10^4$ of section 5 remain theoretical expectations. No code in this archive computes them.

**Open items.** (i) Explain why the fit wants $\Upsilon_{\rm disk}\to0$; if the answer is that $v_\infty\zeta(r)$ alone suffices, the framework is a two-parameter interpolation and should be presented as one. (ii) The four $>2\sigma$ bins all lie in the transition, which is exactly where the ansatz has no independent content. (iii) Once a cited TRGB distance exists, the 5.27 Mpc rescale should be promoted from sensitivity row to primary fit — and the manuscript will then have to report that its threshold is passed by $0.007$ in $\chi^2_\nu$, which is not a robust margin.

## Canonical audit resolution and evidence qualification

The earlier $\Phi_v$ acceleration activation, the separate transition-radius factor, and every audit-row value predating this revision are superseded. The canonical activation is $\zeta(r)=\tfrac12[1+\tanh((r-1.83\,\mathrm{kpc})/(0.46\,\mathrm{kpc}))]$ and the canonical closure is

$$v_{\rm model}^2(r)=v_{\rm bar}^2(r)+\left[v_\infty^2-v_{\rm bar}^2(r)\right]\zeta(r),$$

with $v_\infty=116.2$ km s$^{-1}$ the **total** asymptotic circular speed. SI conversion is $1$ kpc $=3.0857\times10^{19}$ m. The statistic is $\chi_\nu^2=\sum[(v_{\rm obs}-v_{\rm model})/\sigma]^2/(N-p)$.

Reproduced from the 31-bin SPARC table with $p=1$: $\chi^2=39.607$, $\chi_\nu^2=1.320$. With $\Upsilon_{\rm disk}=0.5$ fixed and $v_\infty,R_0,\Delta R$ fitted ($p=3$): $\chi^2=33.326$, $\chi_\nu^2=1.190$.

Withdrawn: $\chi_\nu^2=0.942$ (not reproducible), $\chi_\nu^2=2.716$ (computed on a seven-row table that is not SPARC), and $dv/dr=-0.018$ km s$^{-1}$ kpc$^{-1}$ (unreachable; the model is exactly flat beyond $r\approx6$ kpc, computed slope $+2\times10^{-6}$). $\Upsilon_*=0.62\,M_\odot/L_\odot$ is an adopted value in the first row, not a fitted one.

The data are now real and bundled, so the earlier caveat that no observational table was present no longer applies. The distance scale is settled at the file's 6.26 Mpc, with the 5.27 Mpc alternative quantified above. What remains unverified are the dissipation claims, for which no code exists.
