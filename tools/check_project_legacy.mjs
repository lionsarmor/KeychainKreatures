// HISTORICAL C5/P2 checker. Current entry point is check_project.mjs.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const json=p=>JSON.parse(read(p));
const digest=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
const errors=[],warnings=[];
const manifest=json('revisions/2026-09-11_cleanup/MOVE_MANIFEST.json');
for(const m of manifest.moves) for(const f of m.files){
  const p=m.to+f.path.slice(m.from.length);
  if(f.sha256&&digest(p)!==f.sha256) errors.push(`Archived content changed: ${p}`);
}
const promotionPath='revisions/2026-09-11_power_routing/PROMOTION.json';
const promotion=fs.existsSync(path.join(root,promotionPath))?json(promotionPath):null;
const finalPromotionPath='revisions/2026-09-12_power_final/PROMOTION.json';
const finalPromotion=fs.existsSync(path.join(root,finalPromotionPath))?json(finalPromotionPath):null;
for(const f of manifest.protectedFiles) if(f.sha256&&digest(f.path)!==f.sha256){
  const changed=promotion?.changed_files.find(p=>p.path===f.path);
  const final=finalPromotion?.changed_files.find(p=>p.path===f.path);
  const chainOK=changed&&changed.before_sha256===f.sha256&&digest(changed.baseline)===f.sha256;
  const latestOK=final?changed&&final.before_sha256===changed.after_sha256&&digest(final.baseline)===final.before_sha256&&digest(f.path)===final.after_sha256:changed&&digest(f.path)===changed.after_sha256;
  if(!chainOK||!latestOK)errors.push(`Unrecorded active CAD change since cleanup: ${f.path}`);
}
const power='KK_power_module/P2_compact';
const main='KK_main_module';
const localRefs=new Set();
for(const dir of [main,power]) for(const name of ['fp-lib-table','sym-lib-table',`${dir===main?'KK_main_module':'KK_power_module'}.kicad_pcb`]){
  for(const m of read(`${dir}/${name}`).matchAll(/\((?:uri|model)\s+"([^"]+)"/g)){
    if(m[1].startsWith('${KIPRJMOD}/')){
      const target=`${dir}/${m[1].slice('${KIPRJMOD}/'.length)}`;
      localRefs.add(target);
      if(!fs.existsSync(path.join(root,target))) errors.push(`Missing project-local library/model: ${target}`);
    }else if(m[1].includes('${KICAD')) warnings.push(`System KiCad model not checked: ${m[1]}`);
  }
}
function nets(p){
  const out=new Map();
  const decode=s=>s.replaceAll('&amp;','&').replaceAll('&quot;','"').replaceAll('&lt;','<').replaceAll('&gt;','>');
  for(const n of read(p).matchAll(/<net\b[^>]*\bname="([^"]+)"[^>]*>([\s\S]*?)<\/net>/g)){
    for(const node of n[2].matchAll(/<node\b[^>]*\bref="([^"]+)"[^>]*\bpin="([^"]+)"[^>]*\/?\s*>/g)){
      const k=`${node[1]}.${node[2]}`;
      if(out.has(k)) errors.push(`Duplicate netlist pin: ${p} ${k}`);
      out.set(k,decode(n[1]).replace(/^\//,''));
    }
  }
  if(!out.size) errors.push(`No netlist parsed: ${p}`);
  return out;
}
const pn=nets(`${power}/netlist.xml`),mn=nets(`${main}/C5_relayout/netlist.xml`);
const design=json(`${power}/design.json`);
for(const part of design.components) for(const [pin,expected] of Object.entries(part.nets)){
  const actual=pn.get(`${part.ref}.${pin}`);
  if(expected===null){if(actual&&!actual.startsWith('unconnected-')) errors.push(`NC connected: ${part.ref}.${pin}`);}
  else if(actual!==expected) errors.push(`Manifest/netlist mismatch: ${part.ref}.${pin}`);
}
const rails=['MCU_5V','GND','LOGIC_3V3','ACT_3V2'];
rails.forEach((rail,i)=>{if(pn.get(`J3.${i+1}`)!==rail||mn.get(`J1.${i+1}`)!==rail)errors.push(`Harness mismatch on pin ${i+1}`);});
if(pn.get('J2.2')!=='BAT_NEG'||pn.get('J4.2')!=='GND')errors.push('Battery return / thermistor ground mismatch');
for(const pin of ['A6','A7','B6','B7','A8','B8']) if(pn.get(`J1.${pin}`)&&!pn.get(`J1.${pin}`).startsWith('unconnected-')) errors.push(`Unexpected USB data/SBU connection: ${pin}`);
const reviewPath=`${power}/review/VERIFICATION.json`;
const release=fs.existsSync(path.join(root,reviewPath))?json(reviewPath):null;
const drc=json(`${power}/${release?'review/review_drc.json':'finish_drc.json'}`);
if(release)for(const [name,key]of [['kicad_pcb','PCB_SHA256'],['kicad_sch','SCHEMATIC_SHA256'],['kicad_pro','PROJECT_SHA256']])if(digest(`${power}/KK_power_module.${name}`)!==release[key])errors.push('Power CAD differs from checked snapshot: '+name);
const screening=json(`${power}/electrical_screening.json`);
const report={
  scope:'Read-only archive integrity, authorized routing revision hashes and saved netlist/report checks; not a fresh native DRC or powered test',
  verified_moves:manifest.moves.length,
  protected_CAD_library_model_files:manifest.protectedFiles.length,
  project_local_references_checked:localRefs.size,
  saved_power_component_count:design.components.length,
  saved_power_IC_count:design.components.filter(p=>/^U\d+$/.test(p.ref)).length,
  saved_power_test_pad_count:design.components.filter(p=>/^TP\d+$/.test(p.ref)).length,
  harness:rails,
  previous_power_DRC:{date:drc.date,unconnected_items:drc.unconnected_items.length,violations:drc.violations.map(v=>({type:v.type,severity:v.severity})),schematic_parity:drc.schematic_parity.length},
  previous_screening:screening.status,
  errors,warnings:[...new Set(warnings)],
  power_review_package:release?.package??null,
  power_CAD_checks_clean:!!release&&!drc.violations.length&&!drc.unconnected_items.length&&!drc.schematic_parity.length&&!errors.length,
  manufacturer_approval:release?.manufacturer_approval??false,
  powered_testing:false,
  fabrication_ready:false
};
console.log(JSON.stringify(report,null,2));
if(errors.length) process.exitCode=1;
