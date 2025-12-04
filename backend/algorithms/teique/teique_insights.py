# ================================================================
#  MindScan — TEIQue Insights
#  Categoria: Algorithm — TEIQue
#  Responsável: Leo Vinci (Inovexa)
#
#  Objetivo:
#      Transformar as dimensões do TEIQue em insights textuais
#      para uso em:
#          - PDF (Inteligência Emocional)
#          - Dashboard
#          - Perfil integrado
#
#  API pública:
#      TEIQueInsights.generate(dimensions: dict) -> dict
# ================================================================

from typing import Dict, Any


class TEIQueInsights:
    """
    Gera insights interpretativos a partir das dimensões TEIQue.

    Espera um dicionário:

        {
            "well_being": 0–10,
            "self_control": 0–10,
            "emotionality": 0–10,
            "sociability": 0–10,
            "global": 0–10
        }
    """

    def generate(self, dimensions: Dict[str, float]) -> Dict[str, Any]:
        wb = dimensions.get("well_being", 0.0)
        sc = dimensions.get("self_control", 0.0)
        em = dimensions.get("emotionality", 0.0)
        so = dimensions.get("sociability", 0.0)
        global_score = dimensions.get("global", 0.0)

        return {
            "well_being": self._insight_well_being(wb),
            "self_control": self._insight_self_control(sc),
            "emotionality": self._insight_emotionality(em),
            "sociability": self._insight_sociability(so),
            "global_profile": self._insight_global(global_score, wb, sc, em, so),
        }

    # ------------------------------------------------------------
    #  Insights por dimensão
    # ------------------------------------------------------------
    def _label(self, value: float) -> str:
        if value >= 7.0:
            return "muito alto"
        if value >= 6.0:
            return "alto"
        if value >= 5.0:
            return "moderado"
        if value >= 4.0:
            return "baixo"
        return "muito baixo"

    def _insight_well_being(self, v: float) -> Dict[str, str]:
        if v >= 6.0:
            text = (
                "Demonstra senso consistente de satisfação pessoal, otimismo "
                "e confiança na própria capacidade emocional."
            )
        else:
            text = (
                "Pode vivenciar oscilação de humor, autocrítica elevada ou "
                "sensação de insatisfação com a própria trajetória."
            )
        return {"label": self._label(v), "text": text}

    def _insight_self_control(self, v: float) -> Dict[str, str]:
        if v >= 6.0:
            text = (
                "Mostra boa capacidade de regular impulsos, manter a calma sob "
                "pressão e se recuperar após eventos estressores."
            )
        else:
            text = (
                "Pode reagir de forma impulsiva em situações de pressão, com "
                "maior dificuldade para modular emoções intensas."
            )
        return {"label": self._label(v), "text": text}

    def _insight_emotionality(self, v: float) -> Dict[str, str]:
        if v >= 6.0:
            text = (
                "Possui elevada sensibilidade emocional e facilidade para "
                "compreender, expressar e compartilhar sentimentos."
            )
        else:
            text = (
                "Pode encontrar desafios para reconhecer as próprias emoções "
                "ou expressá-las de modo claro nas relações."
            )
        return {"label": self._label(v), "text": text}

    def _insight_sociability(self, v: float) -> Dict[str, str]:
        if v >= 6.0:
            text = (
                "Tende a buscar interações, oferecer suporte e influenciar o "
                "ambiente social de forma ativa."
            )
        else:
            text = (
                "Pode preferir interações mais seletivas, evitando exposição "
                "social intensa ou disputas interpessoais."
            )
        return {"label": self._label(v), "text": text}

    def _insight_global(
        self,
        global_score: float,
        wb: float,
        sc: float,
        em: float,
        so: float,
    ) -> Dict[str, str]:
        if global_score >= 6.5:
            core = "Perfil de inteligência emocional globalmente elevado."
        elif global_score >= 5.5:
            core = "Perfil de inteligência emocional equilibrado, com bons recursos internos."
        else:
            core = "Perfil emocional com pontos de atenção importantes."

        # pontos de atenção
        low_dimensions = []
        if wb < 5.0:
            low_dimensions.append("bem-estar")
        if sc < 5.0:
            low_dimensions.append("autocontrole")
        if em < 5.0:
            low_dimensions.append("emocionalidade")
        if so < 5.0:
            low_dimensions.append("sociabilidade")

        if low_dimensions:
            details = (
                " Áreas sensíveis: "
                + ", ".join(low_dimensions)
                + ". Recomenda-se apoio direcionado e monitoramento."
            )
        else:
            details = " Não há dimensões críticas evidentes no momento."

        return {
            "label": self._label(global_score),
            "text": core + details,
        }


if __name__ == "__main__":
    example_dims = {
        "well_being": 6.8,
        "self_control": 5.4,
        "emotionality": 6.2,
        "sociability": 5.0,
        "global": 5.9,
    }
    ins = TEIQueInsights()
    print(ins.generate(example_dims))
