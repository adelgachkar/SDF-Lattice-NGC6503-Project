"""
tests/test_vacuum_viscosity.py
==============================
Unit tests for the Vacuum Viscosity Governor physical model and computational node.
"""
import numpy as np
import pytest

from sdf_lattice.nodes.vacuum_viscosity_governor import (
    VacuumFoamProperties,
    VacuumViscosityGovernor,
    VacuumViscosityGovernorNode,
)
from sdf_lattice.registry import registry


def test_order_parameter_bounds():
    governor = VacuumViscosityGovernor()
    r = np.linspace(0.0, 10.0, 100)
    zeta = governor.order_parameter(r)

    assert np.all(zeta >= 0.0)
    assert np.all(zeta <= 1.0)
    assert np.all(np.diff(zeta) >= 0.0)


def test_cumulative_shell_volume():
    governor = VacuumViscosityGovernor()
    r = np.array([1.0, 2.0, 3.0])
    vols = governor.cumulative_shell_volume(r)
    expected = (4.0 / 3.0) * np.pi * (r ** 3)
    np.testing.assert_allclose(vols, expected, rtol=1e-6)


def test_viscoelastic_stress_keys_and_values():
    governor = VacuumViscosityGovernor()
    r = np.array([1.0, 2.0, 3.0])
    v = np.array([50.0, 80.0, 110.0])

    stresses = governor.compute_viscoelastic_stress(v, r)
    assert "gamma_dot" in stresses
    assert "sigma_viscous" in stresses
    assert "sigma_elastic" in stresses
    assert "sigma_total" in stresses

    assert np.all(stresses["sigma_total"] >= 0.0)
    np.testing.assert_allclose(
        stresses["sigma_total"],
        stresses["sigma_viscous"] + stresses["sigma_elastic"],
        rtol=1e-6,
    )


def test_governor_acceleration_direction():
    governor = VacuumViscosityGovernor()
    r = np.array([1.0, 2.0, 3.0])
    v = np.array([50.0, 80.0, 110.0])

    a_valve = governor.compute_governor_acceleration(v, r)
    # شتاب ترمزدهنده و میراکننده همیشه منفی یا صفر است
    assert np.all(a_valve <= 0.0)


def test_vacuum_viscosity_governor_node_execution():
    node = VacuumViscosityGovernorNode(
        node_id="vac_node_1",
        params={
            "props": {
                "eta_foam": 0.20,
                "mu_foam": 0.10,
                "v_inf": 120.0,
                "r_0": 2.0,
                "delta_r": 0.5,
            }
        },
    )

    inputs = {
        "v": np.array([40.0, 80.0, 120.0]),
        "r": np.array([1.0, 2.0, 4.0]),
    }

    outputs = node.compute(inputs)
    assert "stresses" in outputs
    assert "acceleration" in outputs
    assert np.all(outputs["acceleration"] <= 0.0)
    assert "sigma_total" in outputs["stresses"]


def test_registry_integration():
    node_cls = registry.get("vacuum_viscosity_governor")
    assert node_cls is VacuumViscosityGovernorNode

    instance = node_cls(node_id="reg_test")
    assert instance.node_id == "reg_test"
    assert instance.type_name == "vacuum_viscosity_governor"
