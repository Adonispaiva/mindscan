from datetime import datetime

try:
    from backend.algorithms.big5 import big5_process
except Exception:
    big5_process = None

try:
    from backend.algorithms.hogan import hogan_process
except Exception:
    hogan_process = None

try:
    from backend.algorithms.values import values_process
except Exception:
    values_process = None

try:
    from backend.algorithms.ocai import ocai_process
except Exception:
    ocai_process = None

try:
    from backend.algorithms.dass21 import dass21_process
except Exception:
    dass21_process = None

try:
    from backend.algorithms.shadow import shadow_process
except Exception:
    shadow_process = None

try:
    from backend.algorithms.matcher import matcher_process
except Exception:
    matcher_process = None

try:
    from backend.algorithms.crossmap import crossmap_process
except Exception:
    crossmap_process = None

try:
    from backend.algorithms.bussola import bussola_process
except Exception:
    bussola_process = None

try:
    from backend.algorithms.compass import compass_process
except Exception:
    compass_process = None


class MindScanEngine:
    """Orquestrador central do MindScan."""

    @staticmethod
    def process(dataset: dict) -> list:
        results = []

        if big5_process:
            results.extend(MindScanEngine._normalize("big5", big5_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("big5"))

        if hogan_process:
            results.extend(MindScanEngine._normalize("hogan", hogan_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("hogan"))

        if ocai_process:
            results.extend(MindScanEngine._normalize("ocai", ocai_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("ocai"))

        if dass21_process:
            results.extend(MindScanEngine._normalize("dass21", dass21_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("dass21"))

        if values_process:
            results.extend(MindScanEngine._normalize("values", values_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("values"))

        if shadow_process:
            results.extend(MindScanEngine._normalize("shadow", shadow_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("shadow"))

        if matcher_process:
            results.extend(MindScanEngine._normalize("matcher", matcher_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("matcher"))

        if crossmap_process:
            results.extend(MindScanEngine._normalize("crossmap", crossmap_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("crossmap"))

        if bussola_process:
            results.extend(MindScanEngine._normalize("bussola", bussola_process(dataset)))
        elif compass_process:
            results.extend(MindScanEngine._normalize("compass", compass_process(dataset)))
        else:
            results.append(MindScanEngine._missing_block("bussola"))

        return results

    @staticmethod
    def _normalize(module: str, output) -> list:
        normalized = []

        if output is None:
            return normalized

        if isinstance(output, dict):
            output = [output]

        if isinstance(output, list):
            for item in output:
                if not isinstance(item, dict):
                    continue
                normalized.append({
                    "dimension": item.get("dimension") or f"{module}_dimension",
                    "score": float(item.get("score") or 0.0),
                    "descriptor": item.get("descriptor") or f"Resultado do módulo {module}",
                    "metadata": item.get("metadata") or {
                        "timestamp": datetime.utcnow().isoformat(),
                        "module": module,
                    },
                })

        return normalized

    @staticmethod
    def _missing_block(module: str) -> dict:
        return {
            "dimension": f"{module}_missing",
            "score": 0.0,
            "descriptor": f"O módulo {module} não está implementado.",
            "metadata": {"timestamp": datetime.utcnow().isoformat()},
        }


# ============================================================
# FUNÇÃO DE FACHADA (COMPATIBILIDADE COM diagnostic_service)
# ============================================================

def run_mindscan_engine(dataset: dict) -> list:
    return MindScanEngine.process(dataset)
