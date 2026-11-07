# Radial unfreezing dynamics — canonical verification

## Definition and adopted constants

**$v_\infty$ is the total asymptotic circular speed**, $v_{\rm obs}(r\to\infty)$, an observable of the galaxy rather than a component of the model. For NGC 6503 it is $116.2\pm2.4$ km s$^{-1}$ [@Lelli2016SPARC]. The adopted values, the closure and the $\chi^2_\nu$ convention below are the canonical specification for this project [@SDFRadialUnfreezing2026].

The dimensionless activation function is fixed throughout the project as

$$\zeta(r)=\frac{1}{2}\left[1+\tanh\left(\frac{r-R_0}{\Delta R}\right)\right],$$

with $R_0=1.83\,\mathrm{kpc}$, $\Delta R=0.46\,\mathrm{kpc}$. For $r\geq0$, $0<\zeta<1$, $\zeta(R_0)=1/2$, and $\zeta$ increases monotonically. The exponential/tanh transition radius is the same adopted $R_0$; legacy names such as $r_h$, $R_{\rm trans}$, $r_{\rm crit}$, and $R_{\rm freeze}$ must not imply different fitted values.

The rotation-curve closure is

$$v_{\rm model}^2(r)=v_{\rm bar}^2(r)+\left[v_\infty^2-v_{\rm bar}^2(r)\right]\zeta(r).$$

The bracket is the squared excess the foam must supply at radius $r$, so the closure interpolates between the pure baryonic curve and the observed asymptote:

- $r\to0$: $\zeta\to0$, so $v\to v_{\rm bar}$. The frozen core is approximate, not exact — $\zeta(0)=3.3\times10^{-4}$ gives a residual boost of $+0.05$ km s$^{-1}$ at $v_{\rm bar}=35.8$ km s$^{-1}$.
- $r\to\infty$: $\zeta\to1$, so $v\to v_\infty$ exactly, with no overshoot.

**Do not use** the superseded additive form $v_{\rm model}^2=v_{\rm bar}^2+v_\infty^2\zeta(r)$. It treats $v_\infty$ as an excess and therefore asymptotes to $\sqrt{v_{\rm bar}^2+v_\infty^2}=121.6$ km s$^{-1}$ where the observed curve is $115.3$, overshooting by $+33$ km s$^{-1}$ near $r=2.46$ kpc. The script keeps it as `legacy_model_velocity` only so the regression test can assert it stays rejected.

All velocities are in km/s and the radius in the kernel is in kpc. If an acceleration is computed in SI units, convert first using

The adopted conversion follows the 2015 IAU definition of the astronomical unit and parsec [@IAU2015Parsec]:

$$1\,\mathrm{kpc}=3.0857\times10^{19}\,\mathrm{m},\qquad
 g_{\rm bar}=\frac{[10^3v_{\rm bar}(\mathrm{km/s})]^2}{r(\mathrm{kpc})\,3.0857\times10^{19}}\;\mathrm{m\,s^{-2}}.$$

Do not mix this SI conversion with the dimensionless activation kernel above. The earlier acceleration-threshold kernel $1-\exp[-(\kappa g/a_0)^\beta]$ is not the canonical radial-unfreezing prescription in this release.

## Statistics and reproduced benchmark

For observed velocities $v_i$, model predictions $m_i$, independent 1-$\sigma$ errors $\sigma_i$, and $p$ parameters estimated from the same $N$ points, the pipeline uses the standard weighted least-squares statistic [@BevingtonRobinson2003]:

$$\chi_\nu^2=\frac{1}{N-p}\sum_{i=1}^{N}\left(\frac{v_i-m_i}{\sigma_i}\right)^2 .$$

$v_\infty$ counts as fitted ($p$ includes it) whenever it is taken from the same galaxy being modelled.

The baryonic speed uses the SPARC convention [@Lelli2016SPARC], with the gas term keeping its sign so that a central gas depression does not add spurious mass:

$$v_{\rm bar}^2=V_{\rm gas}\lvert V_{\rm gas}\rvert+\Upsilon_{\rm disk}V_{\rm disk}^2+\Upsilon_{\rm bul}V_{\rm bul}^2 .$$

