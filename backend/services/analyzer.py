# D:\projetos-inovexa\mindscan\backend\services\analyzer.py

from typing import List

class Analyzer:
    def __init__(self, respostas: List[str]):
        self.respostas = respostas

    def diagnosticar(self):
        total = len(self.respostas)
        palavras_negativas = ["cansado", "ansioso", "deprimido", "triste", "desmotivado", "irritado"]
        score = 0

        for r in self.respostas:
            if any(p in r.lower() for p in palavras_negativas):
                score += 1

        risco = score / total if total else 0
        nivel = self.classificar(risco)
        dicas = self.gerar_dicas(nivel)

        return {
            "risco": risco,
            "nivel": nivel,
            "dicas": dicas,
        }

    def classificar(self, risco: float):
        if risco > 0.7:
            return "Alto"
        elif risco > 0.4:
            return "Moderado"
        else:
            return "Baixo"

    def gerar_dicas(self, nivel: str):
        match nivel:
            case "Alto":
                return [
                    "Considere buscar ajuda profissional imediatamente.",
                    "Evite o isolamento e mantenha contato com pessoas de confiança.",
                ]
            case "Moderado":
                return [
                    "Tente manter uma rotina regular de sono e alimentação.",
                    "Pratique exercícios físicos e reserve tempo para lazer.",
                ]
            case "Baixo":
                return [
                    "Continue com hábitos saudáveis.",
                    "Fique atento a mudanças no seu humor ou comportamento.",
                ]
            case _:
                return []
