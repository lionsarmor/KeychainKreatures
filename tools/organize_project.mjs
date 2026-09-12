// One-time, reversible file moves. No CAD regeneration, deletion or routing.
// Dry-run by default; --apply records every moved file and verifies its hash.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const archive='revisions/2026-09-11_cleanup';
const full=p=>path.join(root,p);
const exists=p=>fs.existsSync(full(p));
const moves=[];
function move(from,to=`${archive}/${from}`,alias=false){
  if(exists(from)) moves.push({from,to,alias});
}
for(const name of ['KC NOTES.txt','WIRING DIAGRAM.odt','Keychain_Kreatures_Main_PCB_Astra_Specification.docx']) move(name,`docs/source_material/${name}`);
// Keep the authoritative P.2 project in place, including all local CAD assets.
for(const name of fs.readdirSync(full('KK_power_module'))){
  if(!['P2_compact','CURRENT_STATUS.md'].includes(name)) move(`KK_power_module/${name}`);
}
for(const name of ['.history','archive','pcb/backups','schematic'])
  move(`KK_main_module/${name}`,undefined,['archive','pcb/backups','schematic'].includes(name));
move('KK_main_module/routing');
const historicalDocs=['ARCHITECTURE.md','BOARD_FIRST_PLAN.md','BUDGET_PARTS_LIST.md','C2_PROTOTYPE_REPORT.md','C3_CHECKPOINT_REPORT.md','C3_PROTOTYPE_REPORT.md','C4_PROTOTYPE_REPORT.md','CHANGELOG.md','COMPONENT_DECISIONS.md','COST_ESTIMATE.md','DESIGN_BRIEF.md','DESIGN_REVIEW.md','ENTIRE_KIT_PARTS.md','INTEGRATED_THT_POWER_REVISION.md','io_requirements.csv','kit_component_selection.csv'];
for(const name of historicalDocs) move(`KK_main_module/${name}`);
for(const name of fs.readdirSync(full('KK_main_module/assembly'))){
  // C.5 still explicitly uses the C.4 datasheet packet; retain those sources.
  if(/^C[234]_/.test(name)&&!/^C4_DATASHEET/.test(name)) move(`KK_main_module/assembly/${name}`);
}
for(const name of fs.readdirSync(full('KK_main_module/pcb'))){
  // Retain code: current C.5 tools import earlier geometry/model helper code.
  if((/^c[234][_-]/i.test(name)||name==='KK_main_module_C4_assembly.step'||name==='__pycache__')&&!/\.(py|mjs)$/.test(name)) move(`KK_main_module/pcb/${name}`);
}
for(const name of fs.readdirSync(full('KK_power_module/P2_compact'))){
  if(/^P2_.*\.(kicad_pcb|dsn|ses)$/.test(name)||name==='LOCAL_ROUTES.json') move(`KK_power_module/P2_compact/${name}`);
}
const manifest=`${archive}/MOVE_MANIFEST.json`;
if(exists(manifest)) throw Error('Cleanup already recorded. Do not rerun; consult the manifest.');
for(const m of moves){
  if(exists(m.to)) throw Error(`Destination already exists: ${m.to}`);
  if(fs.lstatSync(full(m.from)).isSymbolicLink()) throw Error(`Unexpected source symlink: ${m.from}`);
}
const digest=p=>crypto.createHash('sha256').update(fs.readFileSync(full(p))).digest('hex');
function files(p){
  const s=fs.lstatSync(full(p));
  if(s.isSymbolicLink()) return [{path:p,symlink:fs.readlinkSync(full(p))}];
  if(s.isDirectory()) return fs.readdirSync(full(p)).flatMap(n=>files(`${p}/${n}`));
  return [{path:p,sha256:digest(p)}];
}
const protectedFiles=[...files('KK_main_module'),...files('KK_power_module/P2_compact')]
  .filter(f=>!moves.some(m=>f.path===m.from||f.path.startsWith(m.from+'/')))
  .filter(f=>/\.(kicad_pcb|kicad_sch|kicad_pro|kicad_mod|kicad_sym|wrl|step)$/.test(f.path)||/lib-table$/.test(f.path));
console.log(JSON.stringify({move_count:moves.length,moves,protected_file_count:protectedFiles.length},null,2));
if(!process.argv.includes('--apply')) process.exit(0);
fs.mkdirSync(full(archive),{recursive:true});
const log={date:new Date().toISOString(),status:'IN_PROGRESS',moves:[],protectedFiles};
const save=()=>fs.writeFileSync(full(manifest),JSON.stringify(log,null,2)+'\n');
save();
for(const m of moves){
  const entries=files(m.from);
  const record={...m,files:entries,status:'PLANNED'}; log.moves.push(record); save();
  fs.mkdirSync(path.dirname(full(m.to)),{recursive:true});
  fs.renameSync(full(m.from),full(m.to));
  if(m.alias) fs.symlinkSync(path.relative(path.dirname(full(m.from)),full(m.to)),full(m.from),'dir');
  for(const e of entries){
    const target=m.to+e.path.slice(m.from.length);
    if(e.sha256&&digest(target)!==e.sha256) throw Error(`Moved file hash mismatch: ${target}`);
    if(e.symlink&&fs.readlinkSync(full(target))!==e.symlink) throw Error(`Symlink changed: ${target}`);
  }
  record.status='MOVED_AND_VERIFIED'; save();
}
for(const f of protectedFiles) if(f.sha256&&digest(f.path)!==f.sha256) throw Error(`Active source changed: ${f.path}`);
log.status='COMPLETE';save();
console.log(`Verified ${log.moves.length} moves; ${protectedFiles.length} active CAD/library/model files unchanged. Nothing deleted.`);
