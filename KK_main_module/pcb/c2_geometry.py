"""Export copper geometry for local constrained repair; no board changes."""
from pathlib import Path
import pcbnew as k,json
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(root/'routing/KK_main_module_C2_candidate.kicad_pcb'))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
d={'pads':[],'tracks':[],'vias':[]}
for f in b.GetFootprints():
    for p in f.Pads():
        d['pads'].append({'key':f.GetReference()+':'+p.GetNumber(),'net':p.GetNetname(),'xy':xy(p.GetPosition()),'size':xy(p.GetSize()),'shape':int(p.GetShape()),'angle':p.GetOrientationDegrees(),'radius':k.ToMM(p.GetRoundRectCornerRadius()),'drill':xy(p.GetDrillSize())})
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA':d['vias'].append({'net':t.GetNetname(),'xy':xy(t.GetPosition()),'diameter':k.ToMM(t.GetWidth(k.F_Cu)),'drill':k.ToMM(t.GetDrillValue())})
    else:d['tracks'].append({'net':t.GetNetname(),'a':xy(t.GetStart()),'b':xy(t.GetEnd()),'width':k.ToMM(t.GetWidth()),'layer':0 if t.GetLayer()==k.F_Cu else 1})
(root/'routing/c2_geometry.json').write_text(json.dumps(d))
