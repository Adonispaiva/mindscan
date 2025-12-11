# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\utils\expv4_image_embedder.py
# Última atualização: 2025-12-11T09:59:27.636599

class EXPV4ImageEmbedder:
    """
    Embute imagens, gráficos e mapas visuais no fluxo de exportação.
    """

    @staticmethod
    def embed(image: str, data: dict):
        return {"image": image, "mapped_data": data}
