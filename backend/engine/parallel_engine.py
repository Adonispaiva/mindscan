"""
Parallel Engine — MindScan

Executa algoritmos independentes em paralelo lógico.
(Threading real pode ser adicionado depois.)
"""

from typing import Callable, Dict, Any, List


class ParallelEngine:
    def __init__(self, tasks: List[Callable]):
        self.tasks = tasks

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for task in self.tasks:
            output = task(context)
            if not isinstance(output, dict):
                raise TypeError("Task must return dict")
            results.update(output)
        return results
