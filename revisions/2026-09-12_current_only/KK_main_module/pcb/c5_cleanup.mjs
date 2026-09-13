// Remove only native-DRC identified one-layer redundant vias. Preserve a snapshot.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url))),out=path.join(root,'C5_relayout'),file=path.join(out,'KK_main_module.kicad_pcb');
const d=JSON.parse(fs.readFileSync(path.join(out,'repair_drc.json')));
if(d.unconnected_items.length||d.schematic_parity.length||d.violations.some(v=>v.type!=='via_dangling'))throw Error('Unexpected pending DRC; inspect first');
const ids=new Set(d.violations.map(v=>v.items[0].uuid));if(ids.size!==2)throw Error('Expected exactly two one-layer redundant vias');
if(!fs.existsSync(path.join(out,'C5_before_cleanup.kicad_pcb')))fs.copyFileSync(file,path.join(out,'C5_before_cleanup.kicad_pcb'));
const s=fs.readFileSync(file,'utf8'),t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;
function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')')a.push(t[i]==='('?p():t[i++]);i++;return a;}
const b=p(),dump=a=>Array.isArray(a)?'('+a.map(dump).join(' ')+')':a;let removed=0;
const result=b.filter(a=>{if(Array.isArray(a)&&a[0]==='via'){const u=a.find(n=>Array.isArray(n)&&n[0]==='uuid');if(u&&ids.has(JSON.parse(u[1]))){removed++;return false;}}return true;});
if(removed!==2)throw Error('UUID mismatch');
fs.writeFileSync(file,dump(result).replace('C.5 UNROUTED - DO NOT FABRICATE','C.5 ENGINEERING PROTOTYPE - HARDWARE TESTS PENDING')+'\n');
fs.writeFileSync(path.join(out,'CLEANUP.json'),JSON.stringify({removed_redundant_via_uuids:[...ids],recovery:'C5_before_cleanup.kicad_pcb',ground_pads_using_existing_explicit_tracks:['Q2:1','R20:2','U1:16','C7:2']},null,2));
