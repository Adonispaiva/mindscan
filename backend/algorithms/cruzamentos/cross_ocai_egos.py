# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\cruzamentos\cross_ocai_egos.py
# Última atualização: 2025-12-11T09:59:20.636480

"""
CROSS OCAI × EGOS — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona estilos culturais organizacionais (OCAI)
com estados de Ego (Adulto, Crítico, Livre, Cuidador, Adaptado).

Objetivo:
Mapear compatibilidade ou conflito comportamental profundo.
"""

from typing import Dict, Any


class CrossOCAIEgos:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, ocai: Dict[str, float], egos: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Ego Adulto × Hierarquia
        if egos.get("adulto", 0) >= 60 and ocai.get("hierarquia", 0) >= 55:
            patterns["ajuste_adulto_hierarquico"] = (
                "Ego Adulto forte se adapta bem a culturas estruturadas."
            )

        # Ego Livre × Adocracia
        if egos.get("livre", 0) >= 60 and ocai.get("inovacao", 0) >= 60:
            patterns["criatividade_adocratica"] = (
                "Perfil espontâneo com alta compatibilidade em culturas inovadoras."
            )

        # Ego Crítico × Cultura de Mercado
        if egos.get("critico", 0) >= 55 and ocai.get("mercado", 0) >= 55:
            patterns["racionalidade_competitiva"] = (
                "Ego Crítico elevado pode performar bem em culturas exigentes e competitivas."
            )

        # Ego Cuidador × Cultura de Clã
        if egos.get("cuidador", 0) >= 60 and ocai.get("clan", 0) >= 55:
            patterns["apoio_relacional"] = (
                "Ego Cuidador naturalmente se alinha a culturas colaborativas."
            )

        return {
            "module": "cross_ocai_egos",
            "version": self.version,
            "patterns": patterns,
        }
