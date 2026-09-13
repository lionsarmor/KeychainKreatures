// Remove only the four recorded C.3 LED branches from a protected snapshot.
// Text-based editing avoids KiCad SWIG ownership issues during track deletion.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')')a.push(t[i]==='('?p():t[i++]);i++;return a;}return p();}
const val=s=>s?.startsWith('"')?JSON.parse(s):s, kids=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k),get=(a,k)=>kids(a,k)[0],dump=a=>Array.isArray(a)?'('+a.map(dump).join(' ')+')':a;
const board=parse(fs.readFileSync(path.join(root,'pcb/backups/pre_c4_top_rgb/KK_main_module.kicad_pcb'),'utf8'));
const nets=new Map(kids(board,'net').map(n=>[n[1],val(n[2])])),key=p=>p.map(x=>(+x).toFixed(6)).join(','),lines=new Set(),vias=new Set();
const net=e=>nets.get(get(e,'net')[1])||val(get(e,'net')[1]);
const routes=JSON.parse(fs.readFileSync(path.join(root,'routing/C3_RGB_ROUTES.json')));
for(const i of [4,5,6,7]){const r=routes[i];for(let j=1;j<r.path.length;j++){const a=r.path[j-1],b=r.path[j];if(a[0]===b[0]){if(key(a)===key(b))continue;lines.add([r.net,a[0],key(a.slice(1)),key(b.slice(1))].join('|'));}else vias.add(r.net+'|'+key(a.slice(1)));}}
let removed=0;
const staged=board.filter(e=>{if(!Array.isArray(e))return true;
 if(e[0]==='segment'){const n=net(e),l=val(get(e,'layer')[1])==='F.Cu'?0:1,a=key(get(e,'start').slice(1)),b=key(get(e,'end').slice(1));if(lines.has([n,l,a,b].join('|'))||lines.has([n,l,b,a].join('|'))){removed++;return false;}}
 if(e[0]==='via'&&vias.has(net(e)+'|'+key(get(e,'at').slice(1)))){removed++;return false;}return true;});
if(removed!==lines.size+vias.size)throw Error('Removal count mismatch '+removed+' '+(lines.size+vias.size));
const detourPath=path.join(root,'routing/C4_CLEARANCE_DETOURS.json');
const detourIds=new Set(fs.existsSync(detourPath)?JSON.parse(fs.readFileSync(detourPath)).removed.map(t=>t.uuid):[]);
const final=staged.filter(e=>!(Array.isArray(e)&&e[0]==='segment'&&detourIds.has(val(get(e,'uuid')[1]))));
if(staged.length-final.length!==detourIds.size)throw Error('Detour removal mismatch');
fs.writeFileSync(path.join(root,'routing/KK_main_module_C4_stage.kicad_pcb'),dump(final)+'\n');
console.log('Removed only',removed,'recorded LED route segments/vias; remaining routes preserved.');
