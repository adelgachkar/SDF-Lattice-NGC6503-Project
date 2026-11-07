"""
sdf_lattice.registry
====================
Central registry for graph nodes in the SDF-Lattice execution framework.
"""
from typing import Dict, Type
from .nodes.base import Node
from .nodes.vacuum_viscosity_governor import VacuumViscosityGovernorNode
from .nodes.velocity_tangent_governor import VelocityTangentGovernorNode


class NodeRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[Node]] = {}

    def register(self, type_name: str, node_cls: Type[Node]) -> None:
        if not issubclass(node_cls, Node):
            raise TypeError(f"Class {node_cls.__name__} must inherit from Node")
        self._registry[type_name] = node_cls

    def get(self, type_name: str) -> Type[Node]:
        if type_name not in self._registry:
            raise KeyError(f"Node type '{type_name}' is not registered.")
        return self._registry[type_name]

    def list_nodes(self) -> Dict[str, Type[Node]]:
        return dict(self._registry)


registry = NodeRegistry()


def register_defaults() -> None:
    registry.register("vacuum_viscosity_governor", VacuumViscosityGovernorNode)
    registry.register("velocity_tangent_governor", VelocityTangentGovernorNode)


register_defaults()
