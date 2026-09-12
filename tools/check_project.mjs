// Current C6/P3 read-only check. No native CAD generation, routing or writes.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const full=p=>path.join(root,p);
const read=p=>fs.readFileSync(full(p),'utf8');
const json=p=>JSON.parse(read(p));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(full(p))).digest('hex');
const errors=[];
function check(test,message){if(!test)errors.push(message);}
function nets(p){
  const out=new Map();
  for(const n of read(p).matchAll(/<net\b[^>]*\bname="([^"]+)"[^>]*>([\s\S]*?)<\/net>/g))
    for(const pin of n[2].matchAll(/<node\b[^>]*\bref="([^"]+)"[^>]*\bpin="([^"]+)"[^>]*\/?\s*>/g))
      out.set(`${pin[1]}.${pin[2]}`,n[1].replaceAll('&amp;','&').replace(/^\//,''));
  check(out.size>0,'Empty netlist '+p); return out;
}
const index=json('docs/C6_P3_RELEASE_INDEX.json');
const staticAudit=json('docs/C6_P3_STATIC_AUDIT.json');
const boards={}; let verifiedFiles=0;
for(const item of index.boards){
  const stem=`KK_${item.kind}_module`, dir=item.directory, src=item.source;
  const ver=json(`${dir}/RELEASE_VERIFICATION.json`);
  check(sha(item.zip)===item.zip_sha256,'Changed review ZIP '+item.zip);
  check(sha(item.gerbers_zip)===item.gerbers_sha256,'Changed Gerber ZIP '+item.gerbers_zip);
  for(const [name,want]of Object.entries(json(`${dir}/SHA256_MANIFEST.json`).files)){
    check(sha(`${dir}/${name}`)===want,'Changed package file '+dir+'/'+name); verifiedFiles++;
  }
  for(const [name,want]of Object.entries(ver.source_sha256)){
    check(sha(`${src}/${name}`)===want,'Source edited since release '+src+'/'+name);
    check(sha(`${dir}/cad/${name}`)===want,'Packaged source mismatch '+name);
  }
  for(const [name,want]of Object.entries(ver.reports_sha256))check(sha(`${dir}/verification/${name}`)===want,'Report hash mismatch '+name);
  for(const [name,want]of Object.entries(ver.fabrication_sha256))check(sha(`${dir}/fabrication/${name}`)===want,'Fabrication hash mismatch '+name);
  check(ver.source_sha256[`${stem}.kicad_pcb`]===staticAudit.boards[stem].pcb_sha256,'Stale static board audit '+stem);
  const drc=json(`${dir}/verification/DRC.json`),erc=json(`${dir}/verification/ERC.json`);
  check(!drc.violations.length&&!drc.unconnected_items.length&&!drc.schematic_parity.length,'Non-clean DRC '+stem);
  check(erc.sheets.every(s=>!s.violations.length),'Non-clean ERC '+stem);
  for(const [old,want]of Object.entries(json(`${src}/SOURCE_BASELINE.json`)))check(sha(old)===want,'Preserved baseline changed '+old);
  for(const file of ['fp-lib-table','sym-lib-table',`${stem}.kicad_pcb`])
    for(const m of read(`${src}/${file}`).matchAll(/\((?:uri|model)\s+"([^"]+)"/g))
      if(m[1].startsWith('${KIPRJMOD}/'))check(fs.existsSync(full(src+'/'+m[1].slice('${KIPRJMOD}/'.length))),'Missing local asset '+m[1]);
  boards[item.kind]={revision:item.revision,native_ERC:0,native_DRC:0,opens:0,parity:0,source:src,nets:nets(`${src}/netlist.xml`),fitted:ver.fitted,debug_points:ver.bare_debug_points};
}
const pins=['MCU_5V','GND','LOGIC_3V3','ACT_3V2'];
pins.forEach((n,i)=>check(boards.main.nets.get(`J1.${i+1}`)===n&&boards.power.nets.get(`J3.${i+1}`)===n,'Harness mismatch '+(i+1)));
const design=json(`${boards.power.source}/design.json`);
for(const p of design.components)for(const [pin,net]of Object.entries(p.nets)){
  const actual=boards.power.nets.get(`${p.ref}.${pin}`);
  check(net===null?(!actual||actual.startsWith('unconnected-')):actual===net,'Power manifest/netlist mismatch '+p.ref+'.'+pin);
}
check(boards.power.nets.get('J2.2')==='BAT_NEG'&&boards.power.nets.get('J4.2')==='GND','Battery/NTC returns');
for(const pin of ['A6','A7','B6','B7','A8','B8']){
  const n=boards.power.nets.get('J1.'+pin);check(!n||n.startsWith('unconnected-'),'Unexpected USB data/SBU wire '+pin);
}
const archive='revisions/2026-09-12_C6_P3_release/MOVE_MANIFEST.json';
if(fs.existsSync(full(archive)))for(const row of json(archive).files)check(sha(row.to)===row.sha256,'Archive changed '+row.to);
console.log(JSON.stringify({scope:'Saved release integrity and netlist/interface check; NOT fresh native checks or powered testing',verified_package_files:verifiedFiles,boards:Object.fromEntries(Object.entries(boards).map(([k,{nets,...v}])=>[k,v])),harness:pins,errors,manufacturer_approved:false,physical_fit_qualified:false,powered_tested:false,status:errors.length?'FAIL':'PASS — prototype files consistent; physical/DFM/bench qualifications remain'},null,2));
if(errors.length)process.exitCode=1;
