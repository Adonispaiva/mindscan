from pydantic import BaseModel
from typing import Dict, Any


class MindScanInput(BaseModel):
    data: Dict[str, Any]
