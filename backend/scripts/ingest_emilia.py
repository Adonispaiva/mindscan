import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import logging

# Configuração de Identidade Orion
DATABASE_URL = "postgresql://postgres:suasenha@localhost:5432/mindscan"

def clean_likert(value):
    """Converte '4. Concordo' em 4, '0. Não se aplicou' em 0, etc."""
    try:
        return int(str(value).split('.')[0])
    except:
        return 0

def run_ingestion(csv_path):
    print(f"🚀 Iniciando ingestão do arquivo: {csv_path}")
    
    # Lendo o CSV da Emília (ajustado para o formato que você enviou)
    df = pd.read_csv(csv_path)
    
    # Exemplo de mapeamento para o motor de cálculo
    processed_data = {
        "name": "Maria Emília Costa Ramos",
        "email": "emilia@exemplo.com",
        "responses": {
            "big5": {
                "openness": clean_likert(df.iloc[0]['12. Tenho ideias originais...']),
                # ... mapear as demais colunas conforme a árvore de dados
            },
            "dass21": {
                "depression_items": [clean_likert(x) for x in df.iloc[0][['Questão_D1', 'Questão_D2']].values],
                "anxiety_items": [clean_likert(x) for x in df.iloc[0][['Questão_A1', 'Questão_A2']].values],
                "stress_items": [clean_likert(x) for x in df.iloc[0][['Questão_S1', 'Questão_S2']].values],
            }
        },
        "performance_score": 85 # Valor exemplo para a Bússola
    }
    
    print("✅ Dados normalizados. Pronto para o MindScanEngine.")
    return processed_data

if __name__ == "__main__":
    # Teste de carga
    data = run_ingestion("D:/mindscan/data/MINDSCAN_EMILIA.csv")