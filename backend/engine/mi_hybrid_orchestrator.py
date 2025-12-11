# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\mi_hybrid_orchestrator.py
# Última atualização: 2025-12-11T09:59:20.816000

# ============================================================
# MindScan — MI Hybrid Orchestrator (Final Integration Layer)
# ============================================================
# Função:
#   - Orquestrar o fluxo completo do MI Híbrido:
#       1. Engine Híbrido
#       2. Insight Engine
#       3. Reasoning Expander
#       4. Consistency Checker
#       5. Narrative Engine
#       6. Summary Builder
#       7. Score Engine
#       8. Payload Builder
#
#   - Entregar um pacote final ao ReportService
#     para renderização técnica, executiva,
#     psicodinâmica ou premium.
# ============================================================

from typing import Dict, Any

from .mi_engine_hybrid import MIEngineHybrid
from .hybrid_insight_engine import HybridInsightEngine
from .hybrid_reasoning_expander import HybridReasoningExpander
from .hybrid_consistency_checker import HybridConsistencyChecker
from .hybrid_narrative_engine import HybridNarrativeEngine
from .hybrid_summary_builder import HybridSummaryBuilder
from .hybrid_score_engine import HybridScoreEngine
from .hybrid_payload_builder import HybridPayloadBuilder


class MIHybridOrchestrator:

    def __init__(self):
        self.engine = MIEngineHybrid()
        self.insight_engine = HybridInsightEngine()
        self.consistency = HybridConsistencyChecker()
        self.reasoning_expander = HybridReasoningExpander()
        self.narrative_engine = HybridNarrativeEngine()
        self.summary_builder = HybridSummaryBuilder()
        self.score_engine = HybridScoreEngine()
        self.payload_builder = HybridPayloadBuilder()

    # ------------------------------------------------------------
    # EXECUÇÃO COMPLETA DO PIPELINE MI HÍBRIDO
    # ------------------------------------------------------------
    def run(self, payload: Dict[str, Any], mode: str = "hybrid_auto") -> Dict[str, Any]:

        # 1. Seleção do motor (classic, advanced, synmind, hybrid_auto)
        engine_output = self.engine.compute(payload, mode=mode)

        engine_used = engine_output.get("engine")
        mi_payload = engine_output.get("payload", {})
        persona = mi_payload.get("persona", {})

        normalized = mi_payload.get("normalized", {})
        insights_base = mi_payload.get("insights", {})

        # 2. Insights híbridos avançados
        insights = self.insight_engine.generate(normalized, insights_base)

        # 3. Expansão da cadeia de raciocínio
        base_chain = engine_output.get("payload", {}).get("reasoning", {}).get("chain", [])
        expanded_reasoning = self.reasoning_expander.expand(base_chain, insights)

        # 4. Checagem de consistência
        consistency_report = self.consistency.check(normalized, insights)

        # 5. Construção narrativa
        narrative = self.narrative_engine.generate(insights, normalized)

        # 6. Resumo executivo híbrido
        summary = self.summary_builder.build(insights, narrative)

        # 7. Scores híbridos globais
        scores = self.score_engine.compute_scores(normalized, insights)

        # 8. Montagem do payload final
        final_payload = self.payload_builder.assemble(
            engine_used=engine_used,
            normalized=normalized,
            insights=insights,
            narrative=narrative,
            summary=summary,
            scores=scores,
            persona=persona
        )

        # Inclusão do relatório de consistência (não vai para o PDF)
        final_payload["mi_consistency"] = consistency_report

        return final_payload
