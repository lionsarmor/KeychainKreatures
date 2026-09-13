// Remove only top-level via objects named by current KiCad dangling-via DRC.
// File roundtrip avoids KiCad 10 SWIG ownership bugs in BOARD.Remove(via).
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const file=path.join(root,'routing/KK_main_module_C2_candidate.kicad_pcb');
const d=JSON.parse(fs.readFileSync(path.join(root,'routing/candidate_drc.json')));
const ids=new Set(d.violations.filter(v=>v.type==='via_dangling').flatMap(v=>v.items.map(i=>i.uuid)));
const s=fs.readFileSync(file,'utf8'),tokens=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;
function parse(){const a=[];if(tokens[i++]!=='(')throw Error('syntax');while(tokens[i]!==')')a.push(tokens[i]==='('?parse():tokens[i++]);i++;return a;}
const a=parse();if(i!==tokens.length)throw Error('trailing input');
const val=s=>s?.startsWith('"')?JSON.parse(s):s;
let count=0;const filtered=a.filter(x=>{
 if(!Array.isArray(x)||x[0]!=='via')return true;
 const uuid=x.find(y=>Array.isArray(y)&&y[0]==='uuid');
 if(uuid&&ids.has(val(uuid[1]))){count++;return false;}return true;
});
if(count!==ids.size)throw Error('DRC via IDs do not match candidate');
const dump=x=>Array.isArray(x)?'('+x.map(dump).join(' ')+')':x;
fs.writeFileSync(file,dump(filtered)+'\n');console.log('Removed '+count+' redundant vias; subsequent DRC must confirm connectivity.');
