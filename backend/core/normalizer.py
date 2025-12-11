# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\normalizer.py
# Última atualização: 2025-12-11T09:59:20.777102

from typing import Dict, Any


class Normalizer:
    """
    Normalizador de dados psicométricos.
    Padroniza formatos, corrige tipos e garante consistência
    antes do processamento NLP e cálculo de scores.
    """

    def normalize(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        # ------------------------------------------------------------
        # 1. Normalização do candidato
        # ------------------------------------------------------------
        candidate = dataset.get("candidate", {})

        normalized_candidate = {
            "name": candidate.get("name", "").strip(),
            "email": candidate.get("email"),
            "age": int(candidate.get("age")) if candidate.get("age") else None,
            "gender": candidate.get("gender"),
            "notes": candidate.get("notes", "").strip() if candidate.get("notes") else None,
        }

        # ------------------------------------------------------------
        # 2. Normalização dos instrumentos
        # ------------------------------------------------------------
        instruments = dataset.get("instruments", [])
        normalized_instruments = []

        for item in instruments:
            instrument = item.get("instrument")
            answers = item.get("answers", [])

            normalized_answers = []
            for ans in answers:
                normalized_answers.append({
                    "id": ans.get("id"),
                    "value": ans.get("value"),
                })

            normalized_instruments.append({
                "instrument": instrument,
                "answers": normalized_answers,
            })

        # ------------------------------------------------------------
        # 3. Metadados
        # ------------------------------------------------------------
        metadata = dataset.get("metadata", {})

        # Estrutura final normalizada
        return {
            "candidate": normalized_candidate,
            "instruments": normalized_instruments,
            "metadata": metadata,
        }
