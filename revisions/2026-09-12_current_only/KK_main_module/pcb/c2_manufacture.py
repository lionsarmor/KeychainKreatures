"""Fail-closed, local prototype fabrication export. No order is placed.
Requires the reviewed routed candidate to have been promoted to the root board.
"""
from pathlib import Path
import json,subprocess,hashlib,zipfile,datetime,shutil,argparse
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['C2','C3','C4'],default='C2');revision=parser.parse_args().revision
root=Path(__file__).resolve().parent.parent
out=root/'manufacturing';out.mkdir(exist_ok=True)
board=root/'KK_main_module.kicad_pcb';sch=root/'KK_main_module.kicad_sch'
cli=['flatpak','run','--command=kicad-cli','org.kicad.KiCad']
def run(*args):subprocess.run(cli+list(map(str,args)),check=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[board,sch,root/'KK_main_module.kicad_pro',root/'KK_main_module.kicad_dru',root/'KK_Main.kicad_sym',*sorted((root/'KK_Main.pretty').glob('*.kicad_mod'))]
before={str(p.relative_to(root)):digest(p) for p in sources}
run('sch','erc','--format','json','-o',out/'ERC.json',sch)
run('pcb','drc','--format','json','--schematic-parity','-o',out/'DRC.json',board)
erc=json.loads((out/'ERC.json').read_text());drc=json.loads((out/'DRC.json').read_text())
ev=[v for s in erc.get('sheets',[]) for v in s.get('violations',[])]
assert not ev, 'ERC blocks fabrication'
assert not drc.get('violations') and not drc.get('unconnected_items') and not drc.get('schematic_parity'), 'DRC/parity blocks fabrication'
audit=json.loads((root/(f'pcb/{revision}_FINAL_VERIFICATION.json' if revision in ['C3','C4'] else 'pcb/C2_ROUTE_AUDIT.json')).read_text())
assert audit['track_segments']>0,'Cannot manufacture unrouted board'
if revision in ['C3','C4']:assert audit['board_sha256']==digest(board),'Stale independent board verification'
gerbers=out/'gerbers';gerbers.mkdir(exist_ok=True)
run('pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask','-o',str(gerbers)+'/',board)
run('pcb','export','drill','--format','excellon','--drill-origin','absolute','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',out/'DRILL_REPORT.txt','-o',str(gerbers)+'/',board)
run('pcb','export','ipc2581','--help') if False else None
expected=['F_Cu.gtl','B_Cu.gbl','F_Mask.gts','B_Mask.gbs','F_Silkscreen.gto','B_Silkscreen.gbo','Edge_Cuts.gm1']
for suffix in expected:
    files=list(gerbers.glob('*'+suffix));assert len(files)==1 and files[0].stat().st_size>100,suffix
for suffix in ['-PTH.drl','-NPTH.drl']:
    files=list(gerbers.glob('*'+suffix));assert len(files)==1 and files[0].stat().st_size>100,suffix
assert before=={str(p.relative_to(root)):digest(p) for p in sources},'Design changed during export; discard results and repeat'
if revision in ['C3','C4']:
    jobs=list(gerbers.glob('*.gbrjob'));assert len(jobs)==1
    job=json.loads(jobs[0].read_text());job['GeneralSpecs']['Finish']='Lead-free HASL'
    jobs[0].write_text(json.dumps(job,indent=2)+'\n')
manifest={'revision':'C.2','status':'ENGINEERING PROTOTYPE ONLY; no powered qualification','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':before,'erc_violations':len(ev),'drc_violations':len(drc.get('violations',[])),'unconnected_items':len(drc.get('unconnected_items',[])),'schematic_parity_issues':len(drc.get('schematic_parity',[])),'ignored_drc_categories':drc.get('ignored_checks',[]),'manufacturing_files':{str(p.relative_to(out)):digest(p) for p in sorted(gerbers.iterdir()) if p.is_file()}}
manifest['revision']=revision.replace('C','C.')
manifest['board_mm']=audit.get('board_mm',[80,100,1.6])
if revision in ['C3','C4']:manifest['specified_surface_finish']='Lead-free HASL; confirm with fabricator'
manifest['intentional_rule']='Bare TP* holes have no fitted component body: courtyard exception only. Copper, drill and edge checks remain enabled.'
(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(out/f'KK_MAIN_{revision}_PROTOTYPE_FAB.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(gerbers.iterdir()):
        if p.is_file():z.write(p,p.name)
    for name in ['README.md','DRILL_REPORT.txt','MANIFEST.json']:z.write(out/name,name)
print('Prototype fabrication archive exported after clean checks. No order placed.')
