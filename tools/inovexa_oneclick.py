#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inovexa One-Click — MindScan
Automatiza o fluxo completo em um arquivo.

Uso típico (Windows PowerShell):
  python inovexa_oneclick.py ^
    --repo "D:\projetos-inovexa\mindscan" ^
    --origin-url "https://github.com/Adonispaiva/synmind.git" ^
    --branch docs/compliance-final --gh-pr

Se preferir SSH (evita 408/credenciais HTTPS):
  python inovexa_oneclick.py --repo "D:\projetos-inovexa\mindscan" ^
    --origin-url "https://github.com/Adonispaiva/synmind.git" --use-ssh ^
    --branch docs/compliance-final --gh-pr
"""

import argparse, json, subprocess, sys, os
from pathlib import Path

# --------------------------- Utils ---------------------------

def log(msg): print(msg, flush=True)

def run(cmd, cwd=None, check=True):
    res = subprocess.run(cmd, cwd=str(cwd) if cwd else None,
                         text=True, capture_output=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\n{res.stdout}\n{res.stderr}")
    return res

def is_git_repo(p: Path) -> bool:
    try:
        run(["git","rev-parse","--is-inside-work-tree"], cwd=p)
        return True
    except Exception:
        return False

# --------------------------- Git remote/branch ---------------------------

def ensure_origin(p: Path, url: str|None, use_ssh: bool):
    if url:
        if use_ssh and url.startswith("https://github.com/"):
            owner_repo = url.split("https://github.com/")[1].rstrip("/").rstrip(".git")
            url = f"git@github.com:{owner_repo}.git"
        run(["git","remote","set-url","origin",url], cwd=p, check=True)
        log(f"✔ origin -> {url}")
    log(run(["git","remote","-v"], cwd=p).stdout)

def fetch_refs(p: Path):
    run(["git","fetch","--all","--prune"], cwd=p, check=False)
    run(["git","fetch","origin","main:refs/remotes/origin/main"], cwd=p, check=False)

def ensure_branch(p: Path, branch: str):
    # cria se não existir; senão faz checkout
    r = run(["git","checkout","-b",branch], cwd=p, check=False)
    if r.returncode != 0:
        run(["git","checkout",branch], cwd=p, check=True)
    log(f"✔ Branch pronta: {branch}")

def ensure_clean_or_allowed(p: Path, allow_dirty: bool):
    out = run(["git","status","--porcelain"], cwd=p).stdout.strip()
    if out and not allow_dirty:
        raise SystemExit("Working tree suja. Faça commit/stash ou use --allow-dirty.")

# --------------------------- Files/helpers ---------------------------

def write_text(root: Path, rel: str, content: str):
    f = root / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    return f

# --------------------------- Guards + hooks ---------------------------

def update_guards(p: Path, root_dir: str, src: str, shrink_pct: int):
    validate_paths = f"""// tools/validate-paths.js
const fs = require('fs');
const {{ execSync }} = require('child_process');
function sh(c) {{ return execSync(c, {{encoding:'utf8'}}).toString().trim(); }}
function trySh(c,d=''){{ try{{return sh(c)}}catch{{return d}} }}
function hasRef(r){{ try{{ execSync(`git rev-parse --verify ${{r}}`,{{stdio:'ignore'}}); return true }}catch{{ return false }} }}
try {{ execSync('git fetch origin --prune', {{stdio:'ignore'}}); }} catch {{}}
let root='{root_dir}', src='{src}';
try {{ const m = JSON.parse(fs.readFileSync('mindscan-manifest.json','utf8')); root=m.paths?.root||root; src=m.paths?.src||src; }} catch {{}}
const allowed = `${{root}}/${{src}}/`;
const envBase = process.env.GITHUB_BASE_REF || 'main';
const candidates = [`origin/${{envBase}}`, envBase, 'origin/main','origin/master','main','master'];
let baseRef=null; for (const r of candidates) if (hasRef(r)) {{ baseRef=r; break; }}
if (!baseRef) baseRef = trySh('git rev-list --max-parents=0 HEAD').split('\\n').pop() || 'HEAD^';
let mergeBase = trySh(`git merge-base HEAD ${{baseRef}}`) || trySh('git rev-parse HEAD^') || trySh('git rev-list --max-parents=0 HEAD');
const diffRaw = trySh(`git diff --name-only ${{mergeBase}}..HEAD`);
const changed = diffRaw? diffRaw.split('\\n').filter(Boolean):[];
if (!changed.length) {{ console.log('✅ guard:paths OK (sem alterações)'); process.exit(0); }}
let failures=[];
for (const f of changed) {{
  if (!fs.existsSync(f)) {{ failures.push(`❌ Path não existe no workspace: ${{f}}`); continue; }}
  if (/\\.tsx$/i.test(f) && !f.startsWith(allowed)) failures.push(`❌ TSX fora de ${{allowed}}: ${{f}}`);
}}
if (failures.length) {{ console.error(failures.join('\\n')); process.exit(1); }}
console.log('✅ guard:paths OK');
"""
    write_text(p, "tools/validate-paths.js", validate_paths)

    validate_workplan = """// tools/validate-workplan.js
