# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\pdf\pdf_template_registry_v4.py
# Última atualização: 2025-12-11T09:59:27.620971

class PDFTemplateRegistryV4:
    """
    Registro de templates PDF profissionais nível corporativo.
    """

    TEMPLATES = {
        "executive": "<PDF-EXECUTIVE>",
        "behavioral": "<PDF-BEHAVIORAL>",
        "leadership": "<PDF-LEADERSHIP>"
    }

    @staticmethod
    def get(name: str):
        return PDFTemplateRegistryV4.TEMPLATES.get(name, "<PDF-DEFAULT>")
