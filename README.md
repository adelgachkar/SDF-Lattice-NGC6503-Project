# SDF-Lattice NGC 6503

Reference implementation and audit record for the **radial-unfreezing closure** of the
Spacetime Dielectric Foam (SDF / QVEX) framework, tested against the SPARC rotation curve of
the dwarf spiral galaxy **NGC 6503**.

The canonical closure is

$$v_{\rm model}^2(r) = v_{\rm bar}^2(r) + \bigl[v_\infty^2 - v_{\rm bar}^2(r)\bigr]\zeta(r),
\qquad \zeta(r) = \tfrac12\Bigl[1 + \tanh\frac{r - R_0}{\Delta R}\Bigr]$$

with $v_\infty$ the **total** asymptotic circular speed — an observable of the galaxy, not an
additive model component — and
$v_{\rm bar}^2 = V_{\rm gas}\lvert V_{\rm gas}\rvert + \Upsilon_{\rm disk}V_{\rm disk}^2$
(SPARC convention).

> **خلاصه.** این مخزن، کد و دادهٔ لازم برای بازتولید بستهٔ $\zeta(r)$ و آمارهٔ $\chi^2_\nu$ روی جدول
> واقعی SPARC کهکشان NGC 6503 را کنار متن مقاله نگه می‌دارد. همهٔ اعداد با استاندارد-کتابخانهٔ
> پایتون و بدون وابستگی بیرونی بازمحاسبه می‌شوند؛ وضعیت برازش — از جمله شکستِ آستانهٔ خودِ مقاله —
> در ادامه و در `PUBLICATION_AUDIT.md` ثبت شده است.

## Verification status (read this before quoting any number)

Computed from the bundled 31-bin SPARC table. `p` counts parameters fitted to those same
points, and $v_\infty$ counts as fitted because it is taken from the galaxy being modelled.

| Model | $p$ | $\Upsilon_{\rm disk}$ | $v_\infty$ (km/s) | $R_0$ (kpc) | $\Delta R$ (kpc) | $\chi^2$ | $\chi^2_\nu$ |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Adopted parameters | 1 | 0.62 | 116.20 | 1.83 | 0.46 | 39.607 | **1.320** ❌ |
| $\Upsilon_{\rm disk}=0.5$ fixed, rest free | 3 | 0.50 | 116.27 | 1.583 | 1.036 | 33.326 | 1.190 |
| All four free | 4 | 0.010 ⚠️ | 116.28 | 0.985 | 1.042 | 29.864 | 1.106 |

The first row is the manuscript's own parameter set and it **fails** the project's
$\chi^2_\nu < 1.25$ target. The third row shows why the fit is not a baryon-driven
measurement: released, $\Upsilon_{\rm disk}$ runs to its lower bound and the stellar disk is
switched off, leaving a two-parameter smooth step. The outer curve is reproduced almost
exactly because the closure imposes $v \to v_\infty$ there by construction.

**Withdrawn and not to be quoted:** $\chi^2_\nu = 0.356$, $0.942$ and $2.716$; the outer slope
$-0.018$ km s⁻¹ kpc⁻¹; $V_\infty = 108.50$ km/s, $r_h = 1.886$ kpc, $\xi = 1.565$ kpc.

**Distance: 6.26 Mpc (resolved).** The release fits the table at the distance it was built
for. The previously quoted $5.27 \pm 0.15$ Mpc is withdrawn as the adopted value — it had no
reference and would have required rescaling the data — but it is kept as a sensitivity check:
rescaling ($r \propto D$, mass-model components $\propto \sqrt{D}$, $V_{\rm obs}$ unchanged) moves
the adopted-parameter statistic from $\chi^2_\nu = 1.320$ to **1.243**, i.e. across the
$<1.25$ threshold. The verdict is therefore distance-sensitive and must always be quoted with
the distance it belongs to. Reproduce both with `--distance-mpc`; see `data/PROVENANCE.md`.

A full itemised audit — what was retracted, why, and what remains unverified — is in
[`PUBLICATION_AUDIT.md`](PUBLICATION_AUDIT.md).

## Install

Python 3.10+. No runtime dependencies.

```bash
git clone https://github.com/adelgachkar/SDF-Lattice-NGC6503-Project.git
cd SDF-Lattice-NGC6503-Project

pip install -e .            # installs the sdf_lattice package, no third-party deps
pip install -e ".[test]"    # adds pytest, needed only for the test suite
```

To install without touching your environment, use a virtual environment
(`python -m venv .venv && . .venv/bin/activate`; on Windows `.venv\Scripts\activate`).

On an offline machine, `pip` cannot fetch the build backend, so add
`--no-build-isolation` and make sure `setuptools>=77` is already installed:

```bash
pip install --no-build-isolation -e .
```

