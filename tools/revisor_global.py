"""
Revisor Global — MindScan
Autor: Leo Vinci (GPT Inovexa)
Data: 26/11/2025

Objetivo:
    - Validar integridade geral do projeto
    - Comparar com tree_referencia.json
    - Mapear managers e seus métodos principais
    - Relatar divergências estruturais
    - Preparar dados para reconstrução do main.py definitivo

Saídas:
    logs/revisao_global.json
    logs/revisao_global.md
"""

import os
import json
import inspect
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True, parents=True)


# ---------------------------------------------------------
# 1. Carregar árvore de referência (se existir)
# ---------------------------------------------------------

def load_reference_tree():
    ref = ROOT / "tree_referencia.json"
    if not ref.exists():
        return None
    try:
        return json.loads(ref.read_text(encoding="utf-8"))
    except:
        return None


# ---------------------------------------------------------
# 2. Gerar árvore atual
# ---------------------------------------------------------

def build_current_tree():
    structure = {}
    for root, dirs, files in os.walk(ROOT):
        root = Path(root)
        rel = str(root.relative_to(ROOT))
        structure[rel] = {"dirs": dirs, "files": files}
    return structure


# ---------------------------------------------------------
# 3. Encontrar managers e mapear métodos principais
# ---------------------------------------------------------

def identify_managers():
    managers = {}
    manager_dir = ROOT / "core" / "managers"

    if not manager_dir.exists():
        return managers

    for file in manager_dir.glob("*.py"):
        module_name = file.stem
        try:
            module = __import__(f"mindscan.core.managers.{module_name}",
                                fromlist=['*'])
        except:
            continue

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if "Manager" in name:
                methods = [
                    m for m, f in inspect.getmembers(obj, inspect.isfunction)
                    if not m.startswith("_")
                ]
                managers[name] = methods

    return managers


# ---------------------------------------------------------
# 4. Detectar arquivos suspeitos
# ---------------------------------------------------------

def detect_suspicious():
    empty, tiny = [], []

    for root, dirs, files in os.walk(ROOT):
        for f in files:
            path = Path(root) / f
            try:
                size = path.stat().st_size
                if size == 0:
                    empty.append(str(path))
                if size > 0 and size < 5:
                    tiny.append(str(path))
            except:
                continue

    return {"empty": empty, "tiny": tiny}


# ---------------------------------------------------------
# 5. Comparar árvore atual com a referência
# ---------------------------------------------------------

def compare_trees(current, reference):
    if reference is None:
        return {"status": "no_reference"}

    missing = []
    extra = []

    for ref_path in reference.keys():
        if ref_path not in current:
            missing.append(ref_path)

    for cur_path in current.keys():
        if cur_path not in reference:
            extra.append(cur_path)

    return {
        "status": "ok",
        "missing_paths": missing,
        "extra_paths": extra
    }


# ---------------------------------------------------------
# 6. Gerar relatório global
# ---------------------------------------------------------

def generate_report(data):
    ts = datetime.now().isoformat()
    data["timestamp"] = ts

    # JSON
    json_path = LOGS / "revisao_global.json"
    json_path.write_text(json.dumps(data, indent=4, ensure_ascii=False),
                         encoding="utf-8")

    # Markdown
    md = []

    md.append("# 📘 Relatório de Revisão Global — MindScan\n")
    md.append(f"Gerado em: {ts}\n")
    md.append("---\n")

    md.append("## ✔️ Estrutura Atual (Resumo)\n")
    md.append(f"- Total de diretórios mapeados: {len(data['tree_current'])}\n")
    md.append(f"- Referência carregada: {data['tree_comparison']['status']}\n")
    md.append("---\n")

    md.append("## ⚙️ Managers Detectados\n")
    for m, methods in data["managers"].items():
        md.append(f"- **{m}** → métodos: {methods}")
    md.append("---\n")

    md.append("## 🚩 Arquivos Suspeitos\n")
    md.append(f"- Vazios: {len(data['suspicious']['empty'])}")
    md.append(f"- Minúsculos: {len(data['suspicious']['tiny'])}")
    md.append("---\n")

    md.append("## 🧭 Divergências da Árvore de Referência\n")
    comp = data["tree_comparison"]
    if comp["status"] == "ok":
        md.append(f"- Faltando: {len(comp['missing_paths'])}")
        md.append(f"- Extras: {len(comp['extra_paths'])}")
    else:
        md.append("Nenhuma referência disponível.")
    md.append("\n---\n")

    md_path = LOGS / "revisao_global.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    return str(json_path), str(md_path)


# ---------------------------------------------------------
# 7. Execução
# ---------------------------------------------------------

def run():
    ref_tree = load_reference_tree()
    current_tree = build_current_tree()
    managers = identify_managers()
    suspicious = detect_suspicious()
    tree_comp = compare_trees(current_tree, ref_tree)

    data = {
        "tree_current": current_tree,
        "tree_comparison": tree_comp,
        "managers": managers,
        "suspicious": suspicious
    }

    return generate_report(data)


if __name__ == "__main__":
    paths = run()
    print("Relatórios gerados:")
    print(paths)
