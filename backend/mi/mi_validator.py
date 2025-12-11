# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_validator.py
# Última atualização: 2025-12-11T09:59:20.872348

"""
MI Validator — Validador final do módulo Mind Intelligence (MI)

Este componente garante que toda a estrutura MI gerada pelo pipeline 
(metadados, identidade, raciocínio, style, voice, persona, contextos e 
respostas finais) esteja consistente, completa, coerente e de acordo com 
as políticas internas do MindScan.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ValidationError

from .mi_formatter import MIFormatter
from .mi_sanitizer import MISanitizer
from .mi_structurer import MIStructurer


class MIValidationResult(BaseModel):
    """Objeto final retornado após validação completa."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    cleaned_payload: Optional[Dict[str, Any]] = None
    formatted_payload: Optional[str] = None


class MIValidator:
    """
    Validador completo do MI.
    Realiza:
        - Verificação estrutural
        - Sanitização de conteúdo
        - Verificação de campos obrigatórios
        - Garantias de coerência interna
        - Formatação final padronizada
    """

    REQUIRED_KEYS = {
        "persona": ["core", "style", "voice"],
        "reasoning": ["chain", "depth", "evidence"],
        "metadata": ["created_at", "engine_version"],
    }

    def __init__(self):
        self.structurer = MIStructurer()
        self.sanitizer = MISanitizer()
        self.formatter = MIFormatter()

    # ---------------------- VALIDATIONS ----------------------

    def validate_structure(self, payload: Dict[str, Any], errors: List[str]):
        """Garante que as chaves essenciais existem."""
        for section, required_fields in self.REQUIRED_KEYS.items():
            if section not in payload:
                errors.append(f"Seção obrigatória ausente: {section}")
                continue

            for field in required_fields:
                if field not in payload.get(section, {}):
                    errors.append(f"Campo obrigatório ausente em '{section}': {field}")

    def validate_reasoning_logic(self, payload: Dict[str, Any], errors: List[str]):
        """Valida coerência interna da cadeia de raciocínio."""
        reasoning = payload.get("reasoning", {})
        chain = reasoning.get("chain", [])

        if not isinstance(chain, list) or len(chain) < 3:
            errors.append("Cadeia de raciocínio insuficiente — mínimo de 3 passos.")

        # Verifica progressão lógica
        for i in range(len(chain) - 1):
            if chain[i].get("conclusion") is None:
                errors.append(f"Passo {i} da cadeia carece de conclusão explícita.")

    def validate_persona_consistency(self, payload: Dict[str, Any], errors: List[str]):
        """Valida coerência interna da persona."""
        persona = payload.get("persona", {})
        style = persona.get("style", {})
        voice = persona.get("voice", {})

        if style.get("temperature") is None:
            errors.append("Persona.style.temperature não pode ser vazio.")

        if voice.get("tone") not in ["formal", "neutral", "casual", "analytical"]:
            errors.append("Persona.voice.tone inválido ou ausente.")

    # ---------------------- MASTER VALIDATOR ----------------------

    def validate(self, payload: Dict[str, Any]) -> MIValidationResult:
        """Executa toda a cadeia de validação."""

        errors = []
        warnings = []

        # 1. Sanitização
        cleaned = self.sanitizer.clean(payload)

        # 2. Estrutura
        self.validate_structure(cleaned, errors)

        # 3. Lógica de raciocínio
        self.validate_reasoning_logic(cleaned, errors)

        # 4. Persona
        self.validate_persona_consistency(cleaned, errors)

        # 5. Reestruturação final
        structured = self.structurer.organize(cleaned)

        # 6. Formatação final
        formatted = self.formatter.format(structured)

        return MIValidationResult(
            is_valid=(len(errors) == 0),
            errors=errors,
            warnings=warnings,
            cleaned_payload=structured,
            formatted_payload=formatted
        )


# ---------------------- EXECUTION ----------------------

if __name__ == "__main__":
    sample = {
        "metadata": {"created_at": "2025-12-05", "engine_version": "1.0.0"},
        "persona": {"core": {}, "style": {"temperature": 0.7}, "voice": {"tone": "neutral"}},
        "reasoning": {
            "chain": [
                {"step": 1, "conclusion": "A"},
                {"step": 2, "conclusion": "B"},
                {"step": 3, "conclusion": "C"},
            ],
            "depth": 3,
            "evidence": []
        },
    }

    validator = MIValidator()
    result = validator.validate(sample)
    print(result.json(indent=4, ensure_ascii=False))
