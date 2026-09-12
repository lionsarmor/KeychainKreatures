"""50mm compact power placement. Critical converter placements are explicit.

Run in KiCad Python, after P.2 native netlist export. Never overwrites routing.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=(ROOT/'p1_board.py').read_text().split('fixed=')[0]
s=s.replace("OUT=ROOT/'P1_revision'","OUT=ROOT/'P2_compact'")
s=s.replace('W=70;H=65;r=3','W=50;H=50;r=3')
s=s.replace('[(3,3),(67,3),(3,62),(67,62)]','[(3,3),(47,3),(3,47),(47,47)]')
s=s.replace('g.GetLayer()==k.F_CrtYd','g.GetLayer() in (k.F_CrtYd,k.B_CrtYd)')
exec(compile(s,str(ROOT/'p1_board.py'),'exec'),globals())
parts={p['ref']:p for p in d['components']}
fixed={'J1':(12,3.7,180),'SW1':(46,11,90),
       'J2':(10.5,42.5,180),'J3':(35.5,44,180),'J4':(22,44,180),
       'U3':(11,11,0),'U14':(20,7,0),'U13':(23,4.5,0),'U1':(28,7,0),'U4':(36,11,0),
       'U2':(8,31.5,0),'Q1':(5.5,35.5,0),'Q2':(10.5,35.5,0),'Q3':(15.5,35.5,0),
       'U8':(22,33,0),'U9':(27,33,0),'U10':(32,32,0),'U12':(41,30.8,0),'U11':(43,36,0)}
for i,x in enumerate([8,23,38]):
    idx=20+i*10
    fixed.update({f'U{5+i}':(x,23,0),f'L{1+i}':(x,18.25,0),
      f'C{idx}':(x-4.25,22.5,180),f'C{idx+1}':(x-4.25,20,180),
      f'C{idx+2}':(x+3.4,20.5,90),f'C{idx+3}':(x+5.6,20.5,90),f'C{idx+4}':(x+7.8,20.5,90),
      f'C{idx+5}':(x,26.5,180),f'C{idx+8}':(x+3.5,25,270),
      f'R{idx}':(x+5.3,25,90),f'R{idx+1}':(x+7.1,25,270)})
    if i==2:fixed['R43']=(46.5,27.5,0)
for ref,pt in fixed.items():
    p=parts[ref];f=load(p);position(f,*pt);a=bbox(f)
    bad=[n for n,c in occ if collide(a,c,.1)]
    if bad:raise RuntimeError(f'Fixed collision {ref}: {bad}; box {a}')
    accept(p,f)
# Preserve room for short switcher loops, feedback returns and their ground
# stitches; do not fill their inter-component spaces with unrelated circuitry.
occ.append(('CONVERTER_ROUTING_SPACE',[1.5,15.5,48.5,28.2]))
occ.append(('EFUSE_OUTPUT_FANOUT',[37.3,12.4,40.3,14.8]))
occ.append(('USB_LIMITER_FANOUT',[21.4,3,25,6.5]))
targets={'USB-C CHARGING ONLY':(15,11),'USB-A / USB-C INPUT CURRENT':(23,8),
         'CELL CHARGER / POWER PATH':(29,9),'CELL PROTECTION / FUSE':(12,33),
         'SYSTEM SWITCH / INRUSH / UVLO':(37,12),'ALL-RAIL READY / SOFT OUTPUTS':(27,36),
         'VOLTAGE SUPERVISION / STARTUP':(42,32),'MAIN BOARD HARNESS / DEBUG':(35,38)}
todo=[p for p in d['components'] if p['ref'] not in fps and not p['ref'].startswith('TP')]
def preference(p):
    special={'C1':(18,9.7),'C2':(11,13),'C3':(29,4),'C4':(24.5,7),'C5':(31.5,7),
             'C7':(34,10),'C8':(38.5,11),'C9':(33,12),'C60':(43,28),'C72':(20,7)}
    return special.get(p['ref'],targets[p['group']])
todo.sort(key=lambda p:not p['ref'].startswith('C'))
for p in todo:
    f=load(p);tx,ty=preference(p)
    choices=sorted(((x*.25-tx)**2+(y*.25-ty)**2,x*.25,y*.25) for x in range(8,193) for y in range(8,185))
    for _,x,y in choices:
        found=False
        for angle in [0,90,180,270]:
            position(f,x,y,angle);a=bbox(f)
            if min(a[:2])<1.4 or a[2]>W-1.4 or a[3]>H-1.4:continue
            if any(collide(a,c,.2) for _,c in occ):continue
            accept(p,f);found=True;break
        if found:break
    else:raise RuntimeError('Cannot pack '+p['ref'])
# Bare backside probe pads free front-side placement area without adding a
# second assembled component side. Keep clear of through-hole connectors.
backocc=[]
for f in b.GetFootprints():
    for pad in f.Pads():
        if pad.GetDrillSize().x:
            a=pad.GetBoundingBox();backocc.append([mm(a.GetX())-.3,mm(a.GetY())-.3,mm(a.GetRight())+.3,mm(a.GetBottom())+.3])
for p in [p for p in d['components'] if p['ref'].startswith('TP')]:
    i=int(p['ref'][2:])-1;tx=5+3.6*(i%12);ty=29+3.6*(i//12)
    f=load(p);f.Flip(v(0,0),False)
    for _,x,y in sorted(((x*.5-tx)**2+(y*.5-ty)**2,x*.5,y*.5) for x in range(5,96) for y in range(5,92)):
        position(f,x,y,0);a=bbox(f)
        if any(collide(a,c,.25) for c in backocc):continue
        b.Add(f);fps[p['ref']]=f;backocc.append(a)
        f.Reference().SetVisible(True);f.Reference().SetLayer(k.B_SilkS);f.Reference().SetMirrored(True)
        f.Reference().SetTextSize(v(.8,.8));f.Reference().SetTextThickness(k.FromMM(.1));f.Reference().SetPosition(v(x,y-1.1));f.Value().SetVisible(False)
        rows.append(dict(ref=p['ref'],footprint=p['footprint'],position_mm=[x,y],angle=0,side='back',group=p['group'],courtyard_mm=a));break
    else:raise RuntimeError('No back pad position '+p['ref'])
text('KK POWER P.2',33,1.5,size=.85)
text('USB CHARGE',12,8.9,size=.8)
text('1 + / 2 -',10.5,47.7,size=.8)
text('5V GND 3V3 3V2',35,48.5,size=.8)
text('NTC',22,48.5,size=.8)
text('50 x 50 mm / 4 layers / prototype',25,53,k.Dwgs_User,1)
# Position all reference labels on their own assembly side, avoiding exposed
# copper and other ink. Silkscreen is checked again after routing.
def rect(obj):
    a=obj.GetBoundingBox();return [mm(a.GetX()),mm(a.GetY()),mm(a.GetRight()),mm(a.GetBottom())]
for side,silk in [(k.F_Cu,k.F_SilkS),(k.B_Cu,k.B_SilkS)]:
    blocked=[rect(pad) for f in b.GetFootprints() for pad in f.Pads() if pad.IsOnLayer(side)]
    blocked.extend(rect(g) for f in b.GetFootprints() for g in f.GraphicalItems() if g.GetLayer()==silk)
    blocked.extend(rect(g) for g in b.GetDrawings() if g.GetLayer()==silk)
    for f in fps.values():
        if f.GetLayer()!=side:continue
        label=f.Reference();label.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T));a=bbox(f);cx=(a[0]+a[2])/2;cy=(a[1]+a[3])/2
        for _,x,y in sorted(((dx*.35)**2+(dy*.35+.8+(cy-a[1]))**2,cx+dx*.35,cy+dy*.35) for dx in range(-22,23) for dy in range(-22,23)):
            label.SetPosition(v(x,y));bb=rect(label)
            if min(bb[:2])<.7 or bb[2]>W-.7 or bb[3]>H-.7:continue
            if any(collide(bb,c,.15) for c in blocked):continue
            blocked.append(bb);break
        else:
            # Dense power circuitry may not have a nearby readable silk slot.
            # Keep the reference at its actual component on the assembly layer;
            # do not move it across the board and imply the wrong component.
            label.SetLayer(k.F_Fab if side==k.F_Cu else k.B_Fab)
            label.SetPosition(v(cx,cy));label.SetTextSize(v(.7,.7))
            print('Assembly-layer reference:',f.GetReference(),flush=True)
b.SynchronizeNetsAndNetClasses(False)
k.SaveBoard(str(PATH),b)
(OUT/'placement.json').write_text(json.dumps({'status':'COMPACT UNROUTED','outline_mm':[W,H],'copper_layers':4,'components':rows},indent=2)+'\n')
print('Saved P.2 compact board:',W,H,len(rows),'electrical footprints')
