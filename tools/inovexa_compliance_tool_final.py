#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inovexa Compliance Tool — FINAL (MindScan, r2+)
===============================================
Tudo-em-um para implantar e manter os guard-rails de compliance (sem idas e voltas).

Recursos principais
-------------------
- APPLY: implanta/atualiza CI + tools + prompts + manifest + PR template + work_plan.json (auto-detectado).
- VERIFY: roda localmente os guards Node (exports/shrink/envelope/paths/workplan) se você quiser validar sem PR.
- ROLLBACK: restaura o último backup dos arquivos tocados (backup em .backup/compliance-YYYYmmdd-HHMMSS).
- HOOKS: instala pre-push hook (Windows + Unix) para rodar os guards antes do push.
- MULTI-REPO: aplica em vários repositórios (lista ou varrendo uma pasta com --scan-dir/--glob).
- MERGE package.json: adiciona scripts/deps sem sobrescrever o existente.
- PARAMS: raiz/src, limiar de encolhimento, remote/branch, abrir PR (gh), backup/dirty, CODEOWNERS.

Requisitos
----------
- Git e Node 18+ (CI requer Node 20 nas Actions).
- (Opcional) GitHub CLI `gh` para abrir PR automáticamente.

Uso rápido
----------
# Aplicar no MindScan, criar branch, commit, push e PR; instala hook pre-push e faz backup:
python inovexa_compliance_tool_final.py apply "D:\projetos-inovexa\mindscan" --branch docs/compliance-final --gh-pr --install-hooks --backup

# Varrer vários repos (pelo nome) na pasta
python inovexa_compliance_tool_final.py apply --scan-dir "D:\projetos-inovexa" --glob mind* --install-hooks --backup

# Verificar localmente (sem PR)
python inovexa_compliance_tool_final.py verify "D:\projetos-inovexa\mindscan"

# Reverter o último backup
python inovexa_compliance_tool_final.py rollback "D:\projetos-inovexa\mindscan"
"""
from __future__ import annotations
import argparse, json, os, sys, subprocess, shutil, datetime, fnmatch
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# -------- util --------
def log(msg: str): print(msg, flush=True)
def sh(cmd: List[str], cwd: Path | None = None, check: bool=True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=check, text=True, capture_output=True)
def is_git_repo(p: Path) -> bool:
    try: sh(["git","rev-parse","--is-inside-work-tree"], cwd=p); return True
    except Exception: return False
def ensure_clean_repo(p: Path) -> None:
    out = sh(["git","status","--porcelain"], cwd=p, check=True).stdout.strip()
    if out: raise SystemExit(f"Working tree suja em {p}. Use --allow-dirty para prosseguir.")
def nowstamp(): return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
def backup_dir(repo: Path) -> Path: return repo / ".backup" / f"compliance-{nowstamp()}"
def list_backups(repo: Path) -> List[Path]:
    base = repo / ".backup"
    if not base.exists(): return []
    return sorted([p for p in base.glob("compliance-*") if p.is_dir()], key=lambda p: p.name)

def write_text(repo: Path, rel: str, content: str) -> Path:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p

def write_json(repo: Path, rel: str, data: Dict[str,Any]) -> Path:
    return write_text(repo, rel, json.dumps(data, indent=2, ensure_ascii=False))

def merge_package_json(repo: Path, additions: Dict[str,Any]) -> Tuple[Path, bool]:
    pkg_path = repo / "package.json"
    changed = False
    if pkg_path.exists():
        try:
            pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
        except Exception:
            pkg = {"name":"app","private":True,"version":"0.0.0"}
            changed = True
    else:
        pkg = {"name":"app","private":True,"version":"0.0.0"}
        changed = True
    deps = pkg.setdefault("dependencies", {})
    for k,v in additions.get("dependencies", {}).items():
        if k not in deps:
            deps[k]=v; changed=True
    scripts = pkg.setdefault("scripts", {})
    for k,v in additions.get("scripts", {}).items():
        if k not in scripts:
            scripts[k]=v; changed=True
    if changed:
        pkg_path.parent.mkdir(parents=True, exist_ok=True)
        pkg_path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False), encoding="utf-8")
    return pkg_path, changed

def gh_available() -> bool:
    try: subprocess.run(["gh","--version"], check=True, text=True, capture_output=True); return True
    except Exception: return False

# -------- payloads --------
def generate_payloads(root_prefix: str, src_dir: str, shrink_pct: int, codeowners: Optional[str]) -> Dict[str,str]:
    allowed_prefix = f"{root_prefix}/{src_dir}/"
    # Node tools (guards)
    ts_guard = f"""// tools/ts-regression-guard.js
