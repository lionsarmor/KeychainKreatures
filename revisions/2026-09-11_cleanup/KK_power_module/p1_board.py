"""Native KiCad P.1 placement study; never a fabrication/release generator.

Run inside KiCad Flatpak after native netlist export. No root/main files touched.
Refuses to overwrite a board containing tracks so later manual work is retained.
"""
from pathlib import Path
import json,math,xml.etree.ElementTree as ET
import pcbnew as k
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'P1_revision';PATH=OUT/'KK_power_module.kicad_pcb'
if PATH.exists() and list(k.LoadBoard(str(PATH)).GetTracks()):
    raise SystemExit('Refusing to replace a routed P.1 board. Preserve manual work.')
d=json.loads((OUT/'design.json').read_text());xml=ET.parse(OUT/'netlist.xml').getroot()
sm=k.SETTINGS_MANAGER();pro=str(OUT/'KK_power_module.kicad_pro');assert sm.LoadProject(pro)
b=k.BOARD();b.SetProject(sm.GetProject(pro));b.SetCopperLayerCount(4);b.GetDesignSettings().SetBoardThickness(k.FromMM(1.6))
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def mm(x):return k.ToMM(x)
nets={};np={}
for el in xml.findall('./nets/net'):
    name=el.attrib['name'];net=k.NETINFO_ITEM(b,name);b.Add(net);nets[name]=net
    for n in el.findall('node'):np[n.attrib['ref'],n.attrib['pin']]=net
def line(a,c,layer=k.Edge_Cuts,width=.05):
    s=k.PCB_SHAPE(b);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*c));s.SetLayer(layer);s.SetWidth(k.FromMM(width));b.Add(s)
def text(t,x,y,layer=k.F_SilkS,size=.9):
    s=k.PCB_TEXT(b);s.SetText(t);s.SetPosition(v(x,y));s.SetTextSize(v(size,size));s.SetTextThickness(k.FromMM(.13));s.SetLayer(layer);b.Add(s)
# 70 x 65 mm rounded engineering outline; enclosure fit is not approved.
W=70;H=65;r=3
for a,c in [((r,0),(W-r,0)),((W,r),(W,H-r)),((W-r,H),(r,H)),((0,H-r),(0,r))]:line(a,c)
for a,m,c in [((0,r),(r-r/math.sqrt(2),r-r/math.sqrt(2)),(r,0)),((W-r,0),(W-r+r/math.sqrt(2),r-r/math.sqrt(2)),(W,r)),((W,H-r),(W-r+r/math.sqrt(2),H-r+r/math.sqrt(2)),(W-r,H)),((r,H),(r-r/math.sqrt(2),H-r+r/math.sqrt(2)),(0,H-r))]:
    s=k.PCB_SHAPE(b);s.SetShape(k.SHAPE_T_ARC);s.SetArcGeometry(v(*a),v(*m),v(*c));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s)
def bbox(fp):
    rects=[g.GetBoundingBox() for g in fp.GraphicalItems() if g.GetLayer()==k.F_CrtYd]
    if not rects:rects=[fp.GetBoundingBox(False,False)]
    return [min(mm(a.GetX()) for a in rects),min(mm(a.GetY()) for a in rects),max(mm(a.GetRight()) for a in rects),max(mm(a.GetBottom()) for a in rects)]
def collide(a,c,gap=.25):return not(a[2]+gap<c[0] or c[2]+gap<a[0] or a[3]+gap<c[1] or c[3]+gap<a[1])
occ=[];fps={};rows=[]
for i,(x,y) in enumerate([(3,3),(67,3),(3,62),(67,62)],1):
    f=k.FootprintLoad(str(OUT/'KK_Power.pretty'),'MountingHole_2.2mm_M2')
    assert f,'Run p1_libraries.py before placement'
    f.SetReference('H'+str(i));f.SetAttributes(k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES);f.SetPosition(v(x,y));f.Reference().SetVisible(False);f.Value().SetVisible(False);b.Add(f)
    occ.append(('H'+str(i),[x-2.5,y-2.5,x+2.5,y+2.5]))
