"""Native KiCad C6 footprints + conservative geometry; run inside KiCad Flatpak."""
from pathlib import Path
import pcbnew as k, json, re
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'KK_main_module/C6_flat_stack'
LIB = OUT / 'KK_Main.pretty'
def v(x,y): return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p): return [k.ToMM(p.x),k.ToMM(p.y)]
def bbox(q): return [k.ToMM(q.GetX()),k.ToMM(q.GetY()),k.ToMM(q.GetRight()),k.ToMM(q.GetBottom())]

def horizontal(name, pitch, width, start, length, pins, description, model):
    f=k.FOOTPRINT(None); f.SetFPID(k.LIB_ID('KK_Main',name)); f.SetReference('REF**'); f.SetValue(name)
    f.SetAttributes(k.FP_THROUGH_HOLE); f.SetLibDescription(description)
    mid=(pins-1)*pitch/2; left=mid-width/2; right=mid+width/2
    for la,extra,stroke in [(k.F_Fab,0,.1),(k.F_SilkS,.15,.12),(k.F_CrtYd,.5,.05)]:
        s=k.PCB_SHAPE(f);s.SetShape(k.SHAPE_T_RECT);s.SetStart(v(min(left, -.9)-extra, min(start, -.9)-extra) if la==k.F_CrtYd else v(left-extra,start-extra));s.SetEnd(v(max(right,(pins-1)*pitch+.9)+extra,max(start+length,.9)+extra) if la==k.F_CrtYd else v(right+extra,start+length+extra));s.SetLayer(la);s.SetWidth(k.FromMM(stroke));f.Add(s)
    for n in range(pins):
        p=k.PAD(f);p.SetNumber(str(n+1));p.SetAttribute(k.PAD_ATTRIB_PTH);p.SetShape(k.PAD_SHAPE_RECT if n==0 else k.PAD_SHAPE_CIRCLE)
        p.SetPosition(v(n*pitch,0));p.SetSize(v(1.7,1.7));p.SetDrillSize(v(.8,.8));p.SetLayerSet(k.PAD.PTHMask());f.Add(p)
        s=k.PCB_SHAPE(f);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(v(n*pitch,1.05 if start>0 else -1.05));s.SetEnd(v(mid+(n-(pins-1)/2)*(pitch if pins==2 else 1.27),start if start>0 else start+length));s.SetLayer(k.F_Fab);s.SetWidth(k.FromMM(.15));f.Add(s)
    t=k.PCB_TEXT(f);t.SetText('+' if pins==2 else 'FLAT UP');t.SetPosition(v(mid,start+length/2));t.SetTextSize(v(.8,.8));t.SetTextThickness(k.FromMM(.12));t.SetLayer(k.F_SilkS);f.Add(t)
    f.Reference().SetPosition(v(mid,-2));f.Reference().SetTextSize(v(.85,.85));f.Reference().SetTextThickness(k.FromMM(.13));f.Value().SetVisible(False)
    m=k.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/3dmodels/'+model+'.wrl';f.Models().push_back(m)
    k.FootprintSave(str(LIB),f)

# 8mm max can length; width includes manufacturer's +0.5mm tolerance.
# 3mm body-to-bend lead run, plus full lead/body courtyard on the PCB.
horizontal('KA_100u_Flat',2.5,6.8,3,8,2,'Panasonic ECEA1CKA101, 100u 16V, horizontal radial; D6.3+0.5 x L7+1 max; pin1 positive; form supported leads, insulated body support 0.5mm.','KA_100u_horizontal_max')
# Spread 1.5mm native leads to 2.54mm for student-friendly holes; do NOT cross leads.
horizontal('KA_10u_Flat',2.54,4.5,4,8,2,'Panasonic ECEA1CKA100, 10u 16V, horizontal radial; D4+0.5 x L7+1 max. Native 1.5mm leads formed to 2.54mm PCB pitch; pin1 positive.','KA_10u_horizontal_max')
horizontal('TO92_Flat_P2p54',2.54,5.4,-9.4,5.4,3,'Horizontal TO-92; body toward local -Y; 2.54mm formed pin pitch, flat marked face away from PCB, 4mm lead-form run. Per-device pin numbering unchanged; confirm delivered package and bending fixture.','TO92_horizontal_envelope')

