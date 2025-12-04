"""
Schema Validation
Validação estruturada para o nível item→dimensão dos Esquemas.
"""

from typing import Dict, Any


class SchemaValidation:
    """
    Responsável por validar valores normalizados e detectar inconsistências
    em itens/dimensões antes do processamento completo dos 18 Esquemas.
    """

    def __init__(self):
        self.version = "1.0"

    def validate(self, normalized: Dict[str, float]) -> Dict[str, Any]:
        errors = []
        warnings = []

        for key, value in normalized.items():
            if not isinstance(value, (int, float)):
                errors.append(f"Valor inválido em '{key}': não numérico.")
                continue

            if not (0 <= value <= 100):
                errors.append(
                    f"Valor fora da faixa para '{key}': {value} (esperado 0–100)."
                )

            if value >= 90:
                warnings.append(f"Valor extremo detectado em '{key}': {value}")

        return {
            "module": "Esquemas",
            "version": self.version,
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
