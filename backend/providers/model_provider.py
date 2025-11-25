# ============================================================
# MindScan — Model Provider
# ============================================================
# Responsável por:
# - Carregar modelos de IA internos e externos
# - Gerenciar pesos, versões e pipelines
# - Fornecer interface uniforme ao MI Engine
# - Registrar e invocar modelos complexos (deep learning, ML, NLP)
#
# Suporte futuro:
#   • PyTorch / TensorFlow
#   • ONNX Runtime
#   • Modelos de classificação, regressão e risco
#   • Múltiplos modelos simultâneos
#
# Versão: FINAL — SynMind 2025
# ============================================================

from typing import Dict, Any, Callable, Optional
import os
import pickle


class ModelProvider:
    """
    Gerenciador de modelos do MindScan.
    """

    def __init__(self):
        # Estrutura:
        # self.models[name] = { "model": objeto, "metadata": {...} }
        self.models: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------
    # Registrar modelo carregado
    # ------------------------------------------------------------
    def register(self, name: str, model: Any, metadata: Optional[Dict] = None):
        self.models[name] = {
            "model": model,
            "metadata": metadata or {}
        }

    # ------------------------------------------------------------
    # Carregar modelo de arquivo pickle
    # ------------------------------------------------------------
    def load_from_pickle(self, name: str, file_path: str, metadata: Optional[Dict] = None):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo de modelo não encontrado: {file_path}")

        with open(file_path, "rb") as f:
            model = pickle.load(f)

        self.register(name, model, metadata)

    # ------------------------------------------------------------
    # Obter modelo
    # ------------------------------------------------------------
    def get(self, name: str) -> Any:
        if name not in self.models:
            raise ValueError(f"Modelo '{name}' não registrado.")
        return self.models[name]["model"]

    # ------------------------------------------------------------
    # Executar modelo como callable (inferência)
    # ------------------------------------------------------------
    def run(self, name: str, *args, **kwargs) -> Any:
        model = self.get(name)

        if not callable(model):
            raise TypeError(f"O modelo '{name}' não é executável.")

        return model(*args, **kwargs)

    # ------------------------------------------------------------
    # Listar modelos
    # ------------------------------------------------------------
    def list_models(self):
        return list(self.models.keys())

    # ------------------------------------------------------------
    # Metadados
    # ------------------------------------------------------------
    def get_metadata(self, name: str) -> Dict:
        if name not in self.models:
            raise ValueError(f"Modelo '{name}' não registrado.")
        return self.models[name]["metadata"]
