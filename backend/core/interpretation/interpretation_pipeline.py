# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\interpretation\interpretation_pipeline.py
# Última atualização: 2025-12-11T09:59:20.792728

from backend.mi.mi_narrative_polisher import MINarrativePolisher
from backend.mi.mi_risk_detector import MIRiskDetector
from backend.mi.mi_semantic_mapper import MISemanticMapper
from backend.mi.mi_cross_section_engine import MICrossSectionEngine

class InterpretationPipeline:
    """
    Pipeline que transforma resultados puros em uma narrativa interpretativa unificada.
    """

    @staticmethod
    def run(results: dict) -> dict:
        narrative = []

        # Insights semânticos
        semantic = MISemanticMapper.build_map(results)
        cross = MICrossSectionEngine.cross(results)

        narrative.append(f"Competências principais identificadas: {semantic.get('competency_alignment', {})}")
        narrative.append(f"Fatores cruzados relevantes: {cross}")

        # Riscos
        risks = MIRiskDetector.detect(results)
        if risks:
            narrative.append(f"Riscos identificados: {risks}")

        polished = MINarrativePolisher.polish(" ".join(narrative))

        return {
            "semantic": semantic,
            "cross": cross,
            "risks": risks,
            "narrative": polished
        }
