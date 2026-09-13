"""Clear local labels around changed top-entry sockets; no net changes."""
from pathlib import Path
import pcbnew as k,math
root=Path(__file__).resolve().parent.parent
file=root/'routing/KK_main_module_C3_debug_connectors.kicad_pcb'
b=k.LoadBoard(str(file));fps={f.GetReference():f for f in b.GetFootprints()}
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
def box(g):
    a=g.GetBoundingBox();return [k.ToMM(a.GetX()),k.ToMM(a.GetY()),k.ToMM(a.GetRight()),k.ToMM(a.GetBottom())]
def hit(a,z):return not(a[2]+.23<=z[0] or z[2]+.23<=a[0] or a[3]+.23<=z[1] or z[3]+.23<=a[1])
def move(t,anchor,other=None):
    layer=t.GetLayer();t.SetLayer(k.Dwgs_User)
    obs=[]
    for f in fps.values():
        obs.extend(box(p) for p in f.Pads())
        obs.extend(box(g) for g in f.GraphicalItems() if g.GetLayer()==layer and (not hasattr(g,'IsVisible') or g.IsVisible()))
        if f.Reference().GetLayer()==layer and f.Reference().IsVisible():obs.append(box(f.Reference()))
    obs.extend(box(g) for g in b.GetDrawings() if g.GetLayer()==layer)
    t.SetLayer(layer);t.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T));t.SetTextSize(v(.9,.9));t.SetTextThickness(k.FromMM(.15));t.SetMirrored(layer==k.B_SilkS)
    for dx,dy in sorted([(i*.25,j*.25) for i in range(-24,25) for j in range(-24,25)],key=lambda p:p[0]**2+p[1]**2):
        pt=[anchor[0]+dx,anchor[1]+dy]
        if other and math.dist(pt,anchor)+.3>math.dist(pt,other):continue
        t.SetPosition(v(*pt));bb=box(t)
        if bb[0]<1 or bb[1]<1 or bb[2]>79 or bb[3]>99:continue
        if not any(hit(bb,z) for z in obs):return
    raise RuntimeError('No label room '+t.GetText())
for ref in ['J4','J5']:
    f=fps[ref];ps={p.GetNumber():p for p in f.Pads()};a=xy(ps['1'].GetPosition());z=xy(ps['2'].GetPosition())
    mark=min([g for g in b.GetDrawings() if hasattr(g,'GetText') and g.GetText()=='1' and g.GetLayer()==k.B_SilkS],key=lambda g:math.dist(xy(g.GetPosition()),a))
    move(f.Reference(),xy(f.GetPosition()))
    move(mark,a,z)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(file),b)
