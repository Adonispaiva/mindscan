"""
MindScan - Inovexa
scan_project_file_sizes.py (Versão Diretor 2.0)

Função:
    - Escanear recursivamente o projeto
    - Gerar mapa de tamanhos de arquivos
    - Operar SEM interferir nos demais módulos
    - Autodetectar a raiz oficial do MindScan
    - Produzir logs seguros no padrão Inovexa
"""

import os
import json
from pathlib import Path
from datetime import datetime


def detectar_raiz():
    """
    Determina automaticamente a raiz do projeto MindScan,
    independente de onde o script for executado.
    """
    script_dir = Path(__file__).resolve()
    root = script_dir.parent.parent  # /mindscan

    if not root.exists():
        raise RuntimeError(f"Raiz do projeto não encontrada: {root}")

    return root


def scan_sizes(base: Path):
    """
    Varre todos os arquivos do projeto e retorna
    uma lista de (path_relativo, tamanho).
    """
    resultados = []

    for root, _, files in os.walk(base):
        for f in files:
            fpath = Path(root) / f
            try:
                size = fpath.stat().st_size
            except Exception:
                size = -1  # não consegue ler

            rel = fpath.relative_to(base)
            resultados.append({
                "path": str(rel).replace("\\", "/"),
                "size": size
            })

    return resultados


def salvar_relatorio(base: Path, dados):
    """
    Salva o relatório em JSON dentro de logs/estrutura/
    sem interferir nos logs centrais do sistema.
    """
    outdir = base / "logs" / "estrutura"
    outdir.mkdir(parents=True, exist_ok=True)

    fname = f"file_sizes_{datetime.now().strftime('%Y-%m-%d_%Hh%Mmin%Ss')}.json"
    outfile = outdir / fname

    with outfile.open("w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    return outfile


def run():
    print("MindScan :: Scan de Tamanhos (Padrão Inovexa)")

    base = detectar_raiz()
    print(f"[OK] Raiz detectada: {base}")

    dados = scan_sizes(base)
    print(f"[OK] {len(dados)} arquivos escaneados.")

    out = salvar_relatorio(base, dados)
    print(f"[OK] Relatório salvo em: {out}")


if __name__ == "__main__":
    run()
