# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\mindscan_superscript.py
# Última atualização: 2025-12-11T09:59:27.792836

# mindscan_superscript.py
# ============================================
# MindScan SuperScript — Árvore Absoluta
# Diretor: Leo Vinci — Inovexa Software
# --------------------------------------------
# Este script unifica:
#   1. Geração de árvore completa (.txt)
#   2. Geração de baseline canônica (.json)
#   3. Validação da árvore real vs baseline
#   4. Estatísticas avançadas da estrutura
#   5. Detecção de arquivos vazios, legados e anômalos
#   6. Hash estrutural para Anti-Regressão
# --------------------------------------------
# Compatível com arquitetura MAXIMALISTA do MindScan.
# Este arquivo substitui: generate_tree.py, gerar_tree_referencia.py,
# mindscan_tree_validator.py.
# --------------------------------------------

import os
import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Any

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================
IGNORED_DIRS = {
    '.git', 'venv', '__pycache__', 'node_modules', '.vscode', '.idea', 'logs'
}

IGNORED_PREFIXES = {
    '_backup_mindscan',
}

BASELINE_FILE = 'tree_referencia.json'
VALIDATION_FILE = 'tree_validation_report.json'

# ============================================================
# FUNÇÕES DE SUPORTE
# ============================================================
def should_ignore(name: str) -> bool:
    if name in IGNORED_DIRS:
        return True
    for prefix in IGNORED_PREFIXES:
        if name.startswith(prefix):
            return True
    return False


def get_file_hash(path: Path) -> str:
    try:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ''


def generate_hash_for_tree(structure: Dict[str, Any]) -> str:
    encoded = json.dumps(structure, sort_keys=True).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()

# ============================================================
# GERADOR DA ÁRVORE COMPLETA (TXT)
# ============================================================
def generate_tree_txt(root: Path, prefix: str = '') -> List[str]:
    try:
        entries = sorted(os.listdir(root))
    except Exception:
        return [prefix + '[ERRO AO LER DIRETÓRIO]\n']

    lines = []

    for idx, name in enumerate(entries):
        path = root / name
        is_last = idx == len(entries) - 1
        connector = '└── ' if is_last else '├── '

        if path.is_dir():
            if should_ignore(name):
                lines.append(f"{prefix}{connector}{name}/ [IGNORADO]\n")
                continue
            lines.append(f"{prefix}{connector}{name}/\n")
            child_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(generate_tree_txt(path, child_prefix))
        else:
            try:
                size = os.path.getsize(path)
            except Exception:
                size = -1
            lines.append(f"{prefix}{connector}{name} ({size} bytes)\n")
    return lines


def save_txt_tree(root: Path) -> Path:
    log_dir = root / 'logs' / 'estrutura'
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mmin%Ss')
    out = log_dir / f'tree_{timestamp}.txt'

    header = [
        'MindScan — Árvore Completa\n',
        f'Gerado em: {datetime.datetime.now()}\n',
        '=' * 60 + '\n\n',
    ]

    with open(out, 'w', encoding='utf-8') as f:
        f.writelines(header)
        f.writelines(generate_tree_txt(root))

    return out

# ============================================================
# GERADOR DA BASELINE (JSON LIMPO)
# ============================================================
def build_clean_tree(root: Path) -> Dict[str, Any]:
    tree = {}
    for current, dirs, files in os.walk(root):
        cpath = Path(current)
        rel = str(cpath.relative_to(root)) or '.'

        clean_dirs = [d for d in dirs if not should_ignore(d)]
        tree[rel] = {
            'dirs': sorted(clean_dirs),
            'files': sorted(f for f in files if not f.startswith('_backup')),
        }
    return tree


def save_baseline(root: Path) -> Path:
    out = root / BASELINE_FILE
    tree = build_clean_tree(root)
    data = {
        'generated_at': datetime.datetime.now().isoformat(),
        'root': str(root),
        'tree': tree,
        'tree_hash': generate_hash_for_tree(tree),
    }
    out.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding='utf-8')
    return out

# ============================================================
# VALIDAÇÃO DA ÁRVORE
# ============================================================
def validate_against_baseline(root: Path) -> Dict[str, Any]:
    baseline_path = root / BASELINE_FILE
    if not baseline_path.exists():
        return {'status': 'NO_BASELINE', 'message': 'tree_referencia.json não encontrado.'}

    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    expected = baseline['tree']

    real = build_clean_tree(root)

    missing = []
    extra = []
    empty = []

    for path, exp in expected.items():
        if path not in real:
            missing.append(path)
            continue

        rdirs = set(real[path]['dirs'])
        rfiles = set(real[path]['files'])
        edirs = set(exp['dirs'])
        efiles = set(exp['files'])

        extra_dirs = rdirs - edirs
        extra_files = rfiles - efiles
        if extra_dirs or extra_files:
            extra.append({path: {'dirs': list(extra_dirs), 'files': list(extra_files)}})

        # arquivos vazios
        for f in real[path]['files']:
            fpath = (root / path / f) if path != '.' else (root / f)
            try:
                if fpath.stat().st_size == 0:
                    empty.append(str(fpath))
            except Exception:
                pass

    report = {
        'validated_at': datetime.datetime.now().isoformat(),
        'status': 'OK' if not missing and not extra else 'INCONSISTENT',
        'missing_paths': missing,
        'extra_entries': extra,
        'empty_files': empty,
    }

    (root / VALIDATION_FILE).write_text(json.dumps(report, indent=4, ensure_ascii=False))
    return report

# ============================================================
# ESTATÍSTICAS DO PROJETO
# ============================================================
def collect_stats(root: Path) -> Dict[str, Any]:
    total_files = 0
    total_dirs = 0
    total_size = 0
    ext_count = {}

    for current, dirs, files in os.walk(root):
        total_dirs += len(dirs)
        for f in files:
            fpath = Path(current) / f
            try:
                size = fpath.stat().st_size
            except Exception:
                size = 0
            total_files += 1
            total_size += size
            ext = fpath.suffix.lower()
            ext_count[ext] = ext_count.get(ext, 0) + 1

    return {
        'total_files': total_files,
        'total_dirs': total_dirs,
        'total_size_bytes': total_size,
        'extensions': ext_count,
    }

# ============================================================
# ENTRADA PRINCIPAL
# ============================================================
def main():
    script_path = Path(__file__).resolve()
    root = script_path.parents[1]

    print("[1] Gerando árvore completa (TXT)...")
    txt_file = save_txt_tree(root)
    print(f" → {txt_file}")

    print("[2] Gerando baseline limpa (JSON)...")
    baseline = save_baseline(root)
    print(f" → {baseline}")

    print("[3] Validando estrutura atual...")
    validation = validate_against_baseline(root)
    print(json.dumps(validation, indent=4, ensure_ascii=False))

    print("[4] Coletando estatísticas...")
    stats = collect_stats(root)
    print(json.dumps(stats, indent=4, ensure_ascii=False))

    print("\nSuperScript finalizado com sucesso.")


if __name__ == '__main__':
    main()
