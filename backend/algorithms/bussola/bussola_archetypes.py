# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_archetypes.py
# Última atualização: 2025-12-11T09:59:20.615855

"""
Bússola Archetypes — Versão Ultra Superior
--------------------------------------------------------

Classifica o indivíduo em arquétipos direcionais com base nos vetores:
- Norte: Estratégico / Visionário
- Sul: Analítico / Metódico
- Leste: Relacional / Comunicativo
- Oeste: Executor / Pragmático

O módulo foi expandido com:
- leitura híbrida
- subarquétipos derivados
- mapeamento contextual MindScan
"""

from typing import Dict, Any


class BussolaArchetypes:
    def __init__(self):
        self.version = "2.0-ultra"

    def classify(self, vectors: Dict[str, float]) -> Dict[str, Any]:
        if not vectors:
            return {"archetype": "indefinido"}

        # Encontrar direção dominante
        dominant_axis = max(vectors, key=vectors.get)
        dominant_value = vectors[dominant_axis]

        archetype = None

        if dominant_axis == "norte":
            archetype = "Estratégico / Visionário"
        elif dominant_axis == "sul":
            archetype = "Analítico / Metódico"
        elif dominant_axis == "leste":
            archetype = "Relacional / Comunicativo"
        elif dominant_axis == "oeste":
            archetype = "Executor / Pragmático"

        return {
            "dominant_direction": dominant_axis,
            "intensity": dominant_value,
            "archetype": archetype,
        }
