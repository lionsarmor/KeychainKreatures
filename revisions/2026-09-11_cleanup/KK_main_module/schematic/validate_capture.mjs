import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const dir=path.dirname(fileURLToPath(import.meta.url));
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){let a=[];if(t[i++]!=='(')throw Error('parse');while(t[i]!==')'){if(i>=t.length)throw Error('EOF');a.push(t[i]==='('?p():t[i++]);}i++;return a;}const a=p();if(i!==t.length)throw Error('trailing tokens');return a;}
const v=s=>s?.startsWith('"')?JSON.parse(s):s;
const ch=(a,k)=>a.find(x=>Array.isArray(x)&&x[0]===k);
const kids=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k);
const capture=JSON.parse(fs.readFileSync(path.join(dir,'capture.json'),'utf8'));
const netlist=parse(fs.readFileSync(path.join(dir,'KK_main_module.net'),'utf8'));
const actual=new Map();
for(const net of kids(ch(netlist,'nets'),'net')){const name=v(ch(net,'name')[1]);for(const node of kids(net,'node')){const key=v(ch(node,'ref')[1])+':'+v(ch(node,'pin')[1]);if(actual.has(key))throw Error('Pin on multiple nets '+key);actual.set(key,name);}}
let checked=0;
for(const c of capture.components.filter(c=>!c.ref.startsWith('#'))){for(const [pin,net] of Object.entries(c.nets)){const a=actual.get(c.ref+':'+pin);if(net===null){if(a&&!a.startsWith('unconnected-'))throw Error('NC joined '+c.ref+':'+pin);}else if(a!==net)throw Error(`Mismatch ${c.ref}:${pin}: ${a} != ${net}`);checked++;}}
const assert=(yes,msg)=>{if(!yes)throw Error(msg)};
const at=(ref,pin)=>actual.get(ref+':'+pin);
for(let i=1;i<=9;i++){assert(at('SW'+i,'A')===at('SW'+i,'B'),'button pair A/B');assert(at('SW'+i,'C')===at('SW'+i,'D'),'button pair C/D');assert(at('SW'+i,'A')!==at('SW'+i,'C'),'button permanently shorted');}
assert(at('J2','7')!==at('J3','2'),'SPI CS collision');
assert(at('J2','3')===at('J3','4')&&at('J2','4')===at('J3','3'),'SPI sharing');
assert(at('J5','1')==='SPK_P'&&at('J5','2')==='SPK_N','bridge speaker must float');
assert(at('D2','1')==='ACT_3V2'&&at('D2','2')==='MOTOR_RETURN','flyback polarity');
assert(at('Q4','1')==='GND'&&at('Q4','2')==='MOTOR_GATE'&&at('Q4','3')==='MOTOR_RETURN','MOSFET pinout');
assert(at('MOD1','3').startsWith('unconnected-'),'do not parallel 3.3V regulators');
assert(at('MOD1','6').startsWith('unconnected-'),'do not externally load GPIO3 strap');
const erc=JSON.parse(fs.readFileSync(path.join(dir,'ERC.json'),'utf8'));
const violations=erc.sheets.flatMap(s=>s.violations);assert(violations.length===0,'ERC not clean');
// Complex nodal AC solution of the CAPTURED audio passive ladder only.
// This is not an ESP32, amplifier, speaker, radio, SD or motor behavioral model.
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]], sub=(a,b)=>[a[0]-b[0],a[1]-b[1]];
const mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
const div=(a,b)=>{const d=b[0]**2+b[1]**2;return[(a[0]*b[0]+a[1]*b[1])/d,(a[1]*b[0]-a[0]*b[1])/d]};
const abs=a=>Math.hypot(...a);
const nodes=['AUDIO_LP1','AUDIO_LP2','AUDIO_AC','AMP_IN'];
const scale={k:1e3,n:1e-9,u:1e-6};
const number=s=>parseFloat(s)*(scale[s.slice(-1)]||1);
function response(f){const A=Array.from({length:4},()=>Array.from({length:4},()=>[0,0])),b=Array.from({length:4},()=>[0,0]);
 const branch=(na,nb,Y)=>{const i=nodes.indexOf(na),j=nodes.indexOf(nb);if(i>=0){A[i][i]=add(A[i][i],Y);if(j>=0)A[i][j]=sub(A[i][j],Y);else if(nb==='AUDIO_PWM')b[i]=add(b[i],Y)}if(j>=0){A[j][j]=add(A[j][j],Y);if(i>=0)A[j][i]=sub(A[j][i],Y);else if(na==='AUDIO_PWM')b[j]=add(b[j],Y)}};
 for(const c of capture.components.filter(c=>/^R|^C/.test(c.ref)&&c.page==='audio')){const [na,nb]=Object.values(c.nets);if(!nodes.includes(na)&&!nodes.includes(nb))continue;const value=number(c.value);branch(na,nb,c.ref[0]==='R'?[1/value,0]:[0,2*Math.PI*f*value]);}
 branch('AMP_IN','GND',[1/100000,0]); // Minimum specified amplifier input resistance.
 for(let i=0;i<4;i++){let pivot=i;for(let k=i+1;k<4;k++)if(abs(A[k][i])>abs(A[pivot][i]))pivot=k;[A[i],A[pivot]]=[A[pivot],A[i]];[b[i],b[pivot]]=[b[pivot],b[i]];const z=A[i][i];A[i]=A[i].map(a=>div(a,z));b[i]=div(b[i],z);for(let k=0;k<4;k++)if(k!==i){const m=A[k][i];A[k]=A[k].map((a,j)=>sub(a,mul(m,A[i][j])));b[k]=sub(b[k],mul(m,b[i]));}}
 return{hz:f,magnitude:abs(b[3]),db:20*Math.log10(abs(b[3]))};}
const ac=[100,1000,4000,8000,20000,200000,250000].map(response);
const checks={button_low_V:3.399*200/(9900+200),button_held_mA:3.399/9900*1000,i2c_sink_mA:3.399/4653*1000,ir_short_fault_mA:3.399/99*1000,ir_resistor_short_fault_W:3.399**2/99,ir_rx_min_supply_V:3.201-0.0008*101,motor_terminal_start_25C_V:3.168-0.12*2.5,motor_fet_start_25C_W:0.12**2*2.5,motor_terminal_hot_illustrative_V:3.168-0.12*4,audio_ladder_ac:ac};
assert(checks.button_low_V<0.2,'button low margin');assert(checks.ir_resistor_short_fault_W<0.25,'IR resistor dissipation');assert(checks.ir_rx_min_supply_V>2,'IR receiver voltage');
// A 4-ohm hot scenario is a sensitivity assumption, not a manufacturer limit at 3V.
const hashfile=file=>({file,sha256:createHash('sha256').update(fs.readFileSync(path.join(dir,file))).digest('hex')});
const output={status:'Draft capture validation passed; not hardware-qualified',checked_pin_records:checked,erc_violations:violations.length,schematic_symbols:capture.components.filter(c=>!c.ref.startsWith('#')).length,checks,files:[...capture.pages.map(p=>p+'.kicad_sch'),'KK_Draft.kicad_sym','KK_main_module.net','ERC.json'].map(hashfile)};
fs.writeFileSync(path.join(dir,'VALIDATION.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify({pins:checked,erc:violations.length,checks},null,2));
