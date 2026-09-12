"""C.2 electrical placement pass. Refuses to overwrite routed work.
Run inside KiCad Flatpak. Source board and C.1 backup retain all UUIDs.
"""
from pathlib import Path
import json, math, xml.etree.ElementTree as ET
import pcbnew as k
ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'pcb'
board=k.LoadBoard(str(ROOT/'KK_main_module.kicad_pcb'))
assert not list(board.GetTracks()), 'Do not rerun placement on a routed board'
fps={f.GetReference():f for f in board.GetFootprints()}
rows={r['ref']:r for r in json.loads((WORK/'footprint_assignments.json').read_text())}
xml=ET.parse(WORK/'board_netlist.xml').getroot()
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return (k.ToMM(p.x),k.ToMM(p.y))
def bbox(f):
    boxes=[g.GetBoundingBox() for g in f.GraphicalItems() if g.GetLayer() in (k.F_CrtYd,k.B_CrtYd)]
    return [k.ToMM(min(b.GetX() for b in boxes)),k.ToMM(min(b.GetY() for b in boxes)),k.ToMM(max(b.GetRight() for b in boxes)),k.ToMM(max(b.GetBottom() for b in boxes))]
def center(f,x,y,a):
    f.SetOrientationDegrees(a);b=bbox(f);px,py=xy(f.GetPosition())
    f.SetPosition(v(px+x-(b[0]+b[2])/2,py+y-(b[1]+b[3])/2))
def hit(a,b,g=.15):return not(a[2]+g<=b[0] or b[2]+g<=a[0] or a[3]+g<=b[1] or b[3]+g<=a[1])
existing={n.GetNetname():n for n in board.GetNetInfo().NetsByNetcode().values()}
for el in xml.findall('./nets/net'):
    name=el.attrib['name']
    if name not in existing:existing[name]=k.NETINFO_ITEM(board,name);board.Add(existing[name])
    for node in el.findall('node'):
        fp=fps[node.attrib['ref']]
        next(p for p in fp.Pads() if p.GetNumber()==node.attrib['pin']).SetNet(existing[name])
for ref,r in rows.items():
    fp=fps[ref];fp.SetValue(r['value']);fp.SetField('MPN',r['mpn']);fp.GetField('MPN').SetVisible(False)
    comp=xml.find('./components/comp[@ref="'+ref+'"]')
    fp.SetField('Datasheet',comp.findtext('datasheet',''));fp.GetField('Datasheet').SetVisible(False)
    for field in comp.findall('./fields/field'):
        if field.attrib['name'] not in ('Footprint','Value','Reference'):
            fp.SetField(field.attrib['name'],field.text or '');fp.GetField(field.attrib['name']).SetVisible(False)

# High-priority pad-to-pad placement objectives, measured again after placement.
pairs=[('C26:1','U3:2'),('C26:2','U3:4'),('C25:1','U3:2'),
 ('C21:1','U3:8'),('C21:2','U3:5'),('C22:1','U3:5'),
 ('C23:1','U3:1'),('C24:1','U3:3'),('R34:1','C23:2'),('R35:1','C24:2'),
 ('R33:1','U3:7'),('R32:2','U3:7'),('J5:1','U3:1'),('J5:2','U3:3'),
 ('C16:1','J4:1'),('C16:2','J4:2'),('D2:1','J4:1'),('D2:2','J4:2'),
 ('Q4:3','J4:2'),('C17:1','J4:1'),('C15:1','U2:3'),('C14:1','U2:3'),
 ('C8:1','U1:9'),('C9:1','U1:9'),('C10:1','J3:1'),('C11:1','J3:1'),
 ('C12:1','J2:2'),('C13:1','J2:2'),('C1:1','J1:1'),('C3:1','J1:3'),('C5:1','J1:4')]
def padpos(key):
    r,n=key.split(':');return xy(next(p for p in fps[r].Pads() if p.GetNumber()==n).GetPosition())
before={a+' -> '+b:round(math.dist(padpos(a),padpos(b)),3) for a,b in pairs}
occupied=[('RF',[51,0,80,7])];placed=set()
def accept(ref):
    f=fps[ref];occupied.append((ref,bbox(f)));placed.add(ref)
    f.Value().SetVisible(False)
for ref,f in fps.items():
    if ref.startswith('H'):
        x,y=xy(f.GetPosition());occupied.append((ref,[x-2.7,y-2.7,x+2.7,y+2.7]));continue
    if f.GetLayer()==k.F_Cu:accept(ref)
