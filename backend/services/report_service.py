# ... imports anteriores mantidos ...
from .report_templates.technical_renderer import TechnicalRenderer
from .report_templates.executive_renderer import ExecutiveRenderer
from .report_templates.feedback_renderer import FeedbackRenderer # <--- NOVO

class ReportService:
    
    RENDERER_MAP = {
        "technical": TechnicalRenderer,
        "executive": ExecutiveRenderer,
        "feedback": FeedbackRenderer, # <--- Mapeado
    }
    
    # ... método __init__ mantido ...

    def generate_report(self, candidate_data: Dict[str, Any], results: Dict[str, Any], report_type: str = "technical") -> str:
        # A lógica é a mesma, mas agora aceita report_type="feedback"
        # O código de geração (passos 1 a 6) se mantém igual ao que você já tem,
        # pois a arquitetura de 'renderer.build()' é polimórfica.
        
        # Copie o conteúdo da versão anterior e apenas adicione o import e a chave no MAP.
        # Se preferir, posso reenviar o arquivo inteiro, mas é redundante.
        pass