// tools/validate-paths.js
const fs = require('fs');
const { execSync } = require('child_process');
function sh(c) { return execSync(c, {encoding:'utf8'}).toString().trim(); }
function trySh(c,d=''){ try{return sh(c)}catch{return d} }
function hasRef(r){ try{ execSync(`git rev-parse --verify ${r}`,{stdio:'ignore'}); return true }catch{ return false } }
try { execSync('git fetch origin --prune', {stdio:'ignore'}); } catch {}
let root='frontend', src='src';
try { const m = JSON.parse(fs.readFileSync('mindscan-manifest.json','utf8')); root=m.paths?.root||root; src=m.paths?.src||src; } catch {}
const allowed = `${root}/${src}/`;
const envBase = process.env.GITHUB_BASE_REF || 'main';
const candidates = [`origin/${envBase}`, envBase, 'origin/main','origin/master','main','master'];
let baseRef=null; for (const r of candidates) if (hasRef(r)) { baseRef=r; break; }
if (!baseRef) baseRef = trySh('git rev-list --max-parents=0 HEAD').split('\n').pop() || 'HEAD^';
let mergeBase = trySh(`git merge-base HEAD ${baseRef}`) || trySh('git rev-parse HEAD^') || trySh('git rev-list --max-parents=0 HEAD');
const diffRaw = trySh(`git diff --name-only ${mergeBase}..HEAD`);
const changed = diffRaw? diffRaw.split('\n').filter(Boolean):[];
if (!changed.length) { console.log('✅ guard:paths OK (sem alterações)'); process.exit(0); }
let failures=[];
for (const f of changed) {
  if (!fs.existsSync(f)) { failures.push(`❌ Path não existe no workspace: ${f}`); continue; }
  if (/\.tsx$/i.test(f) && !f.startsWith(allowed)) failures.push(`❌ TSX fora de ${allowed}: ${f}`);
}
if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
console.log('✅ guard:paths OK');
