import logging
from typing import Dict, Any

# ⚓ TRUTH_ANCHOR_MINDSCAN: Identidade Fixa SynMind
logger = logging.getLogger("NarrativeEngine")

class NarrativeEngine:
    """
    Engine de Interpretação MI (Mental Intelligence).
    Transforma scores determinísticos em narrativas profissionais PhD.
    """
    
    def __init__(self, mode: str = "segura"):
        self.mode = mode
        self.identity = "PhD multidisciplinar em Psicologia e Gestão"

    def generate(self, scores: Dict[str, Any], report_type: str = "executive") -> str:
        """Gera o texto interpretativo com base nos quadrantes da Bússola."""
        bussola = scores.get("bussola", {})
        quadrante = bussola.get("label", "BUSCADORES")
        
        # Base de conhecimento para a reunião (Narrativa padrão SynMind)
        narrative_base = {
            "INSPIRADORES": "Perfil de alta aderência cultural e performance excepcional. Mobiliza pelo vínculo e inspira pela confiança.",
            "ESPECIALISTAS": "Domínio técnico sólido. O desafio é a sintonia fina com a cultura para evitar o isolamento estratégico.",
            "PROMISSORES": "Grande fit cultural. O foco agora deve ser o desenvolvimento de assertividade para converter potencial em resultado.",
            "BUSCADORES": "Fase de transição e descoberta. Necessita de clareza de propósito para destravar talentos latentes."
        }
        
        intro = f"Análise baseada no perfil {self.identity}. "
        body = narrative_base.get(quadrante, "")
        
        if report_type == "premium":
            body += self._get_deep_insight(scores)
            
        return f"{intro} {body}"

    def _get_deep_insight(self, scores: Dict) -> str:
        # Lógica para relatórios Premium (Cruzamento DASS-21 x BIG5)
        dass = scores.get("dass21", {})
        if dass.get("anxiety", {}).get("level") == "Elevado":
            return " Atenção: O estado atual apresenta picos de ansiedade que podem mascarar a performance real. Recomenda-se suporte imediato."
        return ""