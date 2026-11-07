"""
sdf_lattice.nodes.vacuum_viscosity_governor
===========================================
Implements the continuous unit-surface vacuum stress feedback, radial shell
integration, and momentum node viscoelastic dissipation.
"""
from dataclasses import dataclass
from typing import Any, Dict
import numpy as np

from .base import Node


@dataclass(frozen=True)
class VacuumFoamProperties:
    sigma_vac: float = 1.0
    eta_foam: float = 0.15
    mu_foam: float = 0.08
    v_inf: float = 116.2
    r_0: float = 1.83
    delta_r: float = 0.46


class VacuumViscosityGovernor:
    def __init__(self, props: VacuumFoamProperties | None = None):
        self.props = props or VacuumFoamProperties()

    def order_parameter(self, r: np.ndarray) -> np.ndarray:
        r_arr = np.asarray(r, dtype=np.float64)
        return 0.5 * (1.0 + np.tanh((r_arr - self.props.r_0) / self.props.delta_r))

    def cumulative_shell_volume(self, r: np.ndarray) -> np.ndarray:
        r_arr = np.asarray(r, dtype=np.float64)
        return (4.0 / 3.0) * np.pi * (r_arr ** 3)

    def compute_viscoelastic_stress(self, v: np.ndarray, r: np.ndarray) -> dict:
        v_arr = np.asarray(v, dtype=np.float64)
        r_arr = np.maximum(np.asarray(r, dtype=np.float64), 1e-6)
        gamma_dot = v_arr / r_arr
        sigma_viscous = self.props.eta_foam * gamma_dot
        zeta = self.order_parameter(r_arr)
        velocity_saturation = np.clip(v_arr / self.props.v_inf, 0.0, 1.0)
        sigma_elastic = self.props.mu_foam * zeta * velocity_saturation
        sigma_total = sigma_viscous + sigma_elastic
        return {
            "gamma_dot": gamma_dot,
            "sigma_viscous": sigma_viscous,
            "sigma_elastic": sigma_elastic,
            "sigma_total": sigma_total,
        }

    def compute_governor_acceleration(self, v: np.ndarray, r: np.ndarray) -> np.ndarray:
        v_arr = np.asarray(v, dtype=np.float64)
        r_arr = np.asarray(r, dtype=np.float64)
        stresses = self.compute_viscoelastic_stress(v_arr, r_arr)
        sigma_total = stresses["sigma_total"]
        zeta = self.order_parameter(r_arr)
        ratio_sq = (v_arr / self.props.v_inf) ** 2
        a_valve = - ratio_sq * zeta * (sigma_total / (1.0 + ratio_sq))
        return a_valve


class VacuumViscosityGovernorNode(Node):
    type_name = "vacuum_viscosity_governor"
    NODE_TYPE = type_name

    def __init__(self, node_id: str, params: Dict[str, Any] | None = None):
        super().__init__(node_id, params)
        props_dict = self.params.get("props", {})
        self.governor = VacuumViscosityGovernor(
            props=VacuumFoamProperties(**props_dict) if props_dict else None
        )

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        v = inputs.get("v")
        r = inputs.get("r")
        
        if v is None or r is None:
            raise ValueError("VacuumViscosityGovernorNode requires 'v' and 'r' in inputs.")
        
        v_arr = np.asarray(v, dtype=float)
        r_arr = np.asarray(r, dtype=float)
        
        stresses = self.governor.compute_viscoelastic_stress(v_arr, r_arr)
        acceleration = self.governor.compute_governor_acceleration(v_arr, r_arr)
        
        return {
            "stresses": stresses,
            "acceleration": acceleration,
        }
