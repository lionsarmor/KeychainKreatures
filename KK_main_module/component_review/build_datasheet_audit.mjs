// Run after build_design_tables.mjs. Documents only; no schematic/power-board edits.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {execFileSync, spawnSync} from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>fs.readFileSync(path.join(dir,n),'utf8');
const write=(n,s)=>fs.writeFileSync(path.join(dir,n),s);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const csv=rows=>rows.map(r=>r.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(',')).join('\n')+'\n';
const parse=s=>s.trim().split(/\r?\n/).map(l=>l.slice(1,-1).split('","').map(x=>x.replaceAll('""','"')));
const legacy=JSON.parse(read('datasheet_manifest.json'));
let legacyCount=0;
for(const m of legacy.filter(m=>m.status==='archived')) {
 const b=fs.readFileSync(path.join(dir,'datasheets',m.file));
 assert.equal(hash(b),m.sha256,m.file+' changed since original archive');legacyCount++;
}
const supplements=[
 ['/tmp/kk-st7789v2.pdf','datasheets/st7789v2-controller.pdf','https://www.waveshare.com/w/upload/c/c9/ST7789V2.pdf','Sitronix ST7789V2 V1.0 chip datasheet; not XIITIA module schematic'],
 ['/tmp/kk-sullins-part-list.pdf','datasheets/sullins-order-codes.pdf','https://www.sullinscorp.com/images/AllRoHSParts.pdf','Manufacturer order-code list; use with female-header drawing'],
 ['/tmp/kk-sd-pinout-photo.jpg','source_evidence/sd-pinout.jpg','https://m.media-amazon.com/images/I/61qrQGhmcEL._AC_SL1500_.jpg','Seller pin-label photo; NOT a datasheet'],
 ['/tmp/kk-sd-module-detail.jpg','source_evidence/sd-dimensions.jpg','https://m.media-amazon.com/images/I/612fmkYugOL._AC_SL1500_.jpg','Seller dimension photo; NOT a controlled mechanical drawing']
];
for(const [temp,local] of supplements) {
 const dest=path.join(dir,local);
 if(fs.existsSync(dest)) continue;
 const b=fs.readFileSync(temp);
 if(local.endsWith('.pdf')) {assert.equal(b.subarray(0,5).toString(),'%PDF-');execFileSync('pdfinfo',[temp],{stdio:['ignore','pipe','pipe']});}
 else assert.equal(b.subarray(0,3).toString('hex'),'ffd8ff');
 fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(temp,dest);
}
const sourceMap=new Map(JSON.parse(read('datasheet_sources.json')).map(([file,url])=>['datasheets/'+file,url]));
for(const [,file,url] of supplements)sourceMap.set(file,url);
const all=parse(read('MASTER_BOM.csv'));const headings=all.shift();
const bom=all.map(r=>Object.fromEntries(headings.map((k,i)=>[k,r[i]])));
const mainFunctions=new Set(read('MAIN_BOARD_PRINT.md').split('\n').filter(l=>l.startsWith('| ')).map(l=>l.split('|')[1].trim()));
const relevant=bom.filter(r=>mainFunctions.has(r.function));
const custom=new Set(['MAIN_PCB','TEST_ACCESS','SCREEN_RETENTION','PCB_HARDWARE','ACTUATOR_MOUNT','SD_RETENTION']);
const bundle=new Set(['MCU_HEADER','SD_HEADER']);
const coverage=relevant.map(r=>{
 let type='DESIGN_PENDING', files=[],note='Individual component/MPN or circuit quantity not yet specified; no exact-part datasheet to retrieve.';
 if(r.local_datasheet){type='DOCUMENT_FOUND';files=[r.local_datasheet];note='Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks.';}
 if(r.function==='CONTROLS'){type='DRAWING_FOUND';note='Adafruit-linked drawing available; height conflict with product-page dimensions remains.';}
 if(r.function==='CORE'){type='PARTIAL_MODULE';files=['datasheets/esp32-s3.pdf','datasheets/nologo-reference-schematic.png'];note='Chip datasheet and another supplier reference schematic available; exact Teyleten carrier schematic not found.';}
 if(r.function==='DISPLAY'){type='PARTIAL_MODULE';files=['datasheets/st7789v2-controller.pdf'];note='Exact advertised controller datasheet archived; XIITIA panel/carrier drawing and backlight circuit not found.';}
 if(r.function==='SD_MODULE'){type='PARTIAL_MODULE';files=['source_evidence/sd-pinout.jpg','source_evidence/sd-dimensions.jpg'];note='Exact seller photos document 3V3 and pin labels; no controlled module datasheet recovered.';}
 if(r.function==='SPEAKER'){type='DATASHEET_NOT_FOUND';files=[];note='Exact FUET model listing found, but no controlled datasheet/rating drawing. Do not substitute another 1511 model.';}
 if(bundle.has(r.function)){type='BUNDLED_NO_MPN';files=[];note='Supplier-pictured accessory, not separately identified by manufacturer part number.';}
 if(custom.has(r.function)){type='CUSTOM_DESIGN';files=[];note='Custom layout, mounting or test-access item; dimensions/design must be created before hardware can be specified.';}
 if(['MICROSD','SPEAKER_CONTACT','SYS_IN_CONNECTOR','SYS_IN_HARNESS'].includes(r.function)){type='PART_NOT_SELECTED';files=[];note='Exact card/contact/connector/harness not yet selected; cannot attach an unrelated datasheet as if final.';}
 if(['MCU_SOCKET','DISPLAY_SOCKET','SD_SOCKET'].includes(r.function))files.push('datasheets/sullins-order-codes.pdf');
 for(const f of files)assert(fs.existsSync(path.join(dir,f)),f);
 return {id:r.id,function:r.function,part:r.exact_part_or_open_requirement,type,files,note};
});
const totals=Object.fromEntries([...new Set(coverage.map(r=>r.type))].map(t=>[t,coverage.filter(r=>r.type===t).length]));
const packedFiles=new Set(coverage.flatMap(r=>r.files));
const manifest=[...packedFiles].sort().map(file=>{
 const full=path.join(dir,file),b=fs.readFileSync(full);let pages=null,warnings='';
 if(file.endsWith('.pdf')){assert.equal(b.subarray(0,5).toString(),'%PDF-');const p=spawnSync('pdfinfo',[full],{encoding:'utf8'});assert.equal(p.status,0,file);pages=Number(p.stdout.match(/^Pages:\s+(\d+)/m)?.[1]);assert(pages>0,file);warnings=p.stderr.trim();}
 return {file,url:sourceMap.get(file),bytes:b.length,sha256:hash(b),pages,warnings};
});
write('main_datasheet_manifest.json',JSON.stringify({date:'2026-09-10',original_archive_hashes_verified:legacyCount,coverage_counts:totals,files:manifest},null,2)+'\n');
write('DATASHEET_AUDIT.csv',csv([['bom_id','function','exact_part_or_requirement','documentation_status','local_documents','source_urls','remaining_issue'],...coverage.map(r=>[r.id,r.function,r.part,r.type,r.files.join('; '),r.files.map(f=>sourceMap.get(f)||'').join('; '),r.note])]));
const intro=`2026-09-10. Audited all ${coverage.length} rows of the current main-board print list. Verified ${legacyCount} existing archive hashes. This packet contains ${manifest.length} distinct source documents/images (${manifest.filter(r=>r.pages).length} PDFs); shared family documents cover multiple exact parts. Photos and reference-board diagrams are explicitly distinguished from exact-module datasheets. No component substitutions, purchases or schematic changes were made.`;
let md='# Main-board datasheets — complete coverage index\n\n'+intro+'\n\n[Downloadable packet](MAIN_BOARD_DATASHEETS.zip) · [Printable index](DATASHEET_AUDIT.html) · [CSV](DATASHEET_AUDIT.csv) · [integrity manifest](main_datasheet_manifest.json) · [module evidence and search notes](MODULE_SOURCE_NOTES.md)\n\n';
md+='## Results\n\n| Documentation category | BOM rows |\n|---|---:|\n';
for(const [t,n] of Object.entries(totals))md+=`| ${t} | ${n} |\n`;
md+='\nDOCUMENT_FOUND includes manufacturer series documents and order-code tables, not necessarily a separate PDF for every resistor value. PARTIAL_MODULE means useful evidence exists but not a controlled schematic for the exact seller assembly. DESIGN_PENDING is unfinished engineering, not a failed internet search.\n\n## Every main-board row\n\n| Item | Exact part / requirement | Documentation | Local source | Remaining issue |\n|---|---|---|---|---|\n';
for(const r of coverage)md+=`| ${r.function} | ${r.part.replaceAll('|','/')} | ${r.type} | ${r.files.map(f=>'['+path.basename(f)+']('+f+')').join(' / ')||'[Evidence/selection notes](MODULE_SOURCE_NOTES.md)'} | ${r.note} |\n`;
md+='\n## Original source URLs\n\n';
for(const r of manifest)md+=`- [${r.file}](${r.url}) — ${r.pages ? r.pages+' pages' : 'image'}; local copy [here](${r.file}).\n`;
md+='\nFiles passed PDF parsing and SHA-256 checks. Some legacy PDFs produce nonfatal metadata warnings; these are recorded in the manifest. Parsing is not a full technical design review. Final resistor/capacitor counts and power/interface qualification remain schematic work, not documentation gaps.\n';
write('DATASHEET_AUDIT.md',md);
const h=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
write('DATASHEET_AUDIT.html','<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Main-board datasheet index</title><style>body{font:12px Arial,sans-serif;margin:25px;color:#111}table{width:100%;border-collapse:collapse}td,th{border:1px solid #aaa;padding:5px;text-align:left;vertical-align:top;overflow-wrap:anywhere}thead{display:table-header-group}tr{break-inside:avoid}p{line-height:1.4}@media print{@page{size:A4 landscape;margin:10mm}body{margin:0;font-size:10px}}</style></head><body><h1>Keychain Kreatures — main-board datasheets</h1><p>'+h(intro)+'</p><p>Documentation found does not mean circuit quantities or mechanical fit are finalized. <a href="MODULE_SOURCE_NOTES.md">Module gaps and engineering notes</a></p><table><thead><tr><th>Item</th><th>Part</th><th>Documentation status</th><th>Open document</th><th>Remaining issue</th></tr></thead><tbody>'+coverage.map(r=>'<tr><td>'+h(r.function)+'</td><td>'+h(r.part)+'</td><td>'+h(r.type)+'</td><td>'+r.files.map(f=>'<a href="'+h(f)+'">'+h(path.basename(f))+'</a>').join('<br>')+'</td><td>'+h(r.note)+'</td></tr>').join('')+'</tbody></table></body></html>\n');
const extra=['DATASHEET_AUDIT.md','DATASHEET_AUDIT.html','DATASHEET_AUDIT.csv','main_datasheet_manifest.json','MODULE_SOURCE_NOTES.md','SD_STORAGE.md'];
execFileSync('zip',['-q','MAIN_BOARD_DATASHEETS.zip',...extra,...packedFiles],{cwd:dir});
execFileSync('unzip',['-t','MAIN_BOARD_DATASHEETS.zip'],{cwd:dir,stdio:['ignore','pipe','pipe']});
console.log(JSON.stringify({rows:coverage.length,documents:manifest.length,pdfs:manifest.filter(r=>r.pages).length,coverage:totals,zip_bytes:fs.statSync(path.join(dir,'MAIN_BOARD_DATASHEETS.zip')).size},null,2));
