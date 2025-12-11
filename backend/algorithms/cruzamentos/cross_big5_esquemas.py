# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\cruzamentos\cross_big5_esquemas.py
# Última atualização: 2025-12-11T09:59:20.636480

"""
CROSS Big5 × Esquemas — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona os traços do Big Five com os Esquemas Cognitivos
(Young Schema Theory), identificando:

- vulnerabilidades
- reforços comportamentais
- convergências negativas
- proteção psicológica
"""

from typing import Dict, Any


class CrossBig5Esquemas:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, big5: Dict[str, float], esquemas: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Neuroticismo × Esquema de Abandono
        if big5.get("neuroticismo", 0) >= 65 and esquemas.get("abandono", 0) >= 55:
            patterns["abandono_sensivel"] = (
                "Neuroticismo elevado amplifica a ativação do esquema de abandono."
            )

        # Amabilidade baixa × Esquema de Desconfiança
        if big5.get("amabilidade", 0) <= 25 and esquemas.get("desconfianca", 0) >= 55:
            patterns["desconfianca_relacional"] = (
                "Baixa amabilidade reforça o esquema de desconfiança."
            )

        # Baixa extroversão × Esquema de Isolamento Social
        if big5.get("extroversao", 0) <= 30 and esquemas.get("isolamento", 0) >= 55:
            patterns["isolamento_retraimento"] = (
                "Baixa extroversão intensifica retraimento e isolamento social."
            )

        # Conscienciosidade alta × Padrões Inflexíveis
        if big5.get("conscienciosidade", 0) >= 70 and esquemas.get("padroes_inflexiveis", 0) >= 55:
            patterns["rigidez_cognitiva"] = (
                "Estruturação excessiva amplifica padrões rígidos e perfeccionistas."
            )

        # Abertura alta × Esquema de Busca de Aprovação (positivos)
        if big5.get("abertura", 0) >= 65 and esquemas.get("aprovacao", 0) <= 35:
            patterns["autenticidade_forte"] = (
                "Abertura elevada reduz dependência de validação externa."
            )

        return {
            "module": "cross_big5_esquemas",
            "version": self.version,
            "patterns": patterns,
        }
