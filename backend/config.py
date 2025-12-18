from typing import Dict, Any


def build_dataset_from_answers(answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constrói o dataset unificado para o MindScanEngine
    a partir das respostas brutas armazenadas no banco.

    Este método é propositalmente tolerante:
    - Não exige blocos específicos
    - Permite evolução incremental dos algoritmos
    """

    if not isinstance(answers, dict):
        raise ValueError("Answers inválidas. Deve ser um dicionário.")

    dataset = {
        "raw_answers": answers,
    }

    return dataset
