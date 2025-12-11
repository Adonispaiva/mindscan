# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\diagnostic_engine.py
# Última atualização: 2025-12-11T09:59:20.777102

from typing import Dict, Any, List


class DiagnosticEngine:
    """
    Núcleo consolidado do diagnóstico MindScan 2.0.
    Responsável por transformar scores psicométricos
    em perfis, insights e interpretações profissionais.
    """

    def generate_diagnosis(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        # ------------------------------------------------------------
        # 1. Gerar perfil consolidado
        # ------------------------------------------------------------
        profile = self._build_profile(scores)

        # ------------------------------------------------------------
        # 2. Gerar insights automáticos
        # ------------------------------------------------------------
        insights = self._generate_insights(profile, scores)

        # Estrutura final
        return {
            "profile": profile,
            "insights": insights,
            "scores": scores
        }

    # ------------------------------------------------------------
    #  PERFIL CONSOLIDADO
    # ------------------------------------------------------------
    def _build_profile(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        profile = {}

        for instrument, data in scores.items():
            if instrument == "BIG5":
                profile["personality"] = self._profile_big5(data)
            elif instrument == "TEIQue":
                profile["emotional_intelligence"] = self._profile_teiQue(data)
            elif instrument == "OCAI":
                profile["organizational_culture"] = self._profile_ocai(data)
            elif instrument == "DASS21":
                profile["mental_health"] = self._profile_dass21(data)

        return profile

    # ------------------------------------------------------------
    #  INSIGHTS AUTOMÁTICOS
    # ------------------------------------------------------------
    def _generate_insights(self, profile: Dict[str, Any], scores: Dict[str, Any]) -> List[str]:
        insights = []

        if "personality" in profile:
            p = profile["personality"]
            if p.get("avg", 0) > 3:
                insights.append("Tendência a estabilidade emocional e autocontrole.")
            else:
                insights.append("Possível variação emocional sob pressão.")

        if "mental_health" in profile:
            mh = profile["mental_health"]
            if mh.get("score", 0) > 30:
                insights.append("Indícios de estresse significativo.")
            else:
                insights.append("Níveis saudáveis de bem-estar mental.")

        return insights

    # ------------------------------------------------------------
    #  PROFILES POR INSTRUMENTO (PLACEHOLDERS)
    # ------------------------------------------------------------
    def _profile_big5(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "avg": data.get("avg", 0),
            "interpretation": "Perfil Big Five consolidado (versão simplificada)."
        }

    def _profile_teiQue(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "emotional_intelligence_raw": data.get("sum", 0),
            "interpretation": "Indicadores básicos de inteligência emocional."
        }

    def _profile_ocai(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "culture_profile": data.get("profile", []),
            "interpretation": "Distribuição de cultura organizacional (OCAI)."
        }

    def _profile_dass21(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "score": data.get("score", 0),
            "interpretation": "Nível geral de estresse segundo DASS-21."
        }
