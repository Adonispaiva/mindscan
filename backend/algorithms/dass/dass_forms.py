"""
DASS – FORMS ENGINE (Versão ULTRA SUPERIOR)
Estruturas de coleta, validação e normalização dos formulários
originais do DASS (não DASS21).
"""

from typing import List, Dict


class DASSForms:
    """
    Controlador das perguntas originais do DASS.
    Mantém compatibilidade com motores que utilizam versões clássicas.
    """

    QUESTIONS: Dict[str, List[str]] = {
        "stress": [
            "Dificuldade para relaxar?",
            "Sensação persistente de tensão física?",
            "Ficar facilmente irritado ou frustrado?",
            "Dificuldade em manter a calma sob pressão?"
        ],
        "anxiety": [
            "Sensação de medo ou pânico repentino?",
            "Preocupação intensa com possíveis ameaças?",
            "Tremores ou sinais de ativação corporal?",
            "Nervosismo antecipatório?"
        ],
        "depression": [
            "Perda de interesse nas coisas?",
            "Sensação de desânimo prolongado?",
            "Autoavaliação negativa frequente?",
            "Dificuldade em sentir prazer?"
        ]
    }

    def get_questions(self) -> Dict[str, List[str]]:
        """
        Retorna todas as perguntas do DASS clássico.
        """
        return self.QUESTIONS

    def build_form(self) -> List[Dict]:
        """
        Constrói formulário completo estruturado para motores externos.
        """
        form = []
        for domain, qlist in self.QUESTIONS.items():
            for q in qlist:
                form.append({
                    "domain": domain,
                    "question": q,
                    "type": "likert_0_3",
                    "required": True
                })
        return form
