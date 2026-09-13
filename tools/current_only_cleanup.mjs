// Guarded one-time current-revision promotion. No CAD edits or Git mutations.
// Default is a read-only plan. Run --apply only after KiCad is fully closed.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const archive='revisions/2026-09-12_current_only';
const abs=p=>path.join(root,p);
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(abs(p))).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(abs(p),'utf8'));
const exists=p=>{try{fs.lstatSync(abs(p));return true;}catch{return false;}};
const assert=(v,m)=>{if(!v)throw Error(m);};
assert(!exists(archive),'Cleanup archive already exists; do not rerun');
const index=read('docs/C6_P3_RELEASE_INDEX.json');
const sources={main:'KK_main_module/C6_flat_stack',power:'KK_power_module/P3_matching_stack'};
const plans=[];
const plan=(from,to)=>{assert(exists(from),'Missing source '+from);assert(!exists(to),'Destination exists '+to);plans.push({from,to});};
const mainKeep=new Set(['KK_main_module.kicad_pcb','KK_main_module.kicad_sch','KK_main_module.kicad_pro','KK_main_module.kicad_dru','KK_Main.pretty','KK_Main.kicad_sym','3dmodels','fp-lib-table','sym-lib-table','assembly','datasheets','reports','release_checks','README.md','FABRICATION_REQUIREMENTS.md','SOURCE_BASELINE.json','component_changes.json','netlist.xml']);
const powerKeep=new Set(['KK_power_module.kicad_pcb','KK_power_module.kicad_sch','KK_power_module.kicad_pro','KK_Power.pretty','KK_Power.kicad_sym','3dmodels','fp-lib-table','sym-lib-table','assembly','datasheets','reports','release_checks','README.md','FABRICATION_REQUIREMENTS.md','SOURCE_BASELINE.json','design.json','electrical_screening.json','netlist.xml']);
// First clear the old module roots, keeping issued manufacturing packages intact.
for(const [module,current] of [['KK_main_module','C6_flat_stack'],['KK_power_module','P3_matching_stack']]){
  for(const name of fs.readdirSync(abs(module)).sort()){
    if(name===current||name==='manufacturing')continue;
    plan(`${module}/${name}`,`${archive}/${module}/${name}`);
  }
}
// Promotion targets exist now but are cleared by the preceding moves.
for(const [kind,module,keep] of [['main','KK_main_module',mainKeep],['power','KK_power_module',powerKeep]]){
  for(const name of fs.readdirSync(abs(sources[kind])).sort()){
    const from=`${sources[kind]}/${name}`;
    const to=keep.has(name)?`${module}/${name}`:`${archive}/intermediate/${kind}/${name}`;
    if(exists(to))assert(plans.some(p=>p.from===to),'Unplanned collision '+to);
    plans.push({from,to});
  }
}
const mainOldReports=['copper.json','drc_routed.json','drc_widths_restored.json','freerouting.log','silkscreen_labels.json'];
for(const n of mainOldReports)assert(exists(`${sources.main}/reports/${n}`),'Missing intermediate report '+n);
for(const name of fs.readdirSync(abs('docs')).sort()){
  if(name==='source_material'||name==='CLEANUP_REPORT.md'||name.startsWith('POWER_')||/^C6_P3_STACK_REVIEW-\d+\.(pdf|svg)$/.test(name))plan('docs/'+name,archive+'/docs/'+name);
}
const keptTools=new Set(['README.md','check_project.mjs','github_preflight.mjs','flat_stack_audit.py','flat_stack_fit.py','flat_stack_report.py','stack_release_native.py','current_only_cleanup.mjs']);
for(const name of fs.readdirSync(abs('tools')).sort())if(!keptTools.has(name))plan('tools/'+name,archive+'/tools/'+name);
const protectedFiles={};
for(const b of index.boards){
  assert(b.source===sources[b.kind],'Unexpected current release source');
  const ver=read(b.directory+'/RELEASE_VERIFICATION.json');
  for(const [n,h] of Object.entries(ver.source_sha256)){
    assert(sha(b.source+'/'+n)===h,'CAD edited since release: '+n);
    protectedFiles[(b.kind==='main'?'KK_main_module/':'KK_power_module/')+n]=h;
  }
  assert(sha(b.zip)===b.zip_sha256&&sha(b.gerbers_zip)===b.gerbers_sha256,'Release ZIP changed');
  protectedFiles[b.zip]=b.zip_sha256;protectedFiles[b.gerbers_zip]=b.gerbers_sha256;
}
console.log(JSON.stringify({scope:'Relocation only; current CAD and issued packages protected',archive,planned_path_moves:plans.length,promote:sources,protected_files:Object.keys(protectedFiles).length,apply:process.argv.includes('--apply')},null,2));
if(!process.argv.includes('--apply'))process.exit(0);
const processes=execFileSync('ps',['-eo','comm=']).toString().split('\n').map(s=>s.trim());
assert(!processes.some(s=>['kicad','pcbnew','eeschema'].includes(s)),'Close KiCad completely before promotion to prevent a stale save overwriting C6');
fs.mkdirSync(abs(archive),{recursive:true});
const records=[];
function inventory(from,to){
  const stat=fs.lstatSync(abs(from));
  if(stat.isSymbolicLink())return [{from,to,type:'symlink',target:fs.readlinkSync(abs(from))}];
  if(stat.isFile())return [{from,to,type:'file',sha256:sha(from)}];
  return fs.readdirSync(abs(from)).sort().flatMap(n=>inventory(from+'/'+n,to+'/'+n));
}
function move(from,to){
  assert(exists(from)&&!exists(to),'Move precondition failed: '+from+' -> '+to);
  const list=inventory(from,to);fs.mkdirSync(path.dirname(abs(to)),{recursive:true});fs.renameSync(abs(from),abs(to));
  for(const f of list)assert(f.type==='file'?sha(f.to)===f.sha256:fs.readlinkSync(abs(f.to))===f.target,'Move corrupted '+f.to);
  records.push(...list);
  // Persist recovery data after every successful move.
  fs.writeFileSync(abs(archive+'/MOVE_MANIFEST.json'),JSON.stringify({state:'moving',files:records},null,2)+'\n');
}
for(const p of plans)move(p.from,p.to);
for(const n of mainOldReports)move('KK_main_module/reports/'+n,archive+'/intermediate/main/reports/'+n);
// Remove ONLY empty old current-revision directory shells, no recursive deletion.
for(const p of Object.values(sources)){assert(fs.readdirSync(abs(p)).length===0,'Nonempty old source directory');fs.rmdirSync(abs(p));}
for(const [kind,module] of [['main','KK_main_module'],['power','KK_power_module']]){
  const baseline=module+'/SOURCE_BASELINE.json';
  const original=read(baseline);const snap=archive+'/metadata/'+kind+'_SOURCE_BASELINE.json';
  fs.mkdirSync(path.dirname(abs(snap)),{recursive:true});fs.copyFileSync(abs(baseline),abs(snap));
  records.push({from:baseline,to:snap,type:'file',sha256:sha(snap),operation:'metadata snapshot'});
  const translated={};
  for(const [p,h] of Object.entries(original)){
    const target=archive+'/'+p;assert(sha(target)===h,'Baseline not preserved '+target);translated[target]=h;
  }
  fs.writeFileSync(abs(baseline),JSON.stringify(translated,null,2)+'\n');
}
// A relocation index changes current paths, not historical issued snapshot metadata.
fs.copyFileSync(abs('docs/C6_P3_RELEASE_INDEX.json'),abs(archive+'/metadata/C6_P3_RELEASE_INDEX_before_cleanup.json'));
for(const b of index.boards)b.source=b.kind==='main'?'KK_main_module':'KK_power_module';
index.current_location_note='Current CAD promoted to module roots; source_project paths inside issued packages record their original release locations. Package and CAD bytes unchanged.';
index.cleanup_archive=archive;
fs.writeFileSync(abs('docs/C6_P3_RELEASE_INDEX.json'),JSON.stringify(index,null,2)+'\n');
for(const [p,h] of Object.entries(protectedFiles))assert(sha(p)===h,'Protected CAD/output changed '+p);
// Update active text links mechanically; never rewrite archived or issued files.
const editable=['README.md','START_HERE.md','CONTRIBUTING.md','CHANGELOG.md','docs/README.md','docs/FLAT_STACK_REWORK.md','tools/README.md','tools/flat_stack_audit.py','tools/flat_stack_fit.py','tools/flat_stack_report.py','tools/stack_release_native.py'];
for(const p of editable){
  const old=fs.readFileSync(abs(p),'utf8');
  const next=old.replaceAll('KK_main_module/C6_flat_stack','KK_main_module').replaceAll('KK_power_module/P3_matching_stack','KK_power_module');
  if(next!==old)fs.writeFileSync(abs(p),next);
}
const final={state:'complete',scope:'Archive superseded content and promote current C6/P3 without changing circuits or issued fabrication files',files:records,protected_current_files:protectedFiles,current_sources:{main:'KK_main_module',power:'KK_power_module'},note:'Archived relative compatibility links retain their original text; recover historical trees using the move map. Active code/docs are updated separately. No commit or push performed.'};
fs.writeFileSync(abs(archive+'/MOVE_MANIFEST.json'),JSON.stringify(final,null,2)+'\n');
console.log(JSON.stringify({status:'PROMOTED; documentation finalization/checks still required',moved_files:records.length,protected_files:Object.keys(protectedFiles).length},null,2));
