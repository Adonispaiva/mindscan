# esquemas.py
# MindScan Rebuild – Algoritmo de Esquemas (Schema Model – Young)
# Versão Final e Definitiva
# Autor: Leo Vinci – IA Supervisora Inovexa
# Última atualização: 23/11/2025
# ------------------------------------------------------------------------
# Este módulo implementa a estrutura completa dos 18 esquemas iniciais
# desadaptativos (Young Schema Questionnaire – versão compactada MindScan):
#
# Domínio 1 — Desconexão e Rejeição
#   - Abandono
#   - Desconfiança/Abuso
#   - Privação Emocional
#   - Defectividade/Vergonha
#   - Isolamento Social
#
# Domínio 2 — Autonomia e Desempenho Prejudicados
#   - Dependência/Incompetência
#   - Vulnerabilidade
#   - Emaranhamento
#   - Fracasso
#
# Domínio 3 — Limites Prejudicados
#   - Grandiosidade
#   - Autocontrole/Autodisciplina Insuficientes
#
# Domínio 4 — Direcionamento para o Outro
#   - Subjugação
#   - Autossacrifício
#   - Busca de Aprovação
#
# Domínio 5 — Supervigília e Inibição
#   - Negatividade/Pessimismo
#   - Inibição Emocional
#   - Padrões Inflexíveis
#   - Postura Punitiva
#
# Pontuação:
#   Likert 1–6
# Normalização final: 0–100
#
# Saída padronizada: Modelo MindScan – Esquemas
# ------------------------------------------------------------------------

from typing import Dict, Any


class SchemaModel:
    SCHEMAS = {
        # Domínio 1 — Desconexão e Rejeição
        "AB": "Abandono",
        "DA": "Desconfiança/Abuso",
        "PE": "Privação Emocional",
        "DV": "Defectividade/Vergonha",
        "IS": "Isolamento Social",

        # Domínio 2 — Autonomia e Desempenho Prejudicados
        "DI": "Dependência/Incompetência",
        "VU": "Vulnerabilidade",
        "EM": "Emaranhamento",
        "FR": "Fracasso",

        # Domínio 3 — Limites Prejudicados
        "GR": "Grandiosidade",
        "AI": "Autocontrole/Autodisciplina Insuficientes",

        # Domínio 4 — Direcionamento para o Outro
        "SU": "Subjugação",
        "AS": "Autossacrifício",
        "BA": "Busca de Aprovação",

        # Domínio 5 — Supervigília e Inibição
        "NP": "Negatividade/Pessimismo",
        "IE": "Inibição Emocional",
        "PI": "Padrões Inflexíveis",
        "PU": "Postura Punitiva"
    }

    DOMAINS = {
        "DesconexaoRejeicao": ["AB", "DA", "PE", "DV", "IS"],
        "AutonomiaPrejudicada": ["DI", "VU", "EM", "FR"],
        "LimitesPrejudicados": ["GR", "AI"],
        "DirecionamentoOutro": ["SU", "AS", "BA"],
        "SupervigilanciaInibicao": ["NP", "IE", "PI", "PU"]
    }

    MIN_SCORE = 1
    MAX_SCORE = 6

    NORMALIZATION_RANGE = (0, 100)

    DESCRIPTIONS = {
        "AB": "Medo de abandono e instabilidade nos vínculos.",
        "DA": "Expectativa de abuso, engano ou danos.",
        "PE": "Percepção de falta de carinho, apoio ou empatia.",
        "DV": "Sentimentos de vergonha, inferioridade e inadequação.",
        "IS": "Sentir-se diferente, isolado ou não pertencente.",
        "DI": "Dependência excessiva, sensação de incapacidade.",
        "VU": "Medo intenso de desastres, doenças e perda de controle.",
        "EM": "Fusão emocional, perda de identidade individual.",
        "FR": "Convicção de fracasso ou incompetência.",
        "GR": "Sensação de superioridade, regras não aplicáveis.",
        "AI": "Dificuldade em autocontrole e autodisciplina.",
        "SU": "Submissão, medo de retaliação e supressão da autonomia.",
        "AS": "Excesso de altruísmo e autocancelamento.",
        "BA": "Busca constante de aprovação e validação.",
        "NP": "Foco no negativo, medo excessivo do futuro.",
        "IE": "Supressão emocional significativa.",
        "PI": "Perfeccionismo rígido e padrões impossíveis.",
        "PU": "Autocrítica punitiva e intolerância."
    }

    def __init__(self, responses: Dict[str, int]):
        self.responses = responses
        self._validate_inputs()

    # ---------------------------------------------------------
    # Validação completa
    # ---------------------------------------------------------

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("responses deve ser um dicionário.")

        for code, score in self.responses.items():
            if code not in self.SCHEMAS:
                raise ValueError(f"Esquema inválido: {code}")
            if not isinstance(score, int):
                raise ValueError(f"Pontuação inválida em {code}: {score}")
            if not (self.MIN_SCORE <= score <= self.MAX_SCORE):
                raise ValueError(f"Pontuação fora do permitido: {code}={score}")

    # ---------------------------------------------------------
    # Cálculo bruto
    # ---------------------------------------------------------

    def compute_raw(self) -> Dict[str, float]:
        return {
            schema: float(score)
            for schema, score in self.responses.items()
        }

    # ---------------------------------------------------------
    # Normalização
    # ---------------------------------------------------------

    def _normalize(self, value: float) -> float:
        low, high = self.NORMALIZATION_RANGE
        return ((value - self.MIN_SCORE) / (self.MAX_SCORE - self.MIN_SCORE)) * (high - low) + low

    # ---------------------------------------------------------
    # Saída final
    # ---------------------------------------------------------

    def compute(self) -> Dict[str, Any]:
        raw = self.compute_raw()

        normalized = {
            code: round(self._normalize(score), 2)
            for code, score in raw.items()
        }

        metadata = {
            code: {
                "name": self.SCHEMAS[code],
                "domain": next(domain for domain, items in self.DOMAINS.items() if code in items),
                "description": self.DESCRIPTIONS[code],
                "raw": raw[code],
                "normalized": normalized[code]
            }
            for code in raw
        }

        # Cálculo dos domínios
        domains = {}
        for domain, items in self.DOMAINS.items():
            domain_scores = [normalized[i] for i in items]
            domains[domain] = round(sum(domain_scores) / len(domain_scores), 2)

        return {
            "model": "Esquemas Iniciais Desadaptativos (Young)",
            "results": normalized,
            "metadata": metadata,
            "domains": domains,
            "schema_list": list(self.SCHEMAS.values())
        }
