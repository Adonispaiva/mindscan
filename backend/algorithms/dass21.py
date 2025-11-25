# dass21.py
# MindScan Rebuild – Algoritmo DASS-21 (Versão Final)
# Autor: Leo Vinci – IA Supervisora Inovexa
# Última atualização: 23/11/2025
# --------------------------------------------------------------------
# Escala DASS-21:
#   7 itens Depressão
#   7 itens Ansiedade
#   7 itens Estresse
#
# Pontuação original: 0 a 3 (Likert)
# Conversão para escala completa: soma * 2
# Normalização final MindScan: 0–100
#
# Este módulo entrega um modelo clínico funcional,
# definitivo e pronto para produção.

from typing import Dict, Any


class DASS21:
    DIMENSIONS = {
        "D": "Depressão",
        "A": "Ansiedade",
        "E": "Estresse"
    }

    # Itens por dimensão conforme instrumento oficial
    ITEMS = {
        "D": ["D1", "D2", "D3", "D4", "D5", "D6", "D7"],
        "A": ["A1", "A2", "A3", "A4", "A5", "A6", "A7"],
        "E": ["E1", "E2", "E3", "E4", "E5", "E6", "E7"]
    }

    MIN_SCORE = 0
    MAX_SCORE = 3

    NORMALIZATION_RANGE = (0, 100)

    DESCRIPTIONS = {
        "D": {
            "high": "Sintomas compatíveis com tristeza profunda, baixa energia, pessimismo.",
            "low": "Humor estável, resiliência emocional."
        },
        "A": {
            "high": "Sintomas compatíveis com ansiedade, tensão e hiperativação.",
            "low": "Tranquilidade, controle emocional situacional."
        },
        "E": {
            "high": "Sintomas compatíveis com estresse, irritabilidade e sobrecarga.",
            "low": "Boa adaptação frente a pressões externas."
        }
    }

    FACTOR_WEIGHTS = {
        "D": 1.0,
        "A": 1.0,
        "E": 1.0
    }

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    # ------------------------------------------------------
    # Validações
    # ------------------------------------------------------

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("responses deve ser um dicionário.")

        for item, score in self.responses.items():
            if not isinstance(score, int):
                raise ValueError(f"Resposta inválida em {item}: {score}")

            if not (self.MIN_SCORE <= score <= self.MAX_SCORE):
                raise ValueError(
                    f"Pontuação fora do permitido (0–3): {item}={score}"
                )

    # ------------------------------------------------------
    # Cálculo bruto
    # ------------------------------------------------------

    def compute_raw(self) -> Dict[str, float]:
        raw_scores = {dim: 0 for dim in self.DIMENSIONS}

        for dim, items in self.ITEMS.items():
            for item in items:
                value = self.responses.get(item, 0)
                raw_scores[dim] += value

            raw_scores[dim] *= 2  # regra original DASS-21

        return raw_scores

    # ------------------------------------------------------
    # Normalização final
    # ------------------------------------------------------

    def _normalize(self, value: float) -> float:
        # 0–42 (máximo possível em cada subescala)
        max_raw = 42
        low, high = self.NORMALIZATION_RANGE
        return (value / max_raw) * (high - low) + low

    # ------------------------------------------------------
    # Saída final
    # ------------------------------------------------------

    def compute(self) -> Dict[str, Any]:
        raw = self.compute_raw()

        normalized = {
            dim: round(self._normalize(value) * self.FACTOR_WEIGHTS[dim], 2)
            for dim, value in raw.items()
        }

        metadata = {
            dim: {
                "name": self.DIMENSIONS[dim],
                "raw": raw[dim],
                "normalized": normalized[dim],
                "interpretation_high": self.DESCRIPTIONS[dim]["high"],
                "interpretation_low": self.DESCRIPTIONS[dim]["low"]
            }
            for dim in raw
        }

        return {
            "model": "DASS-21 (Depressão · Ansiedade · Estresse)",
            "results": normalized,
            "metadata": metadata,
            "dimensions": list(self.DIMENSIONS.values())
        }
