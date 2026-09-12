"""Finish routed candidate: explicit ground returns and connector identification."""
from pathlib import Path
import pcbnew as k,json
root=Path(__file__).resolve().parent.parent
file=root/'routing/KK_main_module_C2_candidate.kicad_pcb';b=k.LoadBoard(str(file))
fps={f.GetReference():f for f in b.GetFootprints()}
# These pads have explicit copper ground tracks. Isolated thermal islands
# provide no useful plane return; use the routed return instead.
for ref,num in [('SW1','D'),('U3','4')]:
    p=next(p for p in fps[ref].Pads() if p.GetNumber()==num)
    assert p.GetNetname()=='/GND'
    p.SetLocalZoneConnection(k.ZONE_CONNECTION_NONE)
# Redundant vias are removed by the separate file-based pass before loading.
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def box(item):
    bb=item.GetBoundingBox();return[k.ToMM(bb.GetX()),k.ToMM(bb.GetY()),k.ToMM(bb.GetRight()),k.ToMM(bb.GetBottom())]
def hit(a,z,g=.23):return not(a[2]+g<=z[0] or z[2]+g<=a[0] or a[3]+g<=z[1] or z[3]+g<=a[1])
for g in b.GetDrawings():
    if hasattr(g,'GetText') and 'KK MAIN C.1' in g.GetText():g.SetText('KK MAIN C.2 - ENGINEERING PROTOTYPE')
def label(text,x,y,layer):
    if any(hasattr(t,'GetText') and t.GetText()==text for t in b.GetDrawings()):return
    obstacles=[]
    for f in fps.values():
        obstacles.extend(box(p) for p in f.Pads())
        obstacles.extend(box(g) for g in f.GraphicalItems() if g.GetLayer()==layer)
        if f.Reference().IsVisible() and f.Reference().GetLayer()==layer:obstacles.append(box(f.Reference()))
    obstacles.extend(box(g) for g in b.GetDrawings() if g.GetLayer()==layer)
    t=k.PCB_TEXT(b);t.SetText(text);t.SetTextSize(v(1,1));t.SetTextThickness(k.FromMM(.15));t.SetLayer(layer);t.SetMirrored(layer==k.B_SilkS)
    for dx,dy in sorted([(i*.5,j*.5) for i in range(-16,17) for j in range(-16,17)],key=lambda p:p[0]**2+p[1]**2):
        t.SetPosition(v(x+dx,y+dy));bb=box(t)
        if bb[0]<1 or bb[1]<1 or bb[2]>79 or bb[3]>99:continue
        if not any(hit(bb,o) for o in obstacles):b.Add(t);return
    raise RuntimeError('No clear label location: '+text)
label('MOTOR',71,33,k.B_SilkS)
label('SPK',24,47,k.B_SilkS)
label('SYS_IN',68,47,k.B_SilkS)
label('KK MAIN C.2 / PROTOTYPE',40,86,k.F_SilkS)
b.BuildConnectivity();k.SaveBoard(str(file),b)
# Reload after removing vias: avoids stale connectivity objects in KiCad 10 SWIG.
b=k.LoadBoard(str(file));b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(file),b)
print('Ground tracks retained; isolated thermal contacts removed; connector labels added.')
