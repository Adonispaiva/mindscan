"""
TEIQue Profile Builder
Responsável por construir o perfil emocional final a partir das dimensões
processadas do TEIQue.
"""

from typing import Dict, Any, List


class TeiqueProfileBuilder:
    """
    Constrói o perfil emocional baseado em fatores agregados do TEIQue.
    """

    def __init__(self):
        self.version = "1.0"

    def build(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Recebe scores padronizados e constrói:
            - fatores agregados
            - descrições
            - nível emocional global
        """
        factors = self._aggregate_factors(scores)

        return {
            "module": "TEIQue",
            "version": self.version,
            "factors": factors,
            "emotional_profile": self._compute_emotional_profile(factors),
            "descriptions": self._generate_descriptions(factors),
        }

    def _aggregate_factors(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Exemplo simples:
        Agrupa dimensões específicas por clusters emocionais.
        """

        groups = {
            "Bem-estar": ["otimismo", "autoestima", "satisfacao"],
            "Autocontrole": ["impulsividade", "controle_emocional"],
            "Emoções Sociais": ["empatia", "relacoes"],
            "Emoções Cognitivas": ["autorregulacao", "adaptabilidade"],
        }

        aggregated = {}

        for factor, dims in groups.items():
            values = [scores.get(dim, None) for dim in dims]
            values = [v for v in values if v is not None]

            aggregated[factor] = sum(values) / len(values) if values else 0

        return aggregated

    def _compute_emotional_profile(self, factors: Dict[str, float]) -> float:
        """
        Índice emocional global (0–100).
        """
        if not factors:
            return 0

        return sum(factors.values()) / len(factors)

    def _generate_descriptions(self, factors: Dict[str, float]) -> Dict[str, str]:
        """
        Gera descrições qualitativas das faixas.
        """

        descriptions = {}
        for factor, value in factors.items():
            if value >= 70:
                desc = "Funcionamento emocional consistentemente alto."
            elif value >= 45:
                desc = "Equilíbrio emocional moderado."
            else:
                desc = "Possíveis dificuldades emocionais observáveis."

            descriptions[factor] = desc

        return descriptions
