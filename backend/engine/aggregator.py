# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\aggregator.py
# Última atualização: 2025-12-11T09:59:20.792728

"""
MindScan — Generic Aggregator (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Agregar itens genéricos (blocos, listas, objetos, métricas)
- Uniformizar estrutura para uso em qualquer módulo downstream
"""

from typing import Dict, Any, List


class Aggregator:
    def __init__(self):
        self.items: List[Dict[str, Any]] = []

    def add(self, item: Dict[str, Any]):
        self.items.append(item)

    def extend(self, lst: List[Dict[str, Any]]):
        self.items.extend(lst)

    def export(self) -> Dict[str, Any]:
        return {
            "items": self.items,
            "count": len(self.items),
            "engine": "Aggregator(ULTRA)"
        }
