"""Build hash-bound C6/P3 prototype packages. Sequential, one CPU via caller.
Fresh native checks; never modifies CAD or submits an order. Outputs are immutable.
"""
from pathlib import Path
import subprocess, json, hashlib, csv, shutil, tempfile, zipfile, datetime
ROOT = Path(__file__).resolve().parent.parent
CLI = ['flatpak', 'run', '--command=kicad-cli', 'org.kicad.KiCad']
PY = ['flatpak', 'run', '--command=python3', 'org.kicad.KiCad']
def run(args):
    print('RUN ' + ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), check=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def write(p, data): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(data, indent=2)+'\n')
def copy(a,b): b.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(a,b)
def tree(a,b): shutil.copytree(a,b,dirs_exist_ok=True)
def files(d): return {str(p.relative_to(d)): sha(p) for p in sorted(d.rglob('*')) if p.is_file()}
def zip_checked(directory, target):
    assert not target.exists(), target
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=4, strict_timestamps=False) as z:
        for p in sorted(directory.rglob('*')):
            if p.is_file(): z.write(p, str(p.relative_to(directory)))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for name, want in files(directory).items(): assert hashlib.sha256(z.read(name)).hexdigest()==want
date='2026-09-12'
releases=[]
for kind, rev, folder in [('main','C6','C6_flat_stack'), ('power','P3','P3_matching_stack')]:
    stem='KK_'+kind+'_module'; src=ROOT/stem/folder
    name=f'KK_{kind.upper()}_{rev}_5_PROTOTYPE_REVIEW_{date}'
    dest=ROOT/stem/'manufacturing'/name
    assert not dest.exists() and not dest.with_suffix('.zip').exists(), 'Do not overwrite released output'
    checks=src/'release_checks'; checks.mkdir(exist_ok=True)
    exts=['kicad_pcb','kicad_sch','kicad_pro']+(['kicad_dru'] if kind=='main' else [])
    before={stem+'.'+e:sha(src/(stem+'.'+e)) for e in exts}
    run(CLI+['sch','erc','--format','json','-o',checks/'ERC.json',src/(stem+'.kicad_sch')])
    run(CLI+['pcb','drc','--format','json','--schematic-parity','-o',checks/'DRC.json',src/(stem+'.kicad_pcb')])
    erc=read(checks/'ERC.json'); drc=read(checks/'DRC.json')
    assert 'sheets' in erc and all(not s['violations'] for s in erc['sheets'])
    assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
    # Refresh the conventional final reports only with new clean native results.
    copy(checks/'ERC.json',src/'reports/erc.json')
    copy(checks/'DRC.json',src/'reports'/('drc_repaired.json' if kind=='main' else 'drc.json'))
    run(PY+[ROOT/'tools/stack_release_native.py',kind])
    audit=read(checks/'CAD_AUDIT.json')
    assert all(before[n]==h for n,h in audit['source_sha256'].items())
    run(CLI+['sch','export','netlist','--format','kicadxml','-o',src/'netlist.xml',src/(stem+'.kicad_sch')])
    run(CLI+['sch','export','pdf','-o',src/'assembly/SCHEMATIC.pdf',src/(stem+'.kicad_sch')])
    run(CLI+['pcb','export','pos','--format','csv','--units','mm','--side','both','-o',checks/'POSITIONS_NATIVE.csv',src/(stem+'.kicad_pcb')])
    with (checks/'POSITIONS_NATIVE.csv').open(newline='') as f: pos=list(csv.DictReader(f))
    with (checks/'BOM_AND_PLACEMENT.csv').open(newline='') as f: bom=list(csv.DictReader(f))
    assert {r['Ref'] for r in pos}=={r['Reference'] for r in bom}, 'Placement export excludes/includes wrong parts'
    for svg in sorted((checks/'drawings').glob('*.svg')):
        run(['inkscape',svg,'--export-area-drawing','--export-filename='+str(svg.with_suffix('.pdf'))])
    fab=checks/'fabrication'; fab.mkdir(exist_ok=True)
    layers='F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts' if kind=='main' else 'F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts'
    run(CLI+['pcb','export','gerbers','--layers',layers,'--subtract-soldermask','-o',str(fab)+'/',src/(stem+'.kicad_pcb')])
    run(CLI+['pcb','export','drill','--format','excellon','--drill-origin','absolute','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',fab/'DRILL_REPORT.txt','-o',str(fab)+'/',src/(stem+'.kicad_pcb')])
    run(CLI+['pcb','export','ipcd356','-o',fab/(stem+'.ipc'),src/(stem+'.kicad_pcb')])
    required=['gtl','gbl','gts','gbs','gto','gbo','gm1']+(['g1','g2','gtp','gbp'] if kind=='power' else [])
    for ext in required:
        found=list(fab.glob('*.'+ext)); assert len(found)==1 and found[0].stat().st_size>100,ext
    for suffix in ['-PTH.drl','-NPTH.drl','.ipc']:
        assert (fab/(stem+suffix)).stat().st_size>100,suffix
    jobpaths=list(fab.glob('*.gbrjob')); assert len(jobpaths)==1
    job=read(jobpaths[0]); print('JOB SPECS '+json.dumps(job['GeneralSpecs']),flush=True)
    assert job['GeneralSpecs']['LayerNumber']==(2 if kind=='main' else 4)
    size=job['GeneralSpecs']['Size']; assert abs(size['X']-96)<.1 and abs(size['Y']-105)<.1,size
    # Issued CAD, Gerbers, docs and selected audit evidence only; no failed routes.
    dest.mkdir(parents=True)
    tree(fab,dest/'fabrication'); tree(src/'assembly',dest/'assembly')
    for p in checks.glob('*.csv'): copy(p,dest/'assembly'/p.name)
    tree(checks/'drawings',dest/'drawings')
    for p in [checks/'CAD_AUDIT.json',checks/'DRC.json',checks/'ERC.json']: copy(p,dest/'verification'/p.name)
    for e in exts: copy(src/(stem+'.'+e),dest/'cad'/(stem+'.'+e))
    lib='KK_Main' if kind=='main' else 'KK_Power'
    for n in [lib+'.kicad_sym','fp-lib-table','sym-lib-table','netlist.xml']: copy(src/n,dest/'cad'/n)
    for n in [lib+'.pretty','3dmodels','datasheets']: tree(src/n,dest/'cad'/n)
    if kind=='main':
        copy(src/'component_changes.json',dest/'verification/component_changes.json')
        for n in ['ROUTING_RULES.json','pin_net_preservation.json','trace_fed_ground_pads.json','LOCAL_REPAIRS.json','silkscreen_labels_final.json']: copy(src/'reports'/n,dest/'verification'/n)
        for n in ['main_front.png','main_back.png','main_oblique.png']: copy(src/'reports'/n,dest/'drawings'/n)
        fabnotes='''# C.6 main — five bare prototype PCBs

96 x 105 x 1.6 mm, two copper layers (F.Cu/B.Cu), R4 corners. Four 2.2 mm M2 NPTH holes at (4,4), (92,4), (4,101), (92,101) mm. Do not scale or panelize without preserving the supplied board outline and hole registration. Standard FR-4; CAD nominal 35um copper. Confirm finished copper/plating and lead-free surface finish with fabricator. No battery or charger circuit is on this PCB.

Use BOTH copper, BOTH mask, BOTH silkscreen, Edge.Cuts and BOTH PTH/NPTH drills. Empty paste files intentionally omitted: main-board kit assembly is through-hole, with preassembled socketed modules. 98 electrical positions, 25 bare debugging holes and four mounting holes. No fitted pins in the debug holes beneath other parts. IPC-D-356 provided for bare-board net testing.

All 43 resistors are horizontal, ten electrolytics and six TO-92 bodies lie flat per assembly drawings. Correct lead forms and polarity remain essential. Sockets, optics and buttons retain functional height. See the assembly kit extras separately; BOM chip/module positions do not replace the additional sockets and mating plugs.

Engineering prototype only. Confirm actual part fit, socket retention, inter-board plug/wire clearance and fabrication DFM before ordering. Main C.6 pairs with power P.3; do not mix older C.5/P.2 Gerbers.
'''
        (dest/'FABRICATION_REQUIREMENTS.md').write_text(fabnotes)
    else:
        for n in ['design.json','electrical_screening.json']: copy(src/n,dest/'cad'/n)
        for n in ['rigid_core_preservation.json','model_link_repair.json']: copy(src/'reports'/n,dest/'verification'/n)
        copy(src/'reports/power_front.png',dest/'drawings/power_front.png')
        copy(src/'assembly/FABRICATION_REQUIREMENTS.md',dest/'FABRICATION_REQUIREMENTS.md')
        copy(ROOT/'KK_main_module/C6_flat_stack/assembly/C6_COMPLETE_KIT_EXTRAS.csv',dest/'assembly/C6_P3_COMPLETE_KIT_EXTRAS.csv')
    copy(ROOT/'docs/C6_P3_STACK_REVIEW.pdf',dest/'assembly/STACK_REVIEW_PRINT_ACTUAL_SIZE.pdf')
    text=f'''# {rev} — five engineering samples, not a production approval

Current project: {stem}/{folder}. Open cad/{stem}.kicad_pro in KiCad 10 with its standard footprint/3D libraries installed. Local custom symbols, footprints, models and source datasheets are included. Do not use older 84x95 main or 50x50 power outputs. Both revised boards are 96x105 mm; MAIN HAS TWO COPPER LAYERS, POWER HAS FOUR.

fabrication/: Gerbers, separate PTH/NPTH drills, drill maps/report, IPC-D-356. Read FABRICATION_REQUIREMENTS.md and obtain factory DFM approval before ordering. For POWER this includes filled/capped/planarized via-in-pad and 0.4mm WCSP assembly; ordinary tenting is not sufficient. Factory must verify partial land/via overlaps, stencil and hidden joints, rotations and all substitutions.

assembly/: BOM grouped for FIVE (no attrition), reference BOM/placement, test-point and connector maps, schematic PDF, current assembly/test guide, complete paired-kit extras and mounting review. Placement reference CSV uses native X-right/Y-down coordinates; POSITIONS_NATIVE.csv is KiCad's native Y-up export. Neither is approved machine programming; assembler must validate conventions, side, rotations and polarity. Main is a through-hole kit; power is a factory SMT subassembly. Complete-kit extras apply ONCE per main+power pair, not once per board.

drawings/: front/back assembly and body views plus 3D previews. Bottom views are mirrored. Model attachment coverage is not physical certification. Flat capacitors have actual maximum body envelopes, but sockets, buttons and optics still stand above the board. Physical module/plug fit, 20mm trial stack spacing, battery/case/RF clearance and solder-tail trimming need a real mock-up. No STEP model can approve an unselected battery.

verification/: fresh native ERC/DRC/parity, independent audits and hashes. Clean reported CAD checks do not prove charging safety, thermal margin, current capacity, USB compliance, firmware behavior or toy certification. Existing ignored-check settings are recorded verbatim, not claimed as tests performed.

Power J3 -> main J1: pin1 MCU_5V, pin2 GND, pin3 LOGIC_3V3, pin4 ACT_3V2. Never connect raw battery to main. Power TP3 BAT_NEG is NOT TP4 GND. Charger USB carries no data. Do not combine ESP32 USB power with external main rails until backfeed is qualified. USB-A/default charging is deliberately very slow; running load may still discharge the cell. Battery choice, speaker rating and integrated peak-load qualification remain open. Follow the current-limited first-power-up guide; no real-cell testing without a qualified cell/NTC setup.

Nothing has been uploaded, purchased or ordered. SHA256_MANIFEST.json inventories package files; RELEASE_VERIFICATION.json binds current CAD to checks/exports. No failed route candidates or historical Gerbers are included.
'''
    (dest/'READ_FIRST.md').write_text(text)
    after={n:sha(src/n) for n in before}; assert after==before,'CAD changed during export'
    ver={'revision':rev,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_project':str(src.relative_to(ROOT)),'source_sha256':before,'native_checks':{'ERC':0,'DRC':0,'opens':0,'schematic_parity':0,'ignored_DRC_checks':drc.get('ignored_checks',[])},'cad_audit_sha256':sha(checks/'CAD_AUDIT.json'),'reports_sha256':{'DRC.json':sha(checks/'DRC.json'),'ERC.json':sha(checks/'ERC.json')},'fabrication_sha256':files(fab),'board_mm':[96,105,1.6],'copper_layers':audit['copper_layers'],'fitted':audit['fitted'],'bare_debug_points':audit['test_pads'],'manufacturer_approved':False,'physical_fit_qualified':False,'powered_tested':False,'status':'PROTOTYPE DFM / FABRICATION REVIEW FILES; physical, supply/process and bench approval pending'}
    write(dest/'RELEASE_VERIFICATION.json',ver)
    copy(dest/'RELEASE_VERIFICATION.json',src/'release_checks/RELEASE_VERIFICATION.json')
    # Seal later only after independent two-board static audit and matching-edge checks.
    releases.append({'kind':kind,'revision':rev,'source':str(src.relative_to(ROOT)),'directory':str(dest.relative_to(ROOT))})
run(PY+[ROOT/'tools/flat_stack_audit.py'])
static=read(ROOT/'docs/C6_P3_STATIC_AUDIT.json')
for item in releases:
    dest=ROOT/item['directory']; stem='KK_'+item['kind']+'_module'
    ver=read(dest/'RELEASE_VERIFICATION.json')
    assert ver['source_sha256'][stem+'.kicad_pcb']==static['boards'][stem]['pcb_sha256']
    copy(ROOT/'docs/C6_P3_STATIC_AUDIT.json',dest/'verification/C6_P3_STATIC_AUDIT.json')
def gerber_geometry(p):
    return '\n'.join(line for line in p.read_text().splitlines() if not line.startswith('G04') and not line.startswith('%TF.'))
edge=[next((ROOT/i['directory']/'fabrication').glob('*.gm1')) for i in releases]
assert gerber_geometry(edge[0])==gerber_geometry(edge[1]), 'Board outline Gerber geometry differs'
for item in releases:
    dest=ROOT/item['directory']
    write(dest/'SHA256_MANIFEST.json',{'files':files(dest)})
    zip_checked(dest,dest.with_suffix('.zip'))
    item.update(zip=str(dest.with_suffix('.zip').relative_to(ROOT)),zip_sha256=sha(dest.with_suffix('.zip')),file_count=len(files(dest)))
    # Fabrication-only upload ZIP also carries process requirements and source verification.
    fabzip=dest.parent/f'KK_{item["kind"].upper()}_{item["revision"]}_GERBERS.zip'
    assert not fabzip.exists()
    with zipfile.ZipFile(fabzip,'w',zipfile.ZIP_DEFLATED,compresslevel=4,strict_timestamps=False) as z:
        for p in sorted((dest/'fabrication').iterdir()):
            if p.is_file(): z.write(p,p.name)
        for n in ['FABRICATION_REQUIREMENTS.md','RELEASE_VERIFICATION.json']: z.write(dest/n,n)
    with zipfile.ZipFile(fabzip) as z: assert z.testzip() is None
    item.update(gerbers_zip=str(fabzip.relative_to(ROOT)),gerbers_sha256=sha(fabzip))
write(ROOT/'docs/C6_P3_RELEASE_INDEX.json',{'boards':releases,'matching_outline_gerber_geometry':True,'order_placed':False,'qualified_product':False})
print(json.dumps(releases,indent=2))
