"""Read-only export of authoritative routed copper and assembly obstacles."""
from pathlib import Path
import pcbnew as k, json,sys
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(Path(sys.argv[1]) if len(sys.argv)>1 else root/'KK_main_module.kicad_pcb'))
def xy(p): return [k.ToMM(p.x),k.ToMM(p.y)]
def bounds(item):
    a=item.GetBoundingBox()
    return [k.ToMM(a.GetX()),k.ToMM(a.GetY()),k.ToMM(a.GetRight()),k.ToMM(a.GetBottom())]
d={'pads':[],'tracks':[],'vias':[],'silks':[], 'footprints':[]}
for f in b.GetFootprints():
    boxes=[bounds(g) for g in f.GraphicalItems() if g.GetLayer() in (k.F_CrtYd,k.B_CrtYd)]
    court=[min(z[0] for z in boxes),min(z[1] for z in boxes),max(z[2] for z in boxes),max(z[3] for z in boxes)] if boxes else None
    d['footprints'].append({'ref':f.GetReference(),'side':'front' if f.GetLayer()==k.F_Cu else 'back','xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'courtyard_mm':court})
    for p in f.Pads():
        d['pads'].append({'key':f.GetReference()+':'+p.GetNumber(),'net':p.GetNetname(),'xy':xy(p.GetPosition()),'size':xy(p.GetSize()),'shape':int(p.GetShape()),'angle':p.GetOrientationDegrees(),'radius':k.ToMM(p.GetRoundRectCornerRadius()),'drill':xy(p.GetDrillSize())})
    for g in [*f.GraphicalItems(), f.Reference(),f.Value()]:
        if g.GetLayer() in (k.F_SilkS,k.B_SilkS) and (not hasattr(g,'IsVisible') or g.IsVisible()):
            d['silks'].append({'side':'front' if g.GetLayer()==k.F_SilkS else 'back','box':bounds(g),'text':g.GetText() if hasattr(g,'GetText') else ''})
for g in b.GetDrawings():
    if g.GetLayer() in (k.F_SilkS,k.B_SilkS):d['silks'].append({'side':'front' if g.GetLayer()==k.F_SilkS else 'back','box':bounds(g),'text':g.GetText() if hasattr(g,'GetText') else ''})
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA':d['vias'].append({'net':t.GetNetname(),'xy':xy(t.GetPosition()),'diameter':k.ToMM(t.GetWidth(k.F_Cu)),'drill':k.ToMM(t.GetDrillValue())})
    else:d['tracks'].append({'uuid':str(t.m_Uuid.AsString()),'net':t.GetNetname(),'a':xy(t.GetStart()),'b':xy(t.GetEnd()),'width':k.ToMM(t.GetWidth()),'layer':0 if t.GetLayer()==k.F_Cu else 1})
(root/'routing/c3_geometry.json').write_text(json.dumps(d))
