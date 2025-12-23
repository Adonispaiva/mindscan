import os
from dotenv import load_dotenv
from typing import Dict, Any

# Carrega as variáveis do arquivo .env (onde está o seu DB_PASS)
load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "mindscan_db")

    # URL de Conexão Oficial para PostgreSQL 18.1
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def build_dataset_from_answers(answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constrói o dataset unificado para o MindScanEngine.
    As respostas chegam do formulário (1-6) e são encapsuladas para os algoritmos.
    """
    if not isinstance(answers, dict):
        raise ValueError("Answers inválidas. Deve ser um dicionário.")

    return {
        "raw_answers": answers,
        "metadata": {
            "version": "4.0",
            "scale": "Likert 1-6"
        }
    }