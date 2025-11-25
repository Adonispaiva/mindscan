from typing import Dict, Any


class NLPProcessor:
    """
    Processador NLP simplificado.
    A versão 2.0 permite futura expansão para:
    - análise semântica de notas
    - extração de sentimentos
    - extração de palavras-chave
    - sumarização curta do candidato
    """

    def process(self, dataset: Dict[str, Any]) -> Dict[str, Any]:

        notes = dataset.get("candidate", {}).get("notes")

        nlp_output = {}

        if notes:
            # Processamento simplificado — placeholder
            nlp_output = {
                "keywords": self.extract_keywords(notes),
                "sentiment": self.analyze_sentiment(notes)
            }

        dataset_with_nlp = dataset.copy()
        dataset_with_nlp["nlp"] = nlp_output
        return dataset_with_nlp

    # ------------------------------------------------------------
    #  Métodos NLP — placeholders até integração com modelos reais
    # ------------------------------------------------------------
    @staticmethod
    def extract_keywords(text: str) -> list:
        # Futuro: aplicar modelos de Keyword Extraction
        words = text.split()
        return [w.lower() for w in words if len(w) > 5]

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        # Futuro: integrar com análise de sentimento real
        text_lower = text.lower()
        if any(x in text_lower for x in ["bom", "ótimo", "excelente", "positivo"]):
            return "positive"
        if any(x in text_lower for x in ["ruim", "péssimo", "negativo", "horrível"]):
            return "negative"
        return "neutral"