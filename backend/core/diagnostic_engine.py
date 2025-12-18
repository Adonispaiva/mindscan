"""
MindScan — Diagnostic Engine (EntryPoint Soberano)
Versão: Final
Autor: Leo Vinci — Inovexa Software
Data: 2025-12-15

Este arquivo é o ÚNICO ponto de entrada válido para execução
completa de um diagnóstico MindScan.

Qualquer execução fora deste fluxo é inválida.
"""

from typing import Dict, Any
from datetime import datetime
import uuid

# =========================
# IMPORTS — CORE
# =========================
from backend.core.normalizer import normalize_payload
from backend.core.scoring import calculate_scores

# =========================
# IMPORTS — ALGORITHMS
# =========================
from backend.algorithms.big5.big5 import run_big5
from backend.algorithms.dass21.dass21 import run_dass21
from backend.algorithms.teique.teique import run_teique
from backend.algorithms.ocai.ocai import run_ocai
from backend.algorithms.esquemas.esquemas import run_esquemas
from backend.algorithms.performance.performance import run_performance
from backend.algorithms.cruzamentos.cruzamentos import run_cruzamentos
from backend.algorithms.bussola.bussola import run_bussola

# =========================
# IMPORTS — SERVICES
# =========================
from backend.services.mi_compiler_service import compile_narrative
from backend.services.report_service import build_html_report
from backend.services.pdf_service import generate_pdf_report
from backend.services.export_service import export_report_bundle


class DiagnosticEngine:
    """
    ENTRYPOINT SOBERANO DO MINDSCAN

    Responsável por:
    - validar entrada
    - normalizar dados
    - executar TODOS os algoritmos
    - realizar cruzamentos
    - compilar narrativa (MI)
    - gerar relatório HTML
    - gerar relatório PDF
    - retornar bundle final
    """

    @staticmethod
    def run_diagnostic(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa um diagnóstico MindScan completo, determinístico
        e auditável.

        Entrada:
            payload bruto com respostas psicométricas

        Saída:
            dicionário com resultados + paths de relatório
        """

        diagnostic_id = str(uuid.uuid4())
        started_at = datetime.utcnow().isoformat()

        # -------------------------------------------------
        # 1. NORMALIZAÇÃO
        # -------------------------------------------------
        normalized_data = normalize_payload(payload)

        # -------------------------------------------------
        # 2. SCORING BASE
        # -------------------------------------------------
        base_scores = calculate_scores(normalized_data)

        # -------------------------------------------------
        # 3. EXECUÇÃO DOS ALGORITMOS
        # -------------------------------------------------
        results = {}

        results["big5"] = run_big5(base_scores)
        results["dass21"] = run_dass21(base_scores)
        results["teique"] = run_teique(base_scores)
        results["ocai"] = run_ocai(base_scores)
        results["esquemas"] = run_esquemas(base_scores)
        results["performance"] = run_performance(base_scores)

        # -------------------------------------------------
        # 4. CRUZAMENTOS & BÚSSOLA
        # -------------------------------------------------
        results["cruzamentos"] = run_cruzamentos(results)
        results["bussola"] = run_bussola(results)

        # -------------------------------------------------
        # 5. NARRATIVA (MI)
        # -------------------------------------------------
        narrative = compile_narrative(results)

        # -------------------------------------------------
        # 6. RELATÓRIO HTML
        # -------------------------------------------------
        html_report_path = build_html_report(
            diagnostic_id=diagnostic_id,
            results=results,
            narrative=narrative
        )

        # -------------------------------------------------
        # 7. RELATÓRIO PDF
        # -------------------------------------------------
        pdf_report_path = generate_pdf_report(
            diagnostic_id=diagnostic_id,
            html_path=html_report_path
        )

        # -------------------------------------------------
        # 8. EXPORTAÇÃO FINAL
        # -------------------------------------------------
        bundle = export_report_bundle(
            diagnostic_id=diagnostic_id,
            html_path=html_report_path,
            pdf_path=pdf_report_path
        )

        finished_at = datetime.utcnow().isoformat()

        # -------------------------------------------------
        # 9. RETORNO FINAL
        # -------------------------------------------------
        return {
            "diagnostic_id": diagnostic_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "results": results,
            "narrative": narrative,
            "reports": {
                "html": html_report_path,
                "pdf": pdf_report_path,
                "bundle": bundle
            }
        }
