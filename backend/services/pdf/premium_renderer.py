# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\premium_renderer.py
# Última atualização: 2025-12-11T09:59:21.184463

# D:\mindscan\backend\services\pdf\premium_renderer.py
# ------------------------------------------------------
# Premium Renderer — MindScan PDF Engine v2
# Autor: Leo Vinci — Inovexa Software
#
# Este renderer Premium:
# - Orquestra TODAS as páginas do relatório
# - Gera PDF completo com identidade SynMind
# - É o pipeline principal usado em ambiente corporativo
#
# Fluxo geral:
# 1. Inicializa story e estilos
# 2. Monta capa
# 3. Monta todas as páginas de conteúdo (Fase 2)
# 4. Conclusão + Diagnóstico Final
# 5. Exporta PDF finalizado

from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# Importar páginas da Fase 2
from .capa_enterprise import CapaEnterprise
from .resumo_estrategico import ResumoEstrategico
from .narrativa import NarrativaPDF
from .identidade_emocional import IdentidadeEmocionalPDF
from .identidade_cognitiva import IdentidadeCognitivaPDF
from .estrutura_motivacional import EstruturaMotivacionalPDF
from .competencias import CompetenciasPDF
from .competencias_analiticas import CompetenciasAnaliticasPDF
from .planejamento import PlanejamentoPDF
from .performance import PerformancePDF
from .mapa_comportamental import MapaComportamentalPDF
from .mapa_operacional import MapaOperacionalPDF
from .sintese_executiva import SinteseExecutivaPDF
from .recomendacoes import RecomendacoesPDF
from .conclusao import ConclusaoPDF
from .diagnostico_final import DiagnosticoFinalPDF


class PremiumRenderer:
    """
    Renderer Premium do MindScan.
    Monta o PDF completo com todas as páginas da Fase 2.
    """

    def __init__(self, output_path: str, assets_path: str):
        self.output_path = output_path
        self.assets_path = assets_path

        # Instanciar páginas
        self.capa = CapaEnterprise(assets_path)
        self.resumo = ResumoEstrategico()
        self.narrativa = NarrativaPDF()
        self.emocional = IdentidadeEmocionalPDF()
        self.cognitiva = IdentidadeCognitivaPDF()
        self.motivacional = EstruturaMotivacionalPDF()
        self.competencias = CompetenciasPDF()
        self.competencias_analiticas = CompetenciasAnaliticasPDF()
        self.planejamento = PlanejamentoPDF()
        self.performance = PerformancePDF()
        self.comportamento = MapaComportamentalPDF()
        self.operacional = MapaOperacionalPDF()
        self.sintese = SinteseExecutivaPDF()
        self.recomendacoes = RecomendacoesPDF()
        self.conclusao = ConclusaoPDF(assets_path)
        self.diagnostico_final = DiagnosticoFinalPDF()

    # --------------------------------------------------------------
    # GERADOR PRINCIPAL DO PDF
    # --------------------------------------------------------------

    def render(self, data: dict):
        """
        Constrói o relatório Premium completo.
        'data' inclui:

        {
            "test_id": "...",
            "diagnostics": {...},
            "psychodynamic": {...},
            "competencies": {...},
            "competencies_analytical": {...},
            "planning": {...},
            "performance": {...},
            "behavior": {...},
            "operational": {...},
            "executive_summary": {...},
            "recommendations": {...},
            "conclusion": {...},
            "final_diagnostic": {...}
        }
        """

        story = []

        # ---------------------
        # 1. CAPA
        # ---------------------
        self.capa.build(data.get("test_id", "N/D"), story)
        story.append(PageBreak())

        # ---------------------
        # 2. RESUMO EXECUTIVO
        # ---------------------
        self.resumo.build(data, story)
        story.append(PageBreak())

        # ---------------------
        # 3. NARRATIVA PSICODINÂMICA
        # ---------------------
        self.narrativa.build(data.get("psychodynamic", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 4. IDENTIDADE EMOCIONAL
        # ---------------------
        self.emocional.build(data.get("psychodynamic", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 5. IDENTIDADE COGNITIVA
        # ---------------------
        self.cognitiva.build(data.get("psychdynamic", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 6. ESTRUTURA MOTIVACIONAL
        # ---------------------
        self.motivacional.build(data.get("psychdynamic", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 7. COMPETÊNCIAS
        # ---------------------
        self.competencias.build(data.get("competencies", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 8. COMPETÊNCIAS ANALÍTICAS
        # ---------------------
        self.competencias_analiticas.build(data.get("competencies_analytical", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 9. PLANEJAMENTO
        # ---------------------
        self.planejamento.build(data.get("planning", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 10. PERFORMANCE
        # ---------------------
        self.performance.build(data.get("performance", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 11. COMPORTAMENTO
        # ---------------------
        self.comportamento.build(data.get("behavior", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 12. MAPA OPERACIONAL
        # ---------------------
        self.operacional.build(data.get("operational", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 13. SÍNTESE EXECUTIVA
        # ---------------------
        self.sintese.build(data.get("executive_summary", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 14. RECOMENDAÇÕES
        # ---------------------
        self.recomendacoes.build(data.get("recommendations", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 15. CONCLUSÃO
        # ---------------------
        self.conclusao.build(data.get("conclusion", {}), story)
        story.append(PageBreak())

        # ---------------------
        # 16. DIAGNÓSTICO FINAL
        # ---------------------
        self.diagnostico_final.build(data.get("final_diagnostic", {}), story)

        # ---------------------
        # EXPORTAÇÃO FINAL
        # ---------------------
        pdf = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        pdf.build(story)

        return self.output_path
