# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\builder\expv4_document_builder.py
# Última atualização: 2025-12-11T09:59:27.574098

class EXPV4DocumentBuilder:
    """
    Constrói documento final combinando templates + dados + estilos.
    """

    @staticmethod
    def build(template: str, data: dict, style: dict):
        return {
            "template_used": template,
            "style": style,
            "content_length": len(str(data))
        }
