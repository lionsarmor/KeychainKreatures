// Import the user-supplied footprint and remap only MOD1's schematic pin identifiers.
// Does not redraw the schematic or regenerate placement.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.dirname(here);
const source='/home/legion/Desktop/ESP32-S3-SuperMini.kicad_mod';
const map=JSON.parse(fs.readFileSync(path.join(here,'SUPERMINI_PIN_MAP.json'),'utf8'));
const q=JSON.stringify;
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')'){if(i>=t.length)throw Error('EOF');a.push(t[i]==='('?p():t[i++]);}i++;return a;}const a=p();if(i!==t.length)throw Error('trailing data');return a;}
const val=s=>s?.startsWith('"')?JSON.parse(s):s;
const kids=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k),get=(a,k)=>kids(a,k)[0];
const dump=a=>Array.isArray(a)?`(${a.map(dump).join(' ')})`:a;
const bytes=fs.readFileSync(source),fp=parse(bytes.toString());
const pads=kids(fp,'pad').map(p=>val(p[1]));
if(pads.length!==18||JSON.stringify([...pads].sort())!==JSON.stringify(Object.values(map).sort()))throw Error('Unexpected supplied pad names');
const backup=path.join(here,'backups','supermini-import-'+new Date().toISOString().replaceAll(':','-'));
fs.mkdirSync(backup,{recursive:true});
for(const name of ['KK_main_module.kicad_sch','KK_main_module.kicad_pcb','KK_Main.kicad_sym'])fs.copyFileSync(path.join(root,name),path.join(backup,name));
fs.copyFileSync(path.join(here,'board_netlist.xml'),path.join(backup,'before_netlist.xml'));
fs.writeFileSync(path.join(root,'KK_Main.pretty','ESP32-S3-SuperMini.kicad_mod'),bytes);
const schpath=path.join(root,'KK_main_module.kicad_sch'),sch=parse(fs.readFileSync(schpath,'utf8'));
const mod=kids(sch,'symbol').find(s=>kids(s,'property').some(p=>val(p[1])==='Reference'&&val(p[2])==='MOD1'));
function remapDef(def){
 const pins=kids(def,'symbol').flatMap(u=>kids(u,'pin'));
 const old=pins.some(p=>val(get(p,'number')[1])==='18');
 if(old)for(const p of pins){const n=get(p,'number');if(!(val(n[1]) in map))throw Error('Unmapped symbol pin');n[1]=q(map[val(n[1])]);}
 return old;
}
const def=kids(get(sch,'lib_symbols'),'symbol').find(s=>val(s[1])==='KK_Main:SuperMini_Header');
if(remapDef(def))for(const pin of kids(mod,'pin'))pin[1]=q(map[val(pin[1])]);
const prop=kids(mod,'property').find(p=>val(p[1])==='Footprint');prop[2]=q('KK_Main:ESP32-S3-SuperMini');
for(const t of kids(sch,'text'))if(val(t[1]).includes('carrier pad numbers remain provisional'))t[1]=q(val(t[1]).replace('carrier pad numbers remain provisional','pad names match supplied footprint'));
fs.writeFileSync(schpath,dump(sch)+'\n');
const libpath=path.join(root,'KK_Main.kicad_sym'),lib=parse(fs.readFileSync(libpath,'utf8'));
remapDef(kids(lib,'symbol').find(s=>val(s[1])==='SuperMini_Header'));
fs.writeFileSync(libpath,dump(lib)+'\n');
fs.writeFileSync(path.join(here,'SUPERMINI_IMPORT.json'),JSON.stringify({source,sha256:createHash('sha256').update(bytes).digest('hex'),project_footprint:'KK_Main:ESP32-S3-SuperMini',backup,pin_map:map,geometry_preserved:true,row_spacing_mm:15.24,nominal_pitch_mm:2.54,drill_mm:1,pad_size_mm:1.508,note:'Supplied GPIO13 pad is at y=-2.50 mm, not -2.54; retained unchanged. User-supplied geometry, not a physical fit certification.'},null,2)+'\n');
console.log('Imported exact footprint bytes and matched MOD1 schematic pin names. Backup: '+backup);
