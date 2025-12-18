# MindScan — Report Service (FINAL)
# Responsável por gerar HTML profissional do relatório MindScan + PDF robusto (reportlab)

from __future__ import annotations

from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from datetime import datetime

# PDF (sem dependências externas além do reportlab)
try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
except Exception:  # pragma: no cover
    LETTER = None
    inch = None
    getSampleStyleSheet = None
    SimpleDocTemplate = None
    Paragraph = None
    Spacer = None
    Table = None
    TableStyle = None


BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR.parent / "generated_reports"


def _ensure_reports_dir() -> Path:
    """Garante diretório de saída mesmo em ambientes com permissões restritas."""
    try:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        return REPORTS_DIR
    except Exception:
        fallback = BASE_DIR / "generated_reports"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


_EFFECTIVE_REPORTS_DIR = _ensure_reports_dir()


def build_html_report(
    diagnostic_id: str,
    results: Dict[str, Any],
    narrative: Dict[str, Any],
) -> str:
    """
    Gera relatório HTML final do MindScan.
    Retorna o caminho do arquivo HTML gerado.
    """
    created_at = datetime.utcnow().strftime("%d/%m/%Y %H:%M")

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>MindScan — Relatório Diagnóstico</title>
        <style>
            body {{
                font-family: Arial, Helvetica, sans-serif;
                margin: 40px;
                color: #222;
            }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .section {{ margin-bottom: 25px; }}
            .box {{
                border: 1px solid #ccc;
                padding: 15px;
                border-radius: 6px;
                background: #fafafa;
            }}
        </style>
    </head>
    <body>

        <h1>MindScan — Relatório Diagnóstico</h1>
        <p><strong>ID:</strong> {diagnostic_id}</p>
        <p><strong>Gerado em:</strong> {created_at}</p>

        <div class="section">
            <h2>Resumo Geral</h2>
            <div class="box">
                <p>{narrative.get("summary", "Resumo indisponível.")}</p>
            </div>
        </div>

        <div class="section">
            <h2>Principais Insights</h2>
            <div class="box">
                <ul>
                    {''.join(f"<li>{i}</li>" for i in narrative.get("insights", []))}
                </ul>
            </div>
        </div>

        <div class="section">
            <h2>Resultados Psicométricos</h2>
            <div class="box">
                <pre>{results}</pre>
            </div>
        </div>

        <div class="section">
            <h2>Conclusão</h2>
            <div class="box">
                <p>{narrative.get("conclusion", "Conclusão automática MindScan.")}</p>
            </div>
        </div>

    </body>
    </html>
    """

    output_path = _EFFECTIVE_REPORTS_DIR / f"mindscan_{diagnostic_id}.html"
    output_path.write_text(html, encoding="utf-8")
    return str(output_path)


def _normalize_results(results: Any) -> List[Dict[str, Any]]:
    """Aceita lista de ORM (MindscanResult) ou lista de dicts e normaliza."""
    normalized: List[Dict[str, Any]] = []
    if results is None:
        return normalized

    if isinstance(results, list):
        for item in results:
            if isinstance(item, dict):
                normalized.append(
                    {
                        "dimension": item.get("dimension"),
                        "score": item.get("score"),
                        "descriptor": item.get("descriptor"),
                        "metadata": item.get("metadata"),
                    }
                )
            else:
                normalized.append(
                    {
                        "dimension": getattr(item, "dimension", None),
                        "score": getattr(item, "score", None),
                        "descriptor": getattr(item, "descriptor", None),
                        "metadata": getattr(item, "metadata", None),
                    }
                )
        return normalized

    if isinstance(results, dict):
        normalized.append(results)
    return normalized


def build_pdf_report(
    diagnostic_id: str,
    results: Any,
    title: str = "MindScan — Relatório Executivo",
) -> str:
    """
    Gera um PDF simples e robusto (P0/P1/P2), preservando o HTML como artefato paralelo.
    Não depende de conversão HTML→PDF.

    Retorna o caminho do PDF gerado.
    """
    if SimpleDocTemplate is None:
        raise RuntimeError("reportlab não disponível para geração de PDF.")

    normalized = _normalize_results(results)
    output_path = _EFFECTIVE_REPORTS_DIR / f"mindscan_{diagnostic_id}.pdf"

    doc = SimpleDocTemplate(str(output_path), pagesize=LETTER, title=title)
    styles = getSampleStyleSheet()
    story: List[Any] = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Diagnóstico ID: {diagnostic_id}", styles["Normal"]))
    story.append(Paragraph(f"Gerado em (UTC): {datetime.utcnow().isoformat()}Z", styles["Normal"]))
    story.append(Spacer(1, 0.25 * inch))

    table_data: List[List[str]] = [["Dimensão", "Score", "Descriptor"]]
    for item in normalized:
        dim = str(item.get("dimension", "") or "")
        score = item.get("score")
        score_str = f"{float(score):.3f}" if score is not None else ""
        desc = str(item.get("descriptor", "") or "")
        table_data.append([dim, score_str, desc])

    tbl = Table(table_data, repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )

    story.append(tbl)
    doc.build(story)
    return str(output_path)


class ReportService:
    """
    Adapter canônico exigido pelo Diagnostic Router:

        pdf_path, metadata = ReportService.generate_pdf(test_id, results)

    - Preserva HTML profissional
    - Gera PDF robusto via reportlab
    """

    @staticmethod
    def generate_pdf(test_id: int, results: Any) -> Tuple[str, Dict[str, Any]]:
        diagnostic_id = str(test_id)

        try:
            html_path = build_html_report(
                diagnostic_id,
                {"results": _normalize_results(results)},
                narrative={},
            )
        except Exception:
            html_path = None

        pdf_path = build_pdf_report(diagnostic_id, results)

        metadata: Dict[str, Any] = {
            "report_type": "executive",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "html_path": html_path,
        }
        return pdf_path, metadata


__all__ = ["build_html_report", "build_pdf_report", "ReportService"]
