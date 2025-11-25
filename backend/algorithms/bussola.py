# bussola.py
# MindScan Rebuild – Algoritmo Bússola de Competências (Versão Final)
# Autor: Leo Vinci (IA Supervisora Inovexa)
# Última atualização: 23/11/2025
# ---------------------------------------------------------
# O modelo Bússola trabalha com 7 dimensões de competências:
#   1. Estratégia
#   2. Execução
#   3. Relacionamento
#   4. Comunicação
#   5. Liderança
#   6. Aprendizagem
#   7. Propósito
#
# Este módulo implementa:
#   - Validação de respostas
#   - Reversões (quando aplicáveis)
#   - Pontuação bruta
#   - Normalização (0–100)
#   - Pesos fatoriais
#   - Interpretações qualitativas
#   - Output padrão MindScan (metadata + resultados + modelo)

from typing import Dict, Any


class BussolaCompetencias:
    """
    Modelo definitivo das 7 competências centrais da Bússola MindScan.
    O sistema aceita itens no formato:
        "E1", "L3", "C2" etc.
    Onde a primeira letra indica a dimensão.
    """

    DIMENSIONS = {
        "E": "Estratégia",
        "X": "Execução",
        "R": "Relacionamento",
        "C": "Comunicação",
        "L": "Liderança",
        "A": "Aprendizagem",
        "P": "Propósito"
    }

    # Pesos fatoriais (ajustáveis em calibração futura)
    FACTOR_WEIGHTS = {
        "E": 1.0,
        "X": 1.0,
        "R": 1.0,
        "C": 1.0,
        "L": 1.0,
        "A": 1.0,
        "P": 1.0
    }

    NORMALIZATION_RANGE = (0, 100)

    # Itens reversos (exemplo realista)
    REVERSE_ITEMS = {"R3", "C4", "X2", "L5"}

    MIN_SCORE = 1
    MAX_SCORE = 5

    DESCRIPTIONS = {
        "E": {
            "high": "Capacidade de visão, análise sistêmica e orientação estratégica.",
            "low": "Baixa visão de futuro, foco restrito ao curto prazo."
        },
        "X": {
            "high": "Alta capacidade de execução, organização e entrega.",
            "low": "Dificuldade em manter disciplina e consistência."
        },
        "R": {
            "high": "Criar vínculos, empatia, colaboração natural.",
            "low": "Baixa conexão interpessoal, isolamento social."
        },
        "C": {
            "high": "Comunicação clara, assertiva e eficaz.",
            "low": "Dificuldade em transmitir ideias ou ouvir ativamente."
        },
        "L": {
            "high": "Inspirar, orientar e desenvolver pessoas.",
            "low": "Dificuldade em assumir papéis de influência."
        },
        "A": {
            "high": "Aprendizagem contínua, reflexão, adaptabilidade.",
            "low": "Estagnação, pouca curiosidade ou atualização."
        },
        "P": {
            "high": "Propósito, motivação intrínseca e alinhamento pessoal.",
            "low": "Falta de direção interna, desconexão com objetivos."
        }
    }

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    # --------------------------------------------------------------
    # Validação completa dos dados
    # --------------------------------------------------------------

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("responses deve ser um dicionário.")

        for item, score in self.responses.items():
            if not isinstance(score, int):
                raise ValueError(f"Resposta inválida em {item}: {score}")
            if not (self.MIN_SCORE <= score <= self.MAX_SCORE):
                raise ValueError(f"Pontuação fora do intervalo permitido: {item}={score}")

    # --------------------------------------------------------------
    # Reversão de itens
    # --------------------------------------------------------------

    def _apply_reverse(self, item: str, value: int) -> int:
        if item in self.REVERSE_ITEMS:
            return self.MAX_SCORE - (value - self.MIN_SCORE)
        return value

    # --------------------------------------------------------------
    # Cálculo bruto
    # --------------------------------------------------------------

    def compute_raw(self) -> Dict[str, float]:
        raw = {dim: 0.0 for dim in self.DIMENSIONS}
        count = {dim: 0 for dim in self.DIMENSIONS}

        for item, score in self.responses.items():
            dim = item[0]
            if dim not in self.DIMENSIONS:
                continue

            adj = self._apply_reverse(item, score)
            raw[dim] += adj
            count[dim] += 1

        for dim in raw:
            if count[dim] > 0:
                raw[dim] /= count[dim]

        return raw

    # --------------------------------------------------------------
    # Normalização
    # --------------------------------------------------------------

    def _normalize(self, value: float) -> float:
        min_v, max_v = self.MIN_SCORE, self.MAX_SCORE
        low, high = self.NORMALIZATION_RANGE
        return ((value - min_v) / (max_v - min_v)) * (high - low) + low

    # --------------------------------------------------------------
    # Saída final
    # --------------------------------------------------------------

    def compute(self) -> Dict[str, Any]:
        raw = self.compute_raw()

        normalized = {
            dim: round(self._normalize(raw_val) * self.FACTOR_WEIGHTS[dim], 2)
            for dim, raw_val in raw.items()
        }

        metadata = {
            dim: {
                "name": self.DIMENSIONS[dim],
                "raw": round(raw[dim], 2),
                "normalized": normalized[dim],
                "high": self.DESCRIPTIONS[dim]["high"],
                "low": self.DESCRIPTIONS[dim]["low"]
            }
            for dim in raw
        }

        return {
            "model": "Bússola de Competências MindScan",
            "results": normalized,
            "metadata": metadata,
            "dimensions": list(self.DIMENSIONS.values())
        }
