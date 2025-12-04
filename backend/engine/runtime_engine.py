"""
MindScan — Runtime Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Responsável por:
- Orquestrar a execução sequencial e lógica do pipeline MindScan
- Registrar histórico de execução
- Garantir que cada módulo seja executado com coerência e integridade
"""

from typing import Dict, Any, List, Callable
from datetime import datetime


class RuntimeEngine:
    def __init__(self):
        self._steps: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []
        self._timeline: List[Dict[str, Any]] = []

    # -----------------------------------------------------
    # Registro de passos
    # -----------------------------------------------------
    def add_step(self, step: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self._steps.append(step)

    # -----------------------------------------------------
    # Execução completa
    # -----------------------------------------------------
    def run(self, block: Dict[str, Any]) -> Dict[str, Any]:
        data = dict(block)

        for step in self._steps:
            name = getattr(step, "__name__", "unknown_step")

            before_hash = hash(str(data))
            data = step(data)
            after_hash = hash(str(data))

            self._timeline.append({
                "step": name,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "input_hash": before_hash,
                "output_hash": after_hash
            })

        data["_runtime"] = {
            "steps_executed": len(self._steps),
            "timeline": self._timeline,
            "engine": "RuntimeEngine(ULTRA)"
        }

        return data
