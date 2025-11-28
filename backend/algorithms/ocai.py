# Caminho: D:\backend\algorithms\ocai.py
# MindScan — OCAI Padronizado v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo completo, final e padronizado para integração com a MindScanEngine

from typing import Dict, Any, List
from datetime import datetime

class OCAIModel:
    """
    Modelo OCAI (Organizational Culture Assessment Instrument).

    Dimensões:
        - clan
        - adhocracy
        - market
        - hierarchy

    Cada dimensão é derivada da soma das alocações em seus respectivos itens.
    """

    DIMENSIONS = ["clan", "adhocracy", "market", "hierarchy"]

    DESCRIPTIONS = {
        "clan": {
            "name": "Cultura Clan",
            "high": "Ambiente colaborativo, suporte, senso de família.",
            "low": "Baixa coesão, pouca colaboração.",
        },
        "adhocracy": {
            "name": "Cultura Adhocracia",
            "high": "Inovação, experimentação, autonomia.",
            "low": "Rigidez, baixa criatividade.",
        },
        "market": {
            "name": "Cultura de Mercado",
            "high": "Competitividade, metas, performance.",
            "low": "Baixa orientação a resultados.",
        },
        "hierarchy": {
            "name": "Cultura Hierárquica",
            "high": "Estrutura, controle, estabilidade.",
            "low": "Desorganização, baixa previsibilidade.",
        },
    }

    NORMALIZATION_RANGE = (0, 100)

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("OCAI responses deve ser um dicionário.")
        for item, val in self.responses.items():
            if not isinstance(val, (int, float)):
                raise ValueError(f"Valor inválido em {item}: {val}")

    def compute_raw(self) -> Dict[str, float]:
        scores = {dim: 0.0 for dim in self.DIMENSIONS}
        counts = {dim: 0 for dim in self.DIMENSIONS}

        for item, val in self.responses.items():
            dim = item.split("_")[0]
            if dim not in scores:
                continue
            scores[dim] += float(val)
            counts[dim] += 1

        for dim in scores:
            if counts[dim] > 0:
                scores[dim] /= counts[dim]

        return scores

    def _normalize(self, value: float) -> float:
        raw_min, raw_max = 0, 100
        norm_min, norm_max = self.NORMALIZATION_RANGE
        if raw_max - raw_min == 0:
            return 0
        return ((value - raw_min) / (raw_max - raw_min)) * (norm_max - norm_min) + norm_min

    def compute(self) -> Dict[str, float]:
        raw_scores = self.compute_raw()
        normalized = {
            dim: self._normalize(score) for dim, score in raw_scores.items()
        }
        return normalized


# ---------------------------------------------------------------------------
# Wrapper oficial MindScan — ocai_process
# ---------------------------------------------------------------------------

def ocai_process(dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Wrapper padronizado para integrar o OCAI ao motor psicométrico.

    Entrada esperada:
        dataset["ocai_responses"] = { "clan_1": 25, "market_2": 40, ... }

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

    if "ocai_responses" not in dataset:
        raise ValueError("Dataset não contém 'ocai_responses'.")

    model = OCAIModel(dataset["ocai_responses"])
    results = model.compute()

    output = []
    for dim, score in results.items():
        desc_block = OCAIModel.DESCRIPTIONS.get(dim, {})
        descriptor = desc_block.get("high") if score >= 50 else desc_block.get("low")

        output.append({
            "dimension": dim,
            "score": float(score),
            "descriptor": descriptor,
            "metadata": {
                "model": "ocai",
                "name": desc_block.get("name", dim),
                "timestamp": datetime.utcnow().isoformat(),
            },
        })

    return output
