class MindMatcher:
    """
    Calcula o 'Fit' cultural e técnico (MindMatch).
    Baseado nos documentos 'CNA_FEEDBACK' e 'SUCÃO'.
    """
    
    # Perfil Benchmark (O "Alvo")
    IDEAL_PROFILE = {
        "extroversao": 75.0,      # Vendas e Liderança
        "conscienciosidade": 80.0,# Processos e Gestão
        "amabilidade": 60.0,      # Bom trato, mas firmeza
        "abertura": 65.0,         # Inovação moderada
        "neuroticismo": 30.0      # Baixa ansiedade (Resiliência alta)
    }

    @staticmethod
    def calculate_match_score(candidate_big5: dict) -> float:
        """
        Retorna um score de 0 a 100% de aderência ao perfil ideal.
        Usa distância ponderada invertida.
        """
        diff_sum = 0
        weights_sum = 0
        
        weights = {
            "extroversao": 1.5,      # Peso alto para franqueado
            "conscienciosidade": 2.0,# Peso crítico (gestão)
            "amabilidade": 1.0,
            "abertura": 1.0,
            "neuroticismo": 1.5      # Importante ter controle emocional
        }

        for trait, ideal_val in MindMatcher.IDEAL_PROFILE.items():
            # Pega o valor do candidato (padrão 50 se não existir)
            real_val = candidate_big5.get(trait, 50.0)
            weight = weights.get(trait, 1.0)
            
            # Diferença absoluta
            diff = abs(ideal_val - real_val)
            
            # Penalidade normalizada (máx diff é 100)
            weighted_diff = diff * weight
            
            diff_sum += weighted_diff
            weights_sum += weight * 100 # O máximo de diferença possível ponderada

        # Match Score = 100% - (Erro acumulado / Erro máximo possível)
        match_percentage = 100 * (1 - (diff_sum / weights_sum))
        
        # Ajuste para não penalizar demais (Curva de calibração)
        return max(0.0, min(100.0, match_percentage))