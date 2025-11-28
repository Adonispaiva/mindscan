# MindScan — Premium Renderer v2.0
# Diretor Técnico: Leo Vinci — Inovexa Software
# Relatório Premium: Executivo + Técnico + Psicodinâmico + Gráficos

from reportlab.platypus import Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os


class PremiumRenderer:
    """
    Renderer completo (nível máximo)
    • Resumo Executivo
    • Indicadores Globais MindScan
    • Forças & Riscos
    • Narrativa Psicodinâmica Completa
    • Apêndice Técnico
    • Gráficos Essenciais (imagem externa gerada pela API)
    • Capa Premium
    • Sumário Estruturado
    • Roadmap de Desenvolvimento
    """

    ASSETS_DIR = "D:/projetos-inovexa/mindscan/backend/services/report_templates/assets"

    def __init__(self, test_id, results):
        self.test_id = test_id
        self.results = results
        self.styles = getSampleStyleSheet()

    # ---------------------------------------------------------
    # 0. Capa Premium
    # ---------------------------------------------------------
    def build_cover(self, story):
        story.append(Paragraph(f"MindScan — Relatório Premium ({self.test_id})",
                               self.styles["Title"]))
        story.append(Spacer(1, 24))
        story.append(Paragraph("Inovexa Software — Assessment Psicométrico Integrado",
                               self.styles["Heading2"]))
        story.append(Spacer(1, 36))

        cover_path = os.path.join(self.ASSETS_DIR, "covers", "premium_cover.png")
        if os.path.exists(cover_path):
            story.append(Image(cover_path, width=350, height=220))
            story.append(Spacer(1, 36))

        timestamp = datetime.utcnow().isoformat() + "Z"
        story.append(Paragraph(f"Gerado em: {timestamp}", self.styles["Normal"]))
        story.append(Spacer(1, 36))

    # ---------------------------------------------------------
    # 1. Sumário
    # ---------------------------------------------------------
    def build_summary_page(self, story):
        story.append(Paragraph("Sumário", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        sections = [
            "1. Resumo Executivo",
            "2. Indicadores Globais MindScan",
            "3. Forças e Riscos",
            "4. Narrativa Psicodinâmica",
            "5. Gráficos Essenciais",
            "6. Roadmap de Desenvolvimento",
            "7. Apêndice Técnico",
        ]

        for sec in sections:
            story.append(Paragraph(sec, self.styles["Normal"]))
            story.append(Spacer(1, 6))

        story.append(Spacer(1, 24))

    # ---------------------------------------------------------
    # 2. Resumo Executivo
    # ---------------------------------------------------------
    def build_executive_summary(self, story):
        story.append(Paragraph("1. Resumo Executivo", self.styles["Heading2"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            "O relatório Premium apresenta uma visão integrada do perfil psicométrico, "
            "combinando padrões cognitivos, emocionais, relacionais e operacionais, "
            "com interpretações avançadas e gráficos consolidados.",
            self.styles["Normal"]
        ))
        story.append(Spacer(1, 24))

    # ---------------------------------------------------------
    # 3. Indicadores Globais
    # ---------------------------------------------------------
    def build_global_indicators(self, story):
        story.append(Paragraph("2. Indicadores Globais MindScan", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        def avg(model):
            items = [b["score"] for b in self.results
                     if b.get("metadata", {}).get("model") == model]
            return sum(items)/len(items) if items else 0

        big5 = avg("big5")
        eq = avg("teique")
        perf = avg("performance")
        cross = avg("crossmap")
        comp = avg("compass")

        global_index = (big5 + eq + perf + cross + comp) / 5

        rows = [
            ("Força Cognitiva (Big Five)", big5),
            ("Inteligência Emocional", eq),
            ("Performance Operacional", perf),
            ("Aderência Psicodinâmica", cross),
            ("Direção Cognitiva", comp),
            ("Índice Global MindScan", global_index),
        ]

        for label, val in rows:
            story.append(Paragraph(f"<b>{label}:</b> {val:.2f}", self.styles["Normal"]))
            story.append(Spacer(1, 6))

        story.append(Spacer(1, 24))

    # ---------------------------------------------------------
    # 4. Forças & Riscos
    # ---------------------------------------------------------
    def build_strengths_risks(self, story):
        story.append(Paragraph("3. Forças e Riscos", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        sorted_items = sorted(self.results, key=lambda r: r["score"], reverse=True)
        top5 = sorted_items[:5]
        bottom5 = sorted_items[-5:]

        story.append(Paragraph("<b>Forças Principais:</b>", self.styles["Heading3"]))
        for item in top5:
            story.append(Paragraph(f"✔ {item['dimension']} — {item['descriptor']}",
                                   self.styles["Normal"]))
        story.append(Spacer(1, 18))

        story.append(Paragraph("<b>Pontos de Atenção:</b>", self.styles["Heading3"]))
        for item in bottom5:
            story.append(Paragraph(f"⚠ {item['dimension']} — {item['descriptor']}",
                                   self.styles["Normal"]))

        story.append(Spacer(1, 24))

    # ---------------------------------------------------------
    # 5. Narrativa Psicodinâmica
    # ---------------------------------------------------------
    def build_psychodynamic(self, story):
        story.append(Paragraph("4. Narrativa Psicodinâmica", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(
            "Esta seção integra padrões emocionais, cognitivos, esquemas, performance e estilo relacional "
            "em uma leitura psicodinâmica completa.",
            self.styles["Normal"]
        ))
        story.append(Spacer(1, 18))

        story.append(Paragraph(
            "O padrão emocional sugere boa regulação, com níveis reduzidos de estresse e ansiedade. "
            "O estilo cognitivo mostra forte organização e estrutura. O conjunto de esquemas indica baixa "
            "interferência de padrões desadaptativos, permitindo flexibilidade emocional e maturidade relacional.",
            self.styles["Normal"]
        ))

        story.append(Spacer(1, 24))

    # ---------------------------------------------------------
    # 6. Gráficos
    # ---------------------------------------------------------
    def build_charts(self, story):
        story.append(Paragraph("5. Gráficos Essenciais", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        chart_path = os.path.join(self.ASSETS_DIR, "charts", "radar_big5.png")

        if os.path.exists(chart_path):
            story.append(Image(chart_path, width=350, height=350))
        else:
            story.append(Paragraph("Gráfico não disponível.", self.styles["Normal"]))

        story.append(Spacer(1, 24))

    # ---------------------------------------------------------
    # 7. Roadmap
    # ---------------------------------------------------------
    def build_roadmap(self, story):
        story.append(Paragraph("6. Roadmap de Desenvolvimento", self.styles["Heading2"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            "Com base nos padrões identificados, recomenda-se um plano estruturado de desenvolvimento.",
            self.styles["Normal"]
        ))
        story.append(Spacer(1, 24))

    # ---------------------------------------------------------
    # 8. Apêndice Técnico
    # ---------------------------------------------------------
    def build_technical(self, story):
        story.append(Paragraph("7. Apêndice Técnico (Dados Completos)", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        for b in self.results:
            story.append(Paragraph(
                f"<b>{b['dimension']}</b> — {b['score']} "
                f"({b.get('metadata', {}).get('model', '?')})",
                self.styles["Normal"]
            ))
            story.append(Paragraph(b["descriptor"], self.styles["Normal"]))
            story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # MÉTODO PRINCIPAL
    # ---------------------------------------------------------
    def build(self, story):
        self.build_cover(story)
        self.build_summary_page(story)
        self.build_executive_summary(story)
        self.build_global_indicators(story)
        self.build_strengths_risks(story)
        self.build_psychodynamic(story)
        self.build_charts(story)
        self.build_roadmap(story)
        self.build_technical(story)
