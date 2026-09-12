// Read-only Git publication checks: staged paths, required release files and links.
// No credentials are read, and no file content is printed on a secret-pattern hit.
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const git=(...args)=>execFileSync('git',args,{cwd:root,maxBuffer:32*1024*1024});
const entries=git('ls-files','--stage','-z').toString().split('\0').filter(Boolean).map(x=>{
  const m=x.match(/^(\d+) ([a-f0-9]+) (\d)\t([\s\S]+)$/);return {mode:m[1],sha:m[2],stage:m[3],file:m[4]};
});
const indexed=new Map(entries.map(x=>[x.file,x]));
const errors=[];const check=(v,m)=>{if(!v)errors.push(m);};
let bytes=0;let largest={bytes:0,path:''};let required=0;
for(const e of entries){
  check(e.stage==='0','Unresolved merge: '+e.file);
  if(e.mode==='160000')continue;
  const p=path.join(root,e.file);check(fs.existsSync(p)||fs.lstatSync(p).isSymbolicLink(),'Missing staged path '+e.file);
  if(e.mode==='120000'){
    const target=fs.readlinkSync(p);check(!path.isAbsolute(target),'Absolute symlink: '+e.file);continue;
  }
  const size=fs.statSync(p).size;bytes+=size;
  if(size>largest.bytes)largest={bytes:size,path:e.file};
  check(size<90*1024*1024,'File exceeds conservative 90 MiB upload gate: '+e.file);
  check(!/(^|\/)\.history\/|\.kicad_prl$|\.lck$|__pycache__|\.pyc$/.test(e.file),'Editor/cache state staged: '+e.file);
  if(/\.(md|txt|json|py|mjs|js|ino|env|ya?ml)$/.test(e.file)&&size<8*1024*1024){
    const text=fs.readFileSync(p,'utf8');
    check(!/(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----)/.test(text),'Possible credential in '+e.file);
  }
}
// A fresh checkout must include all files referenced by the active integrity check.
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const need=p=>{required++;check(indexed.has(p),'Required release/audit file is not staged: '+p);};
for(const b of read('docs/C6_P3_RELEASE_INDEX.json').boards){
  need(b.zip);need(b.gerbers_zip);need(b.directory+'/SHA256_MANIFEST.json');
  for(const p of Object.keys(read(b.directory+'/SHA256_MANIFEST.json').files))need(b.directory+'/'+p);
  for(const p of Object.keys(read(b.source+'/SOURCE_BASELINE.json')))need(p);
  need(b.source+'/netlist.xml');need(b.source+'/SOURCE_BASELINE.json');
}
for(const p of read('revisions/2026-09-12_C6_P3_release/MOVE_MANIFEST.json').files)need(p.to);
const docs=['README.md','START_HERE.md','CHANGELOG.md','CONTRIBUTING.md','docs/README.md','docs/FLAT_STACK_REWORK.md','KK_main_module/README.md','KK_power_module/CURRENT_STATUS.md','KK_main_module/assembly/README.md','KK_main_module/routing/README.md','KK_main_module/pcb/README.md','revisions/README.md'];
let links=0;
for(const d of docs){
  need(d);const text=fs.readFileSync(path.join(root,d),'utf8');
  for(const m of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
    let target=m[1];if(/^(https?:|mailto:|#)/.test(target))continue;
    target=decodeURIComponent(target.split('#')[0]);
    const absolute=path.resolve(root,path.dirname(d),target);const rel=path.relative(root,absolute);
    links++;
    check(!rel.startsWith('..'),'Outside repository link in '+d+': '+target);
    check(fs.existsSync(absolute),'Broken link in '+d+': '+target);
    if(fs.existsSync(absolute)&&fs.statSync(absolute).isFile())check(indexed.has(rel),'Link target missing from Git: '+rel);
  }
}
console.log(JSON.stringify({scope:'Read-only staged publication preflight; not native CAD checks',staged_files:entries.length,working_file_bytes:bytes,largest_file:largest,required_release_archive_paths_checked:required,current_document_links_checked:links,errors},null,2));
if(errors.length)process.exitCode=1;
