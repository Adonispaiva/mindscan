# Caminho: D:\backend\algorithms\performance.py
# MindScan — Performance Behavioral Model Padronizado v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo completo, final e padronizado para integração com a MindScanEngine

from typing import Dict, Any, List
from datetime import datetime

class PerformanceModel:
    """
    Modelo oficial de Perfis de Performance MindScan.

    O modelo converte padrões comportamentais (1–5) em scores normalizados.

    Dimensões típicas:
        - foco
        - ritmo
        - consistencia
        - adaptabilidade
        - autonomia
        - proatividade
        - confiabilidade
    """

    DIMENSIONS = [
        "foco",
        "ritmo",
        "consistencia",
        "adaptabilidade",
        "autonomia",
        "proatividade",
        "confiabilidade",
    ]

    DESCRIPTIONS = {
        "foco": {
            "name": "Foco",
            "high": "Alta concentração e direção clara.",
            "low": "Dispersão e dificuldade de manter atenção.",
        },
        "ritmo": {
            "name": "Ritmo",
            "high": "Entrega acelerada e produtividade.",
            "low": "Ritmo lento, menor energia.",
        },
        "consistencia": {
            "name": "Consistência",
            "high": "Estabilidade e previsibilidade.",
            "low": "Oscilações frequentes.",
        },
        "adaptabilidade": {
            "name": "Adaptabilidade",
            "high": "Flexibilidade diante de mudanças.",
            "low": "Rigidez e dificuldade de transição.",
        },
        "autonomia": {
            "name": "Autonomia",
            "high": "Capacidade de trabalhar sem supervisão.",
            "low": "Dependência de orientação constante.",
        },
        "proatividade": {
            "name": "Proatividade",
            "high": "Iniciativa, antecipação de necessidades.",
            "low": "Ação reativa, aguardando instruções.",
        },
        "confiabilidade": {
            "name": "Confiabilidade",
            "high": "Entrega consistente e responsabilidade.",
            "low": "Imprevisibilidade e incumprimento.",
        },
    }

    NORMALIZATION_RANGE = (0, 100)

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("Performance responses deve ser um dicionário.")
        for item, val in self.responses.items():
            if not isinstance(val, int):
                raise ValueError(f"Valor inválido em {item}: {val}")
            if val < 1 or val > 5:
                raise ValueError(f"Pontuação fora do intervalo (1–5): {item}={val}")

    def _normalize(self, value: float) -> float:
        raw_min, raw_max = 1, 5
        norm_min, norm_max = self.NORMALIZATION_RANGE
        return ((value - raw_min) / (raw_max - raw_min)) * (norm_max - norm_min) + norm_min

    def compute(self) -> Dict[str, float]:
        scores = {dim: 0.0 for dim in self.DIMENSIONS}
        counts = {dim: 0 for dim in self.DIMENSIONS}

        for item, val in self.responses.items():
            dim = item.split("_")[0]
            if dim not in scores:
                continue
            scores[dim] += val
            counts[dim] += 1

        for dim in scores:
            if counts[dim] > 0:
                avg = scores[dim] / counts[dim]
                scores[dim] = self._normalize(avg)

        return scores


# ---------------------------------------------------------------------------
# Wrapper oficial MindScan — performance_process
# ---------------------------------------------------------------------------

def performance_process(dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Wrapper padronizado para integrar Performance ao motor MindScan.

    Entrada esperada:
        dataset["performance_responses"] = {
            "foco_1": 4,
            "ritmo_1": 5,
            "consistencia_2": 3,
            ...
        }

    Saída padronizada conforme MindScan v2.0.
    """

    if "performance_responses" not in dataset:
        raise ValueError("Dataset não contém 'performance_responses'.")

    model = PerformanceModel(dataset["performance_responses"])
    results = model.compute()

    output = []
    for dim, score in results.items():
        desc_block = PerformanceModel.DESCRIPTIONS.get(dim, {})
        descriptor = desc_block.get("high") if score >= 50 else desc_block.get("low")

        output.append({
            "dimension": dim,
            "score": float(score),
            "descriptor": descriptor,
            "metadata": {
                "model": "performance",
                "name": desc_block.get("name", dim),
                "timestamp": datetime.utcnow().isoformat(),
            },
        })

    return output