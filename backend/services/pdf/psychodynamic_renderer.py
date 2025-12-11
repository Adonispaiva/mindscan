# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\psychodynamic_renderer.py
# Última atualização: 2025-12-11T09:59:21.200087

# psychodynamic_renderer.py — MindScan Psychodynamic Renderer (Extended)
# Autor: Leo Vinci — Inovexa Software
# --------------------------------------------------------------
# Renderer avançado destinado a análises psicodinâmicas profundas.
# Inclui páginas estendidas:
# - Estrutura Defensiva
# - Mapa de Tensão Emocional
# - Arquétipos de Dominância
# - Carga Cognitiva
# - Fluxo Psicodinâmico Integrado

from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from .narrativa import NarrativaPDF
from .identidade_emocional import IdentidadeEmocionalPDF
from .identidade_cognitiva import IdentidadeCognitivaPDF
from .estrutura_motivacional import EstruturaMotivacionalPDF
from .diagnostico_final import DiagnosticoFinalPDF

# Páginas estendidas (a serem criadas nos próximos lotes)
from .estrutura_defensiva import EstruturaDefensivaPDF
from .mapa_tensao_emocional import MapaTensaoEmocionalPDF
from .arquetipos_dominancia import ArquetiposDominanciaPDF
from .carga_cognitiva import CargaCognitivaPDF
from .fluxo_psicodinamico_integrado import FluxoPsicodinamicoIntegradoPDF


class PsychodynamicRenderer:
    """
    Renderer psicodinâmico completo — versão estendida.
    Destinado ao uso clínico, consultorias avançadas e análises profundas.
    """

    def __init__(self, output_path: str):
        self.output_path = output_path

        # Instanciar páginas
        self.narrativa = NarrativaPDF()
        self.emocional = IdentidadeEmocionalPDF()
        self.cognitiva = IdentidadeCognitivaPDF()
        self.motivacional = EstruturaMotivacionalPDF()
        self.diagnostico_final = DiagnosticoFinalPDF()

        # Extensões avançadas
        self.defensiva = EstruturaDefensivaPDF()
        self.tensao = MapaTensaoEmocionalPDF()
        self.arquetipos = ArquetiposDominanciaPDF()
        self.carga = CargaCognitivaPDF()
        self.fluxo = FluxoPsicodinamicoIntegradoPDF()

    # --------------------------------------------------------------

    def render(self, data: dict):
        """
        Dados esperados:
        {
            "psychodynamic": {...},
            "defensive_structure": {...},
            "emotional_tension": {...},
            "dominance_archetypes": {...},
            "cognitive_load": {...},
            "integrated_flow": {...},
            "final_diagnostic": {...}
        }
        """
        story = []

        # 1. Narrativa psicodinâmica
        self.narrativa.build(data.get("psychdynamic", {}), story)
        story.append(PageBreak())

        # 2. Identidade emocional
        self.emocional.build(data.get("psychdynamic", {}), story)
        story.append(PageBreak())

        # 3. Identidade cognitiva
        self.cognitiva.build(data.get("psychdynamic", {}), story)
        story.append(PageBreak())

        # 4. Estrutura motivacional
        self.motivacional.build(data.get("psychdynamic", {}), story)
        story.append(PageBreak())

        # 5. Estrutura defensiva (NOVA)
        self.defensiva.build(data.get("defensive_structure", {}), story)
        story.append(PageBreak())

        # 6. Mapa de tensão emocional (NOVA)
        self.tensao.build(data.get("emotional_tension", {}), story)
        story.append(PageBreak())

        # 7. Arquétipos de dominância (NOVA)
        self.arquetipos.build(data.get("dominance_archetypes", {}), story)
        story.append(PageBreak())

        # 8. Carga cognitiva (NOVA)
        self.carga.build(data.get("cognitive_load", {}), story)
        story.append(PageBreak())

        # 9. Fluxo psicodinâmico integrado (NOVA)
        self.fluxo.build(data.get("integrated_flow", {}), story)
        story.append(PageBreak())

        # 10. Diagnóstico Final
        self.diagnostico_final.build(data.get("final_diagnostic", {}), story)

        pdf = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        pdf.build(story)

        return self.output_path
