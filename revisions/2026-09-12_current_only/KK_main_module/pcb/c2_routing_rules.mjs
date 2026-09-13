// Generate project routing rules from the current schematic's physical pin nets.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const work=path.dirname(fileURLToPath(import.meta.url)),root=path.dirname(work);
const file=path.join(root,'KK_main_module.kicad_pro'),pro=JSON.parse(fs.readFileSync(file));
const xml=fs.readFileSync(path.join(work,'board_netlist.xml'),'utf8'),nets=new Map();
for(const m of xml.matchAll(/<net code="[^"]+" name="([^"]+)"[^>]*>([\s\S]*?)<\/net>/g))
 for(const n of m[2].matchAll(/<node ref="([^"]+)" pin="([^"]+)"/g))nets.set(n[1]+':'+n[2],m[1].replaceAll('&amp;','&'));
if(nets.size!==267)throw Error('Unexpected pin count '+nets.size);
const base=pro.net_settings.classes.find(c=>c.name==='Default');
const spec=[['Default',.25,.6,.3],['Power',.8,1,.5],['Motor',.8,1,.5],['Speaker',.5,.8,.4],['Audio',.3,.6,.3],['Ground',.6,1,.5],['AuxLoad',.5,.8,.4]];
pro.net_settings.classes=spec.map(([name,w,d,h],i)=>({...base,name,track_width:w,via_diameter:d,via_drill:h,clearance:.2,priority:name==='Default'?2147483647:i}));
const assigned=new Map();
function assign(c,pins){for(const pin of pins){const n=nets.get(pin);if(!n)throw Error(pin);assigned.set(n,c);}}
assign('Audio',['R30:2','R31:2','C20:2','U3:7','U3:8','U3:5','R34:1','R35:1']);
assign('Speaker',['J5:1','J5:2']);
assign('AuxLoad',['D1:1','D1:2','Q3:1','J2:8']);
assign('Power',['J1:1','J1:3','J1:4','U3:2']);
assign('Motor',['J4:2']);assign('Ground',['J1:2']);
pro.net_settings.netclass_assignments=null;
pro.net_settings.netclass_patterns=[...assigned].map(([pattern,netclass])=>({netclass,pattern}));
pro.board.design_settings.track_widths=[.25,.3,.5,.6,.8,1];
pro.board.design_settings.via_dimensions=[{diameter:.6,drill:.3},{diameter:.8,drill:.4},{diameter:1,drill:.5}];
fs.writeFileSync(file,JSON.stringify(pro,null,2)+'\n');
fs.writeFileSync(path.join(work,'C2_ROUTING_RULES.json'),JSON.stringify({copper:'2 layers, 35 um nominal copper; prototype',classes:spec,assignments:Object.fromEntries(assigned)},null,2)+'\n');
let rules='(version 1)\n';
for(const [name,w] of spec)if(name!=='Default')rules+=`(rule "C2 ${name} minimum track" (condition "A.Type == 'Track' && A.NetClass == '${name}'") (constraint track_width (min ${w}mm)))\n`;
fs.writeFileSync(path.join(root,'KK_main_module.kicad_dru'),rules);
console.log('Assigned '+assigned.size+' nets to explicit width classes.');
