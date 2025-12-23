class MasterInsightService:
    """
    Camada MI (Master Insight).
    Responsável pela narrativa e textos do relatório.
    Baseado em: PERFIL_MI_SYNMINDSCAN_SEGURA.docx
    """
    
    def generate_narrative(self, diagnostic_results: dict) -> dict:
        """
        Gera os textos explicativos. 
        No MVP local (sem API Key), usa templates inteligentes.
        No futuro, chama OpenAI/Claude com o Prompt da Persona.
        """
        big5 = diagnostic_results.get('big5', {})
        quadrante = diagnostic_results.get('bussula', {}).get('quadrante')
        
        # Simulação de Texto Gerado (Template Dinâmico)
        resumo_executivo = (
            f"O candidato apresenta um perfil predominantemente {quadrante}. "
            f"Com destaque para Conscienciosidade ({int(big5.get('conscienciosidade',0))}%), "
            "indica forte aderência a processos e rigor operacional, crucial para o sucesso da franquia. "
        )
        
        pdi_sugestao = []
        if big5.get('neuroticismo', 0) > 60:
            pdi_sugestao.append("Fortalecer resiliência emocional sob pressão.")
        if big5.get('extroversao', 0) < 40:
            pdi_sugestao.append("Desenvolver comunicação ativa para liderança de equipe.")

        return {
            "executive_summary": resumo_executivo,
            "pdi_actions": pdi_sugestao,
            "tone": "Profissional, acolhedor e seguro (MI Persona)"
        }