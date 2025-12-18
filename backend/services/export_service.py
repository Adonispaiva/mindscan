# Arquivo: backend/services/export_service.py
# MindScan Backend — Export Service (CSV/JSON)
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão: 1.0.0

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple, Optional

from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.models import Result


class ExportService:
    """
    Exporta resultados do MindScan em formatos utilizáveis.
    - JSON: retorna dict com metadados + resultados normalizados.
    - CSV: gera arquivo em /exports e retorna caminho.
    """

    def get_latest_results(self, db: Session, test_id: int) -> Tuple[Optional[Result], Any]:
        last = (
            db.query(Result)
            .filter(Result.test_id == test_id)
            .order_by(desc(Result.id))
            .first()
        )

        if not last or not last.results:
            return None, []

        try:
            payload = json.loads(last.results)
        except Exception:
            payload = last.results  # fallback raw
        return last, payload

    def export_json(self, db: Session, test_id: int) -> Dict[str, Any]:
        last, payload = self.get_latest_results(db, test_id)
        return {
            "test_id": test_id,
            "result_id": getattr(last, "id", None),
            "results": payload if payload is not None else [],
        }

    def export_csv(self, db: Session, test_id: int) -> str:
        _, payload = self.get_latest_results(db, test_id)

        exports_dir = Path("exports")
        exports_dir.mkdir(parents=True, exist_ok=True)
        file_path = exports_dir / f"mindscan_results_{test_id}.csv"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("dimension,score,descriptor\n")
            if isinstance(payload, list):
                for item in payload:
                    if isinstance(item, dict):
                        dim = _csv(item.get("dimension"))
                        score = _csv(item.get("score"))
                        descp = _csv(item.get("descriptor"))
                        f.write(f"{dim},{score},{descp}\n")
            elif isinstance(payload, dict):
                for k, v in payload.items():
                    f.write(f"{_csv(k)},,{_csv(v)}\n")
            else:
                f.write(f"raw,,{_csv(payload)}\n")

        return str(file_path)


def _csv(value: Any) -> str:
    if value is None:
        return ""
    s = str(value)
    s = s.replace("\n", " ").replace("\r", " ").replace(",", ";")
    return s
