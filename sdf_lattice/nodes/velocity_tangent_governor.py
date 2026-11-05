"""Velocity-tangent negative-feedback governor node for SDF-Lattice.

Stateless valve: overspeed smoothly throttles positive drive pressure.
All speeds and pressures use caller-chosen, internally consistent units.
"""
from __future__ import annotations

import math
from numbers import Real
from typing import Any, Dict

from .base import Node


class VelocityTangentGovernorNode(Node):
    """Throttle positive drive pressure when tangential speed exceeds a setpoint.

    Let u=|v_t|-v_set. For u<=0 the valve is fully open. For u>0:
        f_open = f_min + (1-f_min)/(1 + gain*(u/v_scale)**2)
    Positive drive is multiplied by f_open; zero/negative drive passes unchanged.
    Thus feedback never amplifies the drive and cannot obstruct collapse pressure.
    The smooth, memoryless rule needs no hidden state or graph feedback edge.

    Inputs: tangential_velocity (required, signed scalar), drive_pressure (optional, 0).
    Outputs: speed, speed_error, valve_fraction, regulated_pressure, feedback_pressure.
    feedback_pressure = regulated_pressure - drive_pressure (<=0 for positive drive).
    """
    type_name = "velocity_tangent_governor"
    NODE_TYPE = type_name

    def __init__(self, node_id: str, params: Dict[str, Any] | None = None):
        super().__init__(node_id, params)
        self.speed_setpoint = self._parameter("speed_setpoint", 1.0)
        self.speed_scale = self._parameter("speed_scale", 0.25)
        self.gain = self._parameter("gain", 1.0)
        self.min_open = self._parameter("min_open", 0.0)
        if self.speed_setpoint < 0.0:
            raise ValueError("speed_setpoint must be non-negative")
        if self.speed_scale <= 0.0:
            raise ValueError("speed_scale must be strictly positive")
        if self.gain < 0.0:
            raise ValueError("gain must be non-negative")
        if not 0.0 <= self.min_open <= 1.0:
            raise ValueError("min_open must be in [0, 1]")

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

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, float]:
        if not isinstance(inputs, dict):
            raise TypeError("inputs must be a mapping")
        if "tangential_velocity" not in inputs:
            raise ValueError("missing required input: tangential_velocity")
        signed_velocity = self._finite_real(inputs["tangential_velocity"], "tangential_velocity")
        drive = self._finite_real(inputs.get("drive_pressure", 0.0), "drive_pressure")
        speed = abs(signed_velocity)
        error = max(0.0, speed - self.speed_setpoint)
        if error == 0.0 or self.gain == 0.0:
            opening = 1.0
        else:
            ratio = error / self.speed_scale
            opening = self.min_open + (1.0 - self.min_open) / (1.0 + self.gain * ratio * ratio)
        regulated = drive * opening if drive > 0.0 else drive
        return {
            "speed": speed,
            "speed_error": error,
            "valve_fraction": opening,
            "regulated_pressure": regulated,
            "feedback_pressure": regulated - drive,
        }
