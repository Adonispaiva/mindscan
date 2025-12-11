# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\ui\mindgen_card_manager.py
# Última atualização: 2025-12-11T09:59:27.730331

class MindGenCardManager:
    """
    Gerencia cartões visuais exibidos no dashboard analítico.
    """

    @staticmethod
    def create_card(title: str, content: dict):
        return {
            "title": title,
            "content": content
        }
