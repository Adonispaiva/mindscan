import os
import sys
import pandas as pd
import logging
from datetime import datetime

# Garante que o Python reconheça a pasta backend para importações locais
# Essencial para evitar o erro 'ModuleNotFoundError'
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Importação do núcleo de dados do MindScan
    from database import SessionLocal
    from FORCA_BRUTA_SETUP import Usuario, Diagnostico, MetricaPsicometrica
    print("✅ Módulos de banco de dados carregados com sucesso.")
except ImportError as e:
    print(f"❌ ERRO CRÍTICO: Não foi possível importar database.py ou FORCA_BRUTA_SETUP.py.")
    print(f"Certifique-se de que este script está em: D:\\projetos-inovexa\\mindscan\\backend\\")
    print(f"Detalhes: {e}")
    sys.exit(1)

# Configuração de Logs Padrão Orion/Inovexa
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MindScan.Ingestion")

# --- DEFINIÇÃO DOS ATIVOS (CAMINHOS) ---
# Adonis, confirmamos que o CSV está na subpasta 'data' dentro do backend
CSV_FILENAME = "relatorio_emilia.csv"
CSV_PATH = os.path.join(current_dir, "data", CSV_FILENAME)

def run_ingestion():
    """
    Executa o processamento do CSV e a persistência no PostgreSQL.
    """
    if not os.path.exists(CSV_PATH):
        logger.error(f"❌ ARQUIVO NÃO ENCONTRADO: O sistema não localizou {CSV_PATH}")
        return

    logger.info(f"📂 Iniciando leitura do ativo: {CSV_PATH}")

    db = SessionLocal()
    try:
        # Leitura robusta: sep=None detecta automaticamente vírgula ou ponto-e-vírgula
        df = pd.read_csv(CSV_PATH, sep=None, engine='python', encoding='utf-8-sig')
        
        # 1. VALIDAÇÃO DE USUÁRIO (MARIA EMÍLIA)
        target_email = "emilia@synmind.com.br"
        user = db.query(Usuario).filter(Usuario.email == target_email).first()
        
        if not user:
            user = Usuario(
                nome="Maria Emília",
                email=target_email,
                empresa="SynMind",
                cargo="Diretoria"
            )
            db.add(user)
            db.flush() # Sincroniza para obter o ID
            logger.info(f"👤 Perfil Master criado: {user.nome}")
        else:
            logger.info(f"👤 Perfil Master localizado: {user.nome}")

        # 2. CRIAÇÃO DO DIAGNÓSTICO
        # Criamos um container único para esta importação
        diagnostico = Diagnostico(
            usuario_id=user.id,
            status="concluido",
            tipo_relatorio="premium",
            metadados={
                "engine_version": "3.1",
                "source_file": CSV_FILENAME,
                "timestamp": datetime.now().isoformat()
            }
        )
        db.add(diagnostico)
        db.flush()

        # 3. PROCESSAMENTO DAS MÉTRICAS PSICOMÉTRICAS
        # Normalização das colunas para evitar conflitos de espaços ou cases
        df.columns = [c.strip().lower() for c in df.columns]
        
        count = 0
        for index, row in df.iterrows():
            try:
                # Mapeamento dinâmico baseado no padrão de colunas SynMind
                cat = str(row.get('categoria', 'GERAL')).upper()
                label = str(row.get('metrica', row.get('chave', 'n/a'))).lower()
                val = float(row.get('valor', 0))
                text_interpret = str(row.get('interpretacao', ''))

                if label != 'n/a':
                    metrica_obj = MetricaPsicometrica(
                        diagnostico_id=diagnostico.id,
                        categoria=cat,
                        chave=label,
                        valor=val,
                        interpretacao=text_interpret
                    )
                    db.add(metrica_obj)
                    count += 1
            except Exception as e_row:
                logger.warning(f"⚠️ Falha na linha {index}: {e_row}")

        # COMMIT FINAL: Garante a persistência de tudo o que foi processado
        db.commit()
        
        print("\n" + "★" * 60)
        print(f" ✅ INGESTÃO CONCLUÍDA COM SUCESSO!")
        print(f" 📊 MÉTRICAS IMPORTADAS: {count}")
        print(f" 🔗 ID DIAGNÓSTICO: {diagnostico.id}")
        print(f" 👤 DESTINATÁRIO: {user.nome}")
        print("★" * 60 + "\n")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ ERRO CRÍTICO NA OPERAÇÃO: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" 🚀 MINDSCAN - INOVEXA DATA ENGINE v3.1")
    print("=" * 60)
    run_ingestion()