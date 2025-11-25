# ============================================================
# MindScan — MI Formatter
# ============================================================
# O MI Formatter converte os resultados do MI Engine em texto
# estruturado, limpo e padronizado para uso em:
# - Relatórios (PDF)
# - API
# - Dashboards
# - Interfaces cliente
#
# Funções:
# - formatação de talentos
# - formatação de riscos
# - formatação de contradições
# - formatação de recomendações
# - estrutura textual final
#
# Versão completa, maximizada e definitiva.
# ============================================================

from typing import Dict, Any, List


class MIFormatter:
    """
    Formata o MI Package em blocos textuais prontos
    para exibição, exportação ou consumo API.
    """

    # ------------------------------------------------------------
    # TALENTOS
    # ------------------------------------------------------------
    def format_talents(self, talents: List[Dict[str, Any]]) -> str:
        lines = ["TALENTOS DOMINANTES:"]
        for t in talents:
            lines.append(f"- {t['label']}: {t['strength']}")
        return "\n".join(lines)

    # ------------------------------------------------------------
    # RISCOS
    # ------------------------------------------------------------
    def format_risks(self, risks: List[Dict[str, Any]]) -> str:
        lines = ["FRAGILIDADES POTENCIAIS:"]
        for r in risks:
            lines.append(f"- {r['label']}: {r['detail']}")
        return "\n".join(lines)

    # ------------------------------------------------------------
    # CONTRADIÇÕES
    # ------------------------------------------------------------
    def format_contradictions(self, contradictions: List[str]) -> str:
        lines = ["CONTRADIÇÕES INTERNAS:"]
        for c in contradictions:
            lines.append(f"- {c}")
        return "\n".join(lines)

    # ------------------------------------------------------------
    # RECOMENDAÇÕES
    # ------------------------------------------------------------
    def format_recommendations(self, rec: List[str]) -> str:
        lines = ["RECOMENDAÇÕES:"]
        for r in rec:
            lines.append(f"- {r}")
        return "\n".join(lines)

    # ------------------------------------------------------------
    # FORMATAÇÃO GERAL (PACOTE MI)
    # ------------------------------------------------------------
    def format_package(self, mi_package: Dict[str, Any]) -> Dict[str, str]:
        """
        Retorna blocos formatados em texto.
        """

        return {
            "quadrant": f"Quadrante: {mi_package['quadrant']}",
            "coordinates": f"Coordenadas: X={mi_package['coordinates']['x']} | Y={mi_package['coordinates']['y']}",
            "style": f"Estilo: {mi_package['style']}",
            "risk_level": f"Nível de risco: {mi_package['risk_level']}",

            "talents": self.format_talents(mi_package["talents"]),
            "risks": self.format_risks(mi_package["risks"]),
            "contradictions": self.format_contradictions(mi_package["contradictions"]),
            "recommendations": self.format_recommendations(mi_package["recommendations"]),
        }


# Instância pública
mi_formatter = MIFormatter()
