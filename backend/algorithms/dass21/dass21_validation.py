# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass21\dass21_validation.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
DASS21 Validation — Versão ULTRA SUPERIOR
--------------------------------------------------------------

Validação completa dos dados do DASS21.

Inclui:
- validação de tipos
- limites máximos/mínimos
- prevenção de valores absurdos
"""

from typing import Dict


class DASS21Validation:
    def __init__(self):
        self.version = "2.0-ultra"

    def validate(self, scores: Dict[str, float]) -> Dict[str, float]:
        required = ["depressao", "ansiedade", "stress"]

        for field in required:
            if field not in scores:
                raise ValueError(f"Campo obrigatório ausente: {field}")

            value = scores[field]
            if not isinstance(value, (int, float)):
                raise TypeError(f"O campo {field} deve ser numérico.")
            if value < 0 or value > 100:
                raise ValueError(f"Valor inválido para {field}: {value}. Esperado entre 0 e 100.")

        return scores
