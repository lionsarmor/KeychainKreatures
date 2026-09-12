"""Publish the checked silkscreen revision and preserve the preceding release.
Host Python; no electrical edits, uploads, purchasing, or overwriting archives.
"""
from pathlib import Path
import json,hashlib,shutil,csv,datetime,zipfile,subprocess
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'KK_power_module/work/P2_logo_review';CUR=ROOT/'KK_power_module/P2_compact'
PKG=SRC/'prototype_package';OUT=ROOT/'KK_power_module/manufacturing/P2_5_SAMPLE_REVIEW_2026-09-12'
ARC=ROOT/'revisions/2026-09-12_power_final'
OLD=ROOT/'KK_power_module/manufacturing/P2_5_SAMPLE_REVIEW'
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
def copy(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
drc=read(SRC/'review_drc.json');erc=read(SRC/'final_erc.json');audit=read(PKG/'CAD_AUDIT.json');change=read(SRC/'LOGO_CHANGE_AUDIT.json')
assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
assert all(not s['violations'] for s in erc['sheets']) and not audit['errors']
assert digest(SRC/'KK_power_module.kicad_pcb')==audit['PCB_SHA256']==change['candidate_pcb_sha256']
assert digest(CUR/'KK_power_module.kicad_pcb')==change['source_pcb_sha256']
assert change['copper_unchanged'] and change['copper_signature_before']==change['copper_signature_after']
assert digest(ROOT/'KK_main_module/KK_main_module.kicad_pcb')=='b840262c37afad89ec5307568ace5b6acb4406f89c44c91f1579771642a89003'
assert all(digest(CUR/('KK_power_module.'+ext))==digest(SRC/('KK_power_module.'+ext)) for ext in ['kicad_sch','kicad_pro'])
with (PKG/'TEST_POINTS.csv').open(newline='') as f:tests=list(csv.DictReader(f))
with (PKG/'POSITIONS_NATIVE.csv').open(newline='') as f:positions=list(csv.DictReader(f))
with (PKG/'BOM_AND_PLACEMENT.csv').open(newline='') as f:bom=list(csv.DictReader(f))
assert len(tests)==28 and {r['Reference'] for r in tests}=={'TP'+str(i) for i in range(1,29)}
assert len(positions)==108 and {r['Ref'] for r in positions}=={r['Reference'] for r in bom}
assert all(r['Layer']=='B.Cu' for r in tests)
assert next(r for r in tests if r['Reference']=='TP4')['Signal']=='GND'
assert next(r for r in tests if r['Reference']=='TP3')['Signal']=='BAT_NEG'
exts=['gtl','g1','g2','gbl','gts','gbs','gtp','gbp','gm1','gto','gbo']
for ext in exts:assert list((PKG/'fabrication').glob('*.'+ext)),ext
for n in ['KK_power_module-PTH.drl','KK_power_module-NPTH.drl','KK_power_module.ipc']:assert (PKG/'fabrication'/n).stat().st_size>20,n
assert (PKG/'schematic.pdf').stat().st_size>1000
# Ignore only timestamp comments, not copper commands or net attributes.
def fabrication_content(p):
    return '\n'.join(line for line in p.read_text().splitlines() if not any(token in line for token in ['CreationDate','Created by KiCad','; DRILL file KiCad']))
same=[]
for ext in ['gtl','g1','g2','gbl','gts','gbs','gtp','gbp','gm1']:
    p=next((PKG/'fabrication').glob('*.'+ext));q=OLD/'fabrication'/p.name
    assert fabrication_content(p)==fabrication_content(q),'Unexpected fabrication geometry change: '+p.name
    same.append(p.name)
for name in ['KK_power_module-PTH.drl','KK_power_module-NPTH.drl']:
    assert fabrication_content(PKG/'fabrication'/name)==fabrication_content(OLD/'fabrication'/name),'Unexpected drill geometry change'
    same.append(name)
assert fabrication_content(PKG/'fabrication/KK_power_module-B_Silkscreen.gbo')!=fabrication_content(OLD/'fabrication/KK_power_module-B_Silkscreen.gbo')
assert not OUT.exists() and not ARC.exists(),'Refusing to overwrite a release or archive'
# Small supplemental assembly/fabrication files, derived from native records.
text='# Test-pad guide — rear side\n\n28 bare 1.5 mm probe pads; not fitted pins. Coordinates are front-view KiCad mm (Y down). The rear assembly drawing is mirrored for rear viewing.\n\n**TP4 is GND. TP3 is BAT_NEG, not an interchangeable ground. Never bridge the protection return with grounded test equipment.**\n\n| Pad | Signal | CAD X | CAD Y |\n|---|---|---:|---:|\n'
for r in sorted(tests,key=lambda r:int(r['Reference'][2:])):text+=f"| {r['Reference']} | {r['Signal']} | {r['CAD X mm']} | {r['CAD Y mm (down-positive)']} |\n"
(PKG/'TEST_PAD_GUIDE.md').write_text(text)
with (PKG/'VIA_IN_PAD_REVIEW.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['Reference','Pad','CAD X mm','CAD Y mm (down-positive)','Drill mm','Process'])
    for p in audit['via_in_smd_pad']:w.writerow([p['ref'],p['pin'],*p['xy'],p['drill_mm'],'Filled capped planarized; assembler to check all overlaps'])
for name in ['assembly_top','assembly_bottom','component_bodies_top','component_bodies_bottom']:
    svg=PKG/'drawings'/('KK_power_module-'+name+'.svg');pdf=svg.with_suffix('.pdf')
    subprocess.run(['inkscape',str(svg),'--export-area-drawing','--export-filename='+str(pdf)],check=True,stdout=subprocess.DEVNULL)
shutil.copytree(CUR,ARC/'P2_compact')
shutil.copytree(PKG,OUT)
for name in ['review_drc.json','final_erc.json','LOGO_CHANGE_AUDIT.json']:copy(SRC/name,OUT/'verification'/name)
for name in ['PLANE_AUDIT_POWER_WIDTH.json']:copy(CUR/'review'/name,OUT/'verification'/name)
copy(SRC/'electrical_screening.json',OUT/'verification/electrical_screening.json')
for src,dst in [('POWER_PROTOTYPE_REVIEW.md','READ_FIRST_REVIEW_AND_TEST.md'),('POWER_FINAL_SCAN_2026-09-12.md','FINAL_SCAN.md'),('POWER_FABRICATION_REQUIREMENTS.md','FABRICATION_REQUIREMENTS.md')]:copy(ROOT/'docs'/src,OUT/dst)
for name in ['KK_power_module.kicad_pcb','KK_power_module.kicad_sch','KK_power_module.kicad_pro','KK_Power.kicad_sym','fp-lib-table','sym-lib-table','netlist.xml']:copy(SRC/name,OUT/'cad'/name)
for name in ['KK_Power.pretty','3dmodels','datasheets']:shutil.copytree(SRC/name,OUT/'cad'/name)
copy(SRC/'KK_power_module.kicad_pcb',CUR/'KK_power_module.kicad_pcb')
for name in ['KiCad-Logo_6mm_SilkScreen','OSHW-Logo_5.7x6mm_SilkScreen']:copy(SRC/'KK_Power.pretty'/(name+'.kicad_mod'),CUR/'KK_Power.pretty'/(name+'.kicad_mod'))
for name in ['review_drc.json','final_erc.json','LOGO_CHANGE_AUDIT.json']:copy(SRC/name,CUR/'review'/name)
copy(PKG/'CAD_AUDIT.json',CUR/'review/CAD_AUDIT.json')
copy(ROOT/'docs/POWER_FINAL_SCAN_2026-09-12.md',CUR/'review/FINAL_SCAN.md')
ver=read(ARC/'P2_compact/review/VERIFICATION.json')
ver.update(date=datetime.datetime.now(datetime.timezone.utc).isoformat(),PCB_SHA256=audit['PCB_SHA256'],DRC={'date':drc['date'],'violations':0,'unconnected_items':0,'schematic_parity':0},ERC={'date':erc['date'],'violations':0},logos=2,copper_unchanged_by_artwork=True,fabrication_files_unchanged_except_silkscreen=same,package=str(OUT.relative_to(ROOT)),archive=str(ARC.relative_to(ROOT)))
write(CUR/'review/VERIFICATION.json',ver);write(OUT/'verification/VERIFICATION.json',ver)
write(ARC/'PROMOTION.json',{'changed_files':[{'path':str((CUR/'KK_power_module.kicad_pcb').relative_to(ROOT)),'baseline':str((ARC/'P2_compact/KK_power_module.kicad_pcb').relative_to(ROOT)),'before_sha256':change['source_pcb_sha256'],'after_sha256':audit['PCB_SHA256']}],'package':str(OUT.relative_to(ROOT))})
write(OUT/'SHA256_MANIFEST.json',{'files':[{'path':str(p.relative_to(OUT)),'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file()]})
zip_path=OUT.with_suffix('.zip');assert not zip_path.exists()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=5,strict_timestamps=False) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,str(p.relative_to(OUT.parent)))
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
ARC.joinpath('manufacturing').mkdir()
for old in [OLD,OLD.with_suffix('.zip')]:shutil.move(str(old),str(ARC/'manufacturing'/old.name))
print(json.dumps({'package':str(zip_path),'sha256':digest(zip_path),'test_pads':len(tests),'fitted':len(bom),'unchanged_fabrication_geometry':same,'status':'Review only; manufacturer/bench approval pending'},indent=2))
