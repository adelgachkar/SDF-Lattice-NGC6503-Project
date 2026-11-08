"""
SDF-Lattice NGC 6503 Registry Module
Author: Adel Gachkar
License: MIT (2026)
"""

from __future__ import annotations
from typing import Dict, Type, Any, Optional
from sdf_lattice.nodes.base import Node


class NodeRegistry:
    """رجیستری مرکزی برای مدیریت و ثبت انواع نودهای SDF-Lattice."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Node]] = {}

    def register(self, type_name: str, node_cls: Type[Node]) -> None:
        """ثبت یک کلاس نود مشتق‌شده از Node."""
        if not (isinstance(node_cls, type) and issubclass(node_cls, Node)):
            raise TypeError(
                f"Class '{node_cls.__name__ if hasattr(node_cls, '__name__') else node_cls}' "
                f"must be a subclass of 'Node'."
            )
        self._registry[type_name] = node_cls

    def get(self, type_name: str) -> Type[Node]:
        """بازیابی کلاس نود بر اساس نام ثبت‌شده."""
        if type_name not in self._registry:
            raise KeyError(
                f"Node type '{type_name}' is not registered. "
                f"Available types: {list(self._registry.keys())}"
            )
        return self._registry[type_name]

    def create(self, type_name: str, node_id: str, params: Optional[Dict[str, Any]] = None) -> Node:
        """Instantiate a registered node by type name."""
        node_cls = self.get(type_name)
        return node_cls(node_id=node_id, params=params)

    def list_nodes(self) -> list[str]:
        """فهرست تمام نودهای ثبت‌شده."""
        return list(self._registry.keys())


registry: NodeRegistry = NodeRegistry()


def register_defaults() -> None:
    """Register built-in nodes using local imports to avoid circular imports."""
    registrations = (
        ("vacuum_viscosity_governor", "sdf_lattice.nodes.vacuum_viscosity_governor", "VacuumViscosityGovernorNode"),
        ("shell_density_governor", "sdf_lattice.nodes.shell_density_governor", "ShellDensityGovernorNode"),
        ("foam_accumulation_governor", "sdf_lattice.nodes.foam_accumulation_governor", "FoamAccumulationGovernorNode"),
        ("velocity_tangent_governor", "sdf_lattice.nodes.velocity_tangent_governor", "VelocityTangentGovernorNode"),
        ("produced_foam_accumulation", "sdf_lattice.nodes.foam_accumulation", "FoamAccumulationNode"),
    )
    from importlib import import_module
    for type_name, module_name, class_name in registrations:
        try:
            node_cls = getattr(import_module(module_name), class_name)
        except (ImportError, ModuleNotFoundError) as exc:
            # Ignore only an unavailable optional node module; surface nested dependency errors.
            if exc.name and (exc.name == module_name or module_name.startswith(exc.name + ".")):
                continue
            raise
        registry.register(type_name, node_cls)


register_defaults()

__all__ = ["registry", "NodeRegistry", "register_defaults"]
