# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola.py
# Última atualização: 2025-12-11T09:59:20.613842

"""
Bússola — Versão Ultra Superior
--------------------------------------------------------

Módulo central da Bússola MindScan:
- Recebe dimensões psicológicas e comportamentais
- Mapeia direção predominante do indivíduo
- Classifica padrões estratégicos
- Integra traços Big5, TEIQue, Performance e Cultura
- Gera leitura de orientação profissional e cognitiva

A Bússola funciona como um “mapa direcional” do perfil.
"""

from typing import Dict, Any

from .bussola_archetypes import BussolaArchetypes
from .bussola_vectors import BussolaVectors
from .bussola_alerts import BussolaAlerts


class Bussola:
    def __init__(self):
        self.version = "2.0-ultra"
        self.archetypes = BussolaArchetypes()
        self.vectors = BussolaVectors()
        self.alerts = BussolaAlerts()

    def run(self, dims: Dict[str, float]) -> Dict[str, Any]:
        if not dims:
            return {
                "module": "Bussola",
                "version": self.version,
                "error": "Dados insuficientes."
            }

        # 1) Vetores principais (Norte, Sul, Leste, Oeste)
        vector_output = self.vectors.compute(dims)

        # 2) Arquétipos derivados
        archetype = self.archetypes.classify(vector_output)

        # 3) Alertas comportamentais
        alert_output = self.alerts.generate(vector_output)

        return {
            "module": "Bussola",
            "version": self.version,
            "vectors": vector_output,
            "archetype": archetype,
            "alerts": alert_output,
        }