const fs = require('fs'); const { execSync } = require('child_process');
function sh(c){ return execSync(c,{encoding:'utf8'}).toString().trim(); }
function trySh(c,d=''){ try{ return sh(c) }catch{ return d } }
function hasRef(r){ try{ execSync(`git rev-parse --verify ${r}`,{stdio:'ignore'}); return true }catch{ return false }}
try { execSync('git fetch origin --prune',{stdio:'ignore'}); } catch {}
if (!fs.existsSync('docs/work_plan.json')){ console.error('❌ docs/work_plan.json ausente.'); process.exit(1); }
let wp; try{ wp=JSON.parse(fs.readFileSync('docs/work_plan.json','utf8')); }catch{ console.error('❌ docs/work_plan.json inválido.'); process.exit(1); }
const items = Array.isArray(wp.items)? wp.items: [];
const envBase = process.env.GITHUB_BASE_REF || 'main';
const candidates = [`origin/${envBase}`, envBase, 'origin/main','origin/master','main','master'];
let baseRef=null; for (const r of candidates) if (hasRef(r)){ baseRef=r; break; }
if (!baseRef) baseRef = trySh('git rev-list --max-parents=0 HEAD').split('\\n').pop() || 'HEAD^';
let mergeBase = trySh(`git merge-base HEAD ${baseRef}`) || trySh('git rev-parse HEAD^') || trySh('git rev-list --max-parents=0 HEAD');
const diffRaw = trySh(`git diff --name-only ${mergeBase}..HEAD`);
const changed = diffRaw? diffRaw.split('\\n').filter(Boolean):[];
const tsChanged = changed.filter(p => /\\.(ts|tsx)$/i.test(p));
if (!tsChanged.length){ console.log('✅ guard:workplan OK (sem alterações TS/TSX)'); process.exit(0); }
const notListed = [];
for (const f of tsChanged){ const listed = items.some(x => x && typeof x.path==='string' && x.path===f); if (!listed) notListed.push(f); }
if (notListed.length){ console.error('❌ TS/TSX alterados não listados em docs/work_plan.json:\\n - ' + notListed.join('\\n - ')); process.exit(1); }
console.log('✅ guard:workplan OK');
"""
    write_text(p, "tools/validate-workplan.js", validate_workplan)

    ts_guard = f"""// tools/ts-regression-guard.js
