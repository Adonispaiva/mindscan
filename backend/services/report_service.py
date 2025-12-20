import os
import logging
from datetime import datetime
from typing import Dict, Any

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

# Importação dos renderizadores (assumindo a estrutura de pastas do projeto)
from .report_templates.technical_renderer import TechnicalRenderer
# from .report_templates.executive_renderer import ExecutiveRenderer  # Disponível em breve

logger = logging.getLogger("MindScan.ReportService")

class ReportService:
    """
    Orquestrador central de relatórios SynMind.
    Conecta os resultados da Engine aos templates visuais do ReportLab.
    """
    
    # Mapeamento oficial conforme mindscan_report_architecture.md
    RENDERER_MAP = {
        "technical": TechnicalRenderer,
        # "executive": ExecutiveRenderer, 
        # "psychodynamic": PsychodynamicRenderer,
        # "premium": PremiumRenderer,
    }
    
    def __init__(self, output_dir: str = "generated_reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"📁 Diretório criado: {self.output_dir}")

    def generate_report(self, candidate_data: Dict[str, Any], results: Dict[str, Any], report_type: str = "technical") -> str:
        """
        Executa o pipeline: Seleção -> Renderização -> Build PDF.
        """
        # 1. Seleção do Renderer
        renderer_class = self.RENDERER_MAP.get(report_type, TechnicalRenderer)
        
        # 2. Definição do Nome do Arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        c_name = candidate_data.get('name', 'Candidato').replace(" ", "_")
        filename = f"MindScan_{report_type.upper()}_{c_name}_{timestamp}.pdf"
        file_path = os.path.join(self.output_dir, filename)

        try:
            logger.info(f"🎨 Iniciando renderização {report_type} para: {c_name}")
            
            # 3. Inicialização do Documento ReportLab
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            
            # 4. Instanciação e Construção da 'Story'
            # Passamos o test_id, os resultados e o nome para a base
            renderer = renderer_class(
                test_id=results.get("metadata", {}).get("test_id", "SN-999"),
                results=results,
                candidate_name=candidate_data.get('name')
            )
            
            story = renderer.build() # O Renderer retorna a lista de componentes prontos
            
            # 5. Geração Final do PDF
            doc.build(story)
            
            logger.info(f"✅ PDF Gerado com sucesso: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"❌ Erro crítico na geração do PDF: {str(e)}")
            raise