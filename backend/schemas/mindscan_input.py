from typing import Dict, Any
from pydantic import BaseModel

class MindScanInput(BaseModel):
    responses: Dict[str, Any]
