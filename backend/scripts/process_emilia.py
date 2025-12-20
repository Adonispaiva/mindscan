import sys
import os
import pandas as pd
from datetime import datetime

# Ajuste de path para o pacote backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Diagnostic
from backend.algorithms.psychometrics import Psychometrics

def ingest_emilia():
    csv_path = "D:/mindscan/backend/data/MINDSCAN_EMILIA.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Erro: Arquivo não encontrado em {csv_path}")
        return

    print(f"📂 Lendo dados de: {csv_path}")
    df = pd.read_csv(csv_path)
    row = df.iloc[0] # Maria Emília

    # Simulação de mapeamento de colunas (conforme o formulário dela)
    responses = {
        "dass21": {
            "depression": [3, 2, 3, 1, 2, 3, 3], # Valores exemplo baseados no CSV
            "anxiety": [2, 1, 2, 2, 3, 1, 2],
            "stress": [3, 3, 2, 2, 1, 2, 3]
        },
        "performance_score": 88.5
    }

    # 1. Calcular via Python (Determinístico)
    scores = Psychometrics.calculate_dass21(responses["dass21"])
    # Para o BIG5, usamos um matcher simulado de 82% para a demo
    bussola = Psychometrics.get_bussola_quadrante(responses["performance_score"], 82.0)

    # 2. Persistir no PostgreSQL
    db = SessionLocal()
    try:
        new_diag = Diagnostic(
            candidate_name="Maria Emília Costa Ramos",
            candidate_email="emilia@exemplo.com",
            scores={
                "dass21": scores,
                "big5_match": 82.0
            },
            performance_score=88.5,
            matcher_score=82.0,
            quadrant_label=bussola["label"]
        )
        db.add(new_diag)
        db.commit()
        print(f"✅ Sucesso! Maria Emília processada e salva como: {bussola['label']}")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    ingest_emilia()