const fs = require('fs');
const path = require('path');
const {{ Project }} = require('ts-morph');
const simpleGit = require('simple-git');
const {{ execSync }} = require('child_process');
const git = simpleGit();

function readManifest() {{
  try {{ return JSON.parse(fs.readFileSync('mindscan-manifest.json','utf8')); }} catch {{ return null; }}
}}
async function getChangedTsFiles(base) {{
  const mergeBase = execSync(`git merge-base HEAD ${{base}}`).toString().trim();
  const diff = execSync(`git diff --name-only ${{mergeBase}}..HEAD`).toString().trim().split('\\n').filter(Boolean);
  return diff.filter(p => /\\.(ts|tsx)$/i.test(p));
}}
function exportedSymbols(project, filePath) {{
  const source = project.addSourceFileAtPath(filePath);
  const set = new Set();
  source.getExportedDeclarations().forEach((_, name) => set.add(name));
  if (source.getDefaultExportSymbol()) set.add('default');
  return set;
}}
function sizeOf(file) {{ return fs.existsSync(file) ? fs.statSync(file).size : 0; }}

(async () => {{
  const manifest = readManifest();
  const SHRINK = Number(process.env.GUARD_SHRINK_PCT || (manifest?.rules?.no_shrink_over_percent ?? {shrink_pct}));
  const BASE = process.env.GUARD_BASE || 'origin/main';
  await git.fetch();
  const changed = await getChangedTsFiles(BASE);
  if (changed.length === 0) {{ console.log('No TS/TSX changes to guard.'); process.exit(0); }}
  const project = new Project({{ skipFileDependencyResolution: true, addFilesFromTsConfig: false }});
  let failures = [];
  for (const file of changed) {{
    const tmp = '.guard_tmp'; fs.mkdirSync(tmp, {{recursive:true}});
    const baseFile = path.join(tmp, file.replace(/[\\/\\\\]/g,'__') + '.base');
    try {{ fs.writeFileSync(baseFile, execSync(`git show ${{BASE}}:${{file}}`).toString(), 'utf8'); }} catch {{ /* new file */ }}
    const curSize = sizeOf(file), baseSize = sizeOf(baseFile);
    const shrink = baseSize>0 ? (1 - curSize/baseSize)*100 : 0;
    const curExp = exportedSymbols(project, file);
    let baseExp = new Set(); if (baseSize>0) baseExp = exportedSymbols(project, baseFile);
    if (baseSize>0 && shrink > SHRINK && curExp.size <= baseExp.size)
      failures.push(`❌ ${{file}}: encolheu ${{shrink.toFixed(1)}}% (> ${{SHRINK}}%) sem ganho de API.`);
    for (const name of baseExp) if (!curExp.has(name)) failures.push(`❌ ${{file}}: removeu export '${{name}}'.`);
  }}
  if (failures.length) {{ console.error(failures.join('\\n')); process.exit(1); }}
  console.log('✅ guard:exports OK');
}})();
"""
    check_env = """// tools/check-envelope.js
const body = process.env.GITHUB_PR_BODY || "";
const req = ["Projeto / Caminho completo:", "Tipo de melhoria:", "Evoluções nesta versão:", "Compatibilidade:", "Validações (7 níveis):", "Impacto previsto:"];
const miss = req.filter(t => !body.includes(t));
if (miss.length){ console.error("❌ Envelope ausente:", miss.join(", ")); process.exit(1); }
console.log("✅ guard:envelope OK");
"""
    validate_paths = f"""// tools/validate-paths.js
