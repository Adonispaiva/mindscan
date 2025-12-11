# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\engine_service.py
# Última atualização: 2025-12-11T09:59:21.089476

# Caminho: backend/services/engine_service.py
# MindScan Backend — Engine Service (Orquestrador Central da MI)
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão Final — MindScan v2.0

"""
Engine oficial do MindScan.
Responsável por centralizar todo o processamento psicométrico
conforme o BOOT-SPEC e a especificação SynMind v2.0.

Fluxo:
1) Recebe dataset preparado pelo DataService
2) Dispara os módulos psicométricos:
   - Big Five
   - TEIQUE
   - OCAI
   - DASS-21
   - Esquemas (Early Maladaptive Schemas)
   - Performance
   - Matcher
   - Cruzamento de perfis
   - Bússola MindScan
3) Agrega todas as dimensões
4) Produz estrutura unificada para persistência no banco:
   [
       {
           "dimension": str,
           "score": float,
           "descriptor": str,
           "metadata": dict,
       },
       ...
   ]

Cada módulo psicométrico deve ser implementado de forma modular
em backend/algorithms/.

Esta versão do Engine define o orquestrador e o protocolo de saída.
Os algoritmos podem ser substituídos/expandido sem quebrar o contrato.
"""

from datetime import datetime

# Placeholders para import real dos módulos psicométricos
try:
    from backend.algorithms.big5 import big5_process
except Exception:
    big5_process = None

try:
    from backend.algorithms.teique import teique_process
except Exception:
    teique_process = None

try:
    from backend.algorithms.ocai import ocai_process
except Exception:
    ocai_process = None

try:
    from backend.algorithms.dass21 import dass21_process
except Exception:
    dass21_process = None

try:
    from backend.algorithms.schemas import schema_process
except Exception:
    schema_process = None

try:
    from backend.algorithms.performance import performance_process
except Exception:
    performance_process = None

try:
    from backend.algorithms.matcher import matcher_process
except Exception:
    matcher_process = None

try:
    from backend.algorithms.crossmap import crossmap_process
except Exception:
    crossmap_process = None

try:
    from backend.algorithms.compass import compass_process
except Exception:
    compass_process = None


class MindScanEngine:
    """Orquestrador central do MindScan."""

    @staticmethod
    def process(dataset: dict) -> list:
        """
        Recebe o dataset já validado pelo DataService.

        Retorna lista padronizada de dimensões psicométricas.
        """

        results = []

        # =============================================================
        # 1) BIG FIVE
        # =============================================================
        if big5_process:
            out = big5_process(dataset)
            results.extend(MindScanEngine._normalize("big5", out))
        else:
            results.append(MindScanEngine._missing_block("big5"))

        # =============================================================
        # 2) TEIQUE
        # =============================================================
        if teique_process:
            out = teique_process(dataset)
            results.extend(MindScanEngine._normalize("teique", out))
        else:
            results.append(MindScanEngine._missing_block("teique"))

        # =============================================================
        # 3) OCAI
        # =============================================================
        if ocai_process:
            out = ocai_process(dataset)
            results.extend(MindScanEngine._normalize("ocai", out))
        else:
            results.append(MindScanEngine._missing_block("ocai"))

        # =============================================================
        # 4) DASS-21
        # =============================================================
        if dass21_process:
            out = dass21_process(dataset)
            results.extend(MindScanEngine._normalize("dass21", out))
        else:
            results.append(MindScanEngine._missing_block("dass21"))

        # =============================================================
        # 5) ESQUEMAS
        # =============================================================
        if schema_process:
            out = schema_process(dataset)
            results.extend(MindScanEngine._normalize("schemas", out))
        else:
            results.append(MindScanEngine._missing_block("schemas"))

        # =============================================================
        # 6) PERFORMANCE
        # =============================================================
        if performance_process:
            out = performance_process(dataset)
            results.extend(MindScanEngine._normalize("performance", out))
        else:
            results.append(MindScanEngine._missing_block("performance"))

        # =============================================================
        # 7) MATCHER
        # =============================================================
        if matcher_process:
            out = matcher_process(dataset)
            results.extend(MindScanEngine._normalize("matcher", out))
        else:
            results.append(MindScanEngine._missing_block("matcher"))

        # =============================================================
        # 8) CROSSMAP
        # =============================================================
        if crossmap_process:
            out = crossmap_process(dataset)
            results.extend(MindScanEngine._normalize("crossmap", out))
        else:
            results.append(MindScanEngine._missing_block("crossmap"))

        # =============================================================
        # 9) COMPASS (BÚSSOLA MINDSCAN)
        # =============================================================
        if compass_process:
            out = compass_process(dataset)
            results.extend(MindScanEngine._normalize("compass", out))
        else:
            results.append(MindScanEngine._missing_block("compass"))

        return results

    # =============================================================
    # NORMALIZAÇÃO DE SAÍDA
    # =============================================================
    @staticmethod
    def _normalize(module: str, output) -> list:
        """
        Normaliza a saída de cada módulo psicométrico.

        Cada módulo deve retornar uma lista ou dict no seguinte formato:
        {
            "dimension": str,
            "score": float,
            "descriptor": str,
            "metadata": dict
        }
        """
        if output is None:
            return [MindScanEngine._missing_block(module)]

        normalized = []

        if isinstance(output, dict):
            # single dimension
            normalized.append({
                "dimension": output.get("dimension", module),
                "score": float(output.get("score", 0)),
                "descriptor": output.get("descriptor", ""),
                "metadata": output.get("metadata", {}),
            })

        elif isinstance(output, list):
            for item in output:
                normalized.append({
                    "dimension": item.get("dimension", module),
                    "score": float(item.get("score", 0)),
                    "descriptor": item.get("descriptor", ""),
                    "metadata": item.get("metadata", {}),
                })

        return normalized

    # =============================================================
    # BLOCO DE FALTA (ALGORITMO NÃO IMPLEMENTADO)
    # =============================================================
    @staticmethod
    def _missing_block(module: str) -> dict:
        return {
            "dimension": f"{module}_missing",
            "score": 0.0,
            "descriptor": f"O módulo {module} não está implementado.",
            "metadata": {"timestamp": datetime.utcnow().isoformat()},
        }