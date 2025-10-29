// tools/validate-workplan.js
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
if (!baseRef) baseRef = trySh('git rev-list --max-parents=0 HEAD').split('\n').pop() || 'HEAD^';
let mergeBase = trySh(`git merge-base HEAD ${baseRef}`) || trySh('git rev-parse HEAD^') || trySh('git rev-list --max-parents=0 HEAD');
const diffRaw = trySh(`git diff --name-only ${mergeBase}..HEAD`);
const changed = diffRaw? diffRaw.split('\n').filter(Boolean):[];
const tsChanged = changed.filter(p => /\.(ts|tsx)$/i.test(p));
if (!tsChanged.length){ console.log('✅ guard:workplan OK (sem alterações TS/TSX)'); process.exit(0); }
const notListed = [];
for (const f of tsChanged){ const listed = items.some(x => x && typeof x.path==='string' && x.path===f); if (!listed) notListed.push(f); }
if (notListed.length){ console.error('❌ TS/TSX alterados não listados em docs/work_plan.json:\n - ' + notListed.join('\n - ')); process.exit(1); }
console.log('✅ guard:workplan OK');