## Reproduced statistics on the real SPARC table

From `data/NGC6503_rotmod.dat` (31 bins, $0.76$–$23.50$ kpc, $D=6.26$ Mpc):

| Model | $p$ | $\Upsilon_{\rm disk}$ | $v_\infty$ | $R_0$ | $\Delta R$ | $\chi^2$ | $\chi^2_\nu$ |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Adopted values | 1 | 0.62 | 116.20 | 1.83 | 0.46 | 39.607 | **1.320** |
| $\Upsilon_{\rm disk}=0.5$ fixed, rest free | 3 | 0.50 | 116.27 | 1.583 | 1.036 | 33.326 | **1.190** |
| All four free | 4 | 0.010 ⚠️ | 116.28 | 0.985 | 1.042 | 29.864 | 1.106 |

The adopted parameter set gives $\chi_\nu^2=1.320$ and **fails** the manuscript's own $<1.25$ target. The third row is not usable as evidence: $\Upsilon_{\rm disk}$ collapses to its lower bound, so the fit is reproducing the curve from $v_\infty\zeta(r)$ alone with the stellar disk switched off.

$\Upsilon_*=0.62\,M_\odot/L_\odot$ is an adopted value in the first row, not a fitted one.

The retracted $\chi_\nu^2=0.942$ is not reproducible. The retracted outer slope $-0.018$ km s$^{-1}$ kpc$^{-1}$ is unreachable: $\zeta$ saturates to $1$ within $10^{-6}$ by $r\approx6$ kpc, so the computed OLS slope for $r\geq8$ kpc is $+2\times10^{-6}$ — the model is exactly flat by construction, and an outer slope is not a diagnostic of this closure.

**Interim values withdrawn.** An earlier revision quoted $\chi^2=16.295$ and $\chi_\nu^2=2.716$ from a seven-row `data/ngc6503_audit_rows.csv`. That file is not a subset of SPARC — none of its radii or velocities appears in the official table — so those numbers were computed on invented data and are superseded. The file has been deleted.

**Distance, resolved.** The release fits the table at its own $D=6.26$ Mpc [@Lelli2016SPARC]. The $5.27\pm0.15$ Mpc quoted in earlier revisions is withdrawn as the adopted value (no reference in this bibliography; it would require rescaling the data). Rescaling to 5.27 Mpc ($r\propto D$, components $\propto\sqrt{D}$, $V_{\rm obs}$ unchanged) gives $\chi^2=37.299$, $\chi^2_\nu=1.243$ for the adopted parameters, against $39.607$ and $1.320$ at 6.26 Mpc — the $<1.25$ threshold is crossed by the distance choice alone.

## Verification entry point

`Scripts/radial_unfreezing_verification.py --self-test` asserts the definition (corrected limits, legacy form rejected, no overshoot over $v_\infty$) and **recomputes** $\chi^2=39.607$, $\chi_\nu^2=1.320$ and the zero outer slope from the real 31-bin SPARC table. It then runs the fit and requires the optimiser to reach $\chi^2\le33.5$ with $R_0=1.583$, $\Delta R=1.036$. Nothing is asserted against a stored constant that is not also recomputed.

- `--fit` reports the $\chi^2$ ladder (adopted, $\Upsilon_{\rm disk}$ fixed at 0.5 with $v_\infty/R_0/\Delta R$ free, and all four free).
- `--sparc path.dat` selects a different rotmod file; `--upsilon`, `--R0`, `--DeltaR`, `--v-inf` override the adopted values.
- `--export-csv path.csv` writes the tidy named-column copy of the table.
- `--input path.csv` still evaluates the legacy four-column schema `r_kpc,v_obs_kms,v_bar_kms,sigma_kms`.
- `--n-parameters` sets the degrees of freedom; `--outer-min-kpc` sets the slope cutoff (default 8 kpc).

The script is standard-library only. The bounded Nelder-Mead used for the fits is included in the file so the check runs without numpy or scipy.
