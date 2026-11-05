from abc import ABC, abstractmethod
from typing import Any, Dict

class Node(ABC):
    def __init__(self, node_id: str, params: Dict[str, Any] | None = None):
        self.node_id = node_id
        self.params = params or {}

    @abstractmethod
    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass
