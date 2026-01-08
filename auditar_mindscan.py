# Arquivo: D:\projetos-inovexa\mindscan\auditar_mindscan.py
# Status: Corrigido e Validado

import os
import json
import hashlib
import datetime
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / ".mindscan_audit.log"

def log_event(event, data):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event,
        "data": data,
    }
    # Corrigido: Garantia de string terminada e nova linha
    try:
        current_log = LOG.read_text(encoding='utf-8') if LOG.exists() else ""
    except:
        current_log = ""
    
    new_entry = json.dumps(entry, ensure_ascii=False) + "\n"
    LOG.write_text(current_log + new_entry, encoding='utf-8')

def generate_tree(path, indent=""):
    tree = []
    try:
        items = sorted(os.listdir(path))
        for item in items:
            if item in [".git", "__pycache__", ".venv", "node_modules", ".mindscan_audit.log"]:
                continue
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                tree.append(f"{indent}└── [DIR] {item}/")
                tree.extend(generate_tree(full_path, indent + "    "))
            else:
                size = os.path.getsize(full_path) / 1024
                tree.append(f"{indent}├── {item} ({size:.2f} KB)")
    except Exception as e:
        tree.append(f"Erro: {str(e)}")
    return tree

def detect_ghost_dirs(path):
    ghosts = []
    for root, dirs, files in os.walk(path):
        if "__pycache__" in dirs:
            ghosts.append(os.path.join(root, "__pycache__"))
    return ghosts

def audit_code(tree_list):
    report = {"classes": [], "functions": [], "syntax_errors": []}
    for line in tree_list:
        if ".py" in line and "[DIR]" not in line:
            parts = line.split("├── ")
            if len(parts) > 1:
                filename = parts[1].split(" (")[0].strip()
                for p in ROOT.rglob(filename):
                    try:
                        content = p.read_text(encoding='utf-8')
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                report["classes"].append(f"{filename} > {node.name}")
                            elif isinstance(node, ast.FunctionDef):
                                report["functions"].append(f"{filename} > {node.name}")
                    except SyntaxError:
                        report["syntax_errors"].append(filename)
                    except:
                        continue
    return report

def audit_git():
    try:
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).decode('utf-8')
        return {"changed": status.splitlines()}
    except:
        return {"error": "Git Offline"}

def risk_analysis(tree, code_report, ghosts):
    score = 0
    risks = []
    if len(ghosts) > 3:
        score += 10
        risks.append("Ghost dirs detectados")
    if code_report["syntax_errors"]:
        score += len(code_report["syntax_errors"]) * 20
        risks.append(f"Erros de sintaxe em: {code_report['syntax_errors']}")
    
    level = "BAIXO" if score < 20 else "MEDIO" if score < 50 else "ALTO"
    return {"risks": risks, "score": score, "level": level}

def auditar():
    print("--- Auditoria MindScan em curso ---")
    tree = generate_tree(ROOT)
    ghosts = detect_ghost_dirs(ROOT)
    code_report = audit_code(tree)
    git_report = audit_git()
    risk = risk_analysis(tree, code_report, ghosts)
    
    final = {
        "tree_snapshot": f"{len(tree)} ficheiros",
        "risk_assessment": risk,
        "conclusion": "APROVADO" if risk["level"] != "ALTO" else "REPROVADO"
    }
    log_event("audit_complete", final)
    return final

if __name__ == "__main__":
    auditar()