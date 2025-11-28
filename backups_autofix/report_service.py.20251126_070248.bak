# Caminho completo do arquivo:
# D:\projetos-inovexa\mindscan_rebuild\backend\services\report_service.py

import os
from datetime import datetime
from typing import Dict, Any

class ReportService:
    """
    Serviço responsável pela geração de relatórios PDF finais do MindScan.
    A versão 2.0 é preparada para integração com motores de PDF externos
    e exportações profissionais.
    """

    BASE_OUTPUT_DIR = "D:/projetos-inovexa/mindscan_rebuild/output/reports"  # Ajustável

    @staticmethod
    def _ensure_output_dir() -> None:
        if not os.path.exists(ReportService.BASE_OUTPUT_DIR):
            os.makedirs(ReportService.BASE_OUTPUT_DIR, exist_ok=True)

    @staticmethod
    def generate_pdf(user: Dict[str, Any], diagnostic_data: Dict[str, Any]) -> str:
        """
        Gera um relatório PDF. Implementação simplificada (stub) até a
        integração com o pipeline final de geração.
        """

        ReportService._ensure_output_dir()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = user.get("name", "usuario")

        filename = f"diagnostic_{username}_{timestamp}.pdf"
        filepath = os.path.join(ReportService.BASE_OUTPUT_DIR, filename)

        # --------------------------------------------------------
        # FUTURO: substituir stub por PDF real gerado pelo engine
        # --------------------------------------------------------
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("MIND_SCAN_REPORT_PDF_VERSION_2.0\n\n")
            f.write(str(diagnostic_data))

        return filepath
