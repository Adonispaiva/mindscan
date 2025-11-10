from pathlib import Path
from weasyprint import HTML
from datetime import datetime

# --------------------------------------------------
# 📄 Função: gerar PDF a partir do relatório MI
# --------------------------------------------------
def gerar_pdf_relatorio(markdown_text: str, nome: str = "Relatorio_MI") -> Path:
    """
    Gera um PDF estilizado a partir do texto do relatório em Markdown.
    Retorna o caminho completo do arquivo PDF gerado.
    """
    html_template = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 40px; line-height: 1.6; }}
            h1, h2, h3, h4 {{ color: #333; }}
            hr {{ border: none; border-top: 1px solid #ccc; margin: 20px 0; }}
        </style>
    </head>
    <body>
    <h2>🧠 Relatório Psicodiagnóstico MI</h2>
    <p><strong>Gerado em:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    <hr>
    <pre>{markdown_text}</pre>
    </body>
    </html>
    """

    output_dir = Path("./output/pdf")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{nome.replace(' ', '_')}_MI.pdf"

    HTML(string=html_template).write_pdf(output_path)
    return output_path
