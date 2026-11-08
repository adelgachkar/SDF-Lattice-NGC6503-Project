from abc import ABC, abstractmethod
import math
from numbers import Real
from typing import Any, Dict


class Node(ABC):
    def __init__(self, node_id: str, params: Dict[str, Any] | None = None):
        self.node_id = node_id
        self.params = params if params is not None else {}

    def _parameter(self, name: str, default: Real) -> float:
        """Return a finite real-valued node parameter (booleans are not numbers here)."""
        value = self.params.get(name, default)
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must be a finite real number")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{name} must be a finite real number")
        return result

    @abstractmethod
    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
