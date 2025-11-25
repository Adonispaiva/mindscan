# big5.py
# MindScan Rebuild – Algoritmo Big Five (Versão Final)
# Autor: Leo Vinci (IA Supervisora Inovexa)
# Última atualização: 23/11/2025
# -----------------------------------------------------
# Este módulo implementa um avaliador completo do modelo
# psicométrico Big Five (OCEAN), com pontuação bruta,
# normalização, pesos fatoriais, intervalos, descrições,
# validações e integração com o Runtime Kernel.

from typing import Dict, Any, List


class BigFiveModel:
    """
    Implementação definitiva do modelo OCEAN (Big Five).
    Estrutura:
        - O (Abertura)
        - C (Conscienciosidade)
        - E (Extroversão)
        - A (Amabilidade)
        - N (Neuroticismo)
    """

    DIMENSIONS = ["O", "C", "E", "A", "N"]

    # Pesos fatoriais padronizados (valores aproximados consolidados na literatura)
    FACTOR_WEIGHTS: Dict[str, float] = {
        "O": 1.00,
        "C": 1.00,
        "E": 1.00,
        "A": 1.00,
        "N": 1.00
    }

    # Intervalos normalizados
    NORMALIZATION_RANGE = (0, 100)

    # Descrições por dimensão (versão final)
    DESCRIPTIONS: Dict[str, Dict[str, str]] = {
        "O": {
            "name": "Abertura",
            "high": "Criatividade, imaginação, curiosidade intelectual.",
            "low": "Preferência por rotina, pensamento concreto."
        },
        "C": {
            "name": "Conscienciosidade",
            "high": "Organização, disciplina, responsabilidade.",
            "low": "Baixa autodisciplina, desorganização."
        },
        "E": {
            "name": "Extroversão",
            "high": "Sociabilidade, assertividade, energia social.",
            "low": "Introversão, preferência por ambientes calmos."
        },
        "A": {
            "name": "Amabilidade",
            "high": "Cooperação, empatia, confiança interpessoal.",
            "low": "Competitividade, análise crítica direta."
        },
        "N": {
            "name": "Neuroticismo",
            "high": "Maior sensibilidade emocional, ansiedade.",
            "low": "Estabilidade emocional, resiliência."
        },
    }

    # Itens invertidos (necessários em Big Five)
    REVERSE_ITEMS = {"E3", "E5", "C4", "A2", "N1"}

    MAX_ITEM_SCORE = 5
    MIN_ITEM_SCORE = 1

    def __init__(self, responses: Dict[str, int]):
        """
        responses: {"O1":4, "O2":3, ...}
        """
        self.responses = responses
        self._validate_inputs()

    # ----------------------------------------------------------------------
    # Validações completas
    # ----------------------------------------------------------------------

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("Responses deve ser um dicionário.")

        for item, score in self.responses.items():
            if not isinstance(score, int):
                raise ValueError(f"Score inválido em {item}: {score}")
            if score < self.MIN_ITEM_SCORE or score > self.MAX_ITEM_SCORE:
                raise ValueError(f"Pontuação fora do intervalo permitido: {item}={score}")

    # ----------------------------------------------------------------------
    # Processamento dos itens
    # ----------------------------------------------------------------------

    def _apply_reverse(self, item: str, value: int) -> int:
        """Aplica reversão conforme manual do Big Five."""
        if item in self.REVERSE_ITEMS:
            return self.MAX_ITEM_SCORE - (value - self.MIN_ITEM_SCORE)
        return value

    # ----------------------------------------------------------------------
    # Cálculo bruto das dimensões
    # ----------------------------------------------------------------------

    def compute_raw(self) -> Dict[str, float]:
        scores = {dim: 0.0 for dim in self.DIMENSIONS}
        counts = {dim: 0 for dim in self.DIMENSIONS}

        for item, score in self.responses.items():
            dim = item[0]  # Primeira letra indica dimensão
            if dim not in scores:
                continue

            adjusted = self._apply_reverse(item, score)
            scores[dim] += adjusted
            counts[dim] += 1

        for dim in scores:
            if counts[dim] > 0:
                scores[dim] /= counts[dim]

        return scores

    # ----------------------------------------------------------------------
    # Normalização final
    # ----------------------------------------------------------------------

    def _normalize(self, value: float) -> float:
        min_v, max_v = self.MIN_ITEM_SCORE, self.MAX_ITEM_SCORE
        norm_min, norm_max = self.NORMALIZATION_RANGE
        return ((value - min_v) / (max_v - min_v)) * (norm_max - norm_min) + norm_min

    def compute(self) -> Dict[str, Any]:
        raw = self.compute_raw()

        # Normalização + pesos
        normalized = {
            dim: round(self._normalize(raw[dim]) * self.FACTOR_WEIGHTS[dim], 2)
            for dim in raw
        }

        # Monta metadados completos
        metadata = {
            dim: {
                "name": self.DESCRIPTIONS[dim]["name"],
                "raw": round(raw[dim], 2),
                "normalized": normalized[dim],
                "interpretation_high": self.DESCRIPTIONS[dim]["high"],
                "interpretation_low": self.DESCRIPTIONS[dim]["low"],
            }
            for dim in raw
        }

        return {
            "model": "Big Five (OCEAN)",
            "results": normalized,
            "metadata": metadata,
            "dimensions": self.DIMENSIONS,
        }
