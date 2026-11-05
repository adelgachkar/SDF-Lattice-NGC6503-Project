# SDF-Lattice-NGC6503 — Consolidated manuscript and verification status

## Scope and canonical release values

This master file resolves the project’s radial-unfreezing notation and parameter drift. Throughout this release use $\zeta(r)=\tfrac12[1+\tanh((r-R_0)/\Delta R)]$, with $R_0=1.83$ kpc, $\Delta R=0.46$ kpc, and $v_\infty=116.2$ km s$^{-1}$. Use $1$ kpc $=3.0857\times10^{19}$ m for SI conversions. Legacy parameter sets in earlier prose are superseded and must not be mixed with this specification.

The consolidated reported benchmarks are $\chi_\nu^2=0.942$, outer-halo slope $-0.018$ km s$^{-1}$ kpc$^{-1}$, and stellar $\Upsilon_*=0.62\,M_\odot/L_\odot$. They are **reported targets**, not independently re-fitted results in this delivery: no raw SPARC/WSRT table with uncertainties was present in the inspected archives. The pipeline implements the stated statistic and accepts such a table for reproducible calculation.

## Reproducibility and repository map

- Theory and conventions: `03_Theoretical_BaseLayer.md`.
- Data schema and pipeline: `04_Data_and_Pipeline.md`.
- Audit/evidence status: `05_Empirical_Audits.md`.
- Derivation: `Equations_Snippets/03_radial_unfreezing_dynamics.md`.
- Executable checks: `Scripts/radial_unfreezing_verification.py`.
- Bibliography: `References/08_References.bib`.

The former references to `active_tensor_foam.py` and a `nodes.pipeline_runner` entry point are not supplied as executable modules in the inspected project archive. This release uses the self-contained verification script above; it does not imply those missing modules were executed. Run `python Scripts/radial_unfreezing_verification.py --self-test`. A data-backed run requires CSV columns `r_kpc,v_obs_kms,v_bar_kms,sigma_kms`.

