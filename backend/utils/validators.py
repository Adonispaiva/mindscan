# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\utils\validators.py
# Última atualização: 2025-12-11T09:59:21.308202

# ============================================================
# MindScan — Validators (UTILS)
# ============================================================
# Utilitário central responsável por todas as validações
# estruturais e semânticas usadas pelo backend.
#
# Fornece:
# - validação de tipos
# - validação de intervalos numéricos
# - validação de e-mail e formatos específicos
# - validação de listas, dicionários, JSON
# - sanitização de payloads
#
# Versão completa e maximizada.
# ============================================================

import re
import json
from typing import Any, Dict, List, Optional


class Validators:
    """
    Conjunto unificado de validadores usados no backend MindScan.
    """

    # ------------------------------------------------------------
    # TIPO BÁSICO
    # ------------------------------------------------------------
    @staticmethod
    def ensure_type(value: Any, expected_type: type, field: str = ""):
        if not isinstance(value, expected_type):
            raise ValueError(f"Campo '{field}' deveria ser {expected_type.__name__}, recebeu {type(value).__name__}")

    # ------------------------------------------------------------
    # NÚMERO
    # ------------------------------------------------------------
    @staticmethod
    def number(value: Any, field: str = "", min_val: Optional[float] = None, max_val: Optional[float] = None):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Campo '{field}' deveria ser numérico.")

        if min_val is not None and value < min_val:
            raise ValueError(f"Campo '{field}' é menor que o mínimo permitido: {min_val}")

        if max_val is not None and value > max_val:
            raise ValueError(f"Campo '{field}' excede o máximo permitido: {max_val}")

    # ------------------------------------------------------------
    # TEXTO
    # ------------------------------------------------------------
    @staticmethod
    def text(value: Any, field: str = "", max_length: int = 5000):
        if not isinstance(value, str):
            raise ValueError(f"Campo '{field}' deveria ser texto.")
        if len(value) > max_length:
            raise ValueError(f"Campo '{field}' excede {max_length} caracteres.")

    # ------------------------------------------------------------
    # LISTA
    # ------------------------------------------------------------
    @staticmethod
    def list_of(value: Any, field: str = "", expected_type: Optional[type] = None):
        if not isinstance(value, list):
            raise ValueError(f"Campo '{field}' deveria ser uma lista.")

        if expected_type:
            for item in value:
                if not isinstance(item, expected_type):
                    raise ValueError(f"Item inválido em '{field}': esperado {expected_type.__name__}")

    # ------------------------------------------------------------
    # DICIONÁRIO
    # ------------------------------------------------------------
    @staticmethod
    def dict(value: Any, field: str = ""):
        if not isinstance(value, dict):
            raise ValueError(f"Campo '{field}' deveria ser um objeto (dict).")

    # ------------------------------------------------------------
    # EMAIL
    # ------------------------------------------------------------
    EMAIL_REGEX = re.compile(r"^[\w\.\-]+@[\w\.\-]+\.\w+$")

    @staticmethod
    def email(value: str, field: str = ""):
        if not isinstance(value, str) or not Validators.EMAIL_REGEX.match(value):
            raise ValueError(f"Campo '{field}' não é um e-mail válido.")

    # ------------------------------------------------------------
    # JSON STRING
    # ------------------------------------------------------------
    @staticmethod
    def json_string(value: str, field: str = ""):
        try:
            json.loads(value)
        except Exception:
            raise ValueError(f"Campo '{field}' não contém JSON válido.")

    # ------------------------------------------------------------
    # CHAVES OBRIGATÓRIAS
    # ------------------------------------------------------------
    @staticmethod
    def required_keys(data: Dict[str, Any], keys: List[str], field: str = ""):
        for k in keys:
            if k not in data:
                raise ValueError(f"Campo '{field}' está faltando chave obrigatória: '{k}'")

    # ------------------------------------------------------------
    # NORMALIZAÇÃO DE CAMPOS (strip)
    # ------------------------------------------------------------
    @staticmethod
    def clean_text(value: str) -> str:
        if not isinstance(value, str):
            return ""
        return value.strip().replace("\n", " ")

    # ------------------------------------------------------------
    # VALIDA PAYLOAD PSICOMÉTRICO BÁSICO
    # ------------------------------------------------------------
    @staticmethod
    def validate_psychometric_payload(data: Dict[str, Any]):
        """
        Valida payload bruto recebido do frontend para garantir que
        não quebre o DiagnosticEngine.
        """
        Validators.dict(data, "payload")

        for key, val in data.items():
            # deve ser número, string numérica ou lista de números
            if isinstance(val, (int, float)):
                continue

            if isinstance(val, str) and val.isdigit():
                continue

            if isinstance(val, list):
                for item in val:
                    if not isinstance(item, (int, float)):
                        raise ValueError(f"Lista inválida em '{key}': valores não numéricos.")
                continue

            raise ValueError(f"Valor inválido em '{key}': {val}")
