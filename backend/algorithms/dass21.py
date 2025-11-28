# Caminho: D:\backend\algorithms\dass21.py
# MindScan — DASS-21 Padronizado v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo completo, final e padronizado para integração com a MindScanEngine

from typing import Dict, Any, List
from datetime import datetime

class DASS21Model:
    """
    Modelo oficial DASS-21 (Depressão, Ansiedade, Estresse).

    Cada subescala possui 7 itens.
    O score final = (soma dos itens) * 2
    """

    DIMENSIONS = ["depressao", "ansiedade", "estresse"]

    DESCRIPTIONS = {
        "depressao": {
            "name": "Depressão",
            "high": "Indicadores elevados de humor deprimido, anedonia e baixa energia.",
            "low": "Indicadores reduzidos de humor deprimido.",
        },
        "ansiedade": {
            "name": "Ansiedade",
            "high": "Tensão elevada, hiperativação fisiológica, preocupação constante.",
            "low": "Indicadores reduzidos de ansiedade.",
        },
        "estresse": {
            "name": "Estresse",
            "high": "Sobrecarga emocional, irritabilidade, tensão persistente.",
            "low": "Baixa sobrecarga e boa regulação emocional.",
        },
    }

    NORMALIZATION_RANGE = (0, 100)

    # Mapeamento dos itens → subescala
    ITEM_MAP = {
        # Depressão
        "d1": "depressao", "d2": "depressao", "d3": "depressao",
        "d4": "depressao", "d5": "depressao", "d6": "depressao", "d7": "depressao",
        # Ansiedade
        "a1": "ansiedade", "a2": "ansiedade", "a3": "ansiedade",
        "a4": "ansiedade", "a5": "ansiedade", "a6": "ansiedade", "a7": "ansiedade",
        # Estresse
        "s1": "estresse", "s2": "estresse", "s3": "estresse",
        "s4": "estresse", "s5": "estresse", "s6": "estresse", "s7": "estresse",
    }

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("DASS-21 responses deve ser um dicionário.")

        for item, val in self.responses.items():
            if not isinstance(val, int):
                raise ValueError(f"Valor inválido em {item}: {val}")
            if val < 0 or val > 3:
                raise ValueError(f"Pontuação fora do intervalo permitido (0-3): {item}={val}")

    def compute_raw(self) -> Dict[str, float]:
        scores = {dim: 0 for dim in self.DIMENSIONS}

        for item, val in self.responses.items():
            key = item.lower()
            if key not in self.ITEM_MAP:
                continue
            dim = self.ITEM_MAP[key]
            scores[dim] += val

        # Score final oficial DASS-21
        for dim in scores:
            scores[dim] *= 2

        return scores

    def _normalize(self, value: float) -> float:
        raw_min, raw_max = 0, 42  # máximo da escala: 7 itens * 3 * 2
        norm_min, norm_max = self.NORMALIZATION_RANGE
        return ((value - raw_min) / (raw_max - raw_min)) * (norm_max - norm_min) + norm_min

    def compute(self) -> Dict[str, float]:
        raw = self.compute_raw()
        normalized = {dim: self._normalize(value) for dim, value in raw.items()}
        return normalized


# ---------------------------------------------------------------------------
# Wrapper oficial MindScan — dass21_process
# ---------------------------------------------------------------------------

def dass21_process(dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Wrapper padronizado para integrar o DASS-21 ao motor psicométrico.

    Entrada esperada:
        dataset["dass21_responses"] = {
            "d1": 2, "d2": 1, ..., "a1": 3, ..., "s7": 2
        }

    Saída padronizada:
        [
            {
                "dimension": str,
                "score": float,
                "descriptor": str,
                "metadata": dict
            }
        ]
    """

    if "dass21_responses" not in dataset:
        raise ValueError("Dataset não contém 'dass21_responses'.")

    model = DASS21Model(dataset["dass21_responses"])
    results = model.compute()

    output = []
    for dim, score in results.items():
        desc_block = DASS21Model.DESCRIPTIONS.get(dim, {})
        descriptor = desc_block.get("high") if score >= 50 else desc_block.get("low")

        output.append({
            "dimension": dim,
            "score": float(score),
            "descriptor": descriptor,
            "metadata": {
                "model": "dass21",
                "name": desc_block.get("name", dim),
                "timestamp": datetime.utcnow().isoformat(),
            },
        })

    return output