const fs = require('fs');
const {{ execSync }} = require('child_process');
let root = '{root_prefix}', src = '{src_dir}';
try {{ const m = JSON.parse(fs.readFileSync('mindscan-manifest.json','utf8')); root = m.paths.root || root; src = m.paths.src || src; }} catch{{}}
const allowed = `${{root}}/${{src}}/`;
const base = `origin/${{process.env.GITHUB_BASE_REF || 'main'}}`;
const mergeBase = execSync(`git merge-base HEAD ${{base}}`).toString().trim();
const changed = execSync(`git diff --name-only ${{mergeBase}}..HEAD`).toString().trim().split('\\n').filter(Boolean);
let failures = [];
for (const f of changed) {{
  if (!fs.existsSync(f)) {{ failures.push(`❌ Path não existe no workspace: ${{f}}`); continue; }}
  if (/\\.tsx$/i.test(f) && !f.startsWith(allowed)) failures.push(`❌ TSX fora de ${{allowed}}: ${{f}}`);
}}
if (failures.length){{ console.error(failures.join('\\n')); process.exit(1); }}
console.log('✅ guard:paths OK');
"""
    validate_workplan = """// tools/validate-workplan.js
const fs = require('fs'); const { execSync } = require('child_process');
if (!fs.existsSync('docs/work_plan.json')) { console.error('❌ docs/work_plan.json ausente.'); process.exit(1); }
const wp = JSON.parse(fs.readFileSync('docs/work_plan.json','utf8'));
const base = `origin/${process.env.GITHUB_BASE_REF || 'main'}`;
const mergeBase = execSync(`git merge-base HEAD ${base}`).toString().trim();
const changed = execSync(`git diff --name-only ${mergeBase}..HEAD`).toString().trim().split('\\n').filter(Boolean);
const tsChanged = changed.filter(p => /\\.(ts|tsx)$/i.test(p));
let notListed = [];
for (const f of tsChanged) { const listed = wp.items && wp.items.some(x => x.path === f); if (!listed) notListed.push(f); }
if (notListed.length){ console.error('❌ TS/TSX alterados não listados no work_plan.json:', notListed.join(', ')); process.exit(1); }
console.log('✅ guard:workplan OK');
"""
    workflow = """name: MindScan Compliance
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]
jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install deps
        run: npm ci || npm i
      - name: guard:exports
        env:
          GUARD_BASE: "origin/${{ github.base_ref }}"
        run: npm run guard:exports
      - name: guard:paths
        env:
          GITHUB_BASE_REF: "${{ github.base_ref }}"
        run: npm run guard:paths
      - name: guard:workplan
        env:
          GITHUB_BASE_REF: "${{ github.base_ref }}"
        run: npm run guard:workplan
      - name: guard:envelope
        env:
          GITHUB_PR_BODY: "${{ github.event.pull_request.body }}"
        run: npm run guard:envelope
"""
    pr_template = """## Envelope de Entrega
Projeto / Caminho completo: <preencher>
Tipo de melhoria: <Bugfix|Ampliação|Refactor+Feature|Otimização|Segurança>
Evoluções nesta versão:
- [+] ...
- [+] ...
Compatibilidade: <sim|não> — se não, migração: ...
Validações (7 níveis): sintaxe ✓ | tipos ✓ | lógica ✓ | erros ✓ | perf/memória ✓ | integração ✓ | ecossistema ✓
Impacto previsto: ...

## Matriz Antes vs Depois
| Capacidade/Comportamento | Antes | Depois | Status |
|---|---|---|---|
| Exports/Componentes | ... | ... | ↑ |
| Validação de input | ... | ... | ↑ |
| Erros/observabilidade | ... | ... | ↑ |
| Testes automatizados | ... | ... | ↑ |
| Performance/memória | ... | ... | ↑ |
"""
    prompt_v16 = """# PROMPT LEO VINCI — v1.6 (Supercola de Cumprimento Contínuo)
