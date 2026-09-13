// Exact DSN geometry/rule amendment. C.2 placement/netlist are unchanged.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
let d=fs.readFileSync(path.join(root,'routing/KK_main_module_C2.dsn'),'utf8');
d=d.replace(/^    \(plane .*\n/gm,'');
const anchor='    (via "Via[0-1]_600:300_um"';
if(!d.includes(anchor))throw Error('Unexpected DSN structure');
const extra=['F.Cu','B.Cu'].map(l=>`    (keepout "antenna_under_module" (polygon ${l} 0 59500 -7000 72500 -7000 72500 -15500 59500 -15500 59500 -7000))\n`).join('');
d=d.replace(anchor,extra+anchor);
fs.writeFileSync(path.join(root,'routing/KK_main_module_C2_antenna.dsn'),d);
console.log('Fresh all-net DSN with both antenna keepouts; ground explicitly routed.');
