"""Prepare P.4 compact power candidate; current root board remains untouched.
Run with KiCad Flatpak Python. Preserve all electrical routing and P.3 model fixes.
"""
from pathlib import Path
import pcbnew as k
import json, hashlib, shutil, sys

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'KK_power_module'
OLD=ROOT/'revisions/2026-09-12_current_only/KK_power_module/P2_compact'
OUT=ROOT/'revisions/2026-09-12_power_compact/P4_candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [round(k.ToMM(p.x),6),round(k.ToMM(p.y),6)]
if '--update-label' in sys.argv:
    board=k.LoadBoard(str(OUT/'KK_power_module.kicad_pcb'))
    for item in board.GetDrawings():
        if isinstance(item,k.PCB_TEXT):item.SetText(item.GetText().replace('KK POWER P3','KK POWER P4'))
    k.SaveBoard(str(OUT/'KK_power_module.kicad_pcb'),board)
    p=OUT/'reports/COMPACT_CHANGE_AUDIT.json';d=json.loads(p.read_text())
    d['candidate_sha256']=sha(OUT/'KK_power_module.kicad_pcb');p.write_text(json.dumps(d,indent=2)+'\n')
    print('Candidate silkscreen revision now P4. Current root unchanged.');sys.exit(0)
assert not OUT.exists(),'Candidate exists; do not overwrite'
index=json.loads((ROOT/'docs/C6_P3_RELEASE_INDEX.json').read_text())
item=next(b for b in index['boards'] if b['kind']=='power')
ver=json.loads((ROOT/item['directory']/'RELEASE_VERIFICATION.json').read_text())
assert all(sha(SRC/n)==h for n,h in ver['source_sha256'].items()),'Current power source changed since review'
main=ROOT/'KK_main_module/KK_main_module.kicad_pcb';mainhash=sha(main)
OUT.mkdir(parents=True)
for name in ['KK_power_module.kicad_pcb','KK_power_module.kicad_sch','KK_power_module.kicad_pro','KK_Power.kicad_sym','fp-lib-table','sym-lib-table','design.json','electrical_screening.json']:
    shutil.copy2(SRC/name,OUT/name)
for name in ['KK_Power.pretty','3dmodels','datasheets']:shutil.copytree(SRC/name,OUT/name)
(OUT/'reports').mkdir();(OUT/'assembly').mkdir()
baseline={str((SRC/n).relative_to(ROOT)):h for n,h in ver['source_sha256'].items()}
(OUT/'SOURCE_BASELINE.json').write_text(json.dumps(baseline,indent=2)+'\n')
original=k.LoadBoard(str(OLD/'KK_power_module.kicad_pcb'))
b=k.LoadBoard(str(OUT/'KK_power_module.kicad_pcb'))
def signature(board,transform=False):
    def pos(p):
        x,y=xy(p);return [round(51-x if transform else x,5),round(104-y if transform else y,5)]
    pads=sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),pos(p.GetPosition()),xy(p.GetSize()),xy(p.GetDrillSize()),int(p.GetAttribute())) for f in board.GetFootprints() if not f.GetReference().startswith('H') for p in f.Pads())
    tracks=sorted((t.GetClass(),t.GetNetname(),pos(t.GetStart()),pos(t.GetEnd()),int(t.GetLayer()),t.GetWidth(k.F_Cu) if t.GetClass()=='PCB_VIA' else t.GetWidth(),t.GetDrillValue() if t.GetClass()=='PCB_VIA' else 0) for t in board.GetTracks())
    return {'pads':pads,'tracks':tracks}
expected=signature(b,True)
retained=list(b.GetFootprints())+list(b.GetTracks())+list(b.Zones())+list(b.GetDrawings())
removed=[]
for item in retained:
    obsolete_text=isinstance(item,k.PCB_TEXT) and any(t in item.GetText() for t in ['P3 MATCHING STACK','96 x 105 / COMMON M2','KEEP BATTERY / WIRING / METAL OUT','MECHANICAL CANDIDATE - NOT RELEASED'])
    obsolete_zone=isinstance(item,k.ZONE) and item.GetZoneName()=='P3_MAIN_ANTENNA_CLEARANCE'
    if item.GetLayer()==k.Edge_Cuts or obsolete_text or obsolete_zone:
        b.Remove(item);removed.append(item);continue
    item.Rotate(v(0,0),k.EDA_ANGLE(180,k.DEGREES_T));item.Move(v(51,104))
holes={f.GetReference():f for f in original.GetFootprints() if f.GetReference().startswith('H')}
for f in b.GetFootprints():
    if f.GetReference() in holes:
        h=holes[f.GetReference()];f.SetPosition(h.GetPosition());f.SetOrientationDegrees(h.GetOrientationDegrees())
for item in original.GetDrawings():
    if item.GetLayer()==k.Edge_Cuts:
        new=item.Duplicate();new.SetParent(b);b.Add(new);retained.append(new)
assert signature(b)==expected,'P3 electrical routing was not preserved'
assert signature(b)==signature(original),'Compact electrical pads/tracks differ from original routed P2 core'
b.GetTitleBlock().SetRevision('P.4 compact 50mm prototype')
# Preserve printed core labels; update only its board-revision identifier.
for item in b.GetDrawings():
    if isinstance(item,k.PCB_TEXT):item.SetText(item.GetText().replace('P.3','P.4').replace('P3 ','P4 ').replace('KK POWER P3','KK POWER P4'))
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones())
k.SaveBoard(str(OUT/'KK_power_module.kicad_pcb'),b)
sch=OUT/'KK_power_module.kicad_sch';text=sch.read_text()
assert text.count('(rev "P.3 flat stack engineering")')==1
sch.write_text(text.replace('(rev "P.3 flat stack engineering")','(rev "P.4 compact 50mm prototype")'))
design=json.loads((OUT/'design.json').read_text())
design['revision']='P.4 COMPACT POWER PROTOTYPE'
design['mechanical']={'outline_mm':[50,50],'radius_mm':3,'thickness_mm':1.6,'mounting_centers_mm':{r:xy(f.GetPosition()) for r,f in holes.items()},'note':'Original compact outline and power mounting holes restored; not aligned to C6 main holes. Separate case supports and keyed flexible harness required. Keep compact board/metal clear of main ESP32 antenna.'}
(OUT/'design.json').write_text(json.dumps(design,indent=2)+'\n')
assert sha(main)==mainhash
report={'status':'PASS — electrical pad/net/trace/via geometry preserved; native DRC and physical fit still required','source_p3_sha256':ver['source_sha256']['KK_power_module.kicad_pcb'],'candidate_sha256':sha(OUT/'KK_power_module.kicad_pcb'),'reference_p2_sha256':sha(OLD/'KK_power_module.kicad_pcb'),'main_unchanged_sha256':mainhash,'transform':'x = 51 - P3_x, y = 104 - P3_y; rotate 180 degrees; layers unchanged','outline_mm':[50,50,1.6],'corner_radius_mm':3,'holes_mm':{r:xy(f.GetPosition()) for r,f in holes.items()},'electrical_geometry_matches_original_compact_core':True,'tracks_and_vias':len(expected['tracks']),'pads':len(expected['pads']),'removed_oversize_objects':len(removed),'current_root_not_modified':True}
(OUT/'reports/COMPACT_CHANGE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
