"""Fail closed if debug additions change any original component or route."""
from pathlib import Path
import pcbnew as k,json,hashlib
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(root/'KK_main_module.kicad_pcb'))
old=k.LoadBoard(str(root/'pcb/backups/pre_c3_debug/KK_main_module.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
def pos(p):return(p.x,p.y)
def pads(f):return sorted((p.GetNumber(),p.GetNetname(),pos(p.GetPosition()),pos(p.GetSize()),pos(p.GetDrillSize()),int(p.GetAttribute())) for p in f.Pads())
for f in old.GetFootprints():
    n=fps[f.GetReference()]
    if f.GetReference()=='J5':
        for a,z in zip(pads(f),pads(n)):
            assert a[:2]==z[:2] and a[3:]==z[3:]
            assert z[2]==(a[2][0]-k.FromMM(.25),a[2][1])
    else:assert pads(n)==pads(f),f.GetReference()+' pad changed'
    assert n.GetValue()==f.GetValue() and n.GetPath().AsString()==f.GetPath().AsString()
    assert n.GetOrientationDegrees()==f.GetOrientationDegrees()
    if f.GetReference()!='J5':assert pos(n.GetPosition())==pos(f.GetPosition())
def track(t):
    if t.GetClass()=='PCB_VIA':return ('via',t.GetNetname(),pos(t.GetPosition()),t.GetWidth(k.F_Cu),t.GetDrillValue())
    return('track',t.GetNetname(),pos(t.GetStart()),pos(t.GetEnd()),t.GetWidth(),t.GetLayer())
from collections import Counter
assert not (Counter(track(t) for t in old.GetTracks())-Counter(track(t) for t in b.GetTracks())), 'Existing copper removed/changed'
plan=json.loads((root/'pcb/C3_DEBUG_PLAN.json').read_text())
for i in plan:
    f=fps[i['ref']];p=next(iter(f.Pads()))
    assert f.GetAttributes()&k.FP_BOARD_ONLY and f.GetAttributes()&k.FP_EXCLUDE_FROM_BOM
    assert f.GetFPID().GetLibItemName()=='Debug_PTH_2mm'
    assert p.GetNetname()==i['net'] and p.GetAttribute()==k.PAD_ATTRIB_PTH
    assert p.GetSize().x==k.FromMM(2) and p.GetDrillSize().x==k.FromMM(.8)
assert len(fps)==len(list(old.GetFootprints()))+len(plan)
assert all(f.Reference().IsVisible() for f in old.GetFootprints() if not f.GetReference().startswith('H'))
report={'revision':'C.3 DEBUG/CONNECTOR CHECKPOINT; RGB PENDING SIZE APPROVAL','original_routes_unchanged':True,'component_changes':'J4/J5 top-entry B2B-PH; J5 shifted 0.25mm left; all other original component positions unchanged','added_test_points':len(plan),'added_tap_tracks':len(list(b.GetTracks()))-len(list(old.GetTracks())),'track_segments':sum(t.GetClass()!='PCB_VIA' for t in b.GetTracks()),'vias':sum(t.GetClass()=='PCB_VIA' for t in b.GetTracks()),'plated_holes':sum(p.GetAttribute()==k.PAD_ATTRIB_PTH for f in b.GetFootprints() for p in f.Pads())+sum(t.GetClass()=='PCB_VIA' for t in b.GetTracks()),'npth_holes':sum(p.GetAttribute()==k.PAD_ATTRIB_NPTH for f in b.GetFootprints() for p in f.Pads()),'longest_added_stub_mm':max(i['stub_mm'] for i in plan),'board_sha256':hashlib.sha256((root/'KK_main_module.kicad_pcb').read_bytes()).hexdigest()}
(root/'pcb/C3_FINAL_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
