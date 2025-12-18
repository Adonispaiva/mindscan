from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

REPORTS_DIR = "generated_reports"

def generate_report(results: dict) -> str:
    """
    Gera o relatório final em PDF a partir dos resultados do MindScan.
    Retorna o caminho do arquivo gerado.
    """

    os.makedirs(REPORTS_DIR, exist_ok=True)

    filename = f"mindscan_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(REPORTS_DIR, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica", 10)

    c.drawString(50, y, "MindScan — Relatório de Diagnóstico")
    y -= 30

    for key, value in results.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return file_path
