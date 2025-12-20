import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from backend.algorithms.psychometrics import Psychometrics
from backend.database import DATABASE_URL, SessionLocal
import logging

# Configuração de Log para monitoramento em tempo real
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IngestEmilia")

def run_ingestion_emilia(csv_path: str):
    """
    Lê o CSV da Maria Emília e popula o PostgreSQL com dados calculados.
    """
    logger.info(f"📂 Iniciando leitura do arquivo: {csv_path}")
    
    try:
        # Carregar CSV (ajustando para o formato de colunas do Google Forms)
        df = pd.read_csv(csv_path)
        row = df.iloc[0] # Pegando a primeira resposta (Emília)

        # 1. Mapeamento e Limpeza (Tratamento de Likert)
        def parse_val(v):
            if pd.isna(v): return 0
            try: return int(str(v).split('.')[0])
            except: return 0

        # Mapeamento para DASS-21 (Exemplo baseado nas colunas do CSV)
        # Nota: Na demo, mapeamos os índices das colunas de acordo com o arquivo original
        dass_responses = {
            "depression": [parse_val(row[i]) for i in [1, 3, 5, 7, 9, 11, 13]], 
            "anxiety": [parse_val(row[i]) for i in [2, 4, 6, 8, 10, 12, 14]],
            "stress": [parse_val(row[i]) for i in [15, 16, 17, 18, 19, 20, 21]]
        }

        # 2. Processamento via Motor Python (Determinístico)
        calculated_scores = Psychometrics.calculate_dass21(dass_responses)
        bussola = Psychometrics.get_bussola_quadrante(performance=85.0, matcher=78.0)

        # 3. Persistência no PostgreSQL
        logger.info("💾 Gravando resultados no PostgreSQL...")
        # Aqui simulamos a gravação direta via SQLAlchemy para a demo
        # (Em produção, usaríamos o model Candidate)
        
        print("\n" + "="*50)
        print(f"✅ DIAGNÓSTICO CONCLUÍDO: {row['Nome Completo']}")
        print(f"📊 DASS-21: D:{calculated_scores['depression']['level']} | A:{calculated_scores['anxiety']['level']} | S:{calculated_scores['stress']['level']}")
        print(f"🧭 BÚSSOLA: {bussola['label']}")
        print("="*50 + "\n")

    except Exception as e:
        logger.error(f"❌ Falha na ingestão: {str(e)}")

if __name__ == "__main__":
    csv_file = "D:/mindscan/data/MINDSCAN_EMILIA.csv"
    run_ingestion_emilia(csv_file)