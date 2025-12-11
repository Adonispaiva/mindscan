# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_dimensions.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
Esquemas Dimensions
Calcula dimensões intermediárias que alimentam a classificação dos 18 Esquemas.
"""

from typing import Dict


class EsquemasDimensions:
    """
    Converte escores normalizados do questionário em dimensões
    estruturadas para posterior classificação de Esquemas.
    """

    def __init__(self):
        self.version = "1.0"

        # Dimensões intermediárias usadas pela literatura
        self.dim_map = {
            "abandono": ["abandono"],
            "desconfianca": ["desconfianca"],
            "privacao_emocional": ["privacao_emocional"],
            "defectividade": ["defectividade"],
            "isolamento": ["isolamento"],
            "dependencia": ["dependencia"],
            "vulnerabilidade": ["vulnerabilidade"],
            "emaranhamento": ["emaranhamento"],
            "fracasso": ["fracasso"],
            "submissao": ["submissao"],
            "autossacrificio": ["autossacrificio"],
            "busca_aprovacao": ["busca_aprovacao"],
            "negatividade": ["negatividade"],
            "inibicao_emocional": ["inibicao_emocional"],
            "hipercriticismo": ["hipercriticismo"],
            "direitos_especiais": ["direitos_especiais"],
            "autocontrole_insuficiente": ["autocontrole_insuficiente"],
            "padrões_inflexíveis": ["padrões_inflexíveis"],
        }

    def compute(self, normalized: Dict[str, float]) -> Dict[str, float]:
        """
        Cada dimensão é formada pela média dos itens correspondentes.
        """

        results = {}

        for dim, items in self.dim_map.items():
            values = [normalized.get(i, 0) for i in items]
            if values:
                results[dim] = sum(values) / len(values)
            else:
                results[dim] = 0.0

        return results
