from pathlib import Path
import math
import pytest
import numpy as np

from sdf_lattice.nodes.shell_density_governor import (
    ShellDensityProperties,
    ShellDensityGovernorNode,
)
from sdf_lattice.physics import load_rotmod, baryonic_squared, chi_squared


def test_shell_density_boundary_and_monotonicity():
    node = ShellDensityGovernorNode(props=ShellDensityProperties(r_scale=1.83, alpha=1.0))
    # At r = 0, accumulation factor must be exactly 0
    assert node.accumulation_factor(0.0) == 0.0
    
    # At r = r_scale, (r / 2r)^1.0 == 0.5
    assert math.isclose(node.accumulation_factor(1.83), 0.5, rel_tol=1e-5)
    
    # Monotonically increasing check
    radii = np.linspace(0.1, 25.0, 50)
    factors = node.accumulation_factor(radii)
    assert np.all(np.diff(factors) > 0)
    assert factors[-1] < 1.0


def test_shell_density_sparc_evaluation():
    """
    Evaluates empirical fit against the 31 SPARC points of NGC 6503.
    """
    data_path = Path("data/NGC6503_rotmod.dat")
    if not data_path.exists():
        pytest.skip("data/NGC6503_rotmod.dat not found in current path")

    rows, distance = load_rotmod(data_path)
    assert len(rows) == 31
    assert distance == 6.26

    # Test baseline scale parameters
    props = ShellDensityProperties(r_scale=1.83, alpha=1.0, v_inf=116.2)
    node = ShellDensityGovernorNode(props=props)

    v_obs = [row["v_obs"] for row in rows]
    err = [row["err"] for row in rows]
    
    v_preds = []
    for row in rows:
        v_bar2 = max(0.0, baryonic_squared(row, ups_disk=0.62, ups_bul=0.0))
        v_bar = math.sqrt(v_bar2)
        out = node.compute({"r": row["r"], "v_bar": v_bar})
        v_preds.append(out["v_predicted"])

    chi2, dof = chi_squared(v_obs, v_preds, err, n_parameters=1)
    chi2_nu = chi2 / dof

    print(f"\n[SPARC 31-pt Audit - Non-tanh Shell Density]: chi2 = {chi2:.4f}, chi2_nu = {chi2_nu:.6f} (dof={dof})")
    assert math.isfinite(chi2)
    assert dof == 30
