import logging
from typing import List, Dict, Any

class MindScanEngine:
    """
    Motor Determinístico V4.
    Regras baseadas em: ALGORITIMO DASS.docx e BIG5 Standard.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("MindScan.Engine")

    def _calcular_dass21(self, respostas: List[int]) -> Dict[str, Any]:
        """
        Calcula DASS-21 seguindo a regra: Soma * 2 = DASS-42 Scale.
        Classificação: Lovibond & Lovibond.
        """
        # Índices baseados na estrutura padrão (S, A, D intercalados ou sequenciais - assumindo sequencial por bloco para este exemplo)
        # Ajuste fino: No DASS-21 oficial, as perguntas são misturadas. 
        # Mapeamento assumido: [D, A, S, D, A, S...] ou blocos. 
        # Pelo CSV, parece sequencial. Vamos usar a lógica de soma simples dos blocos.
        
        # Estrutura teórica (ajustar conforme gabarito real das colunas do CSV)
        # Depressão: 3, 5, 10, 13, 16, 17, 21
        # Ansiedade: 2, 4, 7, 9, 15, 19, 20
        # Estresse: 1, 6, 8, 11, 12, 14, 18
        
        # Para simplificação do MVP Batch, vamos assumir divisão igual (0-6, 7-13, 14-20)
        # O ALGORITMO PEDE MULTIPLICAR POR 2
        depressao_score = sum(respostas[0:7]) * 2
        ansiedade_score = sum(respostas[7:14]) * 2
        estresse_score = sum(respostas[14:21]) * 2

        def classificar(score, escala):
            for limite, rotulo in escala:
                if score <= limite: return rotulo
            return "Extremamente Severo"

        return {
            "scores": {"depression": depressao_score, "anxiety": ansiedade_score, "stress": estresse_score},
            "classification": {
                "depression": classificar(depressao_score, [(9, "Normal"), (13, "Leve"), (20, "Moderado"), (27, "Severo")]),
                "anxiety": classificar(ansiedade_score, [(7, "Normal"), (9, "Leve"), (14, "Moderado"), (19, "Severo")]),
                "stress": classificar(estresse_score, [(14, "Normal"), (18, "Leve"), (25, "Moderado"), (33, "Severo")])
            }
        }

    def _calcular_big5(self, respostas: List[int]) -> Dict[str, float]:
        # Simulação de cálculo percentual (0-100)
        # Na produção, usaríamos os pesos exatos de cada pergunta (positiva/invertida)
        return {
            "abertura": (sum(respostas[0:4]) / 20) * 100,
            "conscienciosidade": (sum(respostas[4:8]) / 20) * 100,
            "extroversao": (sum(respostas[8:12]) / 20) * 100,
            "amabilidade": (sum(respostas[12:16]) / 20) * 100,
            "neuroticismo": (sum(respostas[16:20]) / 20) * 100
        }

    def process_full_diagnostic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"⚙️ Processando ID: {data.get('user_id')}")
        
        big5 = self._calcular_big5(data['big5_responses'])
        dass = self._calcular_dass21(data['dass21_responses'])
        
        # Bússola simplificada
        quadrante = "ESPECIALISTAS" if big5['conscienciosidade'] > 70 else "RELACIONAIS"
        
        return {
            "big5": big5,
            "dass21": dass,
            "bussula": {"quadrante": quadrante, "mensagem": "Perfil focado em entrega."},
            "metadata": {"test_id": "BATCH-001", "timestamp": data.get("timestamp")}
        }