# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\reports\html_exporter.py
# Última atualização: 2025-12-11T09:59:21.073776

# ============================================================
# MindScan — HTML Exporter
# ============================================================
# Gera uma versão HTML do relatório MindScan, estruturada,
# responsiva e pronta para exibição em interfaces e APIs.
#
# Versão completa, padronizada e pronta para front-end.
# ============================================================

from typing import Dict, Any
import datetime


class HTMLExporter:
    """
    Exporta o relatório MindScan para HTML completo.
    """

    # ------------------------------------------------------------
    # TEMPLATE PRINCIPAL
    # ------------------------------------------------------------
    def build_html(self, subject_name: str, mi_package: Dict[str, Any], report_text: str) -> str:
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório MindScan — {subject_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #222;
        }}
        h1, h2, h3 {{
            color: #0a3d62;
        }}
        .section {{
            margin-bottom: 35px;
        }}
        .divider {{
            border-bottom: 1px solid #999;
            margin: 20px 0;
        }}
        .meta {{
            color: #555;
            font-size: 14px;
        }}
        .block {{
            margin-bottom: 20px;
        }}
        .risk-high {{
            color: #c0392b;
            font-weight: bold;
        }}
        .risk-medium {{
            color: #e67e22;
            font-weight: bold;
        }}
        .risk-low {{
            color: #27ae60;
            font-weight: bold;
        }}
    </style>
</head>

<body>
    <h1>Relatório MindScan</h1>
    <p class="meta">Sujeito: {subject_name}<br>
    Gerado em: {timestamp}</p>

    <div class="divider"></div>

    <div class="section">
        <h2>Quadrante Final</h2>
        <p><b>Quadrante:</b> {mi_package["quadrant"]}</p>
        <p><b>Coordenadas:</b> X={mi_package["coordinates"]["x"]} | Y={mi_package["coordinates"]["y"]}</p>
        <p><b>Estilo:</b> {mi_package["style"]}</p>
        <p><b>Nível de risco:</b> {mi_package["risk_level"]}</p>
    </div>

    <div class="divider"></div>

    <div class="section">
        <h2>Conteúdo do Relatório</h2>
        {"".join(f"<p>{line}</p>" for line in report_text.split("\\n") if line.strip())}
    </div>

</body>
</html>
"""
        return html

    # ------------------------------------------------------------
    # SALVAR EM ARQUIVO HTML
    # ------------------------------------------------------------
    def save_html(self, output_path: str, html_content: str):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return output_path


# Instância pública
html_exporter = HTMLExporter()
