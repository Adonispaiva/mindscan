# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\cruzamentos\cross_ocai_big5.py
# Última atualização: 2025-12-11T09:59:20.636480

"""
CROSS OCAI × Big5 — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona tipos de cultura organizacional (OCAI)
com traços de personalidade Big Five.

Dimensões OCAI:
- Clã
- Adocracia (inovação)
- Mercado (competição)
- Hierarquia (estrutura)

Objetivo:
Detectar compatibilidade, sinergia ou choque cultural.
"""

from typing import Dict, Any


class CrossOCAIBig5:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, ocai: Dict[str, float], big5: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Cultura de Clã × Amabilidade
        if ocai.get("clan", 0) >= 55 and big5.get("amabilidade", 0) >= 55:
            patterns["sinergia_colaborativa"] = (
                "Ajuste natural entre amabilidade alta e cultura colaborativa de Clã."
            )

        # Cultura de Mercado × Extroversão
        if ocai.get("mercado", 0) >= 55 and big5.get("extroversao", 0) >= 60:
            patterns["agente_competitivo"] = (
                "Extroversão elevada alinhada ao dinamismo competitivo da cultura de Mercado."
            )

        # Cultura de Hierarquia × Conscienciosidade
        if ocai.get("hierarquia", 0) >= 55 and big5.get("conscienciosidade", 0) >= 60:
            patterns["ajuste_estruturado"] = (
                "Alta disciplina cognitiva compatível com ambientes estruturados."
            )

        # Cultura de Adocracia × Abertura
        if ocai.get("inovacao", 0) >= 60 and big5.get("abertura", 0) >= 65:
            patterns["inovador_ideal"] = (
                "Traço de abertura elevado perfeitamente alinhado com culturas inovadoras."
            )

        return {
            "module": "cross_ocai_big5",
            "version": self.version,
            "patterns": patterns,
        }
