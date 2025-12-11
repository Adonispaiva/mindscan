# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\metadata_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
metadata_service.py
-------------------

Responsável por consolidar metadados do relatório:
- informações do candidato
- data
- modelo aplicado
- versão do engine
- sessão de teste
- identificadores internos

Esse módulo alimenta:
- cabeçalho do PDF
- resumo executivo
- logs internos
- compliance futura
"""

from datetime import datetime
from typing import Dict, Any


class MetadataService:

    ENGINE_VERSION = "MindScan Engine v1.0.0"

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    def build(self) -> Dict[str, Any]:
        context = self.payload.get("context", {})
        return {
            "nome": context.get("name", "Indivíduo"),
            "idade": context.get("age", None),
            "cargo": context.get("role", None),
            "empresa": context.get("company", None),

            "data_relatorio": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "modelo_aplicado": self.payload.get("model", "MindScan®"),
            "versao_engine": self.ENGINE_VERSION,
            "test_id": self.payload.get("test_id", "N/A"),
        }
