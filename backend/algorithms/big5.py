# Caminho: D:\backend\algorithms\big5.py
# MindScan — Big Five Padronizado v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo completo, final e padronizado para integração com a MindScanEngine

from typing import Dict, Any, List
from datetime import datetime

class BigFiveModel:
    """
    Implementação definitiva do modelo OCEAN (Big Five).
    Dimensões:
        - O (Abertura)
        - C (Conscienciosidade)
        - E (Extroversão)
        - A (Amabilidade)
        - N (Neuroticismo)
    """

    DIMENSIONS = ["O", "C", "E", "A", "N"]

    FACTOR_WEIGHTS: Dict[str, float] = {
        "O": 1.00,
        "C": 1.00,
        "E": 1.00,
        "A": 1.00,
        "N": 1.00,
    }

    NORMALIZATION_RANGE = (0, 100)

    DESCRIPTIONS: Dict[str, Dict[str, str]] = {
        "O": {"name": "Abertura", "high": "Criatividade, imaginação, curiosidade.", "low": "Preferência por rotina."},
        "C": {"name": "Conscienciosidade", "high": "Organização, disciplina.", "low": "Desorganização."},
        "E": {"name": "Extroversão", "high": "Sociabilidade, energia social.", "low": "Introversão."},
        "A": {"name": "Amabilidade", "high": "Empatia, cooperação.", "low": "Competitividade."},
        "N": {"name": "Neuroticismo", "high": "Sensibilidade emocional.", "low": "Estabilidade emocional."},
    }

    REVERSE_ITEMS = {"E3", "E5", "C4", "A2", "N1"}

    MAX_ITEM_SCORE = 5
    MIN_ITEM_SCORE = 1

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("Responses deve ser um dicionário.")
        for item, score in self.responses.items():
            if not isinstance(score, int):
                raise ValueError(f"Score inválido em {item}: {score}")
            if score < self.MIN_ITEM_SCORE or score > self.MAX_ITEM_SCORE:
                raise ValueError(f"Pontuação fora do intervalo permitido: {item}={score}")

    def _apply_reverse(self, item: str, value: int) -> int:
        if item in self.REVERSE_ITEMS:
            return self.MAX_ITEM_SCORE - (value - self.MIN_ITEM_SCORE)
        return value

    def compute_raw(self) -> Dict[str, float]:
        scores = {dim: 0.0 for dim in self.DIMENSIONS}
        counts = {dim: 0 for dim in self.DIMENSIONS}

        for item, score in self.responses.items():
            dim = item[0]
            if dim not in scores:
                continue
            adjusted = self._apply_reverse(item, score)
            scores[dim] += adjusted
            counts[dim] += 1

        for dim in scores:
            if counts[dim] > 0:
                scores[dim] /= counts[dim]

        return scores

    def _normalize(self, value: float) -> float:
        min_v, max_v = self.MIN_ITEM_SCORE, self.MAX_ITEM_SCORE
        norm_min, norm_max = self.NORMALIZATION_RANGE
        return ((value - min_v) / (max_v - min_v)) * (norm_max - norm_min) + norm_min

    def compute(self) -> Dict[str, Any]:
        raw = self.compute_raw()
        normalized = {dim: self._normalize(value) for dim, value in raw.items()}
        return {
            "model": "Big Five",
            "results": normalized,
            "raw": raw,
            "timestamp": datetime.utcnow().isoformat(),
        }

# ---------------------------------------------------------------------------
# Wrapper oficial MindScan — big5_process
# ---------------------------------------------------------------------------

def big5_process(dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Wrapper padronizado para integração com a MindScanEngine.
    Entrada esperada do dataset:
        dataset["big5_responses"] = { "O1": 4, "C1": 3, ... }

    Saída no padrão MindScan:
        [
            {
                "dimension": str,
                "score": float,
                "descriptor": str,
                "metadata": dict
            }
        ]
    """

    if "big5_responses" not in dataset:
        raise ValueError("Dataset não contém 'big5_responses'.")

    model = BigFiveModel(dataset["big5_responses"])
    computed = model.compute()
    normalized = computed["results"]

    output = []
    for dim, score in normalized.items():
        desc_block = BigFiveModel.DESCRIPTIONS.get(dim, {})
        output.append({
            "dimension": dim,
            "score": float(score),
            "descriptor": desc_block.get("high") if score >= 50 else desc_block.get("low"),
            "metadata": {
                "model": "big5",
                "name": desc_block.get("name", dim),
                "timestamp": computed["timestamp"],
            },
        })

    return output