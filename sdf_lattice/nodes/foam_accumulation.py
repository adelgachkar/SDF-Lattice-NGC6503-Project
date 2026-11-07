"""
sdf_lattice.nodes.foam_accumulation
===================================
Governor node modeling quantum vacuum foam accumulation across galactic radii.
"""

from typing import Dict, Any
import numpy as np
from .base import Node


class FoamAccumulationGovernorNode(Node):
    """
    Computes cumulative vacuum foam acceleration g_foam(r) based on
    a radial threshold r_thresh and asymptotic velocity v_inf.
    """

    def __init__(self, node_id: str, params: Dict[str, Any] = None):
        super().__init__(node_id, params or {})
        self.sigma_vac = float(self.params.get("sigma_vac", 1.0))
        self.r_thresh = float(self.params.get("r_thresh", 0.5))
        self.v_inf = float(self.params.get("v_inf", 116.2))

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        r = np.asarray(inputs.get("r_kpc", 0.0), dtype=float)
        v_bar = np.asarray(inputs.get("v_bar", 0.0), dtype=float)

        # محاسبه شتاب فوم بر اساس عبور از آستانه شعاعی
        g_foam = np.where(
            r <= self.r_thresh,
            0.0,
            self.sigma_vac * (1.0 - np.exp(-(r - self.r_thresh))) * (self.v_inf**2 / np.maximum(r, 1e-6))
        )

        return {
            "g_foam": g_foam,
            "v_bar": v_bar,
            "r_kpc": r
        }
