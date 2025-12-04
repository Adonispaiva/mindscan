"""
CROSS ENGINE — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Motor central responsável por orquestrar dinamicamente todos
os módulos de cruzamentos do MindScan.

Este engine:

- identifica automaticamente quais módulos estão disponíveis
- executa apenas os cruzamentos compatíveis com os dados recebidos
- integra resultados em uma estrutura unificada de alto nível
- oferece telemetria de execução para auditoria técnica

Ele é o “cérebro operacional” do subsistema CRUZAMENTOS.
"""

from typing import Dict, Any

from .cross_big5_dass import CrossBig5DASS
from .cross_big5_egos import CrossBig5Egos
from .cross_big5_ocai import CrossBig5OCAI
from .cross_big5_performance import CrossBig5Performance
from .cross_big5_teique import CrossBig5Teique

from .cross_ocai_dass import CrossOCAIDASS
from .cross_ocai_egos import CrossOCAIEgos
from .cross_ocai_teique import CrossOCAITeique

from .cross_teique_big5 import CrossTeiqueBig5
from .cross_teique_dass import CrossTeiqueDASS
from .cross_teique_egos import CrossTeiqueEgos
from .cross_teique_esquemas import CrossTeiqueEsquemas

from .cross_strengths import CrossStrengths


class CrossEngine:
    def __init__(self):
        self.version = "2.0-ultra"

        # registro automático dos módulos
        self.modules = {
            "big5_dass": CrossBig5DASS(),
            "big5_egos": CrossBig5Egos(),
            "big5_ocai": CrossBig5OCAI(),
            "big5_perf": CrossBig5Performance(),
            "big5_teique": CrossBig5Teique(),

            "ocai_dass": CrossOCAIDASS(),
            "ocai_egos": CrossOCAIEgos(),
            "ocai_teique": CrossOCAITeique(),

            "teique_big5": CrossTeiqueBig5(),
            "teique_dass": CrossTeiqueDASS(),
            "teique_egos": CrossTeiqueEgos(),
            "teique_esquemas": CrossTeiqueEsquemas(),

            "strengths": CrossStrengths(),
        }

    def run(self, payload: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """
        payload:
            {
                "big5": {...},
                "teique": {...},
                "dass21": {...},
                "ocai": {...},
                "performance": {...},
                "egos": {...},
                "esquemas": {...},
                "strengths": {...}
            }
        """

        results = {}
        telemetry = {
            "executed": [],
            "skipped": [],
            "empty_inputs": [],
        }

        def has(*keys):
            return all(key in payload and payload[key] for key in keys)

        # BIG5 → DASS / OCAI / TEIQUE / PERFORMANCE / EGOS
        if has("big5", "dass21"):
            results["big5_dass"] = self.modules["big5_dass"].generate(payload["big5"], payload["dass21"])
            telemetry["executed"].append("big5_dass")
        else:
            telemetry["skipped"].append("big5_dass")

        if has("big5", "egos"):
            results["big5_egos"] = self.modules["big5_egos"].generate(payload["big5"], payload["egos"])
            telemetry["executed"].append("big5_egos")
        else:
            telemetry["skipped"].append("big5_egos")

        if has("big5", "ocai"):
            results["big5_ocai"] = self.modules["big5_ocai"].generate(payload["big5"], payload["ocai"])
            telemetry["executed"].append("big5_ocai")
        else:
            telemetry["skipped"].append("big5_ocai")

        if has("big5", "performance"):
            results["big5_performance"] = self.modules["big5_perf"].generate(payload["big5"], payload["performance"])
            telemetry["executed"].append("big5_performance")
        else:
            telemetry["skipped"].append("big5_performance")

        if has("big5", "teique"):
            results["big5_teique"] = self.modules["big5_teique"].generate(payload["big5"], payload["teique"])
            telemetry["executed"].append("big5_teique")
        else:
            telemetry["skipped"].append("big5_teique")

        # OCAI → DASS / EGOS / TEIQUE
        if has("ocai", "dass21"):
            results["ocai_dass"] = self.modules["ocai_dass"].generate(payload["ocai"], payload["dass21"])
            telemetry["executed"].append("ocai_dass")
        else:
            telemetry["skipped"].append("ocai_dass")

        if has("ocai", "egos"):
            results["ocai_egos"] = self.modules["ocai_egos"].generate(payload["ocai"], payload["egos"])
            telemetry["executed"].append("ocai_egos")
        else:
            telemetry["skipped"].append("ocai_egos")

        if has("ocai", "teique"):
            results["ocai_teique"] = self.modules["ocai_teique"].generate(payload["ocai"], payload["teique"])
            telemetry["executed"].append("ocai_teique")
        else:
            telemetry["skipped"].append("ocai_teique")

        # TEIQUE → BIG5 / DASS / EGOS / ESQUEMAS
        if has("teique", "big5"):
            results["teique_big5"] = self.modules["teique_big5"].generate(payload["teique"], payload["big5"])
            telemetry["executed"].append("teique_big5")
        else:
            telemetry["skipped"].append("teique_big5")

        if has("teique", "dass21"):
            results["teique_dass"] = self.modules["teique_dass"].generate(payload["teique"], payload["dass21"])
            telemetry["executed"].append("teique_dass")
        else:
            telemetry["skipped"].append("teique_dass")

        if has("teique", "egos"):
            results["teique_egos"] = self.modules["teique_egos"].generate(payload["teique"], payload["egos"])
            telemetry["executed"].append("teique_egos")
        else:
            telemetry["skipped"].append("teique_egos")

        if has("teique", "esquemas"):
            results["teique_esquemas"] = self.modules["teique_esquemas"].generate(payload["teique"], payload["esquemas"])
            telemetry["executed"].append("teique_esquemas")
        else:
            telemetry["skipped"].append("teique_esquemas")

        # Strengths (forças comportamentais)
        if "strengths" in payload and payload["strengths"]:
            results["strengths"] = self.modules["strengths"].generate(payload["strengths"], payload)
            telemetry["executed"].append("strengths")
        else:
            telemetry["skipped"].append("strengths")

        return {
            "module": "cross_engine",
            "version": self.version,
            "results": results,
            "telemetry": telemetry,
        }
