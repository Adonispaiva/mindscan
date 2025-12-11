# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\teique.py
# Última atualização: 2025-12-11T09:59:20.591856

# Caminho: D:\backend\algorithms\teique.py
# MindScan — TEIQue Padronizado v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo completo, final e padronizado para integração com a MindScanEngine

from typing import Dict, Any, List
from datetime import datetime

class TEIQUEModel:
    """
    Modelo TEIQue (Traço de Inteligência Emocional).
    Dimensões principais:
        - Bem-estar
        - Autocontrole
        - Emocionalidade
        - Sociabilidade
    """

    DIMENSIONS = ["bem_estar", "autocontrole", "emocionalidade", "sociabilidade"]

    DESCRIPTIONS: Dict[str, Dict[str, str]] = {
        "bem_estar": {
            "name": "Bem-estar",
            "high": "Confiança, otimismo, satisfação geral.",
            "low": "Autocrítica, preocupação, pessimismo.",
        },
        "autocontrole": {
            "name": "Autocontrole",
            "high": "Regulação emocional eficaz.",
            "low": "Impulsividade, dificuldade de controle emocional.",
        },
        "emocionalidade": {
            "name": "Emocionalidade",
            "high": "Expressividade emocional equilibrada.",
            "low": "Dificuldade de percepção emocional.",
        },
        "sociabilidade": {
            "name": "Sociabilidade",
            "high": "Habilidade social, assertividade.",
            "low": "Isolamento, dificuldade de interação.",
        },
    }

    NORMALIZATION_RANGE = (0, 100)

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("Responses deve ser um dicionário.")

    def _normalize(self, value: float) -> float:
        raw_min, raw_max = 1, 5
        norm_min, norm_max = self.NORMALIZATION_RANGE
        return ((value - raw_min) / (raw_max - raw_min)) * (norm_max - norm_min) + norm_min

    def compute(self) -> Dict[str, float]:
        scores = {dim: 0.0 for dim in self.DIMENSIONS}
        counts = {dim: 0 for dim in self.DIMENSIONS}

        for item, value in self.responses.items():
            dim = item.split("_")[0]
            if dim not in scores:
                continue
            scores[dim] += value
            counts[dim] += 1

        for dim in scores:
            if counts[dim] > 0:
                scores[dim] = self._normalize(scores[dim] / counts[dim])

        return scores


# ---------------------------------------------------------------------------
# Wrapper oficial MindScan — teique_process
# ---------------------------------------------------------------------------

def teique_process(dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Wrapper padronizado para integrar o TEIQue ao motor psicométrico.

    Entrada esperada:
        dataset["teique_responses"] = { "bem_estar_1": 4, "autocontrole_2": 3, ... }

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

    if "teique_responses" not in dataset:
        raise ValueError("Dataset não contém 'teique_responses'.")

    model = TEIQUEModel(dataset["teique_responses"])
    results = model.compute()

    output = []
    for dim, score in results.items():
        desc_block = TEIQUEModel.DESCRIPTIONS.get(dim, {})
        descriptor = desc_block.get("high") if score >= 50 else desc_block.get("low")

        output.append({
            "dimension": dim,
            "score": float(score),
            "descriptor": descriptor,
            "metadata": {
                "model": "teique",
                "name": desc_block.get("name", dim),
                "timestamp": datetime.utcnow().isoformat(),
            },
        })

    return output