Invariantes por turno: higiene de contexto; checar base antes de alterar; plano de 1 turno com caminho exato;
anti-regressão (não remover exports / não encolher >20% sem ganho); entrega completa (arquivo + Envelope + Matriz);
auto-correção no mesmo turno. Proibido reenvio idêntico, caminhos errados, versões enxutas ou prometer para depois.
"""
    manifest = {
        "product": "MindScan",
        "paths": {"root": root_prefix, "src": src_dir},
        "rules": {"no_shrink_over_percent": shrink_pct, "no_export_removal": True, "pr_template_required": True}
    }
    codeowners_txt = (f"* {codeowners}\n" if codeowners else "")
    payloads = {
        "tools/ts-regression-guard.js": ts_guard,
        "tools/check-envelope.js": check_env,
        "tools/validate-paths.js": validate_paths,
        "tools/validate-workplan.js": validate_workplan,
        ".github/workflows/mindscan_compliance.yml": workflow,
        ".github/pull_request_template.md": pr_template,
        "docs/prompts/PROMPT-LEO-VINCI-v1.6.md": prompt_v16,
        "mindscan-manifest.json": json.dumps(manifest, indent=2, ensure_ascii=False),
        "README-COMPLIANCE.md": f"# MindScan Compliance — {datetime.date.today().isoformat()}\nGerado por Inovexa Compliance Tool (FINAL).\n"
    }
    if codeowners_txt:
        payloads[".github/CODEOWNERS"] = codeowners_txt
    return payloads

def detect_pages(repo: Path, root: str, src: str) -> List[str]:
    pages_dir = repo / root / src / "pages"
    if not pages_dir.exists(): return []
    return [str(p.relative_to(repo)).replace("\\\\","/") for p in pages_dir.glob("*.tsx")]

def build_work_plan(paths: List[str]) -> Dict[str,Any]:
    def item(p: str, goal: str) -> Dict[str,Any]:
        return {"path": p, "type": "Refactor+Feature", "goal": goal, "nonBreaking": True}
    items: List[Dict[str,Any]] = []
    for p in paths:
        name = Path(p).stem.lower()
        if name == "login":
            items.append(item(p, "Autenticação robusta (form + validação + feedback A11y); preservar estrutura; adicionar testes e loading."))
        elif name == "dashboard":
            items.append(item(p, "KPIs responsivos; skeleton; hooks de dados; manter widgets existentes."))
        elif name == "home":
            items.append(item(p, "Layout base/hero/CTA; melhorar semântica/A11y; manter conteúdo."))
        elif name == "notfound":
            items.append(item(p, "Página 404 com retorno; logs mínimos; integração com roteador."))
        elif name == "status":
            items.append(item(p, "Exibição de estado (ping/versão); loading; manter layout."))
        else:
            items.append(item(p, "Evolução sem regressão; preservar capacidades; adicionar testes onde couber."))
    return {"version": "1.0", "owner": "Leo Vinci", "items": items}

def install_hooks(repo: Path) -> None:
    hooks_dir = repo / ".git" / "hooks"
    if not hooks_dir.exists():
        log("ℹ Diretório .git/hooks não encontrado (repo bare?). Pulando hooks.")
        return
    # pre-push (bash)
    pre_push = """#!/usr/bin/env bash
set -e
if [ -f package.json ]; then
  if command -v npm >/dev/null 2>&1; then
    npm run guard:paths || exit 1
    npm run guard:workplan || exit 1
    npm run guard:exports || exit 1
  fi
fi
"""
    (hooks_dir / "pre-push").write_text(pre_push, encoding="utf-8")
    os.chmod(hooks_dir / "pre-push", 0o755)
    # Windows .cmd
    pre_push_cmd = r"""@echo off
