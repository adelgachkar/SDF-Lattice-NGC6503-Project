# SDF-Lattice NGC 6503: Comprehensive Project & Manuscript Synthesis

## 1. Executive Summary & Data Provenance

- **Galaxy Target:** NGC 6503 (SPARC Mass-Model Table).
- **Radial Bins:** 31 bins spanning $0.76$ to $23.50$ kpc.
- **Adopted Distance ($D$):** $6.26$ Mpc [@Lelli2016SPARC], filed as `data/NGC6503_rotmod.dat` (MD5: `a9e481e375d7ed7d430342f406e917b1`).
- **Distance Sensitivity Note:** The historical $5.27 \pm 0.15$ Mpc (TRGB) distance scale is **withdrawn as the adopted value** due to lack of local bibliographic traceability. It is retained strictly as an empirical sensitivity check (rescaling $r \propto D$ and mass components $\propto \sqrt{D}$ shifts $\chi^2_\nu$ from $1.320$ to $1.243$).

---

## 2. Theoretical Closure & Mathematical Formulation

**Definition (binding):** $v_\infty$ is the **total** asymptotic circular speed, $v_{\rm obs}(r\to\infty)$, treated as an observable galaxy property rather than an additive component.

The canonical unfreezing closure is defined as:
$$v_{\rm model}^2(r)=v_{\rm bar}^2(r)+\left[v_\infty^2-v_{\rm bar}^2(r)\right]\zeta(r)$$

where the transition function is given by:
$$\zeta(r)=\frac{1}{2}\left[1+\tanh\left(\frac{r-R_0}{\Delta R}\right)\right]$$

- **Baryonic Component:** $v_{\rm bar}^2=V_{\rm gas}|V_{\rm gas}|+\Upsilon_{\s*Adap} V_{\rm disk}^2$ (SPARC convention).
- **Core Limit ($r\to 0$):** Recovers baryonic behavior smoothly ($\zeta(0) \approx 3.3 \times 10^{-4}$ with a minute core boost of $+0.05$ km s$^{-1}$).
- **Asymptotic Limit ($r\to \infty$):** Saturates exactly to $v_\infty$ with no overshoot.

---

## 3. Canonical Parameters & Reproduced Statistics

Computed by `Scripts/radial_unfreezing_verification.py` across 31 SPARC bins ($N=31, p$ = degrees of freedom):

- $\chi^2_\nu = \chi^2 / (N - p)$
- $\text{AIC} = \chi^2 + 2p$
- $\text{BIC} = \chi^2 + p \ln N$

| Model / Fit Variant | $p$ | $\Upsilon_{\rm disk}$ | $v_\infty$ (km/s) | $R_0$ (kpc) | $\Delta R$ (kpc) | $\chi^2$ | $\chi^2_\nu$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Adopted Canonical Values** | 1 | 0.62 | 116.20 | 1.83 | 0.46 | 39.607 | **1.320** |
| $\Upsilon_{\rm disk}=0.5$ fixed, rest free | 3 | 0.50 | 116.27 | 1.583 | 1.036 | 33.326 | **1.190** |
| All four parameters free | 4 | 0.010 ⚠️ | 116.28 | 0.985 | 1.042 | 29.864 | **1.106** |

*Note on ⚠️:* In the four-parameter free fit, $\Upsilon_{\rm disk}$ runs to its lower algorithmic boundary ($0.01$), switching off the stellar disk and reproducing the curve from the step transition alone (two-parameter smooth step behavior).

---

## 4. Cross-Model Benchmarks (SDF vs. MOND vs. NFW)

Evaluated under identical data conditions ($N=31$, $D=6.26$ Mpc, fixed $\Upsilon_{\rm disk} = 0.62$):

| Framework | Variant / Fit Description | $p$ | $\chi^2$ | $\chi^2_\nu$ | AIC | $\Delta\text{AIC}$ | BIC |
| :--- | :--- | :---: | ---: | ---: | ---: | ---: | ---: |
| **SDF (Closure)** | Canonical adopted ($v_\infty=116.2$) | 1 | 39.61 | **1.320** | 41.61 | 2.07 | 43.04 |
| **SDF (Transition)** | $v_\infty, R_0, \Delta R$ free (bound warning) | 3 | 33.54 | **1.198** | 39.53 | 0.00 | 43.84 |
| **MOND** | Standard interpolation ($\mu(x)=x/(1+x)$, $a_0$ free) | 1 | 100.12 | **3.337** | 102.12 | 62.59 | 103.56 |
| **Dark Matter** | NFW Halo ($\rho_s, r_s$ free) | 2 | 116.41 | **4.014** | 120.41 | 80.87 | 123.27 |
| **MOND** | Standard interpolation ($a_0$ fixed, prediction) | 0 | 122.34 | **3.947** | 122.34 | 0.00 | 122.34 |
| **MOND** | Simple interpolation ($\mu(x)=x/\sqrt{1+x^2}$, $a_0$ free) | 1 | 198.46 | **6.615** | 200.46 | 160.92 | 201.89 |

**Statistical Conclusion:** With a single active degree of freedom ($p=1$), the SDF lattice closure achieves a decisive statistical preference ($\Delta\text{AIC} > 60$) over standard MOND and NFW halo formulations.

---

## 5. Deprecated / Retracted Notation & Legacy Values

To ensure strict provenance tracking, the following legacy terms/values are formally superseded and withdrawn:

- **Retracted Closure Formula:** $v_{\rm model}^2 = v_{\rm bar}^2 + v_\infty^2 \zeta$ (overeshooting by up to $+33$ km s$^{-1}$ near $r = 2.46$ kpc).
- **Retracted Parameters:** $v_\infty = 108.50$ km s$^{-1}$, $r_h = 1.886$ kpc, $\xi = 1.565$.
- **Retracted Distance:** $5.27$ Mpc (retained only for sensitivity checks).
- **Legacy Symbols:** $\xi(r)$ is replaced by $\zeta(r)$; legacy scale names ($r_h$, $R_{\rm trans}$, $r_{\rm crit}$, $R_{\rm freeze}$) are fully deprecated in favor of $R_0$ and $\Delta R$.

---

## 6. Execution & Verification Commands

- **Self-Test assertions:** `python Scripts/radial_unfreezing_verification.py --self-test`
- **Chi-squared ladder fit:** `python Scripts/radial_unfreezing_verification.py --fit`
- **Cross-model comparison table:** `python Scripts/model_comparison.py --write`
