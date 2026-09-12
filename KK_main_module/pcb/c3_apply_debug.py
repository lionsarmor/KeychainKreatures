"""Add board-only plated debug points and student assembly silkscreen.
Always starts from the preserved C.2 routed board; never deletes copper.
"""
from pathlib import Path
import pcbnew as k,json,math
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(root/'pcb/backups/pre_c3_debug/KK_main_module.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
plan=[i for i in json.loads((root/'pcb/C3_DEBUG_PLAN.json').read_text()) if i['ref'] not in {'TP7','TP36'}]
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
def box(item):
    a=item.GetBoundingBox();return [k.ToMM(a.GetX()),k.ToMM(a.GetY()),k.ToMM(a.GetRight()),k.ToMM(a.GetBottom())]
def hit(a,z,g=.23):return not(a[2]+g<=z[0] or z[2]+g<=a[0] or a[3]+g<=z[1] or z[3]+g<=a[1])
def pad(key):
    ref,num=key.split(':');return next(p for p in fps[ref].Pads() if p.GetNumber()==num)
for item in plan:
    fp=k.FootprintLoad(str(root/'KK_Main.pretty'),'Debug_PTH_2mm');fp.SetParent(b)
    fp.SetFPID(k.LIB_ID('KK_Main','Debug_PTH_2mm'))
    if item['probe_side']=='back':fp.Flip(v(0,0),False)
    fp.SetReference(item['ref']);fp.SetValue(item['label']);fp.SetPosition(v(*item['xy']))
    fp.SetAttributes(k.FP_THROUGH_HOLE|k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES)
    fp.Reference().SetVisible(False);fp.Value().SetVisible(False)
    p=next(iter(fp.Pads()));p.SetNet(pad(item['source_pin']).GetNet())
    # All test points have explicit taps. No unnecessary thermal spokes/islands.
    p.SetLocalZoneConnection(k.ZONE_CONNECTION_NONE)
    b.Add(fp);fps[item['ref']]=fp
    t=k.PCB_TRACK(b);t.SetStart(v(*item['xy']));t.SetEnd(v(*item['end']))
    t.SetLayer(k.F_Cu if item['layer']==0 else k.B_Cu);t.SetWidth(k.FromMM(item['width']));t.SetNet(p.GetNet());b.Add(t)
for g in b.GetDrawings():
    if hasattr(g,'GetText') and 'C.2' in g.GetText():g.SetText(g.GetText().replace('C.2','C.3'))
b.GetTitleBlock().SetRevision('C.3')
labels=[]
def label(text,x,y,layer,maxdist=5,anchor=None):
    obstacles=[]
    for f in fps.values():
        obstacles.extend(box(p) for p in f.Pads())
        obstacles.extend(box(g) for g in f.GraphicalItems() if g.GetLayer()==layer and (not hasattr(g,'IsVisible') or g.IsVisible()))
        if f.Reference().IsVisible() and f.Reference().GetLayer()==layer:obstacles.append(box(f.Reference()))
    obstacles.extend(box(g) for g in b.GetDrawings() if g.GetLayer()==layer)
    t=k.PCB_TEXT(b);t.SetText(text);t.SetTextSize(v(.9,.9));t.SetTextThickness(k.FromMM(.15));t.SetLayer(layer);t.SetMirrored(layer==k.B_SilkS)
    radius=math.ceil(maxdist/.25)
    choices=sorted([(i*.25,j*.25) for i in range(-radius,radius+1) for j in range(-radius,radius+1) if math.hypot(i*.25,j*.25)<=maxdist],key=lambda p:p[0]**2+p[1]**2)
    for dx,dy in choices:
        t.SetPosition(v(x+dx,y+dy));bb=box(t)
        if bb[0]<1 or bb[1]<1 or bb[2]>79 or bb[3]>99:continue
        if anchor:
            # Polarity sign must be closer to its intended pad than the other
            # lead: never allow a crowded placement to reverse its implication.
            a,z=anchor
            if math.dist([x+dx,y+dy],a)+.3>math.dist([x+dx,y+dy],z):continue
        if not any(hit(bb,o) for o in obstacles):
            b.Add(t);labels.append({'text':text,'side':'back' if layer==k.B_SilkS else 'front','xy':[x+dx,y+dy]});return [x+dx,y+dy]
    raise RuntimeError('No readable label space: '+text)
# Add explicit anode/cathode and capacitor-positive markings next to the
# actual mapped pad. Existing outlines, flats, notches and reference IDs stay.
# Electrolytic footprints already contain a '+' cross at pad 1 and a
# hatched negative half. Preserve those unambiguous local polarity marks.
for ref,mark in [('D1','K'),('D2','K')]:
    print('Marking',ref,flush=True)
    a=xy(pad(ref+':1').GetPosition());z=xy(pad(ref+':2').GetPosition())
    label(mark,*a,k.F_SilkS if ref=='D1' else k.B_SilkS,6,(a,z))
for ref in ['U1','U2','U3','J1','J2','J3','J4','J5']:
    print('Marking',ref,flush=True)
    a=xy(pad(ref+':1').GetPosition());z=xy(pad(ref+':2').GetPosition())
    label('1',*a,k.F_SilkS if fps[ref].GetLayer()==k.F_Cu else k.B_SilkS,4,(a,z))
for ref in ['Q1','Q2','Q3','Q4','Q5','Q6']:
    print('Marking',ref,flush=True)
    a=xy(pad(ref+':1').GetPosition());z=xy(pad(ref+':3').GetPosition())
    label('1',*a,k.B_SilkS,4,(a,z))
for item in plan:
    layer=k.B_SilkS if item['probe_side']=='back' else k.F_SilkS
    try:item['label_xy']=label(item['ref'],*item['xy'],layer,5)
    except RuntimeError:
        other='front' if item['probe_side']=='back' else 'back'
        x,y=item['xy']
        occupied=any(f['side']==other and f['courtyard_mm'][0]-1.15<x<f['courtyard_mm'][2]+1.15 and f['courtyard_mm'][1]-1.15<y<f['courtyard_mm'][3]+1.15 for f in json.loads((root/'pcb/PLACEMENT.json').read_text())['components'])
        if occupied:
            item['label_xy']=label(item['ref'],*item['xy'],layer,8)
            continue
        item['probe_side']=other
        layer=k.B_SilkS if other=='back' else k.F_SilkS
        item['label_xy']=label(item['ref'],*item['xy'],layer,5)
    # The reference is board text so that pad access labels are unaffected by
    # footprint library updates. Full signal mapping is supplied separately.
label('IR TX',8,17,k.F_SilkS,6)
label('IR RX',19,5,k.F_SilkS,5)
label('USB END',66,34,k.F_SilkS,5)
label('J1: 1=5V 2=GND 3=3V3 4=3V2',43,84,k.B_SilkS,10)
label('J4 MOTOR: 1=+ 2=SW',42,88,k.B_SilkS,10)
label('J5 SPK: 1=+ 2=- / NOT GND',42,92,k.B_SilkS,10)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones())
k.SaveBoard(str(root/'routing/KK_main_module_C3_candidate.kicad_pcb'),b)
(root/'pcb/C3_DEBUG_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
(root/'pcb/C3_SILK_LABELS.json').write_text(json.dumps(labels,indent=2)+'\n')
print('Created',len(plan),'plated test points and',len(labels),'silkscreen labels in C.3 candidate.')
