"""
Unit tests for Produced Foam Accumulation Node and Governor
Author: Adel Gachkar
"""

import pytest
from sdf_lattice.nodes.foam_accumulation import (
    ProducedFoamProperties,
    ProducedFoamAccumulationGovernor,
    FoamAccumulationNode
)
from sdf_lattice.registry import registry


def test_foam_properties_defaults():
    props = ProducedFoamProperties()
    assert props.r_0 == 1.83
    assert props.delta_r == 0.46
    assert props.v_inf == 116.20
    assert props.c_foam == 1.61e19


def test_zeta_bounds():
    governor = ProducedFoamAccumulationGovernor()
    # At r = r_0, zeta should be exactly 0.5
    assert pytest.approx(governor.zeta(1.83), rel=1e-5) == 0.5
    # Far below r_0, zeta -> 0.0
    assert governor.zeta(0.0) < 0.01
    # Far above r_0, zeta -> 1.0
    assert governor.zeta(10.0) > 0.99


def test_cumulative_foam_integral():
    governor = ProducedFoamAccumulationGovernor()
    r_test = 2.0
    expected = 1.61e19 * 2.0
    assert pytest.approx(governor.cumulative_foam_integral(r_test)) == expected


def test_foam_accumulation_node_scalar_execution():
    node = FoamAccumulationNode(node_id="test_foam_1")
    outputs = node.compute({"r": 1.83, "v": 100.0})
    
    assert "zeta" in outputs
    assert "cumulative_stress" in outputs
    assert "acceleration" in outputs
    assert pytest.approx(outputs["zeta"]) == 0.5
    assert outputs["cumulative_stress"] == 1.61e19 * 1.83


def test_foam_accumulation_optional_velocity_and_required_radius():
    node = FoamAccumulationNode(node_id="test_foam_optional_v")
    output = node.compute({"r": 1.83})
    assert output["zeta"] == pytest.approx(0.5)
    assert output["acceleration"] == 0.0
    assert output["cumulative_stress"] == 1.61e19 * 1.83
    with pytest.raises(ValueError, match="'r'"):
        node.compute({"v": 100.0})


def test_registry_integration_foam():
    # Ensure node type is retrievable from registry
    node_cls = registry.get("produced_foam_accumulation")
    assert node_cls is FoamAccumulationNode
    
    instance = node_cls(node_id="reg_foam_node")
    assert instance.node_id == "reg_foam_node"
    assert instance.type_name == "produced_foam_accumulation"
