# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\diagnostic\diagnostic_engine_v3.py
# Última atualização: 2025-12-11T09:59:20.777102

from backend.algorithms.core.scale_normalizer import ScaleNormalizer
from backend.algorithms.core.statistical_verifier import StatisticalVerifier
from backend.algorithms.core.cross_instrument_mapper import CrossInstrumentMapper
from backend.algorithms.core.performance_estimator import PerformanceEstimator
from backend.mi.mi_semantic_mapper import MISemanticMapper
from backend.mi.mi_cross_section_engine import MICrossSectionEngine
from backend.mi.mi_risk_detector import MIRiskDetector

class DiagnosticEngineV3:
    """
    Motor completo e final do MindScan Enterprise v3.0.
    Orquestra Big5, TEIQue, OCAI, DASS21 e MI.
    """

    @staticmethod
    def run(instruments: dict) -> dict:
        out = {}

        # 1 — Normalização global por instrumento
        if "big5" in instruments:
            out["big5"] = ScaleNormalizer.batch_normalize(instruments["big5"], 1, 5)

        if "teique" in instruments:
            out["teique"] = ScaleNormalizer.batch_normalize(instruments["teique"], 1, 7)

        if "dass21" in instruments:
            out["dass21"] = ScaleNormalizer.batch_normalize(instruments["dass21"], 0, 3)

        if "ocai" in instruments:
            out["ocai"] = ScaleNormalizer.batch_normalize(instruments["ocai"], 1, 5)

        # 2 — Estatística geral
        out["outliers"] = {}
        for k, v in out.items():
            if isinstance(v, dict):
                out["outliers"][k] = StatisticalVerifier.detect_outliers(v)

        # 3 — Cross-Instrument Insights
        out["semantic"] = MISemanticMapper.build_map(out)
        out["cross"] = MICrossSectionEngine.cross(out)

        # 4 — Predição de performance
        out["performance_estimate"] = PerformanceEstimator.estimate(out)

        # 5 — Riscos comportamentais
        out["risks"] = MIRiskDetector.detect(out)

        # 6 — Pontuação global final
        global_scores = []
        for block in ["performance_estimate"]:
            if isinstance(out.get(block), (int, float)):
                global_scores.append(out[block])

        out["global_score"] = round(sum(global_scores) / len(global_scores), 2) if global_scores else 50

        return out