anchors={'U1':(14,35,0),'U3':(39,44,0),'J1':(68,52,0),'J4':(72,38,90)}
for ref,(x,y,a) in anchors.items():
    center(fps[ref],x,y,a)
    assert not any(hit(bbox(fps[ref]),b) for _,b in occupied),ref
    accept(ref)
def target(ref):
    if ref=='J5':return(40,60)
    if ref in ('D2','Q4','R28','R29','C16','C17'):return(68,40)
    if ref in ('Q1','R24','R25','R26','R27','C14','C15'):return(22,12)
    if ref in ('Q5','Q6') or ref.startswith('R') and int(ref[1:])>=30 or ref.startswith('C') and int(ref[1:])>=18:return(40,44)
    if ref.startswith('C') and int(ref[1:])<=6:return(64,54)
    if ref in ('C7','C8','C9'):return(23,32)
    if ref in ('C10','C11'):return(8,30)
    if ref in ('C12','C13'):return(32,15)
    if ref in ('Q2','Q3') or ref.startswith('R') and 14<=int(ref[1:])<=23:return(37,20)
    return(25,61)
order=['C11','C10','C26','C21','C22','C25','C23','C24','R34','R35','R33','R32','C20','C19','R31','C18','R30','J5',
       'C16','D2','Q4','C17','C14','C15','R27','C8','C9','C12','C13',
       'C1','C2','C3','C4','C5','C6','Q6','Q5','R38','R39','R36','R37','R28','R29']
order+=sorted(set(rows)-placed-set(order),key=lambda r:(not r.startswith('Q'),r))
for ref in order:
    f=fps[ref];tx,ty=target(ref);best=None
    endpoints={};special={}
    for a,b in pairs:
        if a.split(':')[0]==ref and b.split(':')[0] in placed:special.setdefault(a.split(':')[1],[]).append(padpos(b))
        if b.split(':')[0]==ref and a.split(':')[0] in placed:special.setdefault(b.split(':')[1],[]).append(padpos(a))
    for p in f.Pads():
        name=p.GetNetname()
        if name in ('/GND','/LOGIC_3V3','/ACT_3V2','/MCU_5V') or name.startswith('unconnected'):continue
        endpoints[p.GetNumber()]=[xy(pp.GetPosition()) for rr in placed for pp in fps[rr].Pads() if pp.GetNetname()==name]
    for angle in (0,90,180,270):
        center(f,0,0,angle);bb=bbox(f);pp={p.GetNumber():xy(p.GetPosition()) for p in f.Pads()}
        for ix in range(3,158):
            x=ix*.5
            for iy in range(3,198):
                y=iy*.5;b=[bb[0]+x,bb[1]+y,bb[2]+x,bb[3]+y]
                if b[0]<1 or b[1]<1 or b[2]>79 or b[3]>99 or any(hit(b,o) for _,o in occupied):continue
                score=.2*((x-tx)**2+(y-ty)**2)
                for pin,ends in special.items():
                    px,py=pp[pin];score+=sum(12*((x+px-ex)**2+(y+py-ey)**2) for ex,ey in ends)
                for pin,ends in endpoints.items():
                    if ends:
                        px,py=pp[pin];score+=min((x+px-ex)**2+(y+py-ey)**2 for ex,ey in ends)
                if best is None or score<best[0]:best=(score,x,y,angle)
    assert best is not None, 'No placement for '+ref
    _,x,y,a=best;center(f,x,y,a);accept(ref)
    print(ref,x,y,a,flush=True)
board.BuildConnectivity()
for z in board.Zones():
    if not z.GetIsRuleArea():z.UnFill()
k.SaveBoard(str(ROOT/'KK_main_module.kicad_pcb'),board)
positions=[{'reference':r,'side':'front' if fps[r].GetLayer()==k.F_Cu else 'back','courtyard_mm':bbox(fps[r]),'angle':fps[r].GetOrientationDegrees()} for r in rows]
(WORK/'PLACEMENT.json').write_text(json.dumps({'status':'C.2 electrical placement, unrouted','components':positions},indent=2)+'\n')
(WORK/'C2_PLACEMENT_DISTANCES.json').write_text(json.dumps([{'connection':a+' -> '+b,'before_mm':before[a+' -> '+b],'after_mm':round(math.dist(padpos(a),padpos(b)),3)} for a,b in pairs],indent=2)+'\n')
print('C.2 placement complete; routing and DRC required.')
