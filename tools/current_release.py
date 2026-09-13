"""Immutable C6/P4 review packages; fresh sequential native checks, no routing.

Caller should use nice -n 15 taskset -c 0. No upload, purchase, or order.
"""
from pathlib import Path
import subprocess, json, hashlib, csv, shutil, zipfile, datetime, sys
ROOT=Path(__file__).resolve().parent.parent
CLI=['flatpak','run','--command=kicad-cli','org.kicad.KiCad']
PY=['flatpak','run','--command=python3','org.kicad.KiCad']
OLD=ROOT/'revisions/2026-09-12_power_compact/P3_previous'
def run(args):
    print('RUN '+' '.join(map(str,args)),flush=True)
    subprocess.run(list(map(str,args)),check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def copy(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
def tree(a,b):shutil.copytree(a,b,dirs_exist_ok=True)
def files(d):return {str(p.relative_to(d)):sha(p) for p in sorted(d.rglob('*')) if p.is_file()}
def rel(p):return str(p.relative_to(ROOT))
def zip_checked(d,p):
    assert not p.exists(),p
    with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=4,strict_timestamps=False) as z:
        for f in sorted(d.rglob('*')):
            if f.is_file():z.write(f,str(f.relative_to(d)))
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        for n,h in files(d).items():assert hashlib.sha256(z.read(n)).hexdigest()==h
date='2026-09-12'
assert not (ROOT/'docs/CURRENT_RELEASE_INDEX.json').exists(),'Already issued; do not overwrite'
release=[]
if '--seal-existing' not in sys.argv:run(['python3',ROOT/'tools/flat_stack_report.py'])
for kind,rev,label,dims in [('main','C6','C6_P4_PAIRING',[96,105]),('power','P4','P4',[50,50])]:
    stem='KK_'+kind+'_module';src=ROOT/stem
    dest=src/'manufacturing'/f'KK_{kind.upper()}_{label}_5_PROTOTYPE_REVIEW_{date}'
    if '--seal-existing' in sys.argv:
        assert dest.exists() and not dest.with_suffix('.zip').exists(),'Only unissued complete drafts can be sealed'
        ver=read(dest/'RELEASE_VERIFICATION.json')
        assert all(sha(src/n)==h and sha(dest/'cad'/n)==h for n,h in ver['source_sha256'].items())
        assert files(dest/'fabrication')==ver['fabrication_sha256']
        assert all(sha(dest/'verification'/n)==h for n,h in ver['reports_sha256'].items())
        assert sha(src/'release_checks/CAD_AUDIT.json')==ver['cad_audit_sha256']
        drc=read(dest/'verification/DRC.json');erc=read(dest/'verification/ERC.json')
        assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
        assert all(not s['violations'] for s in erc['sheets'])
        release.append({'kind':kind,'revision':rev,'label':label,'source':rel(src),'directory':rel(dest)})
        continue
    assert not dest.exists() and not dest.with_suffix('.zip').exists(),dest
    checks=src/'release_checks';checks.mkdir(exist_ok=True)
    exts=['kicad_pcb','kicad_sch','kicad_pro']+(['kicad_dru'] if kind=='main' else [])
    before={stem+'.'+e:sha(src/(stem+'.'+e)) for e in exts}
    run(CLI+['sch','erc','--format','json','-o',checks/'ERC.json',src/(stem+'.kicad_sch')])
    run(CLI+['pcb','drc','--format','json','--schematic-parity','-o',checks/'DRC.json',src/(stem+'.kicad_pcb')])
    erc=read(checks/'ERC.json');drc=read(checks/'DRC.json')
    assert 'sheets' in erc and all(not s['violations'] for s in erc['sheets'])
    assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
    copy(checks/'ERC.json',src/'reports/erc.json')
    copy(checks/'DRC.json',src/'reports'/('drc_repaired.json' if kind=='main' else 'drc.json'))
    run(PY+[ROOT/'tools/stack_release_native.py',kind])
    audit=read(checks/'CAD_AUDIT.json');assert all(before[n]==h for n,h in audit['source_sha256'].items())
    run(CLI+['sch','export','netlist','--format','kicadxml','-o',src/'netlist.xml',src/(stem+'.kicad_sch')])
    run(CLI+['sch','export','pdf','-o',src/'assembly/SCHEMATIC.pdf',src/(stem+'.kicad_sch')])
    run(CLI+['pcb','export','pos','--format','csv','--units','mm','--side','both','-o',checks/'POSITIONS_NATIVE.csv',src/(stem+'.kicad_pcb')])
    with (checks/'POSITIONS_NATIVE.csv').open(newline='') as f:pos=list(csv.DictReader(f))
    with (checks/'BOM_AND_PLACEMENT.csv').open(newline='') as f:bom=list(csv.DictReader(f))
    assert {r['Ref'] for r in pos}=={r['Reference'] for r in bom}
    for svg in sorted((checks/'drawings').glob('*.svg')):
        run(['inkscape',svg,'--export-area-drawing','--export-filename='+str(svg.with_suffix('.pdf'))])
    # A fresh fabrication directory prevents inclusion of stale exports.
    fab=checks/'fabrication_P4_pairing';assert not fab.exists();fab.mkdir()
    layers='F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts' if kind=='main' else 'F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts'
    run(CLI+['pcb','export','gerbers','--layers',layers,'--subtract-soldermask','-o',str(fab)+'/',src/(stem+'.kicad_pcb')])
    run(CLI+['pcb','export','drill','--format','excellon','--drill-origin','absolute','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',fab/'DRILL_REPORT.txt','-o',str(fab)+'/',src/(stem+'.kicad_pcb')])
    run(CLI+['pcb','export','ipcd356','-o',fab/(stem+'.ipc'),src/(stem+'.kicad_pcb')])
    for e in ['gtl','gbl','gts','gbs','gto','gbo','gm1']+(['g1','g2','gtp','gbp'] if kind=='power' else []):
        found=list(fab.glob('*.'+e));assert len(found)==1 and found[0].stat().st_size>100,e
    for e in ['-PTH.drl','-NPTH.drl','.ipc']:assert (fab/(stem+e)).stat().st_size>100
    job=read(next(fab.glob('*.gbrjob')))
    assert job['GeneralSpecs']['LayerNumber']==(2 if kind=='main' else 4)
    size=job['GeneralSpecs']['Size'];assert all(abs(size[k]-v)<.06 for k,v in zip(['X','Y'],dims)),size
    dest.mkdir(parents=True)
    tree(fab,dest/'fabrication');tree(src/'assembly',dest/'assembly')
    # Same kit extras apply once per pair; always include main assembly instructions
    # alongside them so speaker and socket notes have context in either package.
    copy(ROOT/'KK_main_module/assembly/ASSEMBLY_GUIDE.md',dest/'assembly/ASSEMBLY_GUIDE.md')
    copy(ROOT/'KK_main_module/FABRICATION_REQUIREMENTS.md',dest/'assembly/MAIN_FABRICATION_REQUIREMENTS.md')
    with (ROOT/'KK_main_module/assembly/C6_COMPLETE_KIT_EXTRAS.csv').open(newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;extras=list(reader)
    for row in extras:
        source=row['Source / drawing']
        if source.startswith('../datasheets/'):
            name=Path(source).name
            copy(ROOT/'KK_main_module/datasheets'/name,dest/'assembly/KIT_DATASHEETS'/name)
            row['Source / drawing']='KIT_DATASHEETS/'+name
        elif source=='../FABRICATION_REQUIREMENTS.md':row['Source / drawing']='MAIN_FABRICATION_REQUIREMENTS.md'
    # Replace the live-source CSV copy too, so both copies in the package agree.
    for name in ['C6_COMPLETE_KIT_EXTRAS.csv','C6_P4_COMPLETE_KIT_EXTRAS.csv']:
        with (dest/'assembly'/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(extras)
    copy(ROOT/'KK_power_module/assembly/P4_REVIEW_AND_TEST.md',dest/'assembly/P4_REVIEW_AND_TEST.md')
    for p in checks.glob('*.csv'):copy(p,dest/'assembly'/p.name)
    tree(checks/'drawings',dest/'drawings')
    for n in ['CAD_AUDIT.json','ERC.json','DRC.json']:copy(checks/n,dest/'verification'/n)
    for e in exts:copy(src/(stem+'.'+e),dest/'cad'/(stem+'.'+e))
    lib='KK_Main' if kind=='main' else 'KK_Power'
    for n in [lib+'.kicad_sym','fp-lib-table','sym-lib-table','netlist.xml']:copy(src/n,dest/'cad'/n)
    for n in [lib+'.pretty','3dmodels','datasheets']:tree(src/n,dest/'cad'/n)
    if kind=='main':
        copy(src/'component_changes.json',dest/'verification/component_changes.json')
        for n in ['ROUTING_RULES.json','pin_net_preservation.json','trace_fed_ground_pads.json','LOCAL_REPAIRS.json','silkscreen_labels_final.json']:copy(src/'reports'/n,dest/'verification'/n)
        for n in ['main_front.png','main_back.png','main_oblique.png']:copy(src/'reports'/n,dest/'drawings'/n)
    else:
        for n in ['design.json','electrical_screening.json']:copy(src/n,dest/'cad'/n)
        copy(src/'reports/COMPACT_CHANGE_AUDIT.json',dest/'verification/COMPACT_CHANGE_AUDIT.json')
        copy(src/'reports/power_compact_front.png',dest/'drawings/power_front.png')
    copy(src/'FABRICATION_REQUIREMENTS.md',dest/'FABRICATION_REQUIREMENTS.md')
    copy(ROOT/'docs/C6_P4_MECHANICAL_REVIEW.pdf',dest/'assembly/MECHANICAL_REVIEW_PRINT_ACTUAL_SIZE.pdf')
    (dest/'READ_FIRST.md').write_text(f'''# {rev} — five engineering samples; not production approval

Current editable project: {stem} at the repository root. This package is the C6/P4 pairing release. Open cad/{stem}.kicad_pro with KiCad 10 and its standard libraries. Custom assets and selected datasheets are included.

Main C.6: 96 x 105 x 1.6 mm, R4, TWO copper layers. Power P.4: 50 x 50 x 1.6 mm, R3, FOUR copper layers. Four 2.2 mm mounting holes on each board, DIFFERENT patterns: use independent case supports. Main CAD/fabrication geometry is unchanged; its documentation is refreshed. Do not use the old common-hole/20 mm shared-spacer instructions. Separate 1:1 templates are included; physical placement, antenna clearance, battery location and spacing are not approved.

fabrication/: Gerbers, separate PTH/NPTH drills, maps/report and IPC-D-356 netlist. Obtain factory DFM approval BEFORE ordering. Power requires filled/capped/planarized via-in-pad and 0.4 mm WCSP assembly approval; ordinary tenting is insufficient. No unreviewed substitutions.

assembly/: BOMs, placement, test-point and connector maps, schematic PDF, assembly/bench guides and paired-kit extras. Extras apply ONCE per pair. References to repository-relative datasheets in kit CSVs refer to the full repository; the selected board's datasheets are under cad/datasheets. Reference positions use CAD X-right/Y-down; POSITIONS_NATIVE.csv uses native KiCad Y-up. Assembler must validate rotations, origins, side, polarity and THT secondary operations before machine programming. Main is a student THT kit; power is factory SMT.

drawings/: assembly/body drawings and model previews; bottom views are mirrored. Model coverage is not delivered-part fit certification. verification/: fresh native checks, static audit and source hashes; ignored-check settings are recorded, not hidden.

Power J3 to main J1: 1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2, keyed pin-for-pin. Never connect raw battery to main. Power TP3 BAT_NEG is NOT TP4 GND. Charger USB has no data. Do not combine ESP32 USB power and main external rails until exact-module backfeed is qualified. Firmware and Wi-Fi game uploads are not implemented by this hardware release.

Read P4_REVIEW_AND_TEST.md before powering. Use current-limited equipment; charging tests need a sink-capable battery emulator or a qualified cell/NTC. Actual simultaneous loads, thermal behavior, rail sequencing, USB behavior, protection, speaker rating and physical/RF fit remain untested. The 3.3 V screening target is 0.4 A versus the older main 0.5 A reservation; measure demand and margin. No real cell is selected. No toy-safety or EMC certification is claimed.

RELEASE_VERIFICATION.json binds source CAD, fresh reports and fabrication outputs. SHA256_MANIFEST.json inventories all package files except itself. This package is for review, not an order; no factory submission or purchase has been made.
''')
    assert {n:sha(src/n) for n in before}==before,'CAD changed during export'
    ver={'revision':rev,'pairing':'C6/P4','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_project':rel(src),'source_sha256':before,'native_checks':{'ERC':0,'DRC':0,'opens':0,'schematic_parity':0,'ignored_DRC_checks':drc.get('ignored_checks',[])},'cad_audit_sha256':sha(checks/'CAD_AUDIT.json'),'reports_sha256':{n:sha(checks/n) for n in ['DRC.json','ERC.json']},'fabrication_sha256':files(fab),'board_mm':dims+[1.6],'copper_layers':audit['copper_layers'],'fitted':audit['fitted'],'bare_debug_points':audit['test_pads'],'manufacturer_approved':False,'physical_fit_qualified':False,'powered_tested':False,'status':'PROTOTYPE DFM REVIEW; physical, process, supply and bench qualification pending'}
    write(dest/'RELEASE_VERIFICATION.json',ver);copy(dest/'RELEASE_VERIFICATION.json',checks/'RELEASE_VERIFICATION.json')
    release.append({'kind':kind,'revision':rev,'label':label,'source':rel(src),'directory':rel(dest)})

run(PY+[ROOT/'tools/flat_stack_audit.py'])
static=read(ROOT/'docs/CURRENT_STATIC_AUDIT.json')
oldmain=OLD/'KK_main_module/manufacturing/KK_MAIN_C6_5_PROTOTYPE_REVIEW_2026-09-12'
newmain=ROOT/release[0]['directory']
oldver=read(oldmain/'RELEASE_VERIFICATION.json');newver=read(newmain/'RELEASE_VERIFICATION.json')
assert oldver['source_sha256']==newver['source_sha256'],'Main native CAD changed'
def geometry(p):
    return '\n'.join(l for l in p.read_text().splitlines() if not l.startswith(('G04','%TF.','; #@!','; Creation date:','; DRILL file KiCad')))
compared=[]
for p in (oldmain/'fabrication').iterdir():
    if p.suffix in ['.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1','.drl']:
        q=newmain/'fabrication'/p.name
        assert geometry(p)==geometry(q),'Main fabrication geometry changed: '+p.name
        compared.append(p.name)
write(ROOT/'docs/MAIN_FABRICATION_PRESERVATION.json',{'status':'PASS','native_source_hashes_unchanged':True,'files_compared_ignoring_generation_metadata':compared,'old_package':rel(oldmain),'new_package':rel(newmain)})
for item in release:
    dest=ROOT/item['directory'];stem='KK_'+item['kind']+'_module'
    assert read(dest/'RELEASE_VERIFICATION.json')['source_sha256'][stem+'.kicad_pcb']==static['boards'][stem]['pcb_sha256']
    copy(ROOT/'docs/CURRENT_STATIC_AUDIT.json',dest/'verification/CURRENT_STATIC_AUDIT.json')
    copy(ROOT/'docs/MAIN_FABRICATION_PRESERVATION.json',dest/'verification/MAIN_FABRICATION_PRESERVATION.json')
    write(dest/'SHA256_MANIFEST.json',{'files':files(dest)})
    zip_checked(dest,dest.with_suffix('.zip'))
    item.update(zip=rel(dest.with_suffix('.zip')),zip_sha256=sha(dest.with_suffix('.zip')),file_count=len(files(dest)))
    fabzip=dest.parent/f'KK_{item["kind"].upper()}_{item["label"]}_GERBERS.zip';assert not fabzip.exists()
    with zipfile.ZipFile(fabzip,'w',zipfile.ZIP_DEFLATED,compresslevel=4,strict_timestamps=False) as z:
        for p in sorted((dest/'fabrication').iterdir()):
            if p.is_file():z.write(p,p.name)
        for n in ['FABRICATION_REQUIREMENTS.md','RELEASE_VERIFICATION.json']:z.write(dest/n,n)
    with zipfile.ZipFile(fabzip) as z:assert z.testzip() is None
    item.update(gerbers_zip=rel(fabzip),gerbers_sha256=sha(fabzip))
    (dest.parent/'README.md').write_text(f'# Current {item["revision"]} / C6-P4 pairing files\n\n[Full five-sample review ZIP]({dest.name}.zip) · [Gerbers and drills]({fabzip.name})\n\nRead fabrication requirements before ordering. Engineering review only; DFM, physical fit and powered qualification remain open. Old packages are archived under revisions/2026-09-12_power_compact/P3_previous at the repository root.\n')
write(ROOT/'docs/CURRENT_RELEASE_INDEX.json',{'boards':release,'matching_outline_gerber_geometry':False,'matching_mounting_holes':False,'pairing':'C6/P4','main_CAD_unchanged':True,'main_fabrication_geometry_unchanged':True,'order_placed':False,'qualified_product':False,'promotion_manifest':'revisions/2026-09-12_power_compact/PROMOTION.json'})
promotion=ROOT/'revisions/2026-09-12_power_compact/PROMOTION.json';p=read(promotion)
p.update(state='complete',release_index='docs/CURRENT_RELEASE_INDEX.json',release_index_sha256=sha(ROOT/'docs/CURRENT_RELEASE_INDEX.json'));write(promotion,p)
copy(ROOT/'docs/C6_P4_MECHANICAL_REVIEW.pdf',Path('/home/legion/Desktop/PRINT THIS.pdf'))
print(json.dumps(release,indent=2),flush=True)
