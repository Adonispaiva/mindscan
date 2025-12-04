"""
TEIQue — Módulo Principal
Integra:
- validação
- normalização
- mapa de traços
- fatores
- forças
- riscos
- sumário
- formatter final
"""

from typing import Dict, Any

from .teique_validation import TeiqueValidation
from .teique_traits_map import TeiqueTraitsMap
from .teique_factor_weights import TeiqueFactorWeights
from .teique_insights import TeiqueInsights
from .teique_strengths import TeiqueStrengths
from .teique_risk_flags import TeiqueRiskFlags
from .teique_risk_map import TeiqueRiskMap
from .teique_profile_builder import TeiqueProfileBuilder
from .teique_summary import TeiqueSummary
from .teique_output_formatter import TeiqueOutputFormatter
from .teique_norms import TeiqueNorms


class TEIQue:
    """
    Pipeline completo do TEIQue utilizado pelo MindScanEngine.
    """

    def __init__(self):
        self.version = "1.0"

        # Componentes
        self.validator = TeiqueValidation()
        self.traits = TeiqueTraitsMap()
        self.norms = TeiqueNorms()
        self.factor_weights = TeiqueFactorWeights()
        self.insights = TeiqueInsights()
        self.strengths = TeiqueStrengths()
        self.risk_flags = TeiqueRiskFlags()
        self.risk_map = TeiqueRiskMap()
        self.profile_builder = TeiqueProfileBuilder()
        self.summary_builder = TeiqueSummary()
        self.formatter = TeiqueOutputFormatter()

    def run(self, raw_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Fluxo oficial:
        1. valida input
        2. normaliza com normas
        3. extrai insights, riscos, forças
        4. gera fatores agregados
        5. constrói perfil
        6. monta sumário
        7. formata payload final
        """

        validation = self.validator.validate(raw_scores)
        if not validation["valid"]:
            return {
                "module": "TEIQue",
                "version": self.version,
                "error": "Invalid TEIQue payload",
                "details": validation,
            }

        normalized = self.norms.normalize(raw_scores)
        insights = self.insights.generate(normalized)
        traits = self.traits.map_traits(normalized)
        factors = self.factor_weights.compute(normalized)
        strengths = self.strengths.extract(normalized)
        risk_flags = self.risk_flags.evaluate(normalized, factors)
        risk_map = self.risk_map.build(risk_flags["dimension_risks"])
        profile = self.profile_builder.build(normalized)
        summary = self.summary_builder.build(
            normalized,
            profile["factors"],
            strengths["strengths"],
            risk_map["risks"],
        )

        return self.formatter.format(
            scores=normalized,
            metadata={
                "validation": validation,
                "insights": insights,
                "traits": traits,
                "profile": profile,
                "summary": summary,
                "risk_map": risk_map,
            },
        )
