# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\engines\corporate_risk_engine.py
# Última atualização: 2025-12-11T09:59:21.150629

# -*- coding: utf-8 -*-
"""
corporate_risk_engine.py
------------------------

Engine responsável por identificar e construir os blocos de risco
e potenciais blind spots do perfil corporativo.
"""

from typing import Dict, Any, List
from services.helpers.report_utils import clean_text


class CorporateRiskEngine:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    def risk(self, title: str, content: str) -> Dict[str, str]:
        return {
            "title": clean_text(title),
            "content": clean_text(content)
        }

    def build(self) -> Dict[str, Any]:
        return {
            "id": "riscos",
            "title": "Riscos e Blind Spots",
            "description": (
                "Esta seção descreve riscos comportamentais e pontos cegos que podem impactar "
                "o desempenho ou a integração do avaliado em determinados contextos organizacionais."
            ),
            "blocks": [
                self.risk(
                    "Rigidificação Cognitiva",
                    "Em cenários de mudança rápida, pode apresentar resistência inicial para abandonar padrões consolidados."
                ),
                self.risk(
                    "Delegação Insuficiente",
                    "Tende a assumir demasiada responsabilidade direta, o que pode reduzir a velocidade de execução em equipes maiores."
                ),
                self.risk(
                    "Exposição Emocional Restrita",
                    "Baixa demonstração emocional pode ser interpretada como distanciamento ou frieza por alguns perfis sociáveis."
                ),
            ]
        }
