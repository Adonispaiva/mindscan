# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pysettings.py
# Última atualização: 2025-12-11T09:59:20.558303

# Caminho: backend/pysettings.py
"""
Settings – Núcleo de Configuração do MindScan®
Inovexa Software | SynMind

Responsável por:
- Gerenciar variáveis de ambiente
- Carregar chaves do sistema
- Definir parâmetros globais
- Configurar modos de execução
- Fornecer acesso seguro ao backend
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe principal de configuração do MindScan.
    Todas as partes do sistema dependem dela.
    """

    # ---------------------------------------------------------
    # MODO DE EXECUÇÃO
    # ---------------------------------------------------------
    MODE: str = os.getenv("MINDSCAN_MODE", "development")
    API_ENABLED: bool = os.getenv("API_ENABLED", "true").lower() == "true"
    WORKER_ENABLED: bool = os.getenv("WORKER_ENABLED", "false").lower() == "true"

    # ---------------------------------------------------------
    # API SETTINGS
    # ---------------------------------------------------------
    API_HOST: str = os.getenv("MINDSCAN_API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("MINDSCAN_API_PORT", 8000))

    # ---------------------------------------------------------
    # DATABASE
    # ---------------------------------------------------------
    DATABASE_URL: str = os.getenv("MINDSCAN_DATABASE_URL", "sqlite:///mindscan.db")

    # ---------------------------------------------------------
    # FILESYSTEM / PATHS
    # ---------------------------------------------------------
    PROJECT_ROOT: str = os.getenv("PROJECT_ROOT", os.getcwd())
    STORAGE_DIR: str = os.path.join(PROJECT_ROOT, "storage")
    PDF_OUTPUT_DIR: str = os.path.join(STORAGE_DIR, "pdf_output")

    # ---------------------------------------------------------
    # WHATSAPP (Twilio)
    # ---------------------------------------------------------
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")

    # ---------------------------------------------------------
    # PDF PUBLISHER
    # ---------------------------------------------------------
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "s3")  # s3 | r2 | minio
    STORAGE_ACCESS_KEY: str = os.getenv("STORAGE_ACCESS_KEY", "")
    STORAGE_SECRET_KEY: str = os.getenv("STORAGE_SECRET_KEY", "")
    STORAGE_BUCKET: str = os.getenv("STORAGE_BUCKET", "mindscan-reports")
    STORAGE_ENDPOINT: str = os.getenv("STORAGE_ENDPOINT", "")

    # ---------------------------------------------------------
    # PIPELINE PROCESSING
    # ---------------------------------------------------------
    WORKER_INTERVAL: int = int(os.getenv("MINDSCAN_WORKER_INTERVAL", 2))

    # ---------------------------------------------------------
    # MI – Mente Interna
    # ---------------------------------------------------------
    MI_MODEL: str = os.getenv("MI_MODEL", "gpt-4o-mini")
    MI_SYSTEM_PROMPT: str = os.getenv(
        "MI_SYSTEM_PROMPT",
        "Você é o módulo de suporte automático do MindScan. Seu objetivo é ajudar o usuário a preencher o questionário."
    )

    # ---------------------------------------------------------
    # SELF-HEALING / RESILIÊNCIA
    # ---------------------------------------------------------
    SELF_HEALING_ENABLED: bool = os.getenv("SELF_HEALING_ENABLED", "true").lower() == "true"

    # ---------------------------------------------------------
    # Pydantic config
    # ---------------------------------------------------------
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# ---------------------------------------------------------
# Função global de acesso ao Settings (singleton)
# ---------------------------------------------------------
@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Instância única exposta ao backend
settings = get_settings()
