"""One-shot silkscreen-only candidate; preserve the issued P.2 board.
Run with KiCad Python, nice/taskset on one CPU. No routing or circuit changes.
"""
from pathlib import Path
import json,hashlib,shutil,sys
import pcbnew as k
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'KK_power_module/P2_compact';OUT=ROOT/'KK_power_module/work/P2_logo_review'
verify_only='--verify-only' in sys.argv or '--artwork-metadata' in sys.argv
if not verify_only:assert not OUT.exists(),'Candidate already exists; do not overwrite'
verified=json.loads((SRC/'review/VERIFICATION.json').read_text())
assert hashlib.sha256((SRC/'KK_power_module.kicad_pcb').read_bytes()).hexdigest()==verified['PCB_SHA256']
if not verify_only:shutil.copytree(SRC,OUT)
sm=k.SETTINGS_MANAGER();project=str(OUT/'KK_power_module.kicad_pro');assert sm.LoadProject(project)
b=k.LoadBoard(str(OUT/'KK_power_module.kicad_pcb'));b.SetProject(sm.GetProject(project))
def xy(p):return [p.x,p.y]
def signature(board):
    pads=sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),xy(p.GetPosition()),xy(p.GetSize()),xy(p.GetDrillSize()),p.GetOrientationDegrees(),p.GetLayerSet().FmtHex()) for f in board.GetFootprints() for p in f.Pads())
    tracks=sorted((t.GetClass(),t.GetNetname(),xy(t.GetStart()),xy(t.GetEnd()),int(t.GetLayer()),t.GetWidth(k.F_Cu) if t.GetClass()=='PCB_VIA' else t.GetWidth(),t.GetDrillValue() if t.GetClass()=='PCB_VIA' else 0) for t in board.GetTracks())
    zones=[]
    for z in board.Zones():
        layers=[]
        for la in board.GetEnabledLayers().CuStack():
            if not z.IsOnLayer(la):continue
            polys=z.GetFilledPolysList(la)
            layers.append([int(la),[[xy(polys.COutline(i).CPoint(j)) for j in range(polys.COutline(i).PointCount())] for i in range(polys.OutlineCount())],[[[xy(polys.CHole(i,h).CPoint(j)) for j in range(polys.CHole(i,h).PointCount())] for h in range(polys.HoleCount(i))] for i in range(polys.OutlineCount())]])
        zones.append([z.GetNetname(),layers])
    return hashlib.sha256(json.dumps([pads,tracks,zones],sort_keys=True).encode()).hexdigest()
before=signature(k.LoadBoard(str(SRC/'KK_power_module.kicad_pcb')))
for ref,name,point in ([] if verify_only else [('LOGO1','KiCad-Logo_6mm_SilkScreen',(17,15)),('LOGO2','OSHW-Logo_5.7x6mm_SilkScreen',(32,15))]):
    library=Path('/app/extensions/Library/footprints/Symbol.pretty')
    shutil.copy2(library/(name+'.kicad_mod'),OUT/'KK_Power.pretty'/(name+'.kicad_mod'))
    f=k.FootprintLoad(str(OUT/'KK_Power.pretty'),name);assert f is not None
    f.SetParent(b);f.SetReference(ref);f.SetFPID(k.LIB_ID('KK_Power',name))
    f.SetAttributes(k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES)
    f.Reference().SetVisible(False);f.Value().SetVisible(False)
    f.Flip(f.GetPosition(),k.FLIP_DIRECTION_LEFT_RIGHT)
    f.SetPosition(k.VECTOR2I(k.FromMM(point[0]),k.FromMM(point[1])));b.Add(f)
assert signature(b)==before,'Electrical copper changed while adding logos'
if '--artwork-metadata' in sys.argv:
    for f in b.GetFootprints():
        if f.GetReference().startswith('LOGO'):f.SetAllowMissingCourtyard(True)
if not verify_only or '--artwork-metadata' in sys.argv:k.SaveBoard(str(OUT/'KK_power_module.kicad_pcb'),b)
saved=k.LoadBoard(str(OUT/'KK_power_module.kicad_pcb'))
assert signature(saved)==before,'Electrical copper changed on save'
report={'scope':'Silkscreen-only logo addition','source_pcb_sha256':verified['PCB_SHA256'],'candidate_pcb_sha256':hashlib.sha256((OUT/'KK_power_module.kicad_pcb').read_bytes()).hexdigest(),'copper_signature_before':before,'copper_signature_after':signature(saved),'copper_unchanged':True,'test_pads':28,'logos':[{'ref':f.GetReference(),'name':str(f.GetFPID().GetLibItemName()),'layer':saved.GetLayerName(f.GetLayer()),'xy_mm':[k.ToMM(f.GetPosition().x),k.ToMM(f.GetPosition().y)]} for f in saved.GetFootprints() if f.GetReference().startswith('LOGO')],'note':'Standard KiCad/OSHW library artwork; no certification claim. Native DRC required.'}
(OUT/'LOGO_CHANGE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