Verified in a clean virtual environment: `sdf-lattice-ngc6503` 0.1.0 installs with an MIT
license expression and no runtime `Requires-Dist` (only the `test` extra), and the test suite
passes against the installed package rather than the working directory. The isolated-build
route was not exercised here because this machine has no network access; it is the standard
route for an online install and needs no extra flags.

## Quickstart

```bash
# Recompute the adopted-parameter statistic from data/NGC6503_rotmod.dat
python Scripts/radial_unfreezing_verification.py

# Assert the canonical definition and every reproduced number (exit 0 = pass)
python Scripts/radial_unfreezing_verification.py --self-test

# chi-square ladder: v_inf adopted, transition fitted, disk released
python Scripts/radial_unfreezing_verification.py --fit

# same ladder on the table rescaled to the withdrawn 5.27 Mpc distance
python Scripts/radial_unfreezing_verification.py --fit --distance-mpc 5.27

# Regenerate the tidy CSV from the verbatim .dat file
python Scripts/radial_unfreezing_verification.py --export-csv data/ngc6503_sparc.csv

# Same-conditions fit: SDF vs NFW vs MOND on one table, one Upsilon, one p
python Scripts/model_comparison.py --self-test      # pinned numbers
python Scripts/model_comparison.py --write          # rewrite MODEL_COMPARISON.md

# Check that every bibliography entry is cited and every [@key] resolves
python Scripts/check_citations.py --list

# Tests (29 tests, 9 subtests)
python -m pytest -q
```

The verification script is standard-library only: its least-squares fit uses a bounded
Nelder–Mead routine implemented in the file, so no NumPy or SciPy is required. The same
numbers come out of `scipy.optimize.least_squares`, but that agreement was checked outside
the shipped code and is not part of it.

## Repository map

| Path | Contents |
| :--- | :--- |
| `00_Master_Paper.md` | Consolidated manuscript status: canonical values, reproduced statistics, retractions |
| `01_Abstract_Keywords.md` … `07_Conclusion.md` | Manuscript sections |
| `03_radial_unfreezing_dynamics.md` | Derivation of the closure (duplicated in `Equations_Snippets/`) |
| `References/08_References.bib` | Bibliography, 38 entries, all cited in the text |
| `data/NGC6503_rotmod.dat` | Verbatim SPARC mass-model file, 31 bins, MD5 `a9e481e375d7ed7d430342f406e917b1` |
| `data/PROVENANCE.md` | Retrieval sources, checksum, column schema, known corrections |
| `Scripts/radial_unfreezing_verification.py` | Executable verification, chi-square ladder, CSV export |
| `Scripts/model_comparison.py` | Same-conditions fit of SDF, NFW and MOND (two `mu` maps) with AIC/BIC |
| `MODEL_COMPARISON.md` | Generated comparison tables: fixed and free `Upsilon`, `N=31`, `p` counted per model |
| `Scripts/check_citations.py` | Citation-coverage checker (fails on uncited or undefined keys) |
| `sdf_lattice/` | Installable package: graph/node base classes and the velocity-tangent governor |
| `tests/` | Unit tests for the governor node and the shared physics kernels |
| `Assets/` | Audit plots produced by earlier pipeline revisions (see caveats in the audit) |
| `PUBLICATION_AUDIT.md` | Full audit: findings, fixes, remaining blockers |

## Data

The rotation curve is the real SPARC mass model for NGC 6503 (Lelli, McGaugh & Schombert
2016, AJ 152, 157), filed verbatim and retrieved from two independent byte-identical
copies. `data/PROVENANCE.md` records both sources, the MD5, the column meanings and the
distance conflict. If you use the data, cite the SPARC paper, not this repository.

## Citation

`CITATION.cff` is in the repository root, so GitHub's *Cite this repository* button works.
A BibTeX entry for the code:

```bibtex
@software{gachkar2026sdflattice,
  author  = {Gachkar, Adel},
  title   = {{SDF-Lattice NGC 6503: radial-unfreezing closure, verification code and audit record}},
  year    = {2026},
  version = {0.1.0},
  license = {MIT},
  url     = {https://github.com/adelgachkar/SDF-Lattice-NGC6503-Project}
}
```

For the rotation-curve data and the baryonic decomposition, cite:

```bibtex
@article{Lelli2016SPARC,
  author  = {Lelli, Federico and McGaugh, Stacy S. and Schombert, James M.},
  title   = {{SPARC}: Mass Models for 175 Disk Galaxies with {Spitzer} Photometry and Accurate Rotation Curves},
  journal = {The Astronomical Journal},
  volume  = {152},
  number  = {6},
  pages   = {157},
  year    = {2016},
  doi     = {10.3847/0004-6256/152/6/157}
}
```

## License

MIT — see [`LICENSE`](LICENSE). The license covers the code and the manuscript files in this
repository; the bundled SPARC data remain the property of their authors and are redistributed
here for reproducibility, with provenance recorded in `data/PROVENANCE.md`.
