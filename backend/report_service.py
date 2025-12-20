import os
import logging
from datetime import datetime
from typing import Dict, Any

# Configuração de Logs conforme BOOT-SPEC da SynMind
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MindScan.ReportService")

class ReportService:
    """
    Serviço central de geração de relatórios do ecossistema MindScan (SynMind).
    Gerencia a renderização dos templates: technical, executive, psychodynamic e premium.
    """
    
    def __init__(self, output_dir: str = "generated_reports"):
        # Define diretório de saída a partir da raiz do projeto
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
                logger.info(f"📁 Diretório de relatórios criado: {self.output_dir}")
            except Exception as e:
                logger.error(f"❌ Erro ao criar diretório de saída: {e}")

    def generate_report(self, candidate_data: Dict[str, Any], results: Dict[str, Any], report_type: str = "technical") -> str:
        """
        Orquestra a geração do PDF com base no nível de diagnóstico solicitado.
        """
        # Validação de template conforme mindscan_report_architecture.md
        valid_types = ["technical", "executive", "psychodynamic", "premium"]
        if report_type not in valid_types:
            logger.warning(f"⚠️ Template '{report_type}' inválido. Revertendo para 'technical'.")
            report_type = "technical"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        candidate_id = candidate_data.get('id', 'anon')
        filename = f"MindScan_{report_type.upper()}_{candidate_id}_{timestamp}.pdf"
        file_path = os.path.join(self.output_dir, filename)

        try:
            logger.info(f"🚀 Iniciando processamento do relatório {report_type} | Candidato: {candidate_data.get('name')}")
            
            # TODO: Integração com os renderizadores específicos (technical_renderer, etc)
            # Simulação de escrita de arquivo para validação do fluxo ponta-a-ponta
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"--- SYNMIND MINDSCAN REPORT ---\n")
                f.write(f"Template: {report_type.upper()}\n")
                f.write(f"Candidato: {candidate_data.get('name')}\n")
                f.write(f"Data de Processamento: {datetime.now().isoformat()}\n")
                f.write(f"Status: Validado pelo Motor Determinístico\n")

            logger.info(f"✅ Relatório gerado com sucesso em: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"❌ Falha crítica na geração do PDF: {str(e)}")
            return ""

# Instância única para importação global no backend
report_manager = ReportService()