// C.5 placement ECO: exact same values/nets, documented resistor/IR lead forms.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url))),out=path.join(root,'C5_relayout');
const refs=new Set(JSON.parse(fs.readFileSync(path.join(out,'upright_refs.json'))));
const s=fs.readFileSync(path.join(root,'pcb/backups/pre_c5_relayout/KK_main_module.kicad_sch'),'utf8'),t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;
function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')')a.push(t[i]==='('?p():t[i++]);i++;return a;}
const b=p(),val=s=>s?.startsWith('"')?JSON.parse(s):s,kids=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k),dump=a=>Array.isArray(a)?'('+a.map(dump).join(' ')+')':a;
for(const a of kids(b,'symbol')){
 const props=kids(a,'property'),get=n=>props.find(p=>val(p[1])===n),r=val(get('Reference')?.[2]);
 if(refs.has(r))get('Footprint')[2]=JSON.stringify('KK_Main:MFR25_Upright_P2p54');
 if(r==='D1')get('Footprint')[2]=JSON.stringify('KK_Main:TSAL6200_C5_EdgeFormed');
}
let text=dump(b).replaceAll('C.4','C.5').replace('Socketed upper-right RGB + populated 3D','Landscape screen / rear MCU / compact through-hole placement');
fs.writeFileSync(path.join(out,'KK_main_module.kicad_sch'),text+'\n');
console.log('C.5 schematic: 26 footprint assignments updated, values/nets retained.');
