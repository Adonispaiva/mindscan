# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\schemas.py
# Última atualização: 2025-12-11T09:59:20.745854

from pydantic import BaseModel

class MindScanResult(BaseModel):
    status: str
    reports: list[str]
