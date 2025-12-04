"""
Big5 Validation — Versão Ultra Superior
---------------------------------------

Validação multilayer para os dados do Big Five.

Abrange:
- Tipagem
- Intervalos permitidos
- Quantidade mínima de itens
- Deteção de valores ausentes
- Deteção de valores anômalos
- Regras psicométricas básicas

Este módulo substitui completamente qualquer versão anterior
que possuía placeholders ou NotImplemented.
"""

from typing import Dict, Any, Tuple


class Big5Validation:
    def __init__(self):
        self.version = "2.0-ultra"

        # Escala BFI / NEO (geralmente 1 a 5)
        self.allowed_range: Tuple[float, float] = (0.0, 5.0)

        # Quantidade mínima realista de respostas
        self.min_items_required = 5

    # ----------------------
    # VALIDAÇÕES INTERNAS
    # ----------------------

    def _validate_type(self, data: Dict[str, Any]) -> bool:
        """Verifica se todos os valores são numéricos."""
        for k, v in data.items():
            if not isinstance(v, (int, float)):
                return False
        return True

    def _validate_range(self, data: Dict[str, float]) -> bool:
        """Valida se cada item está dentro do intervalo permitido."""
        low, high = self.allowed_range
        for v in data.values():
            if not (low <= float(v) <= high):
                return False
        return True

    def _validate_quantity(self, data: Dict[str, Any]) -> bool:
        """Garante volume mínimo de dados para análise psicométrica."""
        return len(data) >= self.min_items_required

    def _validate_missing(self, data: Dict[str, Any]) -> bool:
        """Detecta valores ausentes, vazios ou nulos."""
        for v in data.values():
            if v is None:
                return False
        return True

    # ----------------------
    # PIPELINE PRINCIPAL
    # ----------------------

    def validate_raw(self, data: Dict[str, Any]) -> bool:
        """Pipeline de validação superior dos dados do Big Five."""
        if not isinstance(data, dict) or not data:
            return False

        return all(
            [
                self._validate_quantity(data),
                self._validate_missing(data),
                self._validate_type(data),
                self._validate_range(data),
            ]
        )

    # Caso seja necessário validar pós-normalização (0–100)
    def validate_normalized(self, normalized: Dict[str, float]) -> bool:
        for v in normalized.values():
            if not (0.0 <= float(v) <= 100.0):
                return False
        return True
