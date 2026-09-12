"""Read-only geometry export, retaining actual layers and pad shapes."""
from pathlib import Path
import json,pcbnew as k
out=Path(__file__).resolve().parent/'P2_compact';b=k.LoadBoard(str(out/'KK_power_module.kicad_pcb'))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
data={'pads':[],'tracks':[],'vias':[]}
layers=list(b.GetEnabledLayers().CuStack())
for f in b.GetFootprints():
    for p in f.Pads():
        data['pads'].append(dict(key=f.GetReference()+':'+p.GetNumber(),net=p.GetNetname(),xy=xy(p.GetPosition()),size=xy(p.GetSize()),shape=int(p.GetShape()),angle=p.GetOrientationDegrees(),radius=k.ToMM(p.GetRoundRectCornerRadius()),drill=xy(p.GetDrillSize()),layers=[b.GetLayerName(l) for l in layers if p.IsOnLayer(l)]))
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA':data['vias'].append(dict(net=t.GetNetname(),xy=xy(t.GetPosition()),diameter=k.ToMM(t.GetWidth(k.F_Cu)),drill=k.ToMM(t.GetDrillValue()),layers=[b.GetLayerName(l) for l in layers]))
    else:data['tracks'].append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),a=xy(t.GetStart()),b=xy(t.GetEnd()),width=k.ToMM(t.GetWidth()),layer=b.GetLayerName(t.GetLayer()),locked=t.IsLocked()))
(out/'geometry.json').write_text(json.dumps(data,indent=2)+'\n')
print(len(data['tracks']),'tracks;',len(data['vias']),'vias')
