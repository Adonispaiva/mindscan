# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_summary.py
# Última atualização: 2025-12-11T09:59:20.620871

"""
Bússola Summary — Versão Ultra Superior
--------------------------------------------------------

Resumo executivo do mapa direcional:
- direção dominante
- equilíbrio vetorial
- interpretação estratégica
- risco de polarização
"""

from typing import Dict, Any


class BussolaSummary:
    def __init__(self):
        self.version = "2.0-ultra"

    def summarize(self, vectors: Dict[str, float]) -> Dict[str, Any]:
        dominant = max(vectors, key=vectors.get)
        lowest = min(vectors, key=vectors.get)

        balance = max(vectors.values()) - min(vectors.values())

        if balance <= 25:
            pattern = "perfil direcional equilibrado"
        elif balance <= 45:
            pattern = "perfil variado com leve predominância"
        else:
            pattern = "alta polarização direcional"

        return {
            "module": "Bussola",
            "version": self.version,
            "dominant_direction": dominant,
            "weaker_direction": lowest,
            "balance_pattern": pattern,
        }
