"""Check schematic pad parity and arrange readable assembly references.
Run with KiCad's Python. This never routes the board or creates fabrication files.
"""
from pathlib import Path
import json, xml.etree.ElementTree as ET
import pcbnew as k

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'pcb'
board=k.LoadBoard(str(ROOT/'KK_main_module.kicad_pcb'))
xml=ET.parse(WORK/'board_netlist.xml').getroot()
rows=json.loads((WORK/'footprint_assignments.json').read_text())
expected={(n.attrib['ref'],n.attrib['pin']):net.attrib['name']
          for net in xml.findall('./nets/net') for n in net.findall('node')}
fps={f.GetReference():f for f in board.GetFootprints()}
errors=[]; count=0
for row in rows:
    f=fps.get(row['ref'])
    if f is None: errors.append('Missing '+row['ref']);continue
    fid=f.GetFPID()
    if str(fid.GetLibNickname())+':'+str(fid.GetLibItemName())!=row['footprint']:errors.append('Footprint mismatch '+row['ref'])
    if f.GetPath().AsString()!=row['path']:errors.append('Schematic UUID mismatch '+row['ref'])
    pads={p.GetNumber():p for p in f.Pads()}
    wanted={pin for ref,pin in expected if ref==row['ref']}
    if set(pads)!=wanted:errors.append('Pad number set mismatch '+row['ref'])
    for num,p in pads.items():
        count+=1
        if p.GetAttribute()!=k.PAD_ATTRIB_PTH:errors.append('Non-THT component pad '+row['ref']+':'+num)
        if p.GetNetname()!=expected.get((row['ref'],num)):errors.append('Net mismatch '+row['ref']+':'+num)
        if min(p.GetDrillSize().x,p.GetDrillSize().y)<=0:errors.append('Missing drill '+row['ref']+':'+num)

def mm(n):return k.ToMM(n)
def vec(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def box(item):
    b=item.GetBoundingBox()
    return [mm(b.GetX()),mm(b.GetY()),mm(b.GetRight()),mm(b.GetBottom())]
def hit(a,b,gap=.2):return not(a[2]+gap<=b[0] or b[2]+gap<=a[0] or a[3]+gap<=b[1] or b[3]+gap<=a[1])

obstacles={k.F_SilkS:[],k.B_SilkS:[]}
movable=[]
for f in fps.values():
    for p in f.Pads():
        for layer in obstacles:obstacles[layer].append(box(p))
    for g in f.GraphicalItems():
        if g.GetLayer() in obstacles:
            if hasattr(g,'GetText'):movable.append(g)
            else:obstacles[g.GetLayer()].append(box(g))
for g in board.GetDrawings():
    if g.GetLayer() in obstacles:obstacles[g.GetLayer()].append(box(g))

label_failures=[]
for t in movable:
    x,y=mm(t.GetPosition().x),mm(t.GetPosition().y)
    for dx,dy in sorted([(i*.5,j*.5) for i in range(-12,13) for j in range(-12,13)],key=lambda v:v[0]**2+v[1]**2):
        t.SetPosition(vec(x+dx,y+dy));b=box(t)
        if b[0]<.5 or b[1]<.5 or b[2]>79.5 or b[3]>99.5:continue
        if any(hit(b,o,.23) for o in obstacles[t.GetLayer()]):continue
        obstacles[t.GetLayer()].append(b);break
    else:label_failures.append('footprint text '+t.GetText())
for row in sorted(rows,key=lambda r:(-len(r['ref']),r['ref'])):
    f=fps[row['ref']];t=f.Reference();layer=k.B_SilkS if f.GetLayer()==k.B_Cu else k.F_SilkS
    t.SetVisible(True);t.SetLayer(layer);t.SetTextSize(vec(1,1));t.SetTextThickness(k.FromMM(.15))
    t.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T));t.SetMirrored(layer==k.B_SilkS)
    points=[box(p) for p in f.Pads()]
    x=(min(p[0] for p in points)+max(p[2] for p in points))/2
    y=(min(p[1] for p in points)+max(p[3] for p in points))/2
    offsets=sorted([(i*.5,j*.5) for i in range(-36,37) for j in range(-36,37)],key=lambda v:v[0]**2+v[1]**2)
    found=False
    for dx,dy in offsets:
        t.SetPosition(vec(x+dx,y+dy));b=box(t)
        if b[0]<.5 or b[1]<.5 or b[2]>79.5 or b[3]>99.5:continue
        if any(hit(b,o,.23) for o in obstacles[layer]):continue
        obstacles[layer].append(b);found=True;break
    if not found:label_failures.append(row['ref'])

report={'status':'UNROUTED PLACEMENT PROTOTYPE - NOT FOR FABRICATION',
        'schematic_components':len(rows),'component_pads':count,
        'schematic_pad_net_mismatches':errors,'unplaced_reference_labels':label_failures,
        'tracks':len(list(board.GetTracks())),
        'holds':['Dry-fit actual SuperMini/socket against the user-supplied footprint; stack height unverified',
                 'Display and SD header offset, card extraction and stack height need a physical fit check',
                 'Placement is a packing study; routed power/SPI/audio performance not validated']}
(WORK/'PLACEMENT_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
if errors or label_failures:raise RuntimeError(json.dumps(report))
k.SaveBoard(str(ROOT/'KK_main_module.kicad_pcb'),board)
print(json.dumps(report,indent=2))
