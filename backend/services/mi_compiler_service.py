# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\mi_compiler_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
mi_compiler_service.py
----------------------

MI = MindScan Intelligence.
Este módulo é responsável por consolidar os resultados provenientes de
várias fontes (traits, emoções, performance, riscos, insights, narrativa)
em um único dicionário padronizado que serve de input para:

- Corporate Orchestrator
- Renderers
- PDI
- Roadmap
- Resumo Estratégico
"""

from typing import Dict, Any


class MICompilerService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    def build(self) -> Dict[str, Any]:
        return {
            "context": self.payload.get("context", {}),
            "test_id": self.payload.get("test_id", ""),

            "traits": self.payload.get("results", {}).get("traits", {}),
            "emotional": self.payload.get("results", {}).get("emotional", {}),
            "performance": self.payload.get("results", {}).get("performance", {}),
            "risks": self.payload.get("results", {}).get("risks", {}),

            "insights": self.payload.get("insights", []),
            "narrativa": self.payload.get("narrativa", {}),
            "metadata": self.payload.get("metadata", {}),
            "roadmap": self.payload.get("roadmap", {}),
            "pdi": self.payload.get("pdi", {}),
        }
