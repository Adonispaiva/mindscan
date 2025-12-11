# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\data_service.py
# Última atualização: 2025-12-11T09:59:21.089476

# Caminho: D:\backend\services\data_service.py
# MindScan — DataService Padronizado v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo definitivo e integrado ao MindScanEngine

from typing import Dict, Any
from datetime import datetime

class DataService:
    """
    Serviço responsável por estruturar e validar o dataset completo
    a ser processado pelo MindScanEngine.

    Entrada esperada:
        payload bruto vindo da API.

    Saída gerada:
        dataset padronizado contendo:
            - big5_responses
            - teique_responses
            - ocai_responses
            - dass21_responses
            - schema_responses
            - performance_responses
            - metadados gerais
    """

    REQUIRED_BLOCKS = [
        "big5_responses",
        "teique_responses",
        "ocai_responses",
        "dass21_responses",
        "schema_responses",
        "performance_responses",
    ]

    @staticmethod
    def validate_block(name: str, block: Any):
        if not isinstance(block, dict):
            raise ValueError(f"Bloco '{name}' deve ser um dicionário.")
        if len(block) == 0:
            raise ValueError(f"Bloco '{name}' está vazio.")

    @staticmethod
    def prepare_dataset(payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("Payload inválido. Deve ser um dicionário.")

        dataset = {}

        # -------------------------
        # Validar blocos obrigatórios
        # -------------------------
        for block in DataService.REQUIRED_BLOCKS:
            if block not in payload:
                raise ValueError(f"Payload não contém bloco obrigatório: '{block}'.")
            DataService.validate_block(block, payload[block])
            dataset[block] = payload[block]

        # -------------------------
        # Metadados globais
        # -------------------------
        dataset["metadata"] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "MindScan Backend API v2.0",
            "version": "2.0",
        }

        return dataset
