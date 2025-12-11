# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\mi_engine_hybrid.py
# Última atualização: 2025-12-11T09:59:20.815001

# ============================================================
# MindScan — MI Engine Hybrid (Motor Híbrido Definitivo)
# ============================================================
# Integra:
# - MIEngine (clássico)
# - MIEngineAdvanced (avançado)
# - MI SynMind (persona, reasoning, normalizer, formatter, validator)
#
# Modo operacional:
#   classic       → usa apenas MIEngine
#   advanced      → usa MIEngineAdvanced
#   synmind       → usa MI SynMind
#   hybrid_auto   → usa heurística para escolher o melhor
#
# Este módulo é o núcleo da fusão MI.
# ============================================================

from typing import Dict, Any

from .mi_engine import MIEngine
from .mi_engine_advanced import MIEngineAdvanced

# Camada MI SynMind
from backend.mi.mi_normalizer import mi_normalizer
from backend.mi.mi_sanitizer import MISanitizer
from backend.mi.mi_formatter import mi_formatter
from backend.mi.mi_validator import MIValidator
from backend.mi.persona.persona_core import PersonaCore
from backend.mi.mi_reasoning import MIReasoning


class MIEngineHybrid:

    def __init__(self):
        # Motores originais
        self.engine_classic = MIEngine()
        self.engine_advanced = MIEngineAdvanced()

        # Núcleo SynMind
        self.persona = PersonaCore()
        self.normalizer = mi_normalizer
        self.reasoner = MIReasoning()
        self.sanitizer = MISanitizer()
        self.formatter = mi_formatter
        self.validator = MIValidator()

    # ------------------------------------------------------------
    # MODO DE EXECUÇÃO
    # ------------------------------------------------------------
    def compute(self, payload: Dict[str, Any], mode: str = "hybrid_auto") -> Dict[str, Any]:

        mode = mode.lower().strip()

        if mode == "classic":
            return self._run_classic(payload)

        elif mode == "advanced":
            return self._run_advanced(payload)

        elif mode == "synmind":
            return self._run_synmind(payload)

        elif mode == "hybrid_auto":
            return self._run_hybrid_auto(payload)

        else:
            raise ValueError(f"Modo MI desconhecido: {mode}")

    # ------------------------------------------------------------
    # MODOS INDIVIDUAIS
    # ------------------------------------------------------------
    def _run_classic(self, payload: Dict[str, Any]):
        return {
            "engine": "classic",
            "result": self.engine_classic.compute_mi(payload),
        }

    def _run_advanced(self, payload: Dict[str, Any]):
        return {
            "engine": "advanced",
            "result": self.engine_advanced.compute(payload),
        }

    def _run_synmind(self, payload: Dict[str, Any]):
        return self._execute_synmind_pipeline(payload)

    # ------------------------------------------------------------
    # PIPELINE HYBRID AUTO
    # ------------------------------------------------------------
    def _run_hybrid_auto(self, payload: Dict[str, Any]):
        """
        Estratégia híbrida:
        - Se performance ou cross tiverem variância alta → advanced
        - Se bussola + personalidade estiverem completos → synmind
        - Caso contrário → classic
        """
        try:
            perf = payload.get("performance", {})
            cross = payload.get("cross", {})
            bussola = payload.get("bussola", {})

            variance_perf = sum(abs(v.get("score", 0)) for v in perf.values())
            variance_cross = sum(abs(v.get("score", 0)) for v in cross.values())
            bussola_ok = len(bussola.keys()) > 5

            if variance_perf + variance_cross > 200:
                return self._run_advanced(payload)
            elif bussola_ok:
                return self._run_synmind(payload)
            else:
                return self._run_classic(payload)

        except Exception:
            # fallback seguro
            return self._run_classic(payload)

    # ------------------------------------------------------------
    # PIPELINE SYNMIND COMPLETO
    # ------------------------------------------------------------
    def _execute_synmind_pipeline(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        # 1. Normalização unificada
        normalized = self.normalizer.normalize_all(
            payload.get("big5", {}),
            payload.get("teique", {}),
            payload.get("dass21", {}),
            payload.get("ocai", {}),
            payload.get("esquemas", {}),
            payload.get("performance", {}),
            payload.get("cross", {}),
            payload.get("bussola", {}),
        )

        # 2. Persona aplicada
        persona_block = self.persona.build()

        # 3. Raciocínio inferencial
        reasoning_block = self.reasoner.infer(normalized)

        # 4. Sanitização pré-validação
        raw_mi_structure = {
            "metadata": {
                "engine_version": "hybrid.1.0",
                "created_at": "AUTO"
            },
            "persona": {
                "core": persona_block,
                "style": {"temperature": 0.65},
                "voice": {"tone": "analytical"}
            },
            "normalized": normalized,
            "reasoning": {
                "chain": [
                    {"step": 1, "conclusion": "Análise inicial dos blocos."},
                    {"step": 2, "conclusion": "Consolidação dos padrões psicométricos."},
                    {"step": 3, "conclusion": "Síntese interpretativa final."},
                ],
                "depth": 3,
                "evidence": []
            },
            "insights": reasoning_block
        }

        cleaned = self.sanitizer.clean(raw_mi_structure)

        # 5. Validação completa MI SynMind
        result = self.validator.validate(cleaned)

        return {
            "engine": "synmind",
            "valid": result.is_valid,
            "errors": result.errors,
            "warnings": result.warnings,
            "payload": result.cleaned_payload,
            "formatted": result.formatted_payload
        }
