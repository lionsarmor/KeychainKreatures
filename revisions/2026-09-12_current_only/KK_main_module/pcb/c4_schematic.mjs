// Mechanical ECO only: unchanged pin/net mapping, updated socket footprint.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const src=path.join(root,'pcb/backups/pre_c4_top_rgb/KK_main_module.kicad_sch');
let s=fs.readFileSync(src,'utf8').replaceAll('KK_Main:RGB_CA_5mm_LeadFormed','KK_Main:RGB_CA_5mm_Socketed').replaceAll('C.3','C.4').replace('2026-09-10','2026-09-11');
s=s.replace('RGB mood lamp + top-entry connectors','Socketed upper-right RGB + populated 3D');
s=s.replace('C.4: form 1.27 mm leads to 2.54 mm fixture spacing before soldering. 1=R, 2=A+, 3=B, 4=G.','C.4: Sullins PPTC041LFBN-RC socket, formed LED leads at 2.54mm. Actual lead retention qualification required. 1=R, 2=A+, 3=B, 4=G.');
fs.writeFileSync(path.join(root,'KK_main_module.kicad_sch'),s);
console.log('Mechanical-only schematic ECO: D3 socket footprint, unchanged electrical circuit.');
