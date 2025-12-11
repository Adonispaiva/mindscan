# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\utils\http_error_handler.py
# Última atualização: 2025-12-11T09:59:27.886588

from fastapi import HTTPException

class HTTPErrorHandler:
    """
    Unifica respostas de erro em módulos Web.
    """

    @staticmethod
    def raise_error(code: int, msg: str):
        raise HTTPException(status_code=code, detail=msg)
