# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\resumo_estrategico.py
# Última atualização: 2025-12-11T09:59:21.200087

# D:\mindscan\backend\services\pdf\resumo_estrategico.py
# -------------------------------------------------------
# Resumo Estratégico MindScan — Página Executiva
# Autor: Leo Vinci — Inovexa Software
#
# Esta página é utilizada pelos templates:
# - Executive Renderer
# - Premium Renderer
#
# Funções:
# - Apresentar visão executiva do perfil MindScan
# - Destacar forças e riscos globais
# - Introduzir indicadores corporativos essenciais

from reportlab.platypus import Paragraph, Spacer, Frame, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class ResumoEstrategico:
    """
    Constrói a segunda página do relatório MindScan,
    contendo visão executiva de alto nível.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = self._build_title_style()
        self.section_style = self._build_section_style()

    # ----------------------------------------------------------------------
    # ESTILOS
    # ----------------------------------------------------------------------

    def _build_title_style(self):
        style = self.styles["Heading1"]
        style.fontSize = 20
        style.leading = 24
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 14
        return style

    def _build_section_style(self):
        style = self.styles["Heading2"]
        style.fontSize = 14
        style.leading = 18
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 10
        return style

    # ----------------------------------------------------------------------
    # CONSTRUÇÃO
    # ----------------------------------------------------------------------

    def build(self, report_data: dict, story: list):
        """
        Monta o resumo estratégico a partir dos dados corporativos.
        """

        # Título da página
        story.append(Paragraph("Resumo Estratégico", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        # --------------------------------------------------------------
        # Forças & Riscos
        # --------------------------------------------------------------

        diagnostics = report_data.get("diagnostics", {})

        strengths = diagnostics.get("strengths", ["Dados não fornecidos"])
        risks = diagnostics.get("risks", ["Dados não fornecidos"])

        strengths_text = "<br/>".join([f"• {s}" for s in strengths])
        risks_text = "<br/>".join([f"• {r}" for r in risks])

        table_data = [
            ["Principais Forças", "Riscos Globais"],
            [strengths_text, risks_text],
        ]

        table = Table(
            table_data,
            colWidths=[9 * cm, 9 * cm],
            hAlign="LEFT",
        )

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EEF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#003366")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#003366")),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(table)
        story.append(Spacer(0, 1.2 * cm))

        # --------------------------------------------------------------
        # Indicadores Globais MindScan
        # --------------------------------------------------------------

        indicators = report_data.get("global_indicators", {})

        if indicators:
            story.append(Paragraph("Indicadores Globais MindScan", self.section_style))

            rows = []
            for key, value in indicators.items():
                rows.append([key, f"{value}"])

            indicators_table = Table(
                [["Indicador", "Valor"]] + rows,
                colWidths=[10 * cm, 8 * cm],
            )

            indicators_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EEF7")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#003366")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#003366")),
                    ("VALIGN", (0, 1), (-1, -1), "TOP"),
                ])
            )

            story.append(indicators_table)
            story.append(Spacer(0, 1 * cm))

        return story
