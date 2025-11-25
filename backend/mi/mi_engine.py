# ============================================================
# MindScan — MI Engine (Mind Intelligence Layer)
# ============================================================
# O MI Engine interpreta os resultados psicométricos e gera:
# - Insights Inteligentes
# - Padrões de comportamento
# - Talentos dominantes
# - Fragilidades potenciais
# - Recomendações práticas
# - Detecção de contradições internas
#
# Entrada:
# - big5
# - teique
# - dass21
# - ocai
# - esquemas
# - performance
# - cruzamentos (identidade psicoprofissional)
# - bussola (quadrante final)
#
# Versão completa, maximizada e definitiva.
# ============================================================

from typing import Dict, Any, List


class MIEngine:
    """
    Interpretação avançada dos resultados psicométricos.
    """

    # ------------------------------------------------------------
    # INSIGHT: TALENTOS DOMINANTES
    # ------------------------------------------------------------
    def map_talents(self, cross: Dict[str, Any]) -> List[Dict[str, Any]]:
        talents = []

        if cross["potencial_performance"]["score"] >= 70:
            talents.append({
                "label": "Potencial de Performance",
                "strength": "Alta capacidade de entrega, disciplina e ritmo.",
            })

        if cross["softskills_relacionais"]["score"] >= 70:
            talents.append({
                "label": "Soft-Skills Relacionais",
                "strength": "Empatia, comunicação clara e facilidade de conexão.",
            })

        if cross["expressividade_energia"]["score"] >= 70:
            talents.append({
                "label": "Expressividade & Energia",
                "strength": "Presença, iniciativa e impulso de ação.",
            })

        if not talents:
            talents.append({
                "label": "Talentos Moderados",
                "strength": "Potenciais comportamentais distribuídos sem destaque extremo."
            })

        return talents

    # ------------------------------------------------------------
    # INSIGHT: FRAGILIDADES POTENCIAIS
    # ------------------------------------------------------------
    def map_risks(self, cross: Dict[str, Any]) -> List[Dict[str, Any]]:
        risks = []
        r_val = cross["risco_cognitivo_emocional"]["score"]

        if r_val >= 70:
            risks.append({
                "label": "Risco Cognitivo-Emocional Elevado",
                "detail": "Padrões emocionais que podem gerar instabilidade em decisões."
            })
        elif r_val >= 40:
            risks.append({
                "label": "Risco Moderado",
                "detail": "Algumas tendências emocionais que exigem monitoramento."
            })
        else:
            risks.append({
                "label": "Baixo Risco",
                "detail": "Boa estrutura emocional geral."
            })

        return risks

    # ------------------------------------------------------------
    # INSIGHT: CONTRADIÇÕES INTERNAS
    # ------------------------------------------------------------
    def detect_contradictions(self, big5, teique, performance) -> List[str]:
        contradictions = []

        # Exemplo: alta extroversão + baixo emocionality (TEIQue)
        if big5["extraversion"]["score"] >= 70 and teique["emotionality"]["score"] <= 40:
            contradictions.append(
                "Alta energia social com baixa consciência emocional (possíveis ruídos interpessoais)."
            )

        # Produtividade alta + organização baixa
        if performance["productivity"]["score"] >= 70 and performance["organization"]["score"] <= 40:
            contradictions.append(
                "Alta produtividade com baixa organização — risco de caos operacional."
            )

        if not contradictions:
            contradictions.append("Nenhuma contradição relevante identificada.")

        return contradictions

    # ------------------------------------------------------------
    # INSIGHT: RECOMENDAÇÕES
    # ------------------------------------------------------------
    def generate_recommendations(self, cross: Dict[str, Any]) -> List[str]:
        rec = []

        if cross["estabilidade_emocional"]["score"] < 50:
            rec.append("Desenvolver práticas de regulação emocional e pausas estruturadas.")

        if cross["expressividade_energia"]["score"] > 70:
            rec.append("Canalizar energia para projetos focados e metas específicas.")

        if cross["softskills_relacionais"]["score"] < 50:
            rec.append("Treinar escuta ativa e comunicação empática.")

        if cross["potencial_performance"]["score"] > 70:
            rec.append("Assumir responsabilidades estratégicas compatíveis com o potencial.")

        if not rec:
            rec.append("Perfil equilibrado — recomendações gerais de manutenção.")

        return rec

    # ------------------------------------------------------------
    # PACOTE MI COMPLETO
    # ------------------------------------------------------------
    def generate_mi_package(
        self,
        big5: Dict[str, Any],
        teique: Dict[str, Any],
        dass21: Dict[str, Any],
        ocai: Dict[str, Any],
        esquemas: Dict[str, Any],
        performance: Dict[str, Any],
        cross: Dict[str, Any],
        bussola: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Produz o MI Package completo — consumido por relatórios.
        """

        return {
            "quadrant": bussola["quadrant"],
            "coordinates": bussola["coordinates"],
            "style": bussola["style"],
            "risk_level": bussola["risk"]["level"],

            "talents": self.map_talents(cross),
            "risks": self.map_risks(cross),
            "contradictions": self.detect_contradictions(big5, teique, performance),
            "recommendations": self.generate_recommendations(cross),

            "metadata": {
                "sources": [
                    "big5", "teique", "dass21", "ocai",
                    "esquemas", "performance", "cruzamentos", "bussola"
                ],
                "mi_version": "3.1"
            }
        }


# Instância pública
mi_engine = MIEngine()
