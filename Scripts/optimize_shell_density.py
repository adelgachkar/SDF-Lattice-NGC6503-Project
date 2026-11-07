import sys
from pathlib import Path

# Add project root to sys.path so sdf_lattice can be imported directly
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import math
import numpy as np
from scipy.optimize import minimize

from sdf_lattice.nodes.shell_density_governor import ShellDensityProperties, ShellDensityGovernorNode
from sdf_lattice.physics import load_rotmod, baryonic_squared, chi_squared

# Load SPARC data
data_path = project_root / "data" / "NGC6503_rotmod.dat"
rows, distance = load_rotmod(data_path)

v_obs = [row["v_obs"] for row in rows]
err = [row["err"] for row in rows]

def objective(params):
    alpha, r0 = params
    # Safety constraints: parameters must be strictly positive
    if alpha <= 0 or r0 <= 0:
        return 1e10
    
    node = ShellDensityGovernorNode(props=ShellDensityProperties(r_scale=r0, alpha=alpha))
    
    v_preds = []
    for row in rows:
        v_bar2 = max(0.0, baryonic_squared(row, ups_disk=0.62, ups_bul=0.0))
        v_bar = math.sqrt(v_bar2)
        out = node.compute({"r": row["r"], "v_bar": v_bar})
        v_preds.append(out["v_predicted"])
    
    # Calculate chi2 (n_parameters=2: alpha and r0)
    chi2, _ = chi_squared(v_obs, v_preds, err, n_parameters=2)
    return chi2

# Initial guess
initial_guess = [1.0, 1.83]
bounds = [(0.05, 5.0), (0.1, 15.0)] # Bounds for alpha and r_scale

print(f"Starting optimization for NGC 6503 (31 SPARC points)...")
result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')

if result.success:
    opt_alpha, opt_r0 = result.x
    dof = len(rows) - 2 # 31 - 2 = 29
    reduced_chi2 = result.fun / dof
    print(f"\n==========================================")
    print(f"Optimization Successful!")
    print(f"Optimal Alpha (alpha)   : {opt_alpha:.6f}")
    print(f"Optimal R_scale (r0)   : {opt_r0:.6f} kpc")
    print(f"Minimum Chi2 (chi2)    : {result.fun:.6f}")
    print(f"Reduced Chi2 (chi2_nu) : {reduced_chi2:.6f} (dof={dof})")
    print(f"==========================================")
else:
    print(f"\nOptimization failed: {result.message}")