def load(p):
    name=p['footprint'].split(':')[1];f=k.FootprintLoad(str(OUT/'KK_Power.pretty'),name)
    assert f,p['ref'];f.SetParent(b);f.SetFPID(k.LIB_ID('KK_Power',name));f.SetReference(p['ref']);f.SetValue(p['value'])
    path=k.KIID_PATH()
    for s in [d['sheet_uuid'],p['uuid']]:path.push_back(k.KIID(s))
    f.SetPath(path)
    for field in ['MPN','Notes','Datasheet']:
        f.SetField(field,p[{'MPN':'mpn','Notes':'note','Datasheet':'datasheet'}[field]]);f.GetField(field).SetVisible(False)
    f.SetField('Description','');f.GetField('Description').SetVisible(False)
    for pad in f.Pads():
        n=np.get((p['ref'],pad.GetNumber()))
        if n:pad.SetNet(n)
        elif pad.GetNumber():raise RuntimeError('Missing exported net for '+p['ref']+'.'+pad.GetNumber())
    return f
def position(f,x,y,angle):
    f.SetPosition(v(0,0));f.SetOrientationDegrees(angle);a=bbox(f)
    f.SetPosition(v(x-(a[0]+a[2])/2,y-(a[1]+a[3])/2))
def accept(p,f):
    a=bbox(f);occ.append((p['ref'],a));b.Add(f);fps[p['ref']]=f
    f.Reference().SetVisible(True);f.Reference().SetLayer(k.F_SilkS);f.Reference().SetTextSize(v(.8,.8));f.Reference().SetTextThickness(k.FromMM(.1));f.Reference().SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T));f.Reference().SetPosition(v((a[0]+a[2])/2,a[1]-.75));f.Value().SetVisible(False)
    rows.append(dict(ref=p['ref'],footprint=p['footprint'],courtyard_mm=a,position_mm=[mm(f.GetPosition().x),mm(f.GetPosition().y)],angle=f.GetOrientationDegrees(),group=p['group']))
fixed={'J1':(13,3.7,180),'J2':(15,58,180),'J3':(51,58,180),'J4':(27,58,180),'J5':(61,43,90),'SW1':(66,17,90),
       'U3':(14,13,0),'U14':(22,10,0),'U1':(28,12,0),'U2':(9,48,0),'U4':(48,12,0),'U12':(43,44,0),'U11':(51,48,0),'U13':(39,7,0),
       'U5':(14,29,0),'U6':(34,29,0),'U7':(54,29,0),'L1':(14,23.5,90),'L2':(34,23.5,90),'L3':(54,23.5,90),
       'U8':(20,43,0),'U9':(27,43,0),'U10':(34,43,0),
       'Q1':(6.5,54,0),'Q2':(14,49,0),'Q3':(19,49,0)}
parts={p['ref']:p for p in d['components']}
for ref,point in fixed.items():
    p=parts[ref];f=load(p);position(f,*point);a=bbox(f)
    bad=[n for n,c in occ if collide(a,c)]
    if bad:raise RuntimeError(f'Fixed collision {ref}: {bad}')
    accept(p,f)
def target(p):
    ref=p['ref'];group=p['group']
    if ref.startswith('TP'):
        i=int(ref[2:])-1;return (6+2.8*(i%21),62)
    if group.endswith('BUCK-BOOST'):
        idx=['5 V BUCK-BOOST','3.3 V BUCK-BOOST','3.2 V BUCK-BOOST'].index(group);x=14+idx*20;n=int(ref[1:]);t=n-(20+idx*10)
        if ref.startswith('C'):
            return (x-4,29+t*2.1) if t in [0,1] else (x+4,27+(t-2)*2.3) if t in [2,3,4] else (x-2,34) if t==5 else (x-3,30) if t==6 else (x+3,29) if t==7 else (x+3,33)
        return (x+4,33+(t%3)*2)
    return {'USB-C CHARGING ONLY':(13,14),'USB-A / USB-C INPUT CURRENT':(39,10),'CELL CHARGER / POWER PATH':(30,12),'CELL PROTECTION / FUSE':(12,47),'SYSTEM SWITCH / INRUSH / UVLO':(48,13),'ALL-RAIL READY / SOFT OUTPUTS':(28,43),'VOLTAGE SUPERVISION / STARTUP':(44,46),'MAIN BOARD HARNESS / DEBUG':(58,49)}[group]
