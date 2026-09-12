"""One-time final documentation seal and recoverable release organization.
Preserves preflight ZIPs and all superseded outputs. Does not modify routed CAD.
"""
from pathlib import Path
import json, hashlib, shutil, zipfile, re, os
ROOT=Path(__file__).resolve().parent.parent
ARC=ROOT/'revisions/2026-09-12_C6_P3_release'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def write(p,d): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def copy(a,b): b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
def files(p): return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file()}
index=read(ROOT/'docs/C6_P3_RELEASE_INDEX.json')
assert not ARC.exists(),'One-time finalization already performed'
for item in index['boards']:
    assert sha(ROOT/item['zip'])==item['zip_sha256']
    assert sha(ROOT/item['gerbers_zip'])==item['gerbers_sha256']
    out=ROOT/item['directory']; ver=read(out/'RELEASE_VERIFICATION.json')
    assert all(sha(ROOT/item['source']/n)==h for n,h in ver['source_sha256'].items())
    assert all(sha(out/n)==h for n,h in read(out/'SHA256_MANIFEST.json')['files'].items())
ARC.mkdir(parents=True)
records=[]
def archive(src,dst,move=False):
    if src.is_dir():
        for n,h in files(src).items(): records.append({'from':str((src/n).relative_to(ROOT)), 'to':str((dst/n).relative_to(ROOT)), 'sha256':h, 'operation':'move' if move else 'copy'})
        dst.parent.mkdir(parents=True,exist_ok=True)
        if move: shutil.move(str(src),str(dst))
        else: shutil.copytree(src,dst)
    else:
        records.append({'from':str(src.relative_to(ROOT)) if src.is_relative_to(ROOT) else str(src), 'to':str(dst.relative_to(ROOT)), 'sha256':sha(src), 'operation':'move' if move else 'copy'})
        dst.parent.mkdir(parents=True,exist_ok=True)
        if move: shutil.move(str(src),str(dst))
        else: shutil.copy2(src,dst)
for item in index['boards']:
    archive(ROOT/item['zip'],ARC/'preflight_packages'/Path(item['zip']).name)
    archive(ROOT/item['directory']/'SHA256_MANIFEST.json',ARC/'preflight_packages'/(item['revision']+'_SHA256_MANIFEST.json'))
# Precise superseded targets only. Baseline CAD and user Git changes untouched.
main_old=['DRC.json','DRILL_REPORT.txt','ERC.json','KK_MAIN_C5_PROTOTYPE_FAB.zip','MANIFEST.json','ORDER_HOLD_FLAT_STACK.md','README.md','gerbers']
power_old=['ORDER_HOLD_MATCHING_STACK.md','P2_5_SAMPLE_REVIEW_2026-09-12','P2_5_SAMPLE_REVIEW_2026-09-12.zip','P2_5_SAMPLE_REVIEW_2026-09-12.zip.sha256']
for module,names in [('KK_main_module',main_old),('KK_power_module',power_old)]:
    for name in names:
        src=ROOT/module/'manufacturing'/name
        assert src.exists(),str(src)
        archive(src,ARC/module/'manufacturing'/name,move=True)
