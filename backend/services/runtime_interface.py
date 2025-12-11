# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\runtime_interface.py
# Última atualização: 2025-12-11T09:59:21.120711

from typing import Dict, Any

class RuntimeInterface:
    """
    Interface responsável por padronizar a comunicação entre
    a API (FastAPI) e o motor de diagnóstico MindScan.

    A versão 2.0 define um contrato mínimo obrigatório para:
    - validação dos dados de entrada
    - formatação padronizada para a engine
    - retorno de resultados já estruturados para o Response
    """

    @staticmethod
    def validate_input(dataset: Dict[str, Any]) -> bool:
        """
        Valida a estrutura mínima esperada pelo motor de diagnóstico.
        """
        if not isinstance(dataset, dict):
            return False

        if "candidate" not in dataset:
            return False

        if "instruments" not in dataset:
            return False

        return True

    @staticmethod
    def format_for_engine(dataset: Dict[str, Any]) -> Dict[str, Any]:
        """
        Garante que o dataset esteja pronto para processamento pela engine.
        """
        # Aqui poderíamos aplicar normalizações, conversões, etc.
        # No futuro, isso será expandido pelo MI 2.0.
        return dataset

    @staticmethod
    def format_engine_output(result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara o resultado bruto da engine para o modelo DiagnosticResponse.
        """
        return {
            "status": "ok",
            "insights": result.get("insights"),
            "profile": result.get("profile"),
            "scores": result.get("scores"),
        }