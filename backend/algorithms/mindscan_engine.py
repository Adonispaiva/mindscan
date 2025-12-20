import logging
from typing import Dict, List, Any, Tuple
import numpy as np

logger = logging.getLogger("MindScan.Engine")

class MindScanEngine:
    """
    Motor Determinístico do MindScan.
    Responsável por realizar os cálculos psicométricos puros, isolados da camada de IA.
    """

    @staticmethod
    def _parse_likert(value: Any) -> int:
        """Converte strings '4. Concordo' ou '1- Completamente falso' em int 1-6"""
        try:
            # Tenta pegar o primeiro caractere se for string numérica
            return int(str(value)[0])
        except (ValueError, IndexError, TypeError):
            return 0

    @staticmethod
    def calculate_dass21(answers: List[int]) -> Dict[str, Any]:
        """
        Calcula o inventário DASS-21 (Depressão, Ansiedade, Estresse).
        Regra: (Soma dos 7 itens de cada escala) * 2.
        """
        if len(answers) != 21:
            logger.error(f"❌ DASS-21: Número de respostas inválido ({len(answers)})")
            return {"error": "Esperadas 21 respostas."}

        idx_depressao = [2, 4, 9, 12, 15, 16, 20] 
        idx_ansiedade = [1, 3, 6, 8, 14, 18, 19] 
        idx_estresse = [0, 5, 7, 10, 11, 13, 17]

        def get_score(indices):
            return sum(answers[i] for i in indices) * 2

        score_d = get_score(idx_depressao)
        score_a = get_score(idx_ansiedade)
        score_s = get_score(idx_estresse)

        return {
            "scores": {"depression": score_d, "anxiety": score_a, "stress": score_s},
            "classification": {
                "depression": MindScanEngine._classify_dass(score_d, "D"),
                "anxiety": MindScanEngine._classify_dass(score_a, "A"),
                "stress": MindScanEngine._classify_dass(score_s, "S")
            }
        }

    @staticmethod
    def calculate_big5(answers: List[int]) -> Dict[str, float]:
        """
        Calcula as 5 dimensões da personalidade (0-100%).
        Mapeamento baseado no formulário padrão MindScan.
        """
        # Mapeamento de grupos de itens (exemplo baseado na estrutura do CSV)
        mapping = {
            "extroversao": [0, 1, 2],
            "amabilidade": [4, 5, 6],
            "neuroticismo": [7, 8, 9, 10],
            "abertura": [11, 12, 13],
            "conscienciosidade": [15, 16, 17, 18]
        }
        
        results = {}
        for fator, indices in mapping.items():
            raw_sum = sum(answers[i] for i in indices if i < len(answers))
            max_score = len(indices) * 6
            results[fator] = round((raw_sum / max_score) * 100, 2)
        return results

    @staticmethod
    def calculate_teique(answers: List[int]) -> float:
        """Calcula o Score Global de Inteligência Emocional (0-100%)"""
        if not answers: return 0.0
        raw_avg = sum(answers) / len(answers)
        return round((raw_avg / 6) * 100, 2)

    @staticmethod
    def calculate_bussula(performance_score: float, matcher_score: float) -> Dict[str, str]:
        """
        Define o Quadrante na Bússola de Talentos.
        Ref: MINDSCAN_BUSSULA DE TALENTOS.docx
        """
        if performance_score >= 80 and matcher_score >= 80:
            return {"quadrante": "INSPIRADORES", "mensagem": "Talento e ambiente em sintonia total."}
        elif performance_score >= 80 and matcher_score < 80:
            return {"quadrante": "ESPECIALISTAS", "mensagem": "Entrega excepcional, foco em palco ideal."}
        elif performance_score < 80 and matcher_score >= 80:
            return {"quadrante": "PROMISSORES", "mensagem": "Fit cultural alto, acelerar performance."}
        else:
            return {"quadrante": "BUSCADORES", "mensagem": "Potencial em descoberta e transformação."}

    @staticmethod
    def _classify_dass(score: int, type: str) -> str:
        if type == "D":
            if score <= 9: return "Normal"
            if score <= 13: return "Leve"
            if score <= 20: return "Moderado"
            if score <= 27: return "Grave"
            return "Extremamente Grave"
        elif type == "A":
            if score <= 7: return "Normal"
            if score <= 9: return "Leve"
            if score <= 14: return "Moderado"
            if score <= 19: return "Grave"
            return "Extremamente Grave"
        elif type == "S":
            if score <= 14: return "Normal"
            if score <= 18: return "Leve"
            if score <= 25: return "Moderado"
            if score <= 33: return "Grave"
            return "Extremamente Grave"
        return "N/A"

    @staticmethod
    def process_full_diagnostic(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orquestrador de cálculos.
        data: Dicionário contendo listas de inteiros para cada teste.
        """
        # Cálculo dos Scores
        big5_scores = MindScanEngine.calculate_big5(data.get("big5_responses", []))
        teique_score = MindScanEngine.calculate_teique(data.get("teique_responses", []))
        
        # Matcher simplificado (média ponderada de Big5 e IE para liderança)
        matcher_score = (big5_scores.get("extroversao", 0) + teique_score) / 2
        perf_score = data.get("performance_raw", 75.0) # Default ou vindo do CSV (itens 72,73)

        results = {
            "metadata": {
                "user_id": data.get("user_id"),
                "timestamp": data.get("timestamp")
            },
            "dass21": MindScanEngine.calculate_dass21(data.get("dass21_responses", [])),
            "big5": big5_scores,
            "teique_global": teique_score,
            "bussula": MindScanEngine.calculate_bussula(perf_score, matcher_score),
            "scores_consolidated": {
                "performance": perf_score,
                "matcher": matcher_score
            }
        }
        return results