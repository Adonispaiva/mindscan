"""
Big5 Alerts — Versão Ultra Superior
-----------------------------------

Gera ALERTAS principais com foco em:
- comportamento
- desempenho
- relações profissionais
- estabilidade emocional
- risco estratégico

Este módulo trabalha em camada paralela às risk_flags.
"""

from typing import Dict, List


class Big5Alerts:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, dims: Dict[str, float]) -> List[str]:
        alerts = []

        # 1) Estabilidade emocional geral
        neuro = dims.get("neuroticismo", 0)
        if neuro >= 65:
            alerts.append("Atenção: tendência a estresse elevado e reatividade afetiva.")

        # 2) Riscos de baixa Consciência
        cons = dims.get("conscienciosidade", 0)
        if cons <= 35:
            alerts.append("Baixa disciplina e organização podem comprometer resultados.")

        # 3) Abertura muito baixa
        if dims.get("abertura", 0) <= 30:
            alerts.append("Baixa abertura pode reduzir adaptabilidade a mudanças.")

        # 4) Extroversão extrema
        if dims.get("extroversao", 0) >= 85:
            alerts.append("Extroversão excessiva pode gerar impulsividade social.")

        # 5) Amabilidade crítica
        if dims.get("amabilidade", 0) <= 20:
            alerts.append("Baixa amabilidade pode aumentar conflitos interpessoais.")

        return alerts
