import pytest
from sdf_lattice.registry import registry
from sdf_lattice.nodes.foam_accumulation import FoamAccumulationNode

def test_registry_integration():
    node = registry.create("produced_foam_accumulation", "test_node")
    assert isinstance(node, FoamAccumulationNode)
    assert node.type_name == "produced_foam_accumulation"

def test_accumulation_values():
    node = registry.create("produced_foam_accumulation", "test_node")
    # تست در R0 (انتظار zeta=0.5)
    result = node.compute({"r": 1.83})
    assert abs(result["zeta"] - 0.5) < 1e-5
    assert abs(result["v_foam"] - (116.20 * (0.5**0.5))) < 1e-5
