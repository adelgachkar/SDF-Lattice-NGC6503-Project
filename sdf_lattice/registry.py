"""Factory registry for all built-in standalone SDF-Lattice nodes."""
from typing import Any, Dict, Optional, Tuple

class NodeRegistry:
    def __init__(self):
        self._factories = {}
    def register(self, type_name, factory):
        if type_name in self._factories:
            raise ValueError(f"already registered: {type_name}")
        self._factories[type_name] = factory
    def create(self, type_name, node_id, params: Optional[Dict[str, Any]] = None):
        try:
            factory = self._factories[type_name]
        except KeyError:
            raise KeyError(f"unknown node type: {type_name}")
        return factory(node_id, params)
    def types(self) -> Tuple[str, ...]:
        return tuple(sorted(self._factories))

def register_defaults(registry: NodeRegistry) -> None:
    from .nodes import (
        StrainTensorNode, PermittivityEnvelopeNode, VoidCouplingNode,
        ClosureConstraintsNode, SupercellCouplingNode, PeristalticPumpNode,
        RetardedCausalityNode, BerryDynamicsNode, BerryTorqueNode,
        CavityResilienceNode, PassthroughNode, VelocityTangentGovernorNode,
    )
    for cls in (StrainTensorNode, PermittivityEnvelopeNode, VoidCouplingNode,
                ClosureConstraintsNode, SupercellCouplingNode, PeristalticPumpNode,
                RetardedCausalityNode, BerryDynamicsNode, BerryTorqueNode,
                CavityResilienceNode, PassthroughNode, VelocityTangentGovernorNode):
        type_name = cls.__dict__.get("NODE_TYPE") or cls.__dict__.get("type_name")
        if not type_name or type_name == "base":
            type_name = cls.__name__
        registry.register(type_name, cls)
