"""Find accessible rear PTH probe points with short, clearance-checked taps.
Does not alter existing routing. KiCad DRC is the final acceptance gate.
"""
from pathlib import Path
import json, math
from shapely import Point, LineString, box, union_all, intersects_xy
import numpy as np
from shapely.affinity import rotate, translate
root=Path(__file__).resolve().parent.parent
d=json.loads((root/'routing/c3_geometry.json').read_text())
pads={p['key']:p for p in d['pads']}
def padshape(p):
    x,y=p['size'];s=p['shape'];r=p['radius'] if s==4 else min(x,y)/2 if s==2 else 0
    if s==0:g=Point(0,0).buffer(x/2,quad_segs=24)
    elif r:
        if abs(x-y)<1e-8:g=Point(0,0).buffer(r,quad_segs=24)
        elif abs(min(x,y)-2*r)<1e-8:g=LineString([(-x/2+r,-y/2+r),(x/2-r,y/2-r)]).buffer(r,quad_segs=24)
        else:g=box(-x/2+r,-y/2+r,x/2-r,y/2-r).buffer(r,quad_segs=16)
    else:g=box(-x/2,-y/2,x/2,y/2)
    return translate(rotate(g,-p['angle'],origin=(0,0)),*p['xy'])
shapes=[(p['net'],padshape(p)) for p in d['pads']]
inside=box(4,4,76,96).buffer(4,quad_segs=24).buffer(-1.505)
rf=union_all([box(51,0,80,7),box(59.5,7,72.5,15.5)]).buffer(1.205)
placement=json.loads((root/'pcb/PLACEMENT.json').read_text())['components']
bodies={side:union_all([box(*f['courtyard_mm']).buffer(1.15) for f in placement if f['side']==side]) for side in ('front','back')}
holes=union_all([Point(p['xy']).buffer(max(p['drill'])/2+.4+.26) for p in d['pads']]+[Point(v['xy']).buffer(v['drill']/2+.4+.26) for v in d['vias']]+[Point(x,y).buffer(3.8) for x,y in [(4,4),(76,60),(4,96),(76,96)]])
silks=union_all([box(*s['box']).buffer(1.15) for s in d['silks']])
targets=[('5V','J1:1'),('3V3','J1:3'),('3V2','J1:4'),('GND-P','J1:2'),('AMP-V','U3:2'),('GND-A','U3:4'),('GND-L','U1:10'),('GND-M','Q4:1'),('SDA','MOD1:4'),('SCL','MOD1:5'),('KEY-IRQ','MOD1:1'),('FN','MOD1:2'),('SCK','MOD1:13'),('MOSI','MOD1:11'),('MISO','MOD1:12'),('SD-CS','MOD1:10'),('TFT-CS','MOD1:RX'),('TFT-DC','MOD1:TX'),('TFT-RST','U1:7'),('BL-PWM','MOD1:9'),('BLK','J2:8'),('AUD-PWM','MOD1:8'),('AUD-LP2','R31:2'),('AMP-IN','U3:7'),('AMP-EN','U1:5'),('SPK+','J5:1'),('SPK-','J5:2'),('MOT-EN','U1:6'),('MOT-RET','J4:2'),('IR-TX','MOD1:7'),('IR-RX','MOD1:6'),('IR-V','U2:3'),('IO-RST','U1:18'),('AMP-G','Q6:2'),('MOT-G','Q4:2'),('GND-I','U2:2')]
classes=json.loads((root/'pcb/C2_ROUTING_RULES.json').read_text())
result=[]
for index,(label,key) in enumerate(targets,1):
    src=pads[key];net=src['net']; origin=src['xy']
    # Test branches retain the existing net's largest nominal track width.
    widths=[t['width'] for t in d['tracks'] if t['net']==net]
    width=max(widths,default=.25)
    raw=[[],[]]
    for n,g in shapes:
        if n!=net:
            for r in raw:r.append(g)
    for t in d['tracks']:
        if t['net']!=net:raw[t['layer']].append(LineString([t['a'],t['b']]).buffer(t['width']/2,quad_segs=12))
    for v in d['vias']:
        if v['net']!=net:
            for r in raw:r.append(Point(v['xy']).buffer(v['diameter']/2))
    copper=[union_all(r) for r in raw]
    blocked=union_all([* [g.buffer(1.21) for g in copper],rf,bodies['front'].intersection(bodies['back']),holes,silks,*[Point(t['xy']).buffer(2.6) for t in result]])
    obstacles=[g.buffer(width/2+.21) for g in copper]
    ends=[]
    for p in d['pads']:
        if p['net']==net:
            ends.extend([(la,p['xy']) for la in (1,0)])
    # Also tap existing same-net tracks, shortening branches instead of following
    # the track back to its component pad.
    tracks=[t for t in d['tracks'] if t['net']==net]
    xx,yy=np.meshgrid(np.arange(1.5,78.51,.5),np.arange(1.5,98.51,.5))
    valid=intersects_xy(inside,xx,yy)&~intersects_xy(blocked,xx,yy)
    candidates=list(zip(xx[valid].tolist(),yy[valid].tolist()))
    candidates.sort(key=lambda p:math.dist(p,origin))
    best=None
    for pt in candidates:
        if best and math.dist(pt,origin)*.15>best[0]:continue
        local=ends[:]
        for t in tracks:
            line=LineString([t['a'],t['b']]);foot=line.interpolate(line.project(Point(pt)))
            if foot.distance(Point(pt))<7:local.append((t['layer'],list(foot.coords)[0]))
        for la,end in local:
            length=math.dist(pt,end)
            if length>7 or length<.05:continue
            path=LineString([pt,end])
            if obstacles[la].intersects(path):continue
            score=length+math.dist(pt,origin)*.15+(2 if bodies['back'].intersects(Point(pt)) else 0)
            if best is None or score<best[0]:best=(score,pt,la,end,length)
    if not best:
        print('NO ROOM',index,label,key,flush=True);continue
    _,pt,la,end,length=best
    side='front' if bodies['back'].intersects(Point(pt)) else 'back'
    item={'ref':f'TP{index}','label':label,'source_pin':key,'net':net,'xy':pt,'diameter':2.0,'drill':.8,'width':width,'layer':la,'end':end,'stub_mm':length,'probe_side':side}
    result.append(item)
    shapes.append((net,Point(pt).buffer(1,quad_segs=24)))
    d['tracks'].append({'net':net,'a':pt,'b':end,'width':width,'layer':la})
    print(item['ref'],label,pt,'tap',round(length,2),flush=True)
(root/'pcb/C3_DEBUG_PLAN.json').write_text(json.dumps(result,indent=2)+'\n')
print('TOTAL',len(result))