# Placement-only packing; critical loops require explicit copper design next.
todo=[p for p in d['components'] if p['ref'] not in fps]
todo.sort(key=lambda p:(p['ref'].startswith('TP'),not p['group'].endswith('BUCK-BOOST'),not p['ref'].startswith('C')))
for p in todo:
    f=load(p);tx,ty=target(p);choices=[]
    for x in range(4,133):
        xx=x*.5
        for y in range(4,123):
            yy=y*.5;choices.append(((xx-tx)**2+(yy-ty)**2,xx,yy))
    choices.sort();found=False
    for _,x,y in choices:
        for angle in [0,90]:
            position(f,x,y,angle);a=bbox(f)
            if a[0]<1.5 or a[1]<1.5 or a[2]>W-1.5 or a[3]>H-1.5:continue
            if any(collide(a,c) for _,c in occ):continue
            accept(p,f);found=True;break
        if found:break
    if not found:raise RuntimeError('Cannot pack '+p['ref'])
text('P.1 ENGINEERING / UNROUTED',35,1.5,size=.8)
text('CHARGE ONLY',13,9.2,size=.8)
text('1 CELL+ / 2 CELL-',16,63.5,size=.8)
text('1 5V  2 GND  3 3V3  4 3V2',50,63,size=.8)
text('70 x 65 mm / 4-layer placement study - DO NOT FABRICATE',35,68,k.Dwgs_User,1)
text('BAT_NEG is NOT protected GND. No internal USB data.',35,70,k.Dwgs_User,.9)
# Move reference labels into nearby open silkscreen space, not over pads.
def rect(obj):
    a=obj.GetBoundingBox();return [mm(a.GetX()),mm(a.GetY()),mm(a.GetRight()),mm(a.GetBottom())]
blocked=[rect(pad) for f in b.GetFootprints() for pad in f.Pads()]
blocked.extend(rect(g) for f in b.GetFootprints() for g in f.GraphicalItems() if g.GetLayer()==k.F_SilkS)
blocked.extend(rect(g) for g in b.GetDrawings() if g.GetLayer()==k.F_SilkS)
for f in fps.values():
    label=f.Reference();a=bbox(f);cx=(a[0]+a[2])/2;cy=(a[1]+a[3])/2
    candidates=[]
    for dx in range(-18,19):
        for dy in range(-18,19):
            x=cx+dx*.4;y=cy+dy*.4
            score=(x-cx)**2+(y-(a[1]-.8))**2
            candidates.append((score,x,y))
    for _,x,y in sorted(candidates):
        label.SetPosition(v(x,y));rbox=rect(label)
        if rbox[0]<1 or rbox[1]<1 or rbox[2]>W-1 or rbox[3]>H-1:continue
        if any(collide(rbox,c,.16) for c in blocked):continue
        blocked.append(rbox);break
    else:raise RuntimeError('No readable reference location for '+f.GetReference())
b.SynchronizeNetsAndNetClasses(False)
k.SaveBoard(str(PATH),b)
(OUT/'placement.json').write_text(json.dumps({'status':'UNROUTED ENGINEERING STUDY','outline_mm':[W,H],'copper_layers':4,'components':rows},indent=2)+'\n')
print('Saved unrouted placement:',len(rows),'electrical footprints,',len(occ)-len(rows),'mounting holes.')
