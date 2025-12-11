# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_factor_weights.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
Esquemas Factor Weights
Calcula pesos e fatores agregados para interpretação avançada dos esquemas.
"""

from typing import Dict


class EsquemasFactorWeights:
    """
    Agrupa os 18 Esquemas em fatores macro usados por:
    - narrativa psicodinâmica
    - cruzamentos
    - relatórios premium
    """

    def __init__(self):
        self.version = "1.0"

        # Agrupamentos oficiais do modelo de Young
        self.factors = {
            "desconexão_rejeição": [
                "abandono",
                "desconfianca",
                "privacao_emocional",
                "defectividade",
                "isolamento",
            ],
            "autonomia_comprometida": [
                "dependencia",
                "vulnerabilidade",
                "emaranhamento",
                "fracasso",
            ],
            "limites_comprometidos": [
                "direitos_especiais",
                "autocontrole_insuficiente",
            ],
            "direcionamento_ao_outro": [
                "submissao",
                "autossacrificio",
                "busca_aprovacao",
            ],
            "hipervigilancia_inibicao": [
                "negatividade",
                "inibicao_emocional",
                "hipercriticismo",
                "padrões_inflexíveis",
            ],
        }

    def compute(self, classified: Dict[str, float]) -> Dict[str, float]:
        """
        Calcula a média dos esquemas pertencentes a cada macrofator.
        """

        results = {}

        for factor, schemas in self.factors.items():
            values = [classified.get(s, 0) for s in schemas]
            if values:
                results[factor] = sum(values) / len(values)
            else:
                results[factor] = 0.0

        return results
