from typing import Dict, Any
from pydantic import BaseModel

class MindScanOutput(BaseModel):
    diagnostic_id: str
    reports: Dict[str, str]
