"""
MindScan — Routing Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Controlar fluxo condicional entre engines
- Permitir pipelines dinâmicos
- Executar rotas baseadas em condições psicométricas
"""

from typing import Dict, Any, Callable, List
from datetime import datetime


class RoutingEngine:
    def __init__(self):
        self.routes = {}

    def add_route(self, name: str, condition: Callable[[Dict[str, Any]], bool], step: Callable):
        self.routes[name] = {
            "condition": condition,
            "step": step
        }

    def execute(self, block: Dict[str, Any]) -> Dict[str, Any]:
        executed = []

        for name, route in self.routes.items():
            if route["condition"](block):
                block = route["step"](block)
                executed.append({
                    "route": name,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })

        block["_routing"] = {
            "executed_routes": executed,
            "engine": "RoutingEngine(ULTRA)"
        }

        return block
