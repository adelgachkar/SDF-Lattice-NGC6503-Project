"""
sdf_lattice.nodes.shell_density_governor
========================================
Implements a deductive radial shell accumulation governor node
without phenomenological tanh transitions.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Any, Dict
import numpy as np

from .base import Node


@dataclass(frozen=True)
class ShellDensityProperties:
    r_scale: float = 1.83        # Characteristic core scale radius (kpc)
    alpha: float = 1.0          # Cumulative shell accumulation exponent
    v_inf: float = 116.2        # Asymptotic halo ceiling (km/s)


class ShellDensityGovernorNode(Node):
    type_name = "shell_density_governor"

    def __init__(self, node_id: str = "shell_density_node", props: ShellDensityProperties | None = None):
        super().__init__(node_id, params={})
        self.props = props or ShellDensityProperties()

    @classmethod
    def _validate_finite(cls, val: float, name: str) -> float:
        if not isinstance(val, (int, float)) or isinstance(val, bool) or not math.isfinite(float(val)):
            raise ValueError(f"{name} must be a finite real number")
        return float(val)

    def accumulation_factor(self, r: float | np.ndarray) -> float | np.ndarray:
        r_arr = np.asarray(r, dtype=np.float64)
        if np.any(r_arr < 0.0):
            raise ValueError("radius must be non-negative")
        if self.props.r_scale <= 0.0:
            raise ValueError("r_scale must be positive")
        if self.props.alpha <= 0.0:
            raise ValueError("alpha must be positive")
        
        factor = np.where(r_arr == 0.0, 0.0, (r_arr / (r_arr + self.props.r_scale)) ** self.props.alpha)
        return float(factor) if np.ndim(r) == 0 else factor

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(inputs, dict):
            raise TypeError("inputs must be a dictionary")
        if "r" not in inputs or "v_bar" not in inputs:
            raise ValueError("inputs must contain both 'r' and 'v_bar'")

        r = self._validate_finite(inputs["r"], "r")
        v_bar = self._validate_finite(inputs["v_bar"], "v_bar")
        if r < 0.0 or v_bar < 0.0:
            raise ValueError("r and v_bar must be non-negative")

        g_r = float(self.accumulation_factor(r))
        v_inf = self.props.v_inf
        v_bar2 = v_bar * v_bar
        excess = max(0.0, v_inf * v_inf - v_bar2)
        v_pred = math.sqrt(max(v_bar2 + excess * g_r, 1e-12))

        return {
            "r": r,
            "v_bar": v_bar,
            "accumulation_factor": g_r,
            "v_predicted": v_pred
        }
