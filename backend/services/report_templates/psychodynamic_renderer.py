# Caminho: D:\backend\services\report_templates\psychodynamic_renderer.py
# MindScan — Psychodynamic Renderer v2.0
# Diretor Técnico: Leo Vinci — Inovexa Software
# Relatório Psicodinâmico: Narrativa Emocional + Cognitiva + Schemas + Estilo Decisório

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

class PsychodynamicRenderer:
    def __init__(self, test_id, results):
        self.test_id = test_id
        self.results = results
        self.styles = getSampleStyleSheet()

    # Utilidades internas ------------------------------------------------------

    def _get_by_model(self, model):
        return [r for r in self.results if r.get("metadata", {}).get("model") == model]

    def _avg(self, items):
        return sum(items)/len(items) if items else 0

    # Blocos narrativos --------------------------------------------------------

    def build_intro(self, story):
        story.append(Paragraph(f"MindScan — Relatório Psicodinâmico ({self.test_id})", self.styles["Title"]))
        story.append(Spacer(1, 18))
        story.append(Paragraph(
            "Este relatório apresenta uma leitura psicodinâmica integrada, combinando personalidade, esquemas, \n"
            "inteligência emocional, estilo cognitivo e padrões de performance. A narrativa abaixo descreve não apenas \n"
            "os resultados, mas como eles se organizam emocionalmente, racionalmente e comportamentalmente.",
            self.styles["Normal"]
        ))
        story.append(Spacer(1, 18))

    def build_emotional_profile(self, story):
        story.append(Paragraph("1. Estrutura Emocional (TEIQue + DASS21)", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        tei = self._get_by_model("teique")
        dass = self._get_by_model("dass21")

        eq_avg = self._avg([t["score"] for t in tei])
        stress = next((d for d in dass if d["dimension"] == "estresse"), {}).get("score", 0)
        anxiety = next((d for d in dass if d["dimension"] == "ansiedade"), {}).get("score", 0)

        narrative = ""
        if eq_avg >= 70:
            narrative += "O indivíduo apresenta uma estrutura emocional madura, com bom nível de regulação e estabilidade. "
        else:
            narrative += "Há indícios de oscilação emocional, sugerindo capacidade moderada de regulação. "

        if stress <= 30:
            narrative += "Níveis de estresse são baixos, indicando boa tolerância a pressões. "
        else:
            narrative += "Sinais de carga emocional significativa exigem atenção ao manejo de pressões. "

        if anxiety <= 25:
            narrative += "A ansiedade é controlada, contribuindo para clareza emocional."
        else:
            narrative += "A ansiedade elevada pode impactar a tomada de decisão."

        story.append(Paragraph(narrative, self.styles["Normal"]))
        story.append(Spacer(1, 18))

    def build_cognitive_profile(self, story):
        story.append(Paragraph("2. Estrutura Cognitiva (Big Five + Compass)", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        big5 = self._get_by_model("big5")
        compass = self._get_by_model("compass")

        openness = next((b for b in big5 if b["dimension"] == "O"), {}).get("score", 0)
        conscientious = next((b for b in big5 if b["dimension"] == "C"), {}).get("score", 0)
        racional = next((c for c in compass if c["dimension"] == "eixo_racional"), {}).get("score", 0)

        narrative = ""
        if openness >= 70:
            narrative += "Há forte abertura cognitiva, facilitando criatividade, exploração e flexibilidade mental. "
        else:
            narrative += "A abertura cognitiva é moderada, priorizando estabilidade e familiaridade. "

        if conscientious >= 80:
            narrative += "A organização mental é elevada, sustentando capacidade analítica e execução consistente. "
        else:
            narrative += "A organização é funcional, porém com espaço para maior sistematização. "

        if racional >= 70:
            narrative += "A tomada de decisão tende a ser racional, estruturada e orientada por análise."
        else:
            narrative += "A decisão tende a ser influenciada por elementos emocionais ou contextuais."

        story.append(Paragraph(narrative, self.styles["Normal"]))
        story.append(Spacer(1, 18))

    def build_schemas_profile(self, story):
        story.append(Paragraph("3. Schemas e Padrões Profundos (EMS)", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        ems = self._get_by_model("esquemas")
        high_ems = [e for e in ems if e["score"] >= 70]

        if not high_ems:
            story.append(Paragraph(
                "Os esquemas desadaptativos aparecem em níveis baixos ou moderados, sugerindo boa integração emocional interna.",
                self.styles["Normal"]
            ))
        else:
            story.append(Paragraph(
                "Foram identificados esquemas predominantes que influenciam padrões emocionais e relacionais:",
                self.styles["Normal"]
            ))
            story.append(Spacer(1, 12))
            for e in high_ems:
                story.append(Paragraph(f"• <b>{e['dimension']}</b>: {e['descriptor']}", self.styles["Normal"]))

        story.append(Spacer(1, 18))

    def build_operational_profile(self, story):
        story.append(Paragraph("4. Estilo Operacional e Produtivo (Performance)", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        perf = self._get_by_model("performance")
        avg_perf = self._avg([p["score"] for p in perf])

        if avg_perf >= 80:
            narrative = "O perfil operacional é altamente eficiente, consistente e orientado a resultados, com forte autonomia e confiabilidade."
        elif avg_perf >= 60:
            narrative = "O desempenho é sólido, com boa capacidade de entrega e estabilidade."
        else:
            narrative = "Há sinais de variabilidade operacional, sugerindo necessidade de suporte estruturado."

        story.append(Paragraph(narrative, self.styles["Normal"]))
        story.append(Spacer(1, 18))

    def build_crossmap(self, story):
        story.append(Paragraph("5. Integração Psicodinâmica (Crossmap)", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        crossmap = self._get_by_model("crossmap")
        cm_avg = self._avg([c["score"] for c in crossmap])

        if cm_avg >= 70:
            narrative = "Há alta convergência entre personalidade, emoção, esquemas e performance, indicando estabilidade psicodinâmica."
        else:
            narrative = "A integração psicodinâmica mostra áreas de desalinhamento que podem influenciar comportamento sob pressão."

        story.append(Paragraph(narrative, self.styles["Normal"]))
        story.append(Spacer(1, 18))

    # Método principal ----------------------------------------------------------

    def build(self, story):
        timestamp = datetime.utcnow().isoformat() + "Z"
        story.append(Paragraph(f"Gerado em: {timestamp}", self.styles["Normal"]))
        story.append(Spacer(1, 12))

        self.build_intro(story)
        self.build_emotional_profile(story)
        self.build_cognitive_profile(story)
        self.build_schemas_profile(story)
        self.build_operational_profile(story)
        self.build_crossmap(story)

        story.append(Paragraph("Fim do Relatório Psicodinâmico", self.styles["Heading3"]))