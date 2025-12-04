"""
Performance Time Series
Módulo responsável por análise temporal (evolutiva) da performance
profissional ao longo de múltiplas medições.

Funções principais:
- comparar medidas antigas e atuais
- calcular deltas e tendências
- gerar interpretação da evolução
"""

from typing import Dict, List, Any


class PerformanceTimeSeries:
    def __init__(self):
        self.version = "1.0"

    def compute_delta(self, old: Dict[str, float], new: Dict[str, float]) -> Dict[str, float]:
        """
        Calcula a diferença entre duas medições de performance.
        Retorna: {dimensão: delta}
        """
        deltas = {}
        keys = set(old.keys()) | set(new.keys())

        for k in keys:
            deltas[k] = new.get(k, 0) - old.get(k, 0)

        return deltas

    def compute_trend(self, history: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Recebe uma lista de medições ordenadas do mais antigo para o mais recente:
        history = [medicao1, medicao2, ..., medicaoN]

        Retorna:
        - tendência média (por dimensão)
        - direção global (melhora, estabilidade ou queda)
        """

        if not history or len(history) < 2:
            return {
                "trend": {},
                "direction": "insuficiente",
                "message": "Histórico insuficiente para análise temporal."
            }

        all_dims = set()
        for h in history:
            all_dims |= set(h.keys())

        trend = {}

        for dim in all_dims:
            values = [h.get(dim, 0) for h in history]
            if len(values) < 2:
                trend[dim] = 0
            else:
                trend[dim] = values[-1] - values[0]

        # Direção global
        avg_trend = sum(trend.values()) / len(trend) if trend else 0

        if avg_trend > 5:
            direction = "melhora"
        elif avg_trend < -5:
            direction = "queda"
        else:
            direction = "estabilidade"

        return {
            "trend": trend,
            "direction": direction,
            "message": f"Evolução global indica: {direction}.",
            "version": self.version,
        }

    def analyze(self, history: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Pipeline completo de análise temporal.
        """

        trend_data = self.compute_trend(history)

        deltas = {}
        if len(history) >= 2:
            deltas = self.compute_delta(history[-2], history[-1])

        return {
            "module": "Performance",
            "version": self.version,
            "trend": trend_data,
            "delta_latest": deltas,
            "samples": len(history)
        }
