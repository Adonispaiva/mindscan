# Caminho: D:\backend\algorithms\esquemas.py
# MindScan — Esquemas Desadaptativos (EMS) Padronizado v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo completo, final e padronizado para integração com a MindScanEngine

from typing import Dict, Any, List
from datetime import datetime

class EMSModel:
    """
    Modelo oficial de Esquemas Desadaptativos Precoces (Young).

    Esta implementação padronizada converte respostas individuais
    (1 a 6) em médias por esquema, normaliza para 0–100 e gera
    descritores de intensidade.

    Exemplos de esquemas:
    - abandono
    - desconfiança
    - privacao
    - defeito
    - fracasso
    - dependência
    - vulnerabilidade
    - emaranhamento
    - subjugação
    - autosacrificio
    - padroes
    - punicao
    """

    NORMALIZATION_RANGE = (0, 100)

    # Mapeamento de prefixos → Esquemas
    SCHEMA_MAP = {
        "aba": "abandono",
        "des": "desconfianca",
        "pri": "privacao",
        "def": "defeito",
        "fra": "fracasso",
        "dep": "dependencia",
        "vul": "vulnerabilidade",
        "ema": "emaranhamento",
        "sub": "subjugacao",
        "aut": "autosacrificio",
        "pad": "padroes",
        "pun": "punicao",
    }

    DESCRIPTIONS = {
        "abandono": {
            "name": "Abandono",
            "high": "Medo intenso de perda, instabilidade emocional.",
            "low": "Segurança emocional consistente.",
        },
        "desconfianca": {
            "name": "Desconfiança",
            "high": "Expectativa de dano, suspeita constante.",
            "low": "Abertura saudável e confiança.",
        },
        "privacao": {
            "name": "Privação",
            "high": "Sensação de não receber apoio ou cuidado.",
            "low": "Satisfação emocional adequada.",
        },
        "defeito": {
            "name": "Defeito",
            "high": "Autodepreciação, vergonha, autocrítica.",
            "low": "Autoaceitação e autovalor.",
        },
        "fracasso": {
            "name": "Fracasso",
            "high": "Sentimento persistente de incapacidade.",
            "low": "Competência percebida elevada.",
        },
        "dependencia": {
            "name": "Dependência",
            "high": "Dificuldade de autonomia.",
            "low": "Autonomia consistente.",
        },
        "vulnerabilidade": {
            "name": "Vulnerabilidade",
            "high": "Medo de catástrofes, insegurança.",
            "low": "Senso de segurança.",
        },
        "emaranhamento": {
            "name": "Emaranhamento",
            "high": "Fusão emocional, autoidentidade frágil.",
            "low": "Independência emocional.",
        },
        "subjugacao": {
            "name": "Subjugação",
            "high": "Supressão de necessidades em favor de outros.",
            "low": "Assertividade equilibrada.",
        },
        "autosacrificio": {
            "name": "Autosacrifício",
            "high": "Doação excessiva, exaustão.",
            "low": "Equilíbrio entre si e outros.",
        },
        "padroes": {
            "name": "Padrões Inflexíveis",
            "high": "Perfecionismo rígido, autocobrança.",
            "low": "Flexibilidade emocional.",
        },
        "punicao": {
            "name": "Punição",
            "high": "Autopunição, rigidez moral.",
            "low": "Autocompaixão e tolerância.",
        },
    }

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("EMS responses deve ser um dicionário.")
        for item, val in self.responses.items():
            if not isinstance(val, int):
                raise ValueError(f"Valor inválido em {item}: {val}")
            if val < 1 or val > 6:
                raise ValueError(f"Pontuação fora do intervalo (1–6): {item}={val}")

    def _normalize(self, value: float) -> float:
        raw_min, raw_max = 1, 6
        norm_min, norm_max = self.NORMALIZATION_RANGE
        return ((value - raw_min) / (raw_max - raw_min)) * (norm_max - norm_min) + norm_min

    def compute(self) -> Dict[str, float]:
        scores = {}
        counts = {}

        for item, val in self.responses.items():
            prefix = item[:3].lower()
            if prefix not in self.SCHEMA_MAP:
                continue
            schema = self.SCHEMA_MAP[prefix]
            if schema not in scores:
                scores[schema] = 0
                counts[schema] = 0
            scores[schema] += val
            counts[schema] += 1

        for schema in scores:
            avg = scores[schema] / counts[schema]
            scores[schema] = self._normalize(avg)

        return scores


# ---------------------------------------------------------------------------
# Wrapper oficial MindScan — schema_process
# ---------------------------------------------------------------------------

def schema_process(dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Wrapper padronizado para integrar Esquemas Desadaptativos ao motor.

    Entrada esperada:
        dataset["schema_responses"] = {
            "aba1": 5, "aba2": 4,
            "def1": 6, "def2": 5,
            ...
        }

    Saída padronizada conforme MindScan v2.0:
        [
            {
                "dimension": str,
                "score": float,
                "descriptor": str,
                "metadata": dict
            }
        ]
    """

    if "schema_responses" not in dataset:
        raise ValueError("Dataset não contém 'schema_responses'.")

    model = EMSModel(dataset["schema_responses"])
    results = model.compute()

    output = []
    for schema, score in results.items():
        desc_block = EMSModel.DESCRIPTIONS.get(schema, {})
        descriptor = desc_block.get("high") if score >= 50 else desc_block.get("low")

        output.append({
            "dimension": schema,
            "score": float(score),
            "descriptor": descriptor,
            "metadata": {
                "model": "esquemas",
                "name": desc_block.get("name", schema),
                "timestamp": datetime.utcnow().isoformat(),
            },
        })

    return output