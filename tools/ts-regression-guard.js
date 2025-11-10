// tools/ts-regression-guard.js
const fs = require('fs'); const path = require('path'); const { Project } = require('ts-morph'); const { execSync } = require('child_process');
function sh(c){ return execSync(c,{encoding:'utf8'}).toString().trim(); }
function trySh(c,d=''){ try{return sh(c)}catch{return d} }
function hasRef(r){ try{ execSync(`git rev-parse --verify ${r}`,{stdio:'ignore'}); return true }catch{ return false } }
try { execSync('git fetch origin --prune', {stdio:'ignore'}); } catch {}
let shrinkLimit = 20; try{ const m=JSON.parse(fs.readFileSync('mindscan-manifest.json','utf8')); if(m?.rules?.no_shrink_over_percent!=null) shrinkLimit=Number(m.rules.no_shrink_over_percent); }catch{}
if (process.env.GUARD_SHRINK_PCT) shrinkLimit = Number(process.env.GUARD_SHRINK_PCT);
const envBase = process.env.GUARD_BASE || process.env.GITHUB_BASE_REF || 'main';
const candidates=[`origin/${envBase}`, envBase,'origin/main','origin/master','main','master'];
let baseRef=null; for(const r of candidates) if (hasRef(r)){ baseRef=r; break; }
if(!baseRef) baseRef = trySh('git rev-list --max-parents=0 HEAD').split('\n').pop() || 'HEAD^';
let mergeBase = trySh(`git merge-base HEAD ${baseRef}`) || trySh('git rev-parse HEAD^') || trySh('git rev-list --max-parents=0 HEAD');
const diffRaw = trySh(`git diff --name-only ${mergeBase}..HEAD`);
const changed = diffRaw? diffRaw.split('\n').filter(Boolean).filter(p=>/\.(ts|tsx)$/i.test(p)) : [];
if (!changed.length) { console.log('✅ guard:exports OK (sem alterações TS/TSX)'); process.exit(0); }
function sizeOf(f){ return fs.existsSync(f)? fs.statSync(f).size: 0; }
function exportedSymbols(project, filePath){ const sf = project.addSourceFileAtPath(filePath); const set = new Set(); sf.getExportedDeclarations().forEach((_,name)=>set.add(name)); if (sf.getDefaultExportSymbol()) set.add('default'); return set; }
const tmpDir = '.guard_tmp'; fs.mkdirSync(tmpDir,{recursive:true}); const project = new Project({ skipFileDependencyResolution: true, addFilesFromTsConfig: false }); let failures=[];
for (const file of changed){ const baseFile = path.join(tmpDir, file.replace(/[\/\\]/g,'__')+'.base.ts'); try { const baseContent = sh(`git show ${mergeBase}:${file}`); fs.mkdirSync(path.dirname(baseFile),{recursive:true}); fs.writeFileSync(baseFile, baseContent,'utf8'); } catch {}
  const curSize=sizeOf(file), baseSize=sizeOf(baseFile); const shrink = baseSize>0 ? (1-curSize/baseSize)*100 : 0;
  let curExp=new Set(), baseExp=new Set(); try{ curExp=exportedSymbols(project,file); }catch{} try{ if(baseSize>0) baseExp=exportedSymbols(project,baseFile); }catch{}
  if (baseSize>0 && shrink>shrinkLimit && curExp.size<=baseExp.size) failures.push(`❌ ${file}: encolheu ${shrink.toFixed(1)}% (> ${shrinkLimit}%) sem ganho de API.`);
  for (const name of baseExp) if(!curExp.has(name)) failures.push(`❌ ${file}: removeu export '${name}'.`);
}
if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
console.log('✅ guard:exports OK');
