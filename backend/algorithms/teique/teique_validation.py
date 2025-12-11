# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\teique\teique_validation.py
# Última atualização: 2025-12-11T09:59:20.730228

"""
TEIQue Validation
Validação estrutural e de integridade para o módulo TEIQue.
"""

from typing import Dict, Any


class TeiqueValidation:
    """
    Valida:
    - estrutura do input
    - existência das dimensões obrigatórias
    - faixas válidas (0–100)
    """

    def __init__(self):
        self.version = "1.0"

        # Conjunto oficial de dimensões TEIQue
        self.required_dimensions = {
            "otimismo",
            "autoestima",
            "satisfacao",
            "empatia",
            "relacoes",
            "impulsividade",
            "controle_emocional",
            "autorregulacao",
            "adaptabilidade",
        }

    def validate(self, scores: Dict[str, float]) -> Dict[str, Any]:
        errors = []
        warnings = []

        # Verifica dimensões obrigatórias
        missing = self.required_dimensions - scores.keys()
        if missing:
            errors.append(f"Dimensões obrigatórias ausentes: {', '.join(missing)}")

        # Verifica faixas válidas
        for dim, val in scores.items():
            if not (0 <= val <= 100):
                errors.append(f"Valor inválido para '{dim}': {val}")

            if val < 10 or val > 95:
                warnings.append(f"Valor extremo para '{dim}': {val}")

        return {
            "module": "TEIQue",
            "version": self.version,
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
