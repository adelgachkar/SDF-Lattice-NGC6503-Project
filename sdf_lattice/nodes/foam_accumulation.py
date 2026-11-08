"""Produced-foam accumulation constraint and its radial governor."""
from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Any, Dict

from .base import Node


@dataclass(frozen=True)
class ProducedFoamProperties:
    r_0: float = 1.83
    delta_r: float = 0.46
    v_inf: float = 116.20
    c_foam: float = 1.61e19


class ProducedFoamAccumulationGovernor:
    """Smooth radial transition and linearly accumulated foam stress."""
    def __init__(self, properties: ProducedFoamProperties | None = None):
        self.properties = properties if properties is not None else ProducedFoamProperties()

    @staticmethod
    def _finite_real(value: Any, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must be a finite real number")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{name} must be a finite real number")
        return result

    def zeta(self, r: Real) -> float:
        radius = self._finite_real(r, "r")
        return 0.5 * (1.0 + math.tanh((radius - self.properties.r_0) / self.properties.delta_r))

    def cumulative_foam_integral(self, r: Real) -> float:
        radius = self._finite_real(r, "r")
        return self.properties.c_foam * radius


class FoamAccumulationNode(Node):
    type_name = "produced_foam_accumulation"
    NODE_TYPE = type_name

    def __init__(self, node_id: str, params: Dict[str, Any] | None = None):
        super().__init__(node_id, params)
        self.sigma_vac = self._parameter("sigma_vac", 1.0)
        self.v_inf = self._parameter("v_inf", 116.20)
        self.r_0 = self._parameter("r_0", 1.83)
        self.delta_r = self._parameter("delta_r", 0.46)
        self.c_foam = self._parameter("c_foam", 1.61e19)
        if self.delta_r <= 0:
            raise ValueError("delta_r must be strictly positive")
        self.governor = ProducedFoamAccumulationGovernor(
            ProducedFoamProperties(self.r_0, self.delta_r, self.v_inf, self.c_foam)
        )

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(inputs, dict):
            raise TypeError("inputs must be a mapping")
        if "r" not in inputs:
            raise ValueError("FoamAccumulationNode requires 'r' in inputs")
        r = self.governor._finite_real(inputs["r"], "r")
        # Velocity is optional for zeta/foam-only evaluation; default to rest.
        v = self.governor._finite_real(inputs.get("v", 0.0), "v")
        if r <= 0:
            raise ValueError("r must be strictly positive")
        zeta = self.governor.zeta(r)
        v_foam = self.v_inf * math.sqrt(zeta)
        cumulative_stress = self.governor.cumulative_foam_integral(r)
        acceleration = v * v / r
        return {
            "r": r,
            "zeta": zeta,
            "v_foam": v_foam,
            "c_foam": self.c_foam,
            "cumulative_stress": cumulative_stress,
            "acceleration": acceleration,
        }
