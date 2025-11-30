# pdf_engine.py
# MindScan PDF Engine — núcleo responsável pela orquestração da geração de PDFs.

from pathlib import Path
import json
import datetime

ROOT = Path(__file__).resolve().parent

class PDFEngine:
    """
    Núcleo do motor de PDFs do MindScan.
    Responsável por:
    - carregar templates
    - montar contexto de dados
    - integrar seções
    - renderizar PDF
    - salvar artefato
    """

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or (ROOT / "output")
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def render(self, sections: list, context: dict, renderer):
        """
        Renderiza o PDF usando as seções e o mecanismo de renderização escolhido.
        """
        html_chunks = []
        for section in sections:
            html_chunks.append(section.render(context))

        final_html = "\n".join(html_chunks)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = self.output_dir / f"relatorio_mindscan_{timestamp}.pdf"

        renderer.render_html_to_pdf(final_html, pdf_path)
        return pdf_path

