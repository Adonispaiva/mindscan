# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\big5\big5.py
# Última atualização: 2025-12-11T09:59:20.594842

"""
BIG5 — Núcleo Principal (Versão Ultra Superior Inovexa)
--------------------------------------------------------

Pipeline completo do Big Five no MindScan Engine:
1. Validação de dados
2. Normalização avançada (Normas adaptativas)
3. Cálculo dimensional
4. Insights
5. Forças
6. Riscos
7. Crosslinks (com performance, estilos e TEIQue)
8. Necessidades emocionais (mapa expandido)
9. Enriquecimento semântico (trait-level → factor-level)
10. Previsão (modelo heurístico incremental)
11. Summary executivo
12. Formatação final (payload MindScan)

Garantias:
- Zero regressão
- Integrabilidade total com demais módulos
- Robustez contra dados ausentes
- Padrão Inovexa v2.0
"""

from typing import Dict, Any

from .big5_validation import Big5Validation
from .big5_norms import Big5Norms
from .big5_dimensions import Big5Dimensions
from .big5_insights import Big5Insights
from .big5_strengths import Big5Strengths
from .big5_risk_map import Big5RiskMap
from .big5_needs_map import Big5NeedsMap
from .big5_enrichment import Big5Enrichment
from .big5_crosslinks import Big5Crosslinks
from .big5_predictor import Big5Predictor
from .big5_summary import Big5Summary
from .big5_output_formatter import Big5OutputFormatter


class Big5:
    """Pipeline completo da avaliação Big Five para o MindScan."""

    def __init__(self):
        self.version = "2.0-ultra"

        # Motores internos
        self.validation = Big5Validation()
        self.norms = Big5Norms()
        self.dim_engine = Big5Dimensions()
        self.insights_engine = Big5Insights()
        self.strengths_engine = Big5Strengths()
        self.risk_engine = Big5RiskMap()
        self.needs_engine = Big5NeedsMap()
        self.enrichment_engine = Big5Enrichment()
        self.crosslinks_engine = Big5Crosslinks()
        self.predictor = Big5Predictor()
        self.summary_engine = Big5Summary()
        self.formatter = Big5OutputFormatter()

    def run(self, raw_scores: Dict[str, float]) -> Dict[str, Any]:
        # 1) Validação de entrada
        valid = self.validation.validate_raw(raw_scores)
        if not valid:
            return {
                "module": "Big5",
                "version": self.version,
                "error": "Invalid Big5 raw data.",
            }

        # 2) Normalização
        normalized = self.norms.normalize(raw_scores)

        # 3) Dimensões
        dims = self.dim_engine.compute(normalized)

        # 4) Insights dimensionais
        insights = self.insights_engine.generate(dims)

        # 5) Forças
        strengths = self.strengths_engine.extract(dims)

        # 6) Riscos
        risks = self.risk_engine.generate(dims)

        # 7) Necessidades emocionais (schema → personality)
        needs = self.needs_engine.map(dims)

        # 8) Enriquecimento semântico
        enrichment = self.enrichment_engine.enrich(dims)

        # 9) Crosslinks com outros módulos
        cross = self.crosslinks_engine.generate(dims)

        # 10) Previsão de padrões comportamentais
        prediction = self.predictor.predict(dims)

        # 11) Sumário executivo
        summary = self.summary_engine.build(
            dims=dims,
            strengths=strengths,
            risks=risks,
            needs=needs,
            enrichment=enrichment,
        )

        # 12) Payload final
        return self.formatter.format(
            normalized=normalized,
            dims=dims,
            insights=insights,
            strengths=strengths,
            risks=risks,
            needs=needs,
            enrichment=enrichment,
            crosslinks=cross,
            prediction=prediction,
            summary=summary,
        )
