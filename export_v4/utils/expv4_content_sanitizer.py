# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\utils\expv4_content_sanitizer.py
# Última atualização: 2025-12-11T09:59:27.636599

class EXPV4ContentSanitizer:
    """
    Sanitiza conteúdo textual e visual para exportações PDF/DOCX/HTML.
    """

    @staticmethod
    def sanitize(payload: dict):
        return {k: str(v).strip() for k, v in payload.items()}
