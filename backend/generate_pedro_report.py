import os
import sys
import logging

# Garante que o Python encontre os módulos do backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.algorithms.mindscan_engine import MindScanEngine
from backend.services.report_service import ReportService

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MindScan.Test")

def executar_fluxo_pedro():
    # 1. Dados do Pedro (Simulando extração do CSV principal)
    # Estes índices correspondem às respostas do Pedro no formulário oficial
    dados_brutos_pedro = {
        "name": "Pedro Borges Duarte",
        "big5_responses": [5, 4, 3, 5, 6, 2, 4, 3, 2, 1, 2, 5, 4, 6, 5, 4, 3, 5, 6, 2],
        "dass21_responses": [1, 0, 2, 1, 0, 1, 2, 3, 1, 0, 2, 1, 0, 1, 2, 1, 0, 2, 1, 0, 1],
        "performance_raw": 87.0
    }

    logger.info("🧠 Calculando métricas via MindScanEngine...")
    engine = MindScanEngine()
    
    # Prepara dados para a Engine
    payload = {
        "user_id": "PEDRO_001",
        "big5_responses": dados_brutos_pedro["big5_responses"],
        "dass21_responses": dados_brutos_pedro["dass21_responses"],
        "performance_raw": dados_brutos_pedro["performance_raw"],
        "timestamp": "20/12/2025"
    }
    
    resultados = engine.process_full_diagnostic(payload)

    logger.info("🎨 Gerando PDF Profissional via ReportService...")
    service = ReportService(output_dir="backend/generated_reports")
    
    path_final = service.generate_report(
        candidate_data={"name": dados_brutos_pedro["name"]},
        results=resultados,
        report_type="technical"
    )

    print(f"\n✅ SUCESSO! O relatório foi gerado em:\n{os.path.abspath(path_final)}")

if __name__ == "__main__":
    executar_fluxo_pedro()