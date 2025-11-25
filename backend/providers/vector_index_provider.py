# ============================================================
# MindScan — Vector Index Provider
# ============================================================
# Responsável por:
# - indexação de embeddings
# - busca semântica
# - similaridade vetorial interna
# - preparação para FAISS / HNSW / Milvus / Pinecone
#
# Estrutura:
#   - index[name] = { "vector": np.array([...]), "metadata": {...} }
#
# Versão: FINAL — SynMind 2025
# ============================================================

from typing import List, Dict, Optional, Any, Tuple
import numpy as np


class VectorIndexProvider:
    """
    Índice vetorial interno do MindScan.
    
    Funcionalidades:
    - adicionar embeddings com metadados
    - busca por similaridade (cosine)
    - normalização automática
    - retorno ordenado por relevância
    """

    def __init__(self, normalize: bool = True):
        # index[name] = { vector: np.array, metadata: dict }
        self.index: Dict[str, Dict[str, Any]] = {}
        self.normalize = normalize

    # ------------------------------------------------------------
    # Normalizar vetor
    # ------------------------------------------------------------
    def _normalize(self, vector: List[float]) -> np.ndarray:
        vec = np.array(vector, dtype=float)
        norm = np.linalg.norm(vec)
        return vec / norm if norm != 0 else vec

    # ------------------------------------------------------------
    # Registrar embedding no índice
    # ------------------------------------------------------------
    def add(self, name: str, vector: List[float], metadata: Optional[Dict] = None):
        if self.normalize:
            vector = self._normalize(vector)

        self.index[name] = {
            "vector": np.array(vector, dtype=float),
            "metadata": metadata or {}
        }

    # ------------------------------------------------------------
    # Remover entrada
    # ------------------------------------------------------------
    def remove(self, name: str):
        if name in self.index:
            del self.index[name]

    # ------------------------------------------------------------
    # Similaridade de cosseno
    # ------------------------------------------------------------
    def _similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        dot = np.dot(a, b)
        na = np.linalg.norm(a)
        nb = np.linalg.norm(b)
        denom = (na * nb)
        return dot / denom if denom != 0 else 0.0

    # ------------------------------------------------------------
    # Buscar k resultados mais similares
    # ------------------------------------------------------------
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float, Dict]]:
        if self.normalize:
            query_vector = self._normalize(query_vector)

        query = np.array(query_vector, dtype=float)

        results = []
        for name, entry in self.index.items():
            sim = self._similarity(query, entry["vector"])
            results.append((name, sim, entry["metadata"]))

        # Ordenar por similaridade
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    # ------------------------------------------------------------
    # Listar todos os vetores
    # ------------------------------------------------------------
    def list_entries(self) -> List[str]:
        return list(self.index.keys())

    # ------------------------------------------------------------
    # Obter vetor
    # ------------------------------------------------------------
    def get_vector(self, name: str) -> Optional[np.ndarray]:
        if name not in self.index:
            return None
        return self.index[name]["vector"]

    # ------------------------------------------------------------
    # Obter metadados
    # ------------------------------------------------------------
    def get_metadata(self, name: str) -> Optional[Dict]:
        if name not in self.index:
            return None
        return self.index[name]["metadata"]