main=ROOT/'KK_main_module/C6_flat_stack'; power=ROOT/'KK_power_module/P3_matching_stack'
# Current-tree links resolve to sibling datasheets; packaged copies resolve to cad/.
kit=main/'assembly/C6_COMPLETE_KIT_EXTRAS.csv'
kit.write_text(kit.read_text().replace('../cad/datasheets/','../datasheets/'))
copy(kit,power/'assembly/C6_P3_COMPLETE_KIT_EXTRAS.csv')
alignment={}
for item in index['boards']:
    src=ROOT/item['source']; out=ROOT/item['directory']; stem='KK_'+item['kind']+'_module'
    # Replace stale inherited model README only; geometry and model files unchanged.
    copy(src/'3dmodels/README.md',out/'cad/3dmodels/README.md')
    for n in ['C6_COMPLETE_KIT_EXTRAS.csv'] if item['kind']=='main' else ['C6_P3_COMPLETE_KIT_EXTRAS.csv']:
        copy(src/'assembly'/n,out/'assembly'/n)
        p=out/'assembly'/n;p.write_text(p.read_text().replace('../datasheets/','../cad/datasheets/'))
    # Verify actual NPTH drill tool and XY commands, including power locating holes.
    data=(out/'fabrication'/(stem+'-NPTH.drl')).read_text()
    tools={m[1]:float(m[2]) for m in re.finditer(r'^T(\d+)C([\d.]+)$',data,re.M)}
    active=None;holes=[];all_holes=[]
    for line in data.splitlines():
        if re.fullmatch(r'T\d+',line): active=line[1:]
        m=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
        if m:
            point=[float(m[1]),-float(m[2])]; all_holes.append([*point,tools[active]])
            if tools[active]==2.2: holes.append(point)
    assert sorted(holes)==[[4.,4.],[4.,101.],[92.,4.],[92.,101.]]
    alignment[item['kind']]={'mounting_holes_mm':holes,'NPTH_holes_with_diameter_mm':all_holes,'source_drill_sha256':sha(out/'fabrication'/(stem+'-NPTH.drl'))}
    current='''# Current prototype project

This is the authoritative revised CAD directory. Open the .kicad_pro beside this README, not older root or archived CAD. Current BOM/assembly documents are in assembly/; fresh native checks and maps are in release_checks/. The project uses KiCad 10 and standard KiCad library models plus the supplied local libraries.

The project is a prototype only. See ../../START_HERE.md for current manufacturing ZIPs, hashes, paired-board wiring and remaining factory, physical-fit and bench qualification requirements. Do not rerun old placement or routing scripts over this board.
'''
    (src/'README.md').write_text(current)
    (out/'cad/README.md').write_text(current.replace('assembly/','../assembly/').replace('release_checks/','../verification/').replace('../../START_HERE.md','../READ_FIRST.md'))
    # Preserve complete file list and refresh ZIP only after exact CAD and fab recheck.
    ver=read(out/'RELEASE_VERIFICATION.json')
    assert all(sha(src/n)==h for n,h in ver['source_sha256'].items())
    assert all(sha(out/'fabrication'/n)==h for n,h in ver['fabrication_sha256'].items())
    copy(out/'FABRICATION_REQUIREMENTS.md',src/'FABRICATION_REQUIREMENTS.md')
    copy(ROOT/'docs/FLAT_STACK_REWORK.md',out/'verification/FLAT_STACK_REWORK_HISTORY.md')
    # History document's workspace links are not package-relative; clearly identify it.
    history=out/'verification/FLAT_STACK_REWORK_HISTORY.md'
    history.write_text('Workspace history reference; links refer to the original project tree, not this ZIP. Use READ_FIRST.md and assembly/ for this package.\n\n'+history.read_text())
for item in index['boards']:
    out=ROOT/item['directory']
    write(out/'verification/DRILL_ALIGNMENT_AUDIT.json',alignment)
    manifest={n:h for n,h in files(out).items() if n!='SHA256_MANIFEST.json'}
    write(out/'SHA256_MANIFEST.json',{'files':manifest})
    target=ROOT/item['zip'];temp=target.with_suffix('.zip.building')
    assert not temp.exists()
    with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=4,strict_timestamps=False) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(out)))
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None
        for name,h in files(out).items(): assert hashlib.sha256(z.read(name)).hexdigest()==h
    os.replace(temp,target) # generated archive; previous exact bytes preserved above
    item.update(zip_sha256=sha(target),file_count=len(files(out)))
    module='KK_'+item['kind']+'_module'
    (ROOT/module/'manufacturing/README.md').write_text(f'''# Current {item['revision']} prototype outputs

- [{Path(item['zip']).name}]({Path(item['zip']).name}): complete five-sample review, CAD, BOM/placement, assembly/test guides, models, datasheets and checks.
- [{Path(item['gerbers_zip']).name}]({Path(item['gerbers_zip']).name}): Gerbers, drills, maps, IPC-D-356 and fabrication requirements.
- [{Path(item['directory']).name}/]({Path(item['directory']).name}/): unpacked matching review package.

Use {item['revision']} only with the paired C.6/P.3 revision. Both are 96 x 105 mm, but main has TWO copper layers and power FOUR. Factory DFM/component supply, physical fit and bench qualification remain required. Power needs filled/capped/planarized via-in-pad and fine-pitch WCSP assembly approval. Nothing ordered.

Superseded outputs moved to ../../revisions/2026-09-12_C6_P3_release/. Current hashes: ../../docs/C6_P3_RELEASE_INDEX.json. Do not manufacture the historical C.5/P.2 ZIPs.
''')
desktop=ROOT.parent/'PRINT THIS.pdf'
if desktop.exists():archive(desktop,ARC/'desktop/PRINT_THIS_before_C6_P3.pdf')
copy(ROOT/'docs/C6_P3_STACK_REVIEW.pdf',desktop)
index['final_preflight']={'matching_NPTH_mounting_holes':True,'CAD_and_fabrication_unchanged_by_documentation_seal':True,'desktop_print_sheet':str(desktop),'superseded_archive':str(ARC.relative_to(ROOT))}
write(ROOT/'docs/C6_P3_RELEASE_INDEX.json',index)
write(ROOT/'docs/C6_P3_DRILL_ALIGNMENT_AUDIT.json',alignment)
write(ARC/'MOVE_MANIFEST.json',{'scope':'Superseded manufacturing moved; preflight release ZIPs and previous desktop sheet copied for recovery. Baseline CAD untouched.','files':records})
assert all(sha(ROOT/r['to'])==r['sha256'] for r in records)
print(json.dumps({'archived_files':len(records),'releases':index['boards'],'print_sheet':str(desktop)},indent=2))
