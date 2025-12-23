import numpy as np

class MindScanEngine:
    @staticmethod
    def calcular_big5(respostas: list) -> dict:
        """
        Processa as 50 perguntas do Big Five (Likert 1-6).
        Assume que a lista 'respostas' contém os valores na ordem do teste.
        """
        if len(respostas) < 50:
            return {"error": "Dados insuficientes para Big Five"}
        
        # Mapeamento simplificado das 5 dimensões (exemplo de fatiamento)
        scores = {
            "Abertura": round(np.mean(respostas[0:10]), 2),
            "Conscienciosidade": round(np.mean(respostas[10:20]), 2),
            "Extroversão": round(np.mean(respostas[20:30]), 2),
            "Amabilidade": round(np.mean(respostas[30:40]), 2),
            "Neuroticismo": round(np.mean(respostas[40:50]), 2)
        }
        return scores

    @staticmethod
    def calcular_dass21(respostas: list) -> dict:
        """
        Processa as 21 perguntas do DASS-21 (Escala 1-6 adaptada para 0-3).
        Cálculo: (Soma dos itens da subescala) * 2.
        """
        if len(respostas) < 21:
            return {"error": "Dados insuficientes para DASS-21"}
        
        # Converte Likert 1-6 para escala DASS 0-3 (proporcionalmente)
        def ajustar_escala(val):
            if val <= 2: return 0
            if val <= 3: return 1
            if val <= 5: return 2
            return 3

        ajustadas = [ajustar_escala(v) for v in respostas]
        
        # Fatiamento conforme protocolo Lovibond
        depressao = sum(ajustadas[0:7]) * 2
        ansiedade = sum(ajustadas[7:14]) * 2
        estresse = sum(ajustadas[14:21]) * 2

        return {
            "depressao": {"score": depressao, "classificacao": MindScanEngine._nivel_dass(depressao, "dep")},
            "ansiedade": {"score": ansiedade, "classificacao": MindScanEngine._nivel_dass(ansiedade, "ans")},
            "estresse": {"score": estresse, "classificacao": MindScanEngine._nivel_dass(estresse, "est")}
        }

    @staticmethod
    def _nivel_dass(score, tipo):
        if tipo == "dep":
            if score <= 9: return "Normal"
            if score <= 13: return "Leve"
            if score <= 20: return "Moderado"
            return "Severo"
        # ... (lógica similar para ans e est conforme ALGORITIMO DASS.docx)
        return "Analisar"