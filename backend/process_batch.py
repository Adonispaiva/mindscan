import os
import sys
import logging
from datetime import datetime

# Setup de Caminhos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.algorithms.mindscan_engine import MindScanEngine
from backend.algorithms.matcher import MindMatcher
from backend.services.report_service import ReportService
from backend.utils.csv_parser import CSVParser
from backend.utils.helpers import sanitize_filename

# Configuração de Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MindScan.BatchProcessor")

def run_batch(csv_path: str):
    if not os.path.exists(csv_path):
        logger.error(f"❌ Arquivo não encontrado: {csv_path}")
        return

    logger.info(f"📂 Lendo planilha: {csv_path}")
    df = CSVParser.load_data(csv_path)
    
    engine = MindScanEngine()
    matcher = MindMatcher()
    service = ReportService(output_dir="backend/generated_reports")

    success_count = 0
    
    for index, row in df.iterrows():
        try:
            # 1. Identificação do Candidato
            nome = row.get('Nome Completo', f'Candidato_{index}')
            email = row.get('Endereço de e-mail', 'sem_email')
            
            logger.info(f"🔄 Processando [{index+1}/{len(df)}]: {nome}")

            # 2. Extração de Respostas (Big5 + DASS)
            # Ajuste o start_idx conforme a coluna exata onde começam as perguntas (no seu CSV parece ser a 8)
            big5_resp, dass_resp = CSVParser.extract_responses(row, start_idx=8)

            # 3. Processamento Psicométrico (Engine)
            payload = {
                "user_id": email,
                "big5_responses": big5_resp,
                "dass21_responses": dass_resp,
                "timestamp": datetime.now().strftime("%d/%m/%Y")
            }
            results = engine.process_full_diagnostic(payload)
            
            # 4. Cálculo do MindMatch (Aderência ao Perfil Ideal)
            # Injetamos o score calculado pelo Matcher nos resultados
            match_score = matcher.calculate_match_score(results['big5'])
            results['scores_consolidated'] = {"performance": int(match_score)}
            results['metadata']['match_score'] = match_score

            # 5. Geração de Relatórios
            # Executivo (Para o Gestor)
            service.generate_report(
                candidate_data={"name": nome}, 
                results=results, 
                report_type="executive"
            )
            
            # Feedback (Para o Candidato)
            service.generate_report(
                candidate_data={"name": nome}, 
                results=results, 
                report_type="feedback"
            )

            success_count += 1

        except Exception as e:
            logger.error(f"⚠️ Falha ao processar {nome}: {e}")
            continue

    logger.info(f"✅ Processamento concluído! {success_count} relatórios gerados com sucesso.")

if __name__ == "__main__":
    # Caminho padrão ou argumento via linha de comando
    target_csv = sys.argv[1] if len(sys.argv) > 1 else "MINDSCAN_AVALIAÇÃO_PSICOPROFISSIONAL.csv"
    run_batch(target_csv)