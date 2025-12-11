# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\schemas\mindscan_models.py
# Última atualização: 2025-12-11T09:59:20.761538

from pydantic import BaseModel
from typing import Optional, Dict, Any


class MindScanRunRequest(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    form_data: Dict[str, Any]
    report_type: Optional[str] = "executive"


class MindScanRunResponse(BaseModel):
    status: str
    message: str
    test_id: Optional[str]
    session_id: Optional[str]
    report_url: Optional[str]
    results: Optional[Dict[str, Any]]