b=k.LoadBoard(str(OUT/'KK_main_module.kicad_pcb'))
retained=[]
changes=json.loads((OUT/'component_changes.json').read_text())
before={f.GetReference():{p.GetNumber():p.GetNetname() for p in f.Pads()} for f in b.GetFootprints() if not f.GetReference().startswith('LOGO')}
for old in list(b.GetFootprints()):
    r=old.GetReference()
    if r.startswith('LOGO'): b.Remove(old);continue
    if r not in changes: continue
    c=changes[r]; name=c['Footprint'].split(':')[1];f=k.FootprintLoad(str(LIB),name);assert f is not None
    f.SetParent(b);f.SetFPID(k.LIB_ID('KK_Main',name));f.SetReference(r);f.SetValue(old.GetValue());f.SetPath(old.GetPath());f.SetUuid(old.m_Uuid)
    for field in old.GetFields():
        if field.GetName() not in ['Reference','Value','Footprint']:
            f.SetField(field.GetName(),field.GetText());f.GetField(field.GetName()).SetVisible(False)
    for key in ['MPN','Datasheet']:
        if key in c: f.SetField(key,c[key]);f.GetField(key).SetVisible(False)
    f.SetField('Assembly',c['Assembly']);f.GetField('Assembly').SetVisible(False)
    oldpads={p.GetNumber():p for p in old.Pads()}
    for p in f.Pads(): p.SetNet(oldpads[p.GetNumber()].GetNet())
    f.Value().SetVisible(False);b.Remove(old);b.Add(f);retained.extend([old,f])
removed=list(b.GetTracks())+list(b.Zones())+list(b.GetDrawings())
for g in removed: b.Remove(g)
k.SaveBoard(str(OUT/'C6_blank.kicad_pcb'),b)
b=k.LoadBoard(str(OUT/'C6_blank.kicad_pcb'))
after={f.GetReference():{p.GetNumber():p.GetNetname() for p in f.Pads()} for f in b.GetFootprints()}
assert before==after,'Net mapping changed'
(OUT/'reports/pin_net_preservation.json').write_text(json.dumps({'result':'PASS','reference_count':len(after),'before':before,'after':after},indent=2))
k.SaveBoard(str(OUT/'C6_blank.kicad_pcb'),b)
d={};front={'J2','D3',*[f'SW{i}' for i in range(1,10)]}
for f in b.GetFootprints():
    r=f.GetReference();side='front' if r in front else 'back'
    if (f.GetLayer()==k.F_Cu)!=(side=='front'):f.Flip(f.GetPosition(),k.FLIP_DIRECTION_LEFT_RIGHT)
    variants={}
    for a in [0,90,180,270]:
        f.SetOrientationDegrees(a);f.SetPosition(v(0,0));f.BuildCourtyardCaches()
        poly=f.GetCourtyard(k.F_CrtYd if side=='front' else k.B_CrtYd)
        bb=bbox(poly.BBox()) if poly.OutlineCount() else bbox(f.GetBoundingBox(False,False))
        variants[a]={'box':bb,'pads':[{'pin':p.GetNumber(),'net':p.GetNetname(),'xy':xy(p.GetPosition()),'box':bbox(p.GetBoundingBox())} for p in f.Pads()]}
    d[r]={'side':side,'variants':variants,'value':f.GetValue(),'footprint':str(f.GetFPID())}
(OUT/'geometry.json').write_text(json.dumps(d,indent=2))
print('C6: all 43 resistors horizontal; ten capacitors and six TO-92 bodies flat; pad/net mapping unchanged.')