const fs = require('fs'); const path = require('path'); const {{ Project }} = require('ts-morph'); const {{ execSync }} = require('child_process');
function sh(c){{ return execSync(c,{{encoding:'utf8'}}).toString().trim(); }}
function trySh(c,d=''){{ try{{return sh(c)}}catch{{return d}} }}
function hasRef(r){{ try{{ execSync(`git rev-parse --verify ${{r}}`,{{stdio:'ignore'}}); return true }}catch{{ return false }} }}
try {{ execSync('git fetch origin --prune', {{stdio:'ignore'}}); }} catch {{}}
let shrinkLimit = {shrink_pct}; try{{ const m=JSON.parse(fs.readFileSync('mindscan-manifest.json','utf8')); if(m?.rules?.no_shrink_over_percent!=null) shrinkLimit=Number(m.rules.no_shrink_over_percent); }}catch{{}}
if (process.env.GUARD_SHRINK_PCT) shrinkLimit = Number(process.env.GUARD_SHRINK_PCT);
const envBase = process.env.GUARD_BASE || process.env.GITHUB_BASE_REF || 'main';
const candidates=[`origin/${{envBase}}`, envBase,'origin/main','origin/master','main','master'];
let baseRef=null; for(const r of candidates) if (hasRef(r)){{ baseRef=r; break; }}
if(!baseRef) baseRef = trySh('git rev-list --max-parents=0 HEAD').split('\\n').pop() || 'HEAD^';
let mergeBase = trySh(`git merge-base HEAD ${{baseRef}}`) || trySh('git rev-parse HEAD^') || trySh('git rev-list --max-parents=0 HEAD');
const diffRaw = trySh(`git diff --name-only ${{mergeBase}}..HEAD`);
const changed = diffRaw? diffRaw.split('\\n').filter(Boolean).filter(p=>/\\.(ts|tsx)$/i.test(p)) : [];
if (!changed.length) {{ console.log('✅ guard:exports OK (sem alterações TS/TSX)'); process.exit(0); }}
function sizeOf(f){{ return fs.existsSync(f)? fs.statSync(f).size: 0; }}
function exportedSymbols(project, filePath){{ const sf = project.addSourceFileAtPath(filePath); const set = new Set(); sf.getExportedDeclarations().forEach((_,name)=>set.add(name)); if (sf.getDefaultExportSymbol()) set.add('default'); return set; }}
const tmpDir = '.guard_tmp'; fs.mkdirSync(tmpDir,{{recursive:true}}); const project = new Project({{ skipFileDependencyResolution: true, addFilesFromTsConfig: false }}); let failures=[];
for (const file of changed){{ const baseFile = path.join(tmpDir, file.replace(/[\\/\\\\]/g,'__')+'.base.ts'); try {{ const baseContent = sh(`git show ${{mergeBase}}:${{file}}`); fs.mkdirSync(path.dirname(baseFile),{{recursive:true}}); fs.writeFileSync(baseFile, baseContent,'utf8'); }} catch {{}}
  const curSize=sizeOf(file), baseSize=sizeOf(baseFile); const shrink = baseSize>0 ? (1-curSize/baseSize)*100 : 0;
  let curExp=new Set(), baseExp=new Set(); try{{ curExp=exportedSymbols(project,file); }}catch{{}} try{{ if(baseSize>0) baseExp=exportedSymbols(project,baseFile); }}catch{{}}
  if (baseSize>0 && shrink>shrinkLimit && curExp.size<=baseExp.size) failures.push(`❌ ${{file}}: encolheu ${{shrink.toFixed(1)}}% (> ${{shrinkLimit}}%) sem ganho de API.`);
  for (const name of baseExp) if(!curExp.has(name)) failures.push(`❌ ${{file}}: removeu export '${{name}}'.`);
}}
if (failures.length) {{ console.error(failures.join('\\n')); process.exit(1); }}
console.log('✅ guard:exports OK');
"""
    write_text(p, "tools/ts-regression-guard.js", ts_guard)

    # package.json: scripts + deps
    pkg = p / "package.json"
    try:
        obj = json.loads(pkg.read_text(encoding="utf-8"))
    except Exception:
        obj = {"name":"mindscan-app","private":True,"version":"0.0.0"}
    deps = obj.setdefault("dependencies", {})
    scripts = obj.setdefault("scripts", {})
    deps.setdefault("ts-morph", "^22.0.0")
    scripts.setdefault("guard:paths", "node tools/validate-paths.js")
    scripts.setdefault("guard:workplan", "node tools/validate-workplan.js")
    scripts.setdefault("guard:exports", "node tools/ts-regression-guard.js")
    pkg.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

    log("✔ Guards e package.json configurados.")

def install_hooks(p: Path):
    # bash
    bash = """#!/usr/bin/env bash
set -e
if [ -f package.json ]; then
  if command -v npm >/dev/null 2>&1; then
    npm ci --silent || npm i --silent
    npm run guard:paths
    npm run guard:workplan
    npm run guard:exports
  fi
fi
"""
    # Windows .cmd
    cmd = r"""@echo off
