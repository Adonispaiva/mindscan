# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\cruzamentos\cross_alerts.py
# Última atualização: 2025-12-11T09:59:20.620871

"""
CROSS ALERTS — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Gera alertas sistêmicos a partir dos cruzamentos entre:

- Personalidade (Big5)
- Emoções (TEIQue)
- Estresse psicológico (DASS21)
- Cultura e valores (OCAI)
- Performance comportamental

Os alertas são sinais antecipatórios.
"""

from typing import Dict, List, Any


class CrossAlerts:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, payload: Dict[str, Dict[str, float]]) -> List[str]:
        alerts = []

        big5 = payload.get("big5", {})
        teique = payload.get("teique", {})
        dass = payload.get("dass21", {})
        perf = payload.get("performance", {})
        ocai = payload.get("ocai", {})

        # 1) Neuroticismo + Estresse
        if big5.get("neuroticismo", 0) >= 65 and dass.get("stress", 0) >= 60:
            alerts.append("Risco: Reatividade emocional elevada com estresse crítico.")

        # 2) Baixa Consciência + Baixa Performance
        if big5.get("conscienciosidade", 0) <= 35 and perf.get("consistencia", 0) <= 40:
            alerts.append("Alerta: Baixa organização impactando execução prática.")

        # 3) Extroversão alta + TEIQue expressividade baixa
        if big5.get("extroversao", 0) >= 60 and teique.get("expressividade", 0) <= 40:
            alerts.append("Conflito: extroversão não acompanhada de expressividade emocional.")

        # 4) Abertura muito baixa + Cultura inovadora
        if big5.get("abertura", 0) <= 30 and ocai.get("inovacao", 0) >= 60:
            alerts.append("Misfit cultural: abertura baixa em ambiente inovador.")

        # 5) Amabilidade baixa + Clima colaborativo
        if big5.get("amabilidade", 0) <= 20 and ocai.get("colaboracao", 0) >= 60:
            alerts.append("Potencial conflito: baixa amabilidade em cultura colaborativa.")

        return alerts
