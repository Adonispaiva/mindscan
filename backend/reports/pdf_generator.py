# Caminho: D:\projetos-inovexa\mindscan\backend\reports\pdf_generator.py
"""
Gerador REAL de PDF do MindScan®
Inovexa Software | SynMind | MindScan®

Objetivo:
- Gerar PDF final do MindScan com narrativa, perfil, cruzamentos e layout oficial.
- Produzir arquivo físico .pdf para posterior publicação e envio via WhatsApp.

IMPORTANTE:
- Este módulo NÃO contém a lógica psicométrica.
- Ele recebe dados já calculados e apenas renderiza o PDF.
- Totalmente compatível com o pipeline e com a integração WhatsApp.

Tecnologia: ReportLab (renderização profissional)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
import logging
import os

logger = logging.getLogger("pdf_generator")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Função principal
# ---------------------------------------------------------
def generate_mindscan_pdf(user_id: str, data: dict, output_dir: str = "D:/projetos-inovexa/mindscan/output/") -> str:
    """
    Gera o PDF final do MindScan.

    Parâmetros:
    - user_id: ID do usuário avaliado
    - data: dict contendo a narrativa final, perfil, cruzamentos e elementos textuais
    - output_dir: diretório onde o PDF será salvo

    Retorna:
    - caminho completo do PDF gerado
    """

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pdf_path = os.path.join(output_dir, f"{user_id}.pdf")

        logger.info(f"[PDF] Gerando relatório MindScan para usuário {user_id}...")

        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # -------------------------------------------------------------
        # CAPA
        # -------------------------------------------------------------
        title = f"<para align='center'><b>Relatório MindScan®</b><br/><br/>Usuário: {user_id}</para>"
        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 2 * cm))

        # -------------------------------------------------------------
        # NARRATIVA PRINCIPAL
        # -------------------------------------------------------------
        narrative_text = data.get("narrativa", "Narrativa não fornecida.")
        story.append(Paragraph("<b>Narrativa Psicoprofissional</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(narrative_text.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 0.8 * cm))

        # -------------------------------------------------------------
        # PERFIL
        # -------------------------------------------------------------
        perfil = data.get("perfil", "Perfil não informado.")
        story.append(Paragraph("<b>Perfil Principal</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(perfil.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 0.8 * cm))

        # -------------------------------------------------------------
        # CRUZAMENTOS
        # -------------------------------------------------------------
        cruzamentos = data.get("cruzamentos", "Cruzamentos não informados.")
        story.append(Paragraph("<b>Cruzamentos</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(cruzamentos.replace("\n", "<br/>"), styles["BodyText"]))

        # -------------------------------------------------------------
        # FINALIZAÇÃO DO PDF
        # -------------------------------------------------------------
        doc.build(story)

        logger.info(f"[PDF] Relatório MindScan gerado com sucesso → {pdf_path}")
        return pdf_path

    except Exception as e:
        logger.error(f"[PDF] Erro ao gerar PDF: {e}")
        raise