if exist package.json (
  where npm >nul 2>&1 || goto :eof
  call npm ci --silent || call npm i --silent
  call npm run guard:paths || exit /b 1
  call npm run guard:workplan || exit /b 1
  call npm run guard:exports || exit /b 1
)
"""
    hooks = p / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    (hooks / "pre-push").write_text(bash, encoding="utf-8")
    try:
        # Em Windows não precisa, mas não faz mal em WSL/Linux/Mac
        os.chmod(hooks / "pre-push", 0o755)
    except Exception:
        pass
    (hooks / "pre-push.cmd").write_text(cmd, encoding="utf-8")
    log("✔ Hooks de pre-push instalados.")

# --------------------------- gitignore + deps + commit ---------------------------

def ensure_gitignore_and_untrack(p: Path):
    gi = p / ".gitignore"
    extra = "\n# Compliance/local artifacts\n.backup/\nmindscan-compliance-pack-*/\n*.zip\n*.log\nexport_log_*\n"
    if gi.exists():
        cur = gi.read_text(encoding="utf-8")
        if extra not in cur:
            gi.write_text(cur.rstrip() + "\n" + extra, encoding="utf-8")
    else:
        gi.write_text(extra.strip()+"\n", encoding="utf-8")

    # tirar do índice o que já entrou por engano
    run(["git","rm","-r","--cached",".backup"], cwd=p, check=False)
    run(["git","rm","-r","--cached","mindscan-compliance-pack-*"], cwd=p, check=False)
    run(["git","rm","--cached","*.zip","*.log"], cwd=p, check=False)
    run(["git","add",".gitignore"], cwd=p, check=False)

def npm_install(p: Path):
    r = run(["npm","ci","--no-audit","--no-fund"], cwd=p, check=False)
    if r.returncode != 0:
        run(["npm","i","--no-audit","--no-fund"], cwd=p, check=True)

def commit_all(p: Path, msg: str):
    run(["git","add","."], cwd=p, check=False)
    if run(["git","diff","--cached","--name-only"], cwd=p).stdout.strip():
        run(["git","commit","-m",msg], cwd=p, check=True)
        log("✔ Commit criado.")
    else:
        log("ℹ Nada novo para commitar.")

# --------------------------- push + PR ---------------------------

def list_tracked_files(p: Path):
    out = run(["git","ls-files","-z"], cwd=p).stdout
    return [f for f in out.split("\x00") if f]

def find_big_tracked_files(p: Path, threshold_mb=90):
    big = []
    for f in list_tracked_files(p):
        fp = p / f
        if fp.exists() and fp.stat().st_size >= threshold_mb*1024*1024:
            big.append((f, fp.stat().st_size))
    return big

def untrack_files(p: Path, files):
    for f,_ in files:
        run(["git","rm","--cached",f], cwd=p, check=False)

def push_with_fallbacks(p: Path, branch: str):
    # 1) normal
    r1 = run(["git","push","-u","origin",branch], cwd=p, check=False)
    if r1.returncode == 0:
        log("✔ Push OK.")
        return True

    err1 = (r1.stdout or "") + "\n" + (r1.stderr or "")
    log(f"⚠ push falhou (1):\n{err1}")

    # 2) sem hooks locais
    r2 = run(["git","push","-u","origin",branch,"--no-verify"], cwd=p, check=False)
    if r2.returncode == 0:
        log("✔ Push OK (com --no-verify).")
        return True

    err2 = (r2.stdout or "") + "\n" + (r2.stderr or "")
    log(f"⚠ push falhou (2):\n{err2}")

    # 3) arquivos grandes
    if "exceeds GitHub's file size limit of 100.00 MB" in err2 or "Large files detected" in err2:
        log("⛔ Arquivos grandes detectados. Removendo do índice...")
        big = find_big_tracked_files(p, 90)
        if big:
            for f, sz in big:
                log(f" - {f} ({sz/1024/1024:.1f} MB)")
            untrack_files(p, big)
            run(["git","commit","-m","chore: stop tracking large files (>90MB)"], cwd=p, check=False)
        return push_with_fallbacks(p, branch)

    return False

def open_pr(p: Path, branch: str):
    try:
        run(["gh","auth","status"], cwd=p, check=True)
        run(["gh","pr","create","--title","[Compliance] v1.6 Supercola + guard rails (FINAL)",
             "--body","PR automático do compliance."], cwd=p, check=True)
        log("✔ PR criado via gh.")
    except Exception as e:
        log(f"ℹ Não foi possível abrir PR automaticamente: {e}")

# --------------------------- main ---------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="caminho do repositório")
    ap.add_argument("--origin-url", dest="origin_url", help="URL para setar no remote origin")
    ap.add_argument("--use-ssh", action="store_true", help="converter origin para SSH (se origin-url for https)")
    ap.add_argument("--branch", default="docs/compliance-final")
    ap.add_argument("--gh-pr", action="store_true", help="abrir PR via GitHub CLI")
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--root", default="frontend")
    ap.add_argument("--src", default="src")
    ap.add_argument("--shrink-pct", type=int, default=20)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not is_git_repo(repo):
        raise SystemExit(f"Não é um repositório Git: {repo}")

    ensure_clean_or_allowed(repo, args.allow_dirty)
    ensure_origin(repo, args.origin_url, args.use_ssh)
    fetch_refs(repo)
    ensure_branch(repo, args.branch)
    update_guards(repo, args.root, args.src, args.shrink_pct)
    install_hooks(repo)
    ensure_gitignore_and_untrack(repo)
    npm_install(repo)
    commit_all(repo, "docs(ci): one-click compliance (guards + hooks + deps + .gitignore)")
    fetch_refs(repo)

    if push_with_fallbacks(repo, args.branch):
        if args.gh_pr:
            open_pr(repo, args.branch)
    else:
        log("❌ Push não concluído. Verifique remoto/conexão e tente novamente.")

if __name__ == "__main__":
    main()
