"""Place C6 labels against actual pad and silkscreen graphics, not courtyard proxies."""
from pathlib import Path
import pcbnew as k,json,math
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_main_module/C6_flat_stack'
b=k.LoadBoard(str(OUT/'KK_main_module.kicad_pcb'));labels=json.loads((OUT/'reports/silkscreen_labels.json').read_text())
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def bb(g):
    q=g.GetBoundingBox();return [k.ToMM(q.GetX()),k.ToMM(q.GetY()),k.ToMM(q.GetRight()),k.ToMM(q.GetBottom())]
def hit(a,z,g=.21):return not(a[2]+g<=z[0] or z[2]+g<=a[0] or a[3]+g<=z[1] or z[3]+g<=a[1])
removed=[g for g in b.GetDrawings() if g.GetLayer() in (k.F_SilkS,k.B_SilkS) and isinstance(g,k.PCB_TEXT)]
for g in removed:b.Remove(g)
obs={k.F_SilkS:[],k.B_SilkS:[]}
for f in b.GetFootprints():
    for p in f.Pads():
        for la in obs:obs[la].append(bb(p))
    for g in f.GraphicalItems():
        if g.GetLayer() not in obs:continue
        if hasattr(g,'IsVisible') and not g.IsVisible():continue
        q=bb(g)
        if isinstance(g,k.PCB_SHAPE) and g.GetShape()==k.SHAPE_T_RECT:
            x1,y1,x2,y2=q;t=.17
            obs[g.GetLayer()].extend([[x1,y1,x2,y1+t],[x1,y2-t,x2,y2],[x1,y1,x1+t,y2],[x2-t,y1,x2,y2]])
        else:obs[g.GetLayer()].append(q)
for g in b.GetDrawings():
    if g.GetLayer() in obs:obs[g.GetLayer()].append(bb(g))
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA':
        for la in obs:obs[la].append(bb(t))
retained=[];result=[]
offsets=sorted([(i*.25,j*.25) for i in range(-48,49) for j in range(-48,49)],key=lambda p:p[0]**2+p[1]**2)
for d in labels:
    t=d['label'];la=k.F_SilkS if d['side'].startswith('F.') else k.B_SilkS;anchor=d['anchor'];size=1 if t=='KEYCHAIN KREATURES' else .85 if len(t)>4 else .8
    s=k.PCB_TEXT(b);s.SetText(t);s.SetTextSize(v(size,size));s.SetTextThickness(k.FromMM(.13));s.SetLayer(la);s.SetMirrored(la==k.B_SilkS)
    for dx,dy in offsets:
        s.SetPosition(v(anchor[0]+dx,anchor[1]+dy));q=bb(s)
        if q[0]<1 or q[1]<1 or q[2]>95 or q[3]>104:continue
        if not any(hit(q,z) for z in obs[la]):break
    else:raise RuntimeError('No clear label position '+t)
    obs[la].append(q);b.Add(s);retained.append(s);result.append({**d,'xy':[k.ToMM(s.GetPosition().x),k.ToMM(s.GetPosition().y)],'offset_mm':math.hypot(dx,dy)})
k.SaveBoard(str(OUT/'KK_main_module.kicad_pcb'),b)
(OUT/'reports/silkscreen_labels_final.json').write_text(json.dumps(result,indent=2)+'\n')
print('Placed',len(result),'labels against actual artwork; maximum label shift',round(max(p['offset_mm'] for p in result),2),'mm; native DRC still required.')
