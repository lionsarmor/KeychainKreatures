import fs from 'node:fs';
import {createHash} from 'node:crypto';
const [before,after,result]=process.argv.slice(2);
if(!result)throw Error('Usage: node check_redraw.mjs BEFORE.net AFTER.net RESULT.json');
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){let a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')'){if(i>=t.length)throw Error('EOF');a.push(t[i]==='('?p():t[i++]);}i++;return a;}const a=p();if(i!==t.length)throw Error('trailing tokens');return a;}
const kids=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k),ch=(a,k)=>kids(a,k)[0];
const v=s=>s.startsWith('"')?JSON.parse(s):s;
function load(file){const a=parse(fs.readFileSync(file,'utf8'));const components=kids(ch(a,'components'),'comp').map(c=>({ref:v(ch(c,'ref')[1]),value:v(ch(c,'value')[1]),footprint:ch(c,'footprint')?.[1]||'',fields:kids(ch(c,'fields')||[],'field').filter(f=>v(ch(f,'name')[1])==='MPN').map(f=>v(f.at(-1)))})).filter(c=>!c.ref.startsWith('#')).sort((a,b)=>a.ref.localeCompare(b.ref));
const nets=kids(ch(a,'nets'),'net').map(net=>kids(net,'node').map(node=>v(ch(node,'ref')[1])+':'+v(ch(node,'pin')[1])).filter(p=>!p.startsWith('#')).sort()).filter(n=>n.length).sort((a,b)=>a.join('|').localeCompare(b.join('|')));return{components,nets};}
const a=load(before),b=load(after);
if(JSON.stringify(a.components)!==JSON.stringify(b.components))throw Error('Component identity/value/footprint changed');
if(JSON.stringify(a.nets)!==JSON.stringify(b.nets)){const old=new Set(a.nets.map(q=>q.join('|'))),fresh=new Set(b.nets.map(q=>q.join('|')));console.error('Lost/changed',a.nets.filter(n=>!fresh.has(n.join('|'))));console.error('Added/changed',b.nets.filter(n=>!old.has(n.join('|'))));throw Error('Connectivity changed');}
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const output={status:'PASS: component identities and all pin-to-pin net partitions preserved',components:b.components.length,pin_records:b.nets.flat().length,nets:b.nets.length,before_sha256:hash(before),after_sha256:hash(after)};
fs.writeFileSync(result,JSON.stringify(output,null,2)+'\n');console.log(output);
