"""
Gerador da Árvore de Referência Oficial do MindScan
Autor: Leo Vinci (GPT Inovexa)
Data: 26/11/2025

Função:
    - Capturar a árvore REAL do MindScan
    - Salvar como tree_referencia.json
    - Servir como baseline oficial para o revisor_global
"""

import os
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]   # mindscan/
OUT = ROOT / "tree_referencia.json"

def build_tree():
    structure = {}
    for root, dirs, files in os.walk(ROOT):
        root_path = Path(root)
        rel = str(root_path.relative_to(ROOT))
        structure[rel] = {
            "dirs": sorted(dirs),
            "files": sorted(files)
        }
    return structure

def run():
    tree = build_tree()
    data = {
        "generated_at": datetime.now().isoformat(),
        "root": str(ROOT),
        "structure": tree
    }
    OUT.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
    print(f"Árvore de referência gerada em:\n{OUT}")

if __name__ == "__main__":
    run()
