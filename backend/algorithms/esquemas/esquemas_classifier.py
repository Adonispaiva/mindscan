# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_classifier.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
Esquemas Classifier
Converte dimensões normalizadas em pontuações finais dos 18 Esquemas de Young.
"""

from typing import Dict


class EsquemasClassifier:
    """
    Aplica pesos e estrutura hierárquica para classificar os Esquemas.
    """

    def __init__(self):
        self.version = "1.0"

        # Estrutura dos 18 Esquemas Adaptativos
        self.schemas = [
            "abandono",
            "desconfianca",
            "privacao_emocional",
            "defectividade",
            "isolamento",
            "dependencia",
            "vulnerabilidade",
            "emaranhamento",
            "fracasso",
            "submissao",
            "autossacrificio",
            "busca_aprovacao",
            "negatividade",
            "inibicao_emocional",
            "hipercriticismo",
            "direitos_especiais",
            "autocontrole_insuficiente",
            "padrões_inflexíveis",
        ]

    def classify(self, dimensions: Dict[str, float]) -> Dict[str, float]:
        """
        Cada esquema recebe diretamente a dimensão correspondente
        ou uma média quando a dimensão é composta.
        """
        results = {}

        for schema in self.schemas:
            value = dimensions.get(schema, 0)
            results[schema] = value

        return results
