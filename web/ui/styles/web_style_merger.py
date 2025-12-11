# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\styles\web_style_merger.py
# Última atualização: 2025-12-11T09:59:27.886588

class WebStyleMerger:
    """
    Mescla diferentes estilos Web (corporativo, dark, padrão).
    """

    @staticmethod
    def merge(a: dict, b: dict):
        output = a.copy()
        output.update(b)
        return output
