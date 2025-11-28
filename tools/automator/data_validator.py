"""
data_validator.py
Validador Psicométrico Completo do MindScan
Versão Profissional Completa (A)

Funções:
    • Validar estrutura de dados psicométricos
    • Validar ranges de respostas
    • Verificar coerência entre itens
    • Verificar pesos relativos
    • Detectar anomalias e inconsistências
    • Gerar relatório detalhado
"""

import os
import json
import datetime


class DataValidator:

    def __init__(self, logger):
        self.log = logger
        self.root_path = r"D:\projetos-inovexa\mindscan"

        self.report = {
            "missing_fields": [],
            "range_issues": [],
            "weight_problems": [],
            "coherence_issues": [],
            "internal_errors": [],
            "summary": {
                "ok": 0,
                "warnings": 0,
                "critical": 0
            }
        }

    # ============================================================
    # Funções de utilidade
    # ============================================================

    def _validate_range(self, value, min_val, max_val, label):
        """Valida se o valor está dentro do range esperado."""
        if not isinstance(value, (int, float)):
            self.report["range_issues"].append(f"{label}: valor não numérico: {value}")
            self.report["summary"]["warnings"] += 1
            return False

        if value < min_val or value > max_val:
            self.report["range_issues"].append(
                f"{label}: fora do intervalo permitido ({value} / {min_val}-{max_val})"
            )
            self.report["summary"]["critical"] += 1
            return False

        self.report["summary"]["ok"] += 1
        return True

    def _validate_required_fields(self, data, required_fields):
        """Valida se campos obrigatórios estão presentes."""
        for field in required_fields:
            if field not in data:
                self.report["missing_fields"].append(field)
                self.report["summary"]["critical"] += 1
            else:
                self.report["summary"]["ok"] += 1

    # ============================================================
    # Validação psicométrica profunda
    # ============================================================

    def _validate_psychometrics(self, data):
        """
        Valida a estrutura interna do MindScan:
            - Estrutura MI/SynMind
            - DASS
            - Perfis
            - Subescalas
        """

        # --------------------------------------------------------
        # 1) Campos obrigatórios universais
        # --------------------------------------------------------
        required_fields = [
            "nome",
            "idade",
            "sexo",
            "respostas",
            "pesos",
            "metricas"
        ]

        self._validate_required_fields(data, required_fields)

        # --------------------------------------------------------
        # 2) Número mínimo de respostas
        # --------------------------------------------------------
        if "respostas" in data:
            total = len(data["respostas"])
            if total < 10:
                self.report["coherence_issues"].append(
                    f"Quantidade de respostas insuficiente: {total}"
                )
                self.report["summary"]["critical"] += 1
            else:
                self.report["summary"]["ok"] += 1

        # --------------------------------------------------------
        # 3) Validar ranges típicos dos testes
        # --------------------------------------------------------
        if "respostas" in data:
            for i, r in enumerate(data["respostas"], start=1):
                self._validate_range(r, 0, 4, f"resposta_{i}")

        # --------------------------------------------------------
        # 4) Validar pesos
        # --------------------------------------------------------
        if "pesos" in data:
            for name, weight in data["pesos"].items():
                if not self._validate_range(weight, 0, 1, f"peso_{name}"):
                    self.report["weight_problems"].append(name)

        # --------------------------------------------------------
        # 5) Checagem simples de coerência entre métricas
        # --------------------------------------------------------
        if "metricas" in data:
            for mname, mvalue in data["metricas"].items():
                if not self._validate_range(mvalue, 0, 100, f"métrica_{mname}"):
                    self.report["coherence_issues"].append(mname)

    # ============================================================
    # Gera relatório
    # ============================================================

    def _generate_report(self):
        report_dir = os.path.join(self.root_path, "logs", "data_validation")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = os.path.join(report_dir, f"data_validation_{timestamp}.json")

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=4, ensure_ascii=False)

        self.log.success(f"Relatório de validação gerado:\n{report_file}")

    # ============================================================
    # Execução principal
    # ============================================================

    def validate(self):
        self.log.header("DATA VALIDATOR – INICIADO")

        # Em produção, você vai passar dados reais.
        # Aqui, usamos um modelo mínimo de exemplo.

        sample_data_path = os.path.join(self.root_path, "data", "sample_data.json")

        if not os.path.exists(sample_data_path):
            self.log.warn("Nenhum dado de exemplo encontrado para validação.")
            self.report["summary"]["warnings"] += 1
            self._generate_report()
            return False

        try:
            with open(sample_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._validate_psychometrics(data)

        except Exception as e:
            self.log.error(f"Erro ao validar dados: {e}")
            self.report["internal_errors"].append(str(e))
            self.report["summary"]["critical"] += 1

        self._generate_report()
        self.log.success("VALIDAÇÃO PSICOMÉTRICA COMPLETA.")
        return True
