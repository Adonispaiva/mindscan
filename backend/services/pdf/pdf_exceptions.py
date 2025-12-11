# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_exceptions.py
# Última atualização: 2025-12-11T09:59:21.184463

# pdf_exceptions.py — Exceções do PDF Engine MindScan
# Autor: Leo Vinci — Inovexa Software

class PDFEngineError(Exception):
    """Erro genérico do PDF Engine."""
    pass


class PDFRenderError(PDFEngineError):
    """Erro crítico durante renderização do PDF."""
    pass


class PDFPayloadError(PDFEngineError):
    """Erro quando o payload do relatório é inválido."""
    pass


class PDFAssetError(PDFEngineError):
    """Erro quando um arquivo de asset (logos, imagens) não é encontrado."""
    pass