if exist package.json (
  where npm >nul 2>&1 || goto :eof
  call npm run guard:paths || exit /b 1
  call npm run guard:workplan || exit /b 1
  call npm run guard:exports || exit /b 1
)
"""
    (hooks_dir / "pre-push.cmd").write_text(pre_push_cmd, encoding="utf-8")

def create_backup(repo: Path, files: List[Path]) -> Path:
    bdir = backup_dir(repo)
    for rel in files:
        src = repo / rel
        if src.exists():
            dst = bdir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    log(f"↳ Backup em {bdir}")
    return bdir

def restore_last_backup(repo: Path) -> None:
    backups = list_backups(repo)
    if not backups: raise SystemExit("Nenhum backup encontrado em .backup/")
    bdir = backups[-1]
    log(f"→ Restaurando backup: {bdir.name}")
    for src in bdir.rglob("*"):
        if src.is_file():
            rel = src.relative_to(bdir)
            dst = repo / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    log("✔ Backup restaurado.")

# -------- core --------
def apply_repo(repo: Path, args) -> None:
    if not is_git_repo(repo): raise SystemExit(f"Não é um repositório Git: {repo}")
    if not args.allow_dirty: ensure_clean_repo(repo)
    root, src, shrink = args.root, args.src, args.shrink_pct
    log(f"→ APPLY em {repo} (paths: {root}/{src}/, shrink>{shrink}%)")
    try: sh(["git","checkout","-b",args.branch], cwd=repo)
    except subprocess.CalledProcessError: sh(["git","checkout",args.branch], cwd=repo)
    payloads = generate_payloads(root, src, shrink, args.codeowners)
    # work_plan (detecta páginas)
    pages = detect_pages(repo, root, src) or [f"{root}/{src}/pages/{n}.tsx" for n in ["Login","Dashboard","Home","NotFound","Status"]]
    payloads["docs/work_plan.json"] = json.dumps(build_work_plan(pages), indent=2, ensure_ascii=False)
    # package merge
    pkg_add = {
        "dependencies": {"ts-morph": "^22.0.0", "simple-git": "^3.24.0"},
        "scripts": {
            "guard:exports": "node tools/ts-regression-guard.js",
            "guard:envelope": "node tools/check-envelope.js",
            "guard:paths": "node tools/validate-paths.js",
            "guard:workplan": "node tools/validate-workplan.js"
        }
    }
    pkg_path, pkg_changed = merge_package_json(repo, pkg_add)
    # backup (antes de sobrescrever)
    to_touch = [Path(k) for k in payloads.keys()] + [Path(".github/pull_request_template.md")]
    if pkg_changed: to_touch.append(Path("package.json"))
    if args.backup: create_backup(repo, to_touch)
    # write files
    for rel, content in payloads.items():
        write_text(repo, rel, content)
        log(f"  + {rel}")
    # optional hooks
    if args.install_hooks: install_hooks(repo)
    # git ops
    sh(["git","add","."], cwd=repo)
    msg = f"docs(ci): compliance final — v1.6 Supercola + work_plan + guard rails (exports/shrink/envelope/paths/workplan) [{root}/{src}]"
    sh(["git","commit","-m",msg], cwd=repo)
    log("✔ Commit criado.")
    if not args.no_push:
        sh(["git","push","-u",args.remote,args.branch], cwd=repo)
        log("✔ Push realizado.")
        if args.gh_pr and gh_available():
            try:
                title = "[Compliance] v1.6 Supercola + work_plan inicial + guard rails (FINAL)"
                body = "# PR de Compliance (FINAL)\nVeja docs/work_plan.json e workflow MindScan Compliance."
                sh(["gh","pr","create","--title",title,"--body",body], cwd=repo)
                log("✔ PR aberto via gh.")
            except Exception as e:
                log(f"ℹ Não foi possível abrir PR automaticamente: {e}")
    log("✅ APPLY concluído.")

def verify_repo(repo: Path, args) -> None:
    log(f"→ VERIFY em {repo}")
    # tenta rodar os guards via npm
    try:
        sh(["npm","run","guard:paths"], cwd=repo)
        sh(["npm","run","guard:workplan"], cwd=repo)
        sh(["npm","run","guard:exports"], cwd=repo)
        log("✔ Guards locais executados com sucesso.")
    except Exception as e:
        raise SystemExit(f"Falha ao rodar guards locais: {e}")

def rollback_repo(repo: Path, args) -> None:
    log(f"→ ROLLBACK em {repo}")
    restore_last_backup(repo)
    sh(["git","add","."], cwd=repo)
    sh(["git","commit","-m","chore: rollback compliance pack (restore from backup)"], cwd=repo)
    log("✔ Rollback commit criado. Faça push se necessário.")

def find_repos(scan_dir: Path, pattern: str) -> List[Path]:
    repos = []
    for root, dirs, files in os.walk(scan_dir):
        if ".git" in dirs:
            repo = Path(root)
            name = repo.name
            if fnmatch.fnmatch(name.lower(), pattern.lower()):
                repos.append(repo)
            dirs[:] = [d for d in dirs if d != ".git"]
    return repos

# -------- CLI --------
def main():
    ap = argparse.ArgumentParser(description="Inovexa Compliance Tool — FINAL (MindScan)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default="frontend", help="Pasta raiz do app (default: frontend)")
    common.add_argument("--src", default="src", help="Subpasta de código (default: src)")
    common.add_argument("--shrink-pct", type=int, default=20, help="Limite de encolhimento permitido (default: 20)")
    common.add_argument("--branch", default="docs/compliance-final", help="Branch a criar/usar")
    common.add_argument("--remote", default="origin", help="Remote Git (default: origin)")
    common.add_argument("--backup", action="store_true", help="Criar backup dos arquivos afetados")
    common.add_argument("--allow-dirty", action="store_true", help="Permite aplicar com working tree suja")
    common.add_argument("--no-push", action="store_true", help="Evita push automático")
    common.add_argument("--gh-pr", action="store_true", help="Abre PR com GitHub CLI (se disponível)")
    common.add_argument("--install-hooks", action="store_true", help="Instala hook pre-push local")
    common.add_argument("--codeowners", help="Cria .github/CODEOWNERS (ex.: @inovexa/tech-leads)")

    p_apply = sub.add_parser("apply", parents=[common], help="Aplicar em um ou vários repositórios")
    p_apply.add_argument("repos", nargs="*", help="Caminhos de repositórios (se vazio, use --scan-dir)")
    p_apply.add_argument("--scan-dir", help="Varre diretório e aplica em todos sub-repositórios Git")
    p_apply.add_argument("--glob", default="*", help="Filtro glob para nome da pasta do repo ao usar --scan-dir")

    p_verify = sub.add_parser("verify", help="Rodar guards localmente (sem PR)")
    p_verify.add_argument("repo", help="Caminho do repositório")

    p_rollback = sub.add_parser("rollback", help="Restaurar último backup do Compliance")
    p_rollback.add_argument("repo", help="Caminho do repositório")

    args = ap.parse_args()

    if args.cmd == "apply":
        targets: List[Path] = []
        if getattr(args, "repos", None):
            targets = [Path(p).resolve() for p in args.repos]
        elif getattr(args, "scan_dir", None):
            targets = find_repos(Path(args.scan_dir).resolve(), args.glob or "*")
        else:
            raise SystemExit("Informe pelo menos um repositório ou use --scan-dir.")

        if not targets:
            raise SystemExit("Nenhum repositório encontrado.")
        for repo in targets:
            try:
                apply_repo(repo, args)
            except Exception as e:
                log(f"❌ Falha em {repo}: {e}")
                continue

    elif args.cmd == "verify":
        repo = Path(args.repo).resolve()
        if not is_git_repo(repo): raise SystemExit("Não é um repositório Git.")
        verify_repo(repo, args)

    elif args.cmd == "rollback":
        repo = Path(args.repo).resolve()
        if not is_git_repo(repo): raise SystemExit("Não é um repositório Git.")
        rollback_repo(repo, args)

if __name__ == "__main__":
    main()
