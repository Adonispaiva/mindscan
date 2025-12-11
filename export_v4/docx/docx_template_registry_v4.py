# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\docx\docx_template_registry_v4.py
# Última atualização: 2025-12-11T09:59:27.605346

class DOCXTemplateRegistryV4:
    """
    Registro corporativo de templates DOCX do MindScan 4.0.
    """

    TEMPLATES = {
        "executive": "<DOCX-EXEC>",
        "clinical": "<DOCX-CLINICAL>",
        "corporate": "<DOCX-CORP>"
    }

    @staticmethod
    def get(name: str):
        return DOCXTemplateRegistryV4.TEMPLATES.get(name, "<DOCX-DEFAULT>")
