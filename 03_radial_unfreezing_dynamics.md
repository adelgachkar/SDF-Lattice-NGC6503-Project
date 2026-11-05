# Radial unfreezing dynamics — canonical verification

## Definition and adopted constants

The dimensionless activation function is fixed throughout the project as

$$\zeta(r)=\frac{1}{2}\left[1+\tanh\left(\frac{r-R_0}{\Delta R}\right)\right],$$

with $R_0=1.83\,\mathrm{kpc}$, $\Delta R=0.46\,\mathrm{kpc}$, and asymptotic scale $v_\infty=116.2\,\mathrm{km\,s^{-1}}$. For $r\geq0$, $0<\zeta<1$, $\zeta(R_0)=1/2$, and $\zeta$ increases monotonically. The exponential/tanh transition radius is the same adopted $R_0$; legacy names such as $r_h$, $R_{\rm trans}$, $r_{\rm crit}$, and $R_{\rm freeze}$ must not imply different fitted values.

The rotation-curve closure used by the verification script is

$$v_{\rm model}^2(r)=v_{\rm bar}^2(r)+v_\infty^2\zeta(r).$$

All velocities in that expression are in km/s and the radius in the kernel is in kpc. If an acceleration is computed in SI units, convert first using

$$1\,\mathrm{kpc}=3.0857\times10^{19}\,\mathrm{m},\qquad
 g_{\rm bar}=\frac{[10^3v_{\rm bar}(\mathrm{km/s})]^2}{r(\mathrm{kpc})\,3.0857\times10^{19}}\;\mathrm{m\,s^{-2}}.$$

Do not mix this SI conversion with the dimensionless activation kernel above. The earlier acceleration-threshold kernel $1-\exp[-(\kappa g/a_0)^\beta]$ is not the canonical radial-unfreezing prescription in this release.

## Statistics and reported benchmark

For observed velocities $v_i$, model predictions $m_i$, independent 1-$\sigma$ errors $\sigma_i$, and $p$ parameters estimated from the same $N$ points, the pipeline uses

$$\chi_\nu^2=\frac{1}{N-p}\sum_{i=1}^{N}\left(\frac{v_i-m_i}{\sigma_i}\right)^2.$$

The consolidated manuscript benchmark is $\chi_\nu^2=0.942$, outer-halo slope $dv/dr=-0.018\,\mathrm{km\,s^{-1}\,kpc^{-1}}$, and stellar $\Upsilon_*=0.62\,M_\odot/L_\odot$. These are reported project targets. The supplied archive does not contain the raw velocity/error table needed to independently reproduce the first two; the script supports CSV recomputation and labels that evidential limitation explicitly. The stellar M/L is a stated adopted benchmark, not calculated by the rotation-kernel routine.

## Verification entry point

`Scripts/radial_unfreezing_verification.py --self-test` checks mathematical identities and the SI constant. For data-backed values provide a CSV with `r_kpc,v_obs_kms,v_bar_kms,sigma_kms`; use `--n-parameters` to set the fit degrees of freedom. The outer slope is an ordinary least-squares slope of model speeds at radii greater than or equal to `--outer-min-kpc` (default 8 kpc). This slope convention and cutoff must be stated alongside any comparison.
