# MindScan — PDF Service (FINAL)
# Responsável por converter HTML em PDF

from pathlib import Path
from weasyprint import HTML


def generate_pdf_report(diagnostic_id: str, html_path: str) -> str:
    """
    Converte um relatório HTML do MindScan em PDF.
    Retorna o caminho do PDF gerado.
    """

    html_file = Path(html_path)
    if not html_file.exists():
        raise FileNotFoundError(f"HTML não encontrado: {html_path}")

    pdf_path = html_file.with_suffix(".pdf")

    HTML(filename=str(html_file)).write_pdf(str(pdf_path))

    return str(pdf_path)
