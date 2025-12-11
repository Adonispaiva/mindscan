# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\mi\mi_engine.py
# Última atualização: 2025-12-11T09:59:21.163629

from .persona import MindScanPersona
from .style_engine import StyleEngine
from .compliance_filter import ComplianceFilter
from .narrative_engine import NarrativeEngine
from .integration_engine import IntegrationEngine

class MIEngine:
    """
    Orquestrador principal da inteligência MindScan.
    Gera o texto final a ser enviado aos renderers PDF.
    """

    def __init__(self, results):
        self.results = results
        self.persona = MindScanPersona()
        self.style_engine = StyleEngine(self.persona)
        self.compliance = ComplianceFilter()
        self.integrator = IntegrationEngine()
        self.narrative_engine = NarrativeEngine(results)

    def generate(self):
        # 1) Gerar narrativas brutas
        exec_narr = self.narrative_engine.generate_executive_narrative()
        psych_narr = self.narrative_engine.generate_psychodynamic_narrative()
        integrated = self.narrative_engine.generate_integrated()

        # 2) Integrar
        merged = self.integrator.integrate([
            exec_narr,
            psych_narr,
            integrated
        ])

        # 3) Aplicar estilo
        styled = self.style_engine.apply_style(merged)

        # 4) Compliance
        compliant = self.compliance.filter(styled)

        return compliant
