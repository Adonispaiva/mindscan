"""
Task: generate_report
MindScan Automator — Inovexa Software
Autor: Leo Vinci (GPT Inovexa)
Data: 26/11/2025

Objetivo:
- Gerar RELATÓRIO TÉCNICO FINAL do estado do MindScan.
- Integrar:
    • Resultados da auditoria (audit_report.json)
    • Estrutura detectada
    • Status dos módulos, serviços e backend
    • Conclusões técnicas
    • Recomendações para execução completa do sistema

Entrega:
- relatório técnico Markdown (report.md)
- JSON com resumo (report.json)

Esta task fecha o pipeline do Automator.
"""

import json
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------
# Templates do relatório
# ---------------------------------------------------------------------

MD_TEMPLATE = """# 🧠 MindScan — Relatório Técnico Automático
Gerado por: MindScan Automator (Inovexa Software)  
Data: {timestamp}

---

## ✔️ Resumo Geral
{summary}

---

## 🗂 Estrutura Auditada
### Backend
{backend}

### Módulos
{modules}

### Serviços
{services}

---

## ⚠️ Itens Ausentes
{missing}

---

## ❗ Problemas Detectados
{issues}

---

## 📌 Conclusão Técnica
{conclusion}

---

## 📄 Notas
Este relatório foi gerado automaticamente pelo Automator e reflete o estado REAL
da arquitetura atual do MindScan segundo o BOOT-SPEC oficial.
"""


JSON_TEMPLATE = {
    "task": "generate_report",
    "timestamp": None,
    "summary": None,
    "backend": None,
    "modules": None,
    "services": None,
    "missing": None,
    "issues": None,
    "conclusion": None
}


# ---------------------------------------------------------------------
# Funções internas
# ---------------------------------------------------------------------

def load_audit(project_root: Path):
    audit_path = project_root / "logs" / "audit_report.json"
    if not audit_path.exists():
        return None
    with audit_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def format_dict_for_md(data: dict):
    lines = []
    for key, value in data.items():
        exists = value.get("exists", False)
        mark = "🟢" if exists else "🔴"
        lines.append(f"- {mark} **{key}** — {value['path']}")
    return "\n".join(lines)


def format_list_for_md(items: list):
    if not items:
        return "Nenhum item faltante."
    return "\n".join([f"- 🔴 {item}" for item in items])


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

def run(context):
    project_root = Path(context["project_root"])
    logs_dir = Path(context["logs_path"])
    logs_dir.mkdir(exist_ok=True, parents=True)

    audit = load_audit(project_root)
    if audit is None:
        return {
            "status": "error",
            "message": "audit_report.json não encontrado. Rode run_audit antes.",
            "report": None
        }

    ts = datetime.now().isoformat()

    backend_md = format_dict_for_md(audit["details"]["checks"]["backend_dirs"])
    modules_md = format_dict_for_md(audit["details"]["checks"]["modules"])
    services_md = format_dict_for_md(audit["details"]["checks"]["services"])
    missing_md = format_list_for_md(audit["details"]["missing"])
    issues_md = format_list_for_md(audit["details"]["issues"])

    conclusion = audit["summary"]

    # MD
    md_text = MD_TEMPLATE.format(
        timestamp=ts,
        summary=audit["summary"],
        backend=backend_md,
        modules=modules_md,
        services=services_md,
        missing=missing_md,
        issues=issues_md,
        conclusion=conclusion
    )

    md_path = logs_dir / "report.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write(md_text)

    # JSON
    json_data = JSON_TEMPLATE.copy()
    json_data["timestamp"] = ts
    json_data["summary"] = audit["summary"]
    json_data["backend"] = audit["details"]["checks"]["backend_dirs"]
    json_data["modules"] = audit["details"]["checks"]["modules"]
    json_data["services"] = audit["details"]["checks"]["services"]
    json_data["missing"] = audit["details"]["missing"]
    json_data["issues"] = audit["details"]["issues"]
    json_data["conclusion"] = conclusion

    json_path = logs_dir / "report.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return {
        "status": "success",
        "message": "Relatório final gerado com sucesso.",
        "report_md": str(md_path),
        "report_json": str(json_path)
    }


if __name__ == "__main__":
    fake = {
        "project_root": str(Path(__file__).resolve().parents[2]),
        "logs_path": str(Path(__file__).resolve().parents[2] / "logs"),
        "settings": {}
    }
    print(run(fake))
