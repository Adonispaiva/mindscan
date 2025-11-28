# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\mindscan_pipeline.py
"""
Pipeline Principal do MindScan® com Integração do Hook WhatsApp
Inovexa Software | SynMind | MindScan®

Funções incluídas:
- Execução do pipeline psicométrico (simulação — núcleo real permanece em outro módulo)
- Geração do relatório PDF (referência — responsabilidade externa)
- Chamada automática do hook WhatsApp após geração

IMPORTANTE:
Este arquivo apenas integra o hook WhatsApp. Ele NÃO altera:
- lógica psicométrica
- cruzamentos
- narrativas
- arquivos originais do MindScan
"""

import logging
from backend.reports.pdf_generator import generate_mindscan_pdf
from backend.storage.pdf_publisher import publish_pdf
from backend.pipelines.whatsapp_notification import mindscan_postprocess_hook

logger = logging.getLogger("mindscan_pipeline")
logger.setLevel(logging.INFO)


def run_mindscan_pipeline(user_id: str, phone: str, data: dict = None) -> dict:
    """
    Função executora do pipeline MindScan.
    """
    logger.info(f"[MindScan] Iniciando pipeline para usuário {user_id}...")

    # 1. Processamento psicométrico (representação)
    logger.info("[MindScan] Processamento psicométrico concluído.")

    # 2. Geração / obtenção do PDF (placeholder atual)
    pdf_path = generate_mindscan_pdf(user_id, data or {})
    pdf_url = publish_pdf(pdf_path)
    logger.info(f"[MindScan] Relatório disponível em {pdf_url}")

    # 3. Chamada automática do hook WhatsApp
    logger.info("[MindScan] Disparando hook WhatsApp...")
    hook_response = mindscan_postprocess_hook(user_phone=phone, pdf_url=pdf_url)

    # 4. Finalização
    return {
        "status": "completed",
        "user": user_id,
        "pdf_url": pdf_url,
        "whatsapp": hook_response
    }
