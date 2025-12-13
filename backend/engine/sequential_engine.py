"""
Sequential Engine — MindScan

Executa algoritmos em ordem determinística.
"""

from typing import Callable, Dict, Any, List


class SequentialEngine:
    def __init__(self, steps: List[Callable]):
        self.steps = steps

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for step in self.steps:
            output = step(context)
            if not isinstance(output, dict):
                raise TypeError("Step must return dict")
            results.update(output)
        return results
