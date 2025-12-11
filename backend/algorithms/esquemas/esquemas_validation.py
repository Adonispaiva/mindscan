# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_validation.py
# Última atualização: 2025-12-11T09:59:20.683445

"""
Esquemas Validation
Validação estrutural das entradas do questionário de Esquemas Adaptativos.
"""

from typing import Dict, Any


class EsquemasValidation:
    """
    Garante consistência dos dados brutos para o módulo de Esquemas:
    - presença dos itens necessários
    - faixa válida (0 a 36)
    - alerta para valores extremos
    """

    def __init__(self):
        self.version = "1.0"
        self.max_raw = 36.0

    def validate(self, raw_scores: Dict[str, float]) -> Dict[str, Any]:
        errors = []
        warnings = []

        for item, value in raw_scores.items():
            if not isinstance(value, (int, float)):
                errors.append(f"Valor inválido para '{item}': não numérico.")
                continue

            if not (0 <= value <= self.max_raw):
                errors.append(
                    f"Valor fora da faixa em '{item}': {value} (esperado 0–36)."
                )

            if value >= 32:
                warnings.append(
                    f"Valor extremo em '{item}': {value} (acima de 32)."
                )

        return {
            "module": "Esquemas",
            "version": self.version,
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
