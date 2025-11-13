import os
import json
import asyncio
import httpx
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ValidationError

# =============================
# CONFIGURAÇÃO GLOBAL
# =============================
SYNMIND_API_URL = os.getenv("SYNMIND_API_URL", "http://synmind_core:9000")
CACHE_DIR = os.getenv("SYNMIND_CACHE_DIR", "/data/synmind_cache")
TIMEOUT = float(os.getenv("SYNMIND_TIMEOUT", 8.0))
RETRY_LIMIT = 3

os.makedirs(CACHE_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [SynMindAdapter] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(CACHE_DIR, "synmind_adapter.log"), encoding="utf-8")
    ]
)
logger = logging.getLogger("SynMindAdapter")

# =============================
# MODELOS DE DADOS
# =============================
class AssessmentPayload(BaseModel):
    user_id: str
    profile_type: str
    traits: Dict[str, float]
    timestamp: datetime

class InsightResponse(BaseModel):
    insight_id: str
    dominant_trait: str
    recommendations: List[str]
    confidence: float

class SyncResult(BaseModel):
    synced_profiles: int
    updated_records: int
    timestamp: datetime

# =============================
# CLASSE PRINCIPAL
# =============================
class SynMindAdapter:
    def __init__(self):
        self.api_url = SYNMIND_API_URL.rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.api_url, timeout=TIMEOUT)

    async def _safe_post(self, endpoint: str, data: dict) -> Optional[dict]:
        for attempt in range(RETRY_LIMIT):
            try:
                response = await self.client.post(endpoint, json=data)
                if response.status_code == 200:
                    return response.json()
                logger.warning(f"[{attempt+1}/{RETRY_LIMIT}] Código HTTP {response.status_code} em {endpoint}")
            except Exception as e:
                logger.error(f"Erro em POST {endpoint}: {e}")
                await asyncio.sleep(1.5)
        return None

    async def _safe_get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        for attempt in range(RETRY_LIMIT):
            try:
                response = await self.client.get(endpoint, params=params)
                if response.status_code == 200:
                    return response.json()
                logger.warning(f"[{attempt+1}/{RETRY_LIMIT}] Código HTTP {response.status_code} em {endpoint}")
            except Exception as e:
                logger.error(f"Erro em GET {endpoint}: {e}")
                await asyncio.sleep(1.5)
        return None

    async def push_assessment(self, payload: AssessmentPayload) -> bool:
        logger.info(f"Enviando avaliação do usuário {payload.user_id} para SynMind...")
        try:
            result = await self._safe_post("/api/v3/synmind/push", payload.dict())
            if result:
                cache_path = os.path.join(CACHE_DIR, f"push_{payload.user_id}.json")
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2)
                logger.info(f"✅ Avaliação registrada no cache: {cache_path}")
                return True
        except ValidationError as ve:
            logger.error(f"Payload inválido: {ve}")
        return False

    async def fetch_insights(self, user_id: str) -> Optional[InsightResponse]:
        logger.info(f"Obtendo insights do usuário {user_id} no SynMind...")
        data = await self._safe_get("/api/v3/synmind/insights", params={"user_id": user_id})
        if data:
            try:
                insight = InsightResponse(**data)
                cache_path = os.path.join(CACHE_DIR, f"insight_{user_id}.json")
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(insight.dict(), f, indent=2, default=str)
                return insight
            except ValidationError as ve:
                logger.error(f"Erro de validação InsightResponse: {ve}")
        return None

    async def sync_profiles(self, profiles: List[dict]) -> Optional[SyncResult]:
        logger.info(f"Sincronizando {len(profiles)} perfis com SynMind...")
        payload = {"profiles": profiles}
        data = await self._safe_post("/api/v3/synmind/sync", payload)
        if data:
            try:
                result = SyncResult(**data)
                cache_path = os.path.join(CACHE_DIR, f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(result.dict(), f, indent=2, default=str)
                logger.info(f"✅ Sincronização registrada no cache: {cache_path}")
                return result
            except ValidationError as ve:
                logger.error(f"Erro de validação SyncResult: {ve}")
        return None

    async def close(self):
        await self.client.aclose()

# =============================
# EXECUÇÃO DIRETA (DEBUG)
# =============================
if __name__ == "__main__":
    async def _debug():
        adapter = SynMindAdapter()
        payload = AssessmentPayload(
            user_id="debug_001",
            profile_type="Analitico",
            traits={"foco": 0.9, "criatividade": 0.4},
            timestamp=datetime.now()
        )
        await adapter.push_assessment(payload)
        insights = await adapter.fetch_insights("debug_001")
        print("INSIGHTS:", insights)
        await adapter.close()
    asyncio.run(_debug())