"""
OCAI — Cultura Organizacional
Pipeline completo: validação → normas → dimensões → descritores → alertas → crosslinks → resumo → formatação final.
"""

from typing import Dict, Any

from .ocai_norms import OCAINorms
from .ocai_dimensions import OCAIDimensions
from .ocai_descriptives import OCAIDescriptives
from .ocai_alerts import OCAIAlerts
from .ocai_crosslinks import OCAICrosslinks
from .ocai_summary import OCAISummary
from .ocai_output_formatter import OCAIOutputFormatter
from .ocai_validation import OCAIValidation


class OCAI:
    def __init__(self):
        self.norms = OCAINorms()
        self.dimensions = OCAIDimensions()
        self.descriptives = OCAIDescriptives()
        self.alerts = OCAIAlerts()
        self.cross = OCAICrosslinks()
        self.summary_engine = OCAISummary()
        self.formatter = OCAIOutputFormatter()
        self.validation = OCAIValidation()

    def run(self, raw_scores: Dict[str, float]) -> Dict[str, Any]:
        # Validação
        if not self.validation.validate_raw(raw_scores):
            return {"error": "Invalid OCAI raw scores"}

        # Normalização
        normalized = self.norms.normalize(raw_scores)

        # Dimensões
        dims = self.dimensions.compute(normalized)

        # Descritores
        desc = self.descriptives.describe(dims)

        # Alertas
        alerts = self.alerts.generate(dims)

        # Crosslinks
        crosslinks = self.cross.generate(dims)

        # Resumo
        summary = self.summary_engine.summarize(dims)

        # Formatação final
        return self.formatter.format(
            dims=dims,
            descriptives=desc,
            crosslinks=crosslinks,
            alerts=alerts
        ) | {"summary": summary}
