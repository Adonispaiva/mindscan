# Caminho: D:\backend\services\report_templates\executive_renderer.py
# MindScan — Executive Renderer v2.0
# Diretor Técnico: Leo Vinci — Inovexa Software
# Relatório Executivo: Resumo + Indicadores Globais + Gráficos Essenciais + Bloco Técnico Resumido

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

class ExecutiveRenderer:
    def __init__(self, test_id, results):
        self.test_id = test_id
        self.results = results
        self.styles = getSampleStyleSheet()

    # ------------------------------------------------------------
    # 1. Resumo Executivo — Síntese de Alta Liderança
    # ------------------------------------------------------------
    def build_summary(self, story):
        story.append(Paragraph("Resumo Executivo", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(
            "Este relatório apresenta uma análise consolidada do perfil psicométrico, incluindo traços cognitivos, emocionais, culturais e operacionais.\n"
            "Os indicadores abaixo representam as forças predominantes, áreas de atenção e potenciais riscos comportamentais.",
            self.styles["Normal"])
        )
        story.append(Spacer(1, 18))

    # ------------------------------------------------------------
    # 2. Indicadores Globais MindScan — 6 Medidas Síntese
    # ------------------------------------------------------------
    def build_global_indicators(self, story):
        story.append(Paragraph("Indicadores Globais MindScan", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        # Cálculo base: médias aproximadas agrupadas por família
        # (Os valores reais são calculados pelo Engine; aqui reorganizamos conforme o template)

        # BIG FIVE
        bf_scores = [b["score"] for b in self.results if b.get("metadata", {}).get("model") == "big5"]
        big5_avg = sum(bf_scores)/len(bf_scores) if bf_scores else 0

        # TEIQue
        eq_scores = [b["score"] for b in self.results if b.get("metadata", {}).get("model") == "teique"]
        emotional_avg = sum(eq_scores)/len(eq_scores) if eq_scores else 0

        # Performance
        perf_scores = [b["score"] for b in self.results if b.get("metadata", {}).get("model") == "performance"]
        perf_avg = sum(perf_scores)/len(perf_scores) if perf_scores else 0

        # Crossmap
        cm_scores = [b["score"] for b in self.results if b.get("metadata", {}).get("model") == "crossmap"]
        crossmap_avg = sum(cm_scores)/len(cm_scores) if cm_scores else 0

        # Compass
        comp_scores = [b["score"] for b in self.results if b.get("metadata", {}).get("model") == "compass"]
        compass_avg = sum(comp_scores)/len(comp_scores) if comp_scores else 0

        indicators = [
            ("Força Cognitiva (Big Five)", big5_avg),
            ("Força Emocional (TEIQue)", emotional_avg),
            ("Performance Operacional", perf_avg),
            ("Aderência Psicodinâmica (Crossmap)", crossmap_avg),
            ("Direção Cognitiva (Compass)", compass_avg),
            ("Índice Global MindScan", (big5_avg+emotional_avg+perf_avg+crossmap_avg+compass_avg)/5)
        ]

        for name, score in indicators:
            story.append(Paragraph(f"<b>{name}:</b> {score:.2f}", self.styles["Normal"]))
            story.append(Spacer(1, 6))

        story.append(Spacer(1, 18))

    # ------------------------------------------------------------
    # 3. Forças & Riscos — Extração de Pontos Críticos
    # ------------------------------------------------------------
    def build_strengths_risks(self, story):
        story.append(Paragraph("Forças Predominantes", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        sorted_desc = sorted(self.results, key=lambda x: x["score"], reverse=True)
        top5 = sorted_desc[:5]

        for b in top5:
            story.append(Paragraph(f"✔ {b['dimension']} — {b['descriptor']}", self.styles["Normal"]))
        story.append(Spacer(1, 18))

        story.append(Paragraph("Pontos de Atenção", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        bottom5 = sorted_desc[-5:]
        for b in bottom5:
            story.append(Paragraph(f"⚠ {b['dimension']} — {b['descriptor']}", self.styles["Normal"]))
        story.append(Spacer(1, 18))

    # ------------------------------------------------------------
    # 4. Bloco Técnico Resumido (Dados)
    # ------------------------------------------------------------
    def build_technical_section(self, story):
        story.append(Paragraph("Apêndice Técnico (Resumo de Dados)", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        for block in self.results:
            dim = block.get("dimension", "N/A")
            score = block.get("score", 0)
            desc = block.get("descriptor", "")
            model = block.get("metadata", {}).get("model", "?")

            story.append(Paragraph(f"<b>{dim}</b> ({model})", self.styles["Heading3"]))
            story.append(Paragraph(f"Score: {score}", self.styles["Normal"]))
            story.append(Paragraph(f"Descrição: {desc}", self.styles["Normal"]))
            story.append(Spacer(1, 12))

    # ------------------------------------------------------------
    # 5. Método principal (orquestração)
    # ------------------------------------------------------------
    def build(self, story):
        # Cabeçalho
        story.append(Paragraph(f"MindScan — Relatório Executivo ({self.test_id})", self.styles["Title"]))
        story.append(Spacer(1, 18))

        timestamp = datetime.utcnow().isoformat() + "Z"
        story.append(Paragraph(f"Gerado em: {timestamp}", self.styles["Normal"]))
        story.append(Spacer(1, 12))

        # Seções
        self.build_summary(story)
        self.build_global_indicators(story)
        self.build_strengths_risks(story)
        self.build_technical_section(story)

        # Final