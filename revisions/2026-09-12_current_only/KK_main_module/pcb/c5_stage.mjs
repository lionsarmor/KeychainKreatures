// Preserve C.4; create a separate unrouted C.5 engineering workspace.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url))),out=path.join(root,'C5_relayout');
fs.mkdirSync(out,{recursive:true});
const backup=path.join(root,'pcb/backups/pre_c5_relayout');
if(!fs.existsSync(backup)){fs.mkdirSync(backup,{recursive:true});for(const n of ['KK_main_module.kicad_pcb','KK_main_module.kicad_sch','KK_main_module.kicad_pro','KK_main_module.kicad_dru'])fs.copyFileSync(path.join(root,n),path.join(backup,n));}
for(const n of ['KK_Main.pretty','3dmodels','KK_Main.kicad_sym','fp-lib-table','sym-lib-table'])if(!fs.existsSync(path.join(out,n)))fs.symlinkSync('../'+n,path.join(out,n));
for(const ext of ['kicad_pro','kicad_dru','kicad_sch'])if(!fs.existsSync(path.join(out,'KK_main_module.'+ext)))fs.copyFileSync(path.join(backup,'KK_main_module.'+ext),path.join(out,'KK_main_module.'+ext));
const s=fs.readFileSync(path.join(backup,'KK_main_module.kicad_pcb'),'utf8'),t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;
function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')')a.push(t[i]==='('?p():t[i++]);i++;return a;}
const b=p(),drop=new Set(['segment','via','zone','gr_line','gr_arc','gr_rect','gr_poly','gr_text','dimension']),dump=a=>Array.isArray(a)?'('+a.map(dump).join(' ')+')':a;
const small=new Set([...Array.from({length:18},(_,i)=>'R'+(i+1)),'R20','R22','R26','R29','R41','R42','R43']);
const staged=b.filter(e=>!Array.isArray(e)||!drop.has(e[0]));
fs.writeFileSync(path.join(out,'C5_blank.kicad_pcb'),dump(staged)+'\n');
fs.writeFileSync(path.join(out,'upright_refs.json'),JSON.stringify([...small]));
console.log('C.4 protected; C.5 candidate has footprints/nets but no stale routes, zones or drawing labels.');
