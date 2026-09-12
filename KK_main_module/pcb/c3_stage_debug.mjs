// Preserve the RGB proposal separately while board size awaits the user.
// Publish only the checked debug/connector PCB with a matching schematic.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')')a.push(t[i]==='('?p():t[i++]);i++;return a;}return p();}
const dump=a=>Array.isArray(a)?`(${a.map(dump).join(' ')})`:a;
const children=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k);
const value=s=>s?.startsWith('"')?JSON.parse(s):s;
const src=path.join(root,'KK_main_module.kicad_sch');
const proposal=path.join(root,'routing/C3_RGB_schematic_proposal.kicad_sch');
if(!fs.readFileSync(src,'utf8').includes('TLC5916_Functional'))throw Error('Generate RGB proposal before staging');
fs.copyFileSync(src,proposal);
const sch=parse(fs.readFileSync(path.join(root,'pcb/backups/pre_c3_debug/KK_main_module.kicad_sch'),'utf8'));
for(const symbol of children(sch,'symbol')){
 const fields=children(symbol,'property');
 const ref=value(fields.find(p=>value(p[1])==='Reference')?.[2]);
 if(!['J4','J5'].includes(ref))continue;
 for(const [key,val]of [['Footprint','KK_Main:JST_PH_B2B_2'],['MPN','B2B-PH-K-S(LF)(SN)'],['Review','C.3 top-entry connector: mating plug inserts perpendicular to rear PCB.']]){
   const p=fields.find(p=>value(p[1])===key);if(p)p[2]=JSON.stringify(val);
 }
}
const title=children(sch,'title_block')[0];children(title,'rev')[0][1]=JSON.stringify('C.3 / DEBUG + TOP-ENTRY / RGB PENDING');
fs.writeFileSync(src,dump(sch)+'\n');
const check=JSON.parse(fs.readFileSync(path.join(root,'pcb/c3_connectors_drc.json'),'utf8'));
if(check.violations.length||check.unconnected_items.length)throw Error('Do not promote failing candidate');
fs.copyFileSync(path.join(root,'routing/KK_main_module_C3_debug_connectors.kicad_pcb'),path.join(root,'KK_main_module.kicad_pcb'));
console.log('Staged checked debug/connector board; RGB proposal retained separately pending board-size approval.');
