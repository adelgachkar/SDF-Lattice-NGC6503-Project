"""Accumulated vacuum foam flux governor node for SDF-Lattice.

Computes the cumulative shell flux integral Φ_accum(r) and feeds back
the radial elastic tensor pressure to correct rotation velocities.
"""
from __future__ import annotations

import math
from numbers import Real
from typing import Any, Dict
import numpy as np

from .base import Node


class FoamAccumulationGovernorNode(Node):
    """Accumulate vacuum foam flux over spherical/cylindrical shells.

    Inputs: r_kpc (radial bins), v_bar (baryonic velocity).
    Outputs: r_kpc, g_foam, zeta, v_model.
    """
    type_name = "foam_accumulation_governor"
    NODE_TYPE = type_name

    def __init__(self, node_id: str, params: Dict[str, Any] | None = None):
        super().__init__(node_id, params)
        self.sigma_vac = self._parameter("sigma_vac", 1.0)
        self.r_thresh = self._parameter("r_thresh", 0.5)
        self.v_inf = self._parameter("v_inf", 116.2)
        self.r0 = self._parameter("r0", 1.83)
        self.dr = self._parameter("dr", 0.46)
        
        if self.r_thresh < 0.0:
            raise ValueError("r_thresh must be non-negative")
        if self.dr <= 0.0:
            raise ValueError("dr must be strictly positive")

    @staticmethod
    def _finite_real(value: Any, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must be a finite real number")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{name} must be a finite real number")
        return result

    def _parameter(self, name: str, default: float) -> float:
        return self._finite_real(self.params.get(name, default), name)

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(inputs, dict):
            raise TypeError("inputs must be a mapping")
        if "r_kpc" not in inputs or "v_bar" not in inputs:
            raise ValueError("missing required inputs: r_kpc and v_bar")

        r_kpc = np.asarray(inputs["r_kpc"], dtype=float)
        v_bar = np.asarray(inputs["v_bar"], dtype=float)

        # محاسبه مرتبه گذار zeta(r)
        z = 0.5 * (1.0 + np.tanh((r_kpc - self.r0) / self.dr))

        # انتگرال تجمعی شار فوم
        r_clipped = np.maximum(r_kpc, self.r_thresh)
        phi_accum = np.pi * self.sigma_vac * (np.square(r_clipped) - self.r_thresh**2)
        g_foam = np.divide(phi_accum, r_kpc, out=np.zeros_like(r_kpc), where=r_kpc > 1e-6)

        # برهمنهی در فضای مجذور سرعت
        v_bar_sq = np.square(v_bar)
        v_inf_sq = self.v_inf ** 2
        v_model_sq = v_bar_sq + (v_inf_sq - v_bar_sq) * z + g_foam * r_kpc
        v_model_sq = np.maximum(v_model_sq, 1e-12)
        v_model = np.sqrt(v_model_sq)

        return {
            "r_kpc": r_kpc,
            "g_foam": g_foam,
            "zeta": z,
            "v_model": v_model,
        }
