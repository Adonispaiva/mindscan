"""
TEIQue Traits Map
Mapeamento completo de traços emocionais derivados das dimensões TEIQue.
"""

from typing import Dict


class TeiqueTraitsMap:
    """
    Converte dimensões do TEIQue em traços emocionais interpretáveis,
    utilizados no pipeline de perfil, cruzamentos e narrativa.
    """

    def __init__(self):
        self.version = "1.0"

        # Mapeamento oficial MindScan para narrativa e cruzamentos
        self.trait_map = {
            "otimismo": "Tendência a manter perspectiva positiva.",
            "autoestima": "Percepção estável de valor próprio.",
            "satisfacao": "Estabilidade emocional e bem-estar.",
            "empatia": "Sensibilidade às experiências alheias.",
            "relacoes": "Habilidade social para vínculos saudáveis.",
            "impulsividade": "Reatividade rápida a estímulos.",
            "controle_emocional": "Capacidade de gerenciar flutuações afetivas.",
            "autorregulacao": "Ajuste cognitivo e emocional flexível.",
            "adaptabilidade": "Flexibilidade diante de mudanças.",
        }

    def map_traits(self, scores: Dict[str, float]) -> Dict[str, str]:
        """
        Associa cada dimensão à sua descrição correspondente.
        """
        mapped = {}

        for dim, val in scores.items():
            desc = self.trait_map.get(
                dim,
                "Traço emocional associado à dimensão."
            )
            mapped[dim] = desc

        return {
            "module": "TEIQue",
            "version": self.version,
            "traits": mapped
        }
