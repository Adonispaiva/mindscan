# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\diagnostic_matrix_service.py
# Última atualização: 2025-12-11T09:59:21.089476

# -*- coding: utf-8 -*-
"""
diagnostic_matrix_service.py
----------------------------

Responsável por gerar a matriz diagnóstica do MindScan:
- mapeia a interação entre fatores cognitivos, emocionais e comportamentais
- identifica zonas de tensão e zonas de força
- classifica o perfil em eixos estruturais

Este módulo é usado em:
- relatórios executivos
- relatórios premium
- seções PDF de diagnóstico
"""

from typing import Dict, Any


class DiagnosticMatrixService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.results = payload.get("results", {})
        self.traits = self.results.get("traits", {})
        self.performance = self.results.get("performance", {})
        self.emotional = self.results.get("emotional", {})

    def compute_axis_stability(self) -> str:
        stability = self.emotional.get("emotional_stability", 50)
        if stability > 65:
            return "Alta estabilidade emocional"
        if stability > 45:
            return "Estabilidade moderada"
        return "Baixa estabilidade emocional"

    def compute_axis_energy(self) -> str:
        extr = self.traits.get("extraversion", 50)
        if extr > 60:
            return "Alta energia social"
        if extr > 45:
            return "Energia moderada"
        return "Energia reduzida"

    def compute_axis_drive(self) -> str:
        cons = self.traits.get("conscientiousness", 50)
        if cons > 65:
            return "Alto drive de execução"
        if cons > 45:
            return "Drive moderado"
        return "Drive reduzido"

    def compute_matrix(self) -> Dict[str, str]:
        return {
            "eixo_estabilidade": self.compute_axis_stability(),
            "eixo_energia": self.compute_axis_energy(),
            "eixo_execucao": self.compute_axis_drive(),
        }

    def build(self) -> Dict[str, Any]:
        return {
            "matriz_diagnostica": self.compute_matrix()
        }
