from pydantic import BaseModel

class MindScanResult(BaseModel):
    status: str
    reports: list[str]
