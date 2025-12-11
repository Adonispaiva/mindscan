# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\storage\pdf_publisher.py
# Última atualização: 2025-12-11T09:59:21.292589

# Caminho: D:\projetos-inovexa\mindscan\backend\storage\pdf_publisher.py
"""
Publicador de PDF MindScan® — Armazenamento em S3 / Cloudflare R2 / MinIO
Inovexa Software | SynMind

Objetivo:
- Fazer upload do PDF gerado para um storage externo
- Retornar uma URL pública segura para envio via WhatsApp

Compatível com:
- Amazon S3
- Cloudflare R2
- MinIO

Depende de credenciais setadas via variáveis de ambiente:
- STORAGE_PROVIDER → "s3" | "r2" | "minio"
- STORAGE_ACCESS_KEY
- STORAGE_SECRET_KEY
- STORAGE_BUCKET
- STORAGE_ENDPOINT (para R2 e MinIO)
"""

import os
import logging
import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger("pdf_publisher")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Carregamento de variáveis de ambiente
# ---------------------------------------------------------
PROVIDER = os.getenv("STORAGE_PROVIDER", "s3")  # s3 | r2 | minio
ACCESS_KEY = os.getenv("STORAGE_ACCESS_KEY", "")
SECRET_KEY = os.getenv("STORAGE_SECRET_KEY", "")
BUCKET = os.getenv("STORAGE_BUCKET", "mindscan-reports")
ENDPOINT = os.getenv("STORAGE_ENDPOINT", "")  # R2 e MinIO usam endpoint custom

# ---------------------------------------------------------
# Cliente único para todos os provedores
# ---------------------------------------------------------
def _get_client():
    if PROVIDER == "s3":
        logger.info("[Storage] Usando Amazon S3")
        return boto3.client(
            "s3",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )

    if PROVIDER == "r2":
        logger.info("[Storage] Usando Cloudflare R2")
        return boto3.client(
            "s3",
            endpoint_url=ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            config=Config(signature_version="s3v4")
        )

    if PROVIDER == "minio":
        logger.info("[Storage] Usando MinIO")
        return boto3.client(
            "s3",
            endpoint_url=ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            config=Config(signature_version="s3v4")
        )

    raise ValueError(f"Provedor de storage inválido: {PROVIDER}")


# ---------------------------------------------------------
# Publicador de PDF
# ---------------------------------------------------------
def publish_pdf(pdf_path: str, object_name: str = None) -> str:
    """
    Publica um PDF e retorna uma URL pública.

    Parâmetros:
    - pdf_path: caminho local do PDF
    - object_name: nome do arquivo no bucket

    Retorna:
    - URL pública do PDF
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

    if object_name is None:
        object_name = os.path.basename(pdf_path)

    logger.info(f"[Storage] Publicando PDF: {object_name}")

    client = _get_client()

    try:
        # Upload do PDF
        client.upload_file(pdf_path, BUCKET, object_name, ExtraArgs={"ContentType": "application/pdf"})

        # Geração de URL pública
        if PROVIDER in ("s3", "minio", "r2"):
            url = f"{ENDPOINT}/{BUCKET}/{object_name}" if ENDPOINT else f"https://{BUCKET}.s3.amazonaws.com/{object_name}"
        else:
            raise ValueError("Provedor inválido para geração de URL pública.")

        logger.info(f"[Storage] PDF publicado com sucesso: {url}")
        return url

    except (BotoCoreError, ClientError) as e:
        logger.error(f"[Storage] Erro ao publicar PDF: {e}")
        raise
