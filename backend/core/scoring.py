# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\scoring.py
# Última atualização: 2025-12-11T09:59:20.777102

from typing import Dict, Any, List


class ScoringEngine:
    """
    Engine de pontuação psicométrica do MindScan 2.0.

    A versão superior unifica o cálculo de scores para todos
    os instrumentos suportados:
    - BIG5
    - TEIQue
    - OCAI
    - DASS-21
    - E instrumentos futuros.
    """

    # ------------------------------------------------------------
    #  MAPA DE PONTUAÇÃO PADRÃO (placeholder)
    # ------------------------------------------------------------
    INSTRUMENT_WEIGHTS = {
        "BIG5": 1.0,
        "TEIQue": 1.0,
        "OCAI": 1.0,
        "DASS21": 1.0,
    }

    def compute_scores(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        instruments = dataset.get("instruments", [])
        scores: Dict[str, Any] = {}

        for inst in instruments:
            name = inst.get("instrument")
            answers = inst.get("answers", [])

            if not name:
                continue

            method = getattr(self, f"_score_{name.lower()}", None)
            if callable(method):
                scores[name] = method(answers)
            else:
                scores[name] = self._score_generic(answers)

        return scores

    # ------------------------------------------------------------
    #  SCORES POR INSTRUMENTO
    # ------------------------------------------------------------
    def _score_big5(self, answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        # BIG5: cálculo simplificado para placeholder
        values = [a.get("value", 0) for a in answers]
        avg = sum(values) / len(values) if values else 0
        return {"avg": avg, "raw": values}

    def _score_teiQue(self, answers: List[Dict[str, Any]]):
        # Placeholder TEIQue
        values = [a.get("value", 0) for a in answers]
        return {"sum": sum(values), "count": len(values)}

    def _score_ocai(self, answers: List[Dict[str, Any]]):
        # Placeholder OCAI
        values = [a.get("value", 0) for a in answers]
        return {"profile": values}

    def _score_dass21(self, answers: List[Dict[str, Any]]):
        # Placeholder DASS21
        values = [a.get("value", 0) for a in answers]
        return {"score": sum(values)}

    # ------------------------------------------------------------
    #  SCORE GENÉRICO — fallback
    # ------------------------------------------------------------
    def _score_generic(self, answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        values = [a.get("value", 0) for a in answers]
        return {"generic_score": sum(values)}
