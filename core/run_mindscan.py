from datetime import datetime
from typing import Dict, Any

from core.algorithms import base_algorithm, advanced_algorithm


def run_mindscan(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pipeline principal do MindScan.
    Executa os algoritmos existentes e consolida os resultados.
    """

    results = {}

    # Algoritmo base
    results["base_analysis"] = base_algorithm.run(input_data)

    # Algoritmo avançado
    results["advanced_analysis"] = advanced_algorithm.run(input_data)

    # Metadados
    results["meta"] = {
        "executed_at": datetime.utcnow().isoformat(),
        "engine": "MindScan Core",
        "version": "MVP-REAL-1.0"
    }

    return results
