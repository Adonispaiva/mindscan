# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola.py
# Última atualização: 2025-12-11T09:59:20.573935

# Caminho: D:\backend\algorithms\bussola.py
# MindScan — Bússola Cognitiva Padronizada v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Arquivo completo, final e padronizado para integração com a MindScanEngine

from typing import Dict, Any, List
from datetime import datetime

class CompassModel:
    """
    Bússola Cognitiva MindScan — síntese final.

    Integra padrões psicométricos para determinar:
        - estilo decisório
        - eixo emocional
        - eixo racional
        - direção cognitiva predominante

    Saída esperada pela Engine:
        { dimension, score, descriptor, metadata }
    """

    DIMENSIONS = [
        "eixo_racional",
        "eixo_emocional",
        "estilo_decisorio",
        "direcao_geral",
    ]

    DESCRIPTIONS = {
        "eixo_racional": {
            "name": "Eixo Racional",
            "high": "Decisão orientada por lógica e análise.",
            "low": "Menor uso de análise estruturada.",
        },
        "eixo_emocional": {
            "name": "Eixo Emocional",
            "high": "Alta sensibilidade emocional nas decisões.",
            "low": "Baixa interferência emocional.",
        },
        "estilo_decisorio": {
            "name": "Estilo Decisório",
            "high": "Tomada de decisão rápida e assertiva.",
            "low": "Tomada de decisão cautelosa e reflexiva.",
        },
        "direcao_geral": {
            "name": "Direção Cognitiva Geral",
            "high": "Orientação voltada à ação e resultados.",
            "low": "Orientação voltada à análise e reflexão.",
        },
    }

    NORMALIZATION_RANGE = (0, 100)

    def __init__(self, dataset: Dict[str, Any]):
        self.data = dataset

    # -------------------- Cálculos Sintéticos --------------------

    def compute_eixo_racional(self) -> float:
        big5 = self.data.get("big5_responses", {})
        if not big5:
            return 0
        # Exemplo: racionalidade correlaciona com Conscienciosidade (C)
        c_items = [v for k, v in big5.items() if k.startswith("C")]
        if not c_items:
            return 0
        return (sum(c_items) / len(c_items)) * 20

    def compute_eixo_emocional(self) -> float:
        teique = self.data.get("teique_responses", {})
        if not teique:
            return 0
        media = sum(teique.values()) / max(1, len(teique))
        return (media / 5) * 100

    def compute_estilo_decisorio(self) -> float:
        perf = self.data.get("performance_responses", {})
        if not perf:
            return 0
        ritmo_items = [v for k, v in perf.items() if k.startswith("ritmo")]
        if not ritmo_items:
            return 0
        return (sum(ritmo_items) / len(ritmo_items)) * 20

    def compute_direcao_geral(self) -> float:
        ocai = self.data.get("ocai_responses", {})
        if not ocai:
            return 0
        return min(100, (sum(ocai.values()) / max(1, len(ocai))))

    # -------------------- Orquestração --------------------

    def compute(self) -> Dict[str, float]:
        return {
            "eixo_racional": self.compute_eixo_racional(),
            "eixo_emocional": self.compute_eixo_emocional(),
            "estilo_decisorio": self.compute_estilo_decisorio(),
            "direcao_geral": self.compute_direcao_geral(),
        }


# ---------------------------------------------------------------------------
# Wrapper oficial MindScan — compass_process
# ---------------------------------------------------------------------------

def compass_process(dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Wrapper padronizado para integrar a Bússola Cognitiva ao MindScanEngine.

    Entrada esperada: dataset completo preparado pelo DataService.

    Saída padronizada MindScan v2.0.
    """

    model = CompassModel(dataset)
    results = model.compute()

    output = []
    for dim, score in results.items():
        desc_block = CompassModel.DESCRIPTIONS.get(dim, {})
        descriptor = desc_block.get("high") if score >= 50 else desc_block.get("low")

        output.append({
            "dimension": dim,
            "score": float(score),
            "descriptor": descriptor,
            "metadata": {
                "model": "compass",
                "name": desc_block.get("name", dim),
                "timestamp": datetime.utcnow().isoformat(),
            },
        })

    return output