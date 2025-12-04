"""
Matcher — Engine de Compatibilidade
Responsável por calcular correspondência entre:
- perfis psicológicos
- perfis culturais
- perfis emocionais
- perfis executivos (liderança, performance e esquemas)
"""

from typing import Dict, Any


class Matcher:
    """
    Cálculo de alinhamento de perfis baseado em:
    - distâncias vetoriais
    - similaridade semântica
    - pesos específicos dos domínios
    """

    def __init__(self):
        self.version = "1.0"
        self.weight_profile = 0.40
        self.weight_cultural = 0.30
        self.weight_emotional = 0.30

    def _distance(self, a: Dict[str, float], b: Dict[str, float]) -> float:
        total = 0.0
        for key in a:
            total += abs(a.get(key, 0) - b.get(key, 0))
        return total

    def match(self, base: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estrutura:
        base = {"profile": {...}, "culture": {...}, "emotional": {...}}
        target = {"profile": {...}, "culture": {...}, "emotional": {...}}
        """

        dp = self._distance(base.get("profile", {}), target.get("profile", {}))
        dc = self._distance(base.get("culture", {}), target.get("culture", {}))
        de = self._distance(base.get("emotional", {}), target.get("emotional", {}))

        score = (
            (1 - dp / 100) * self.weight_profile +
            (1 - dc / 100) * self.weight_cultural +
            (1 - de / 100) * self.weight_emotional
        )

        return {
            "module": "Matcher",
            "version": self.version,
            "distance_profile": dp,
            "distance_culture": dc,
            "distance_emotional": de,
            "compatibility_score": max(min(score * 100, 100), 0)
        }
