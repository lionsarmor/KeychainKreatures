"""Explicit 1.5mm SYS_SW bridge on In1, north of converter hot loops.
Connects the existing four-via source bank to the two-via left input bank.
The remaining In1 ground plane must be rechecked after refill.
"""
from pathlib import Path
import json,heapq,math
import numpy as np
from shapely import Point,LineString,box,union_all,intersects_xy
ROOT=Path(__file__).resolve().parent.parent;out=ROOT/'KK_power_module/work/P2_review'
d=json.loads((out/'geometry.json').read_text());net='/SYS_SW';width=1.5;clearance=.155
raw=[]
for v in d['vias']:
    if v['net']!=net:raw.append(Point(v['xy']).buffer(v['diameter']/2))
for p in d['pads']:
    if max(p['drill']) and p['net']!=net:raw.append(Point(p['xy']).buffer(max(p['size'])/2))
for t in d['tracks']:
    if t['layer']=='In1.Cu' and t['net']!=net:raw.append(LineString([t['a'],t['b']]).buffer(t['width']/2))
obs=union_all(raw).buffer(width/2+clearance)
start=[38.7,13.5];end=[19.7,18.3];step=.1
xs=np.arange(1,49.0001,step);ys=np.arange(1,18.8001,step);xx,yy=np.meshgrid(xs,ys)
valid=~intersects_xy(obs,xx,yy)
# Stay above the switch-node/inductor region except at the input via bank.
def node(p):return (round((p[1]-1)/step),round((p[0]-1)/step))
s=node(start);e=node(end);assert valid[s] and valid[e], 'Bridge bank obstructed'
q=[(0,s)];dist={s:0};prev={s:None};closed=set()
while q:
    _,n=heapq.heappop(q)
    if n in closed:continue
    closed.add(n)
    if n==e:break
    y,x=n
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
        m=(y+dy,x+dx)
        if not(0<=m[0]<len(ys) and 0<=m[1]<len(xs) and valid[m]):continue
        if dx and dy and not(valid[y,x+dx] and valid[y+dy,x]):continue
        c=dist[n]+math.hypot(dx,dy)
        if c<dist.get(m,1e20):dist[m]=c;prev[m]=n;heapq.heappush(q,(c+1.2*math.dist(m,e),m))
assert e in prev,'No legal wide bridge; do not use a thin substitute'
pts=[];n=e
while n is not None:pts.append([float(xs[n[1]]),float(ys[n[0]])]);n=prev[n]
pts.reverse();pts[0]=start;pts[-1]=end
# Line-of-sight simplification, with the same physical obstacle margins.
keep=[pts[0]];i=0
while i<len(pts)-1:
    j=len(pts)-1
    while j>i+1:
        segment=LineString([pts[i],pts[j]])
        if not obs.intersects(segment):break
        j-=1
    keep.append(pts[j]);i=j
assert all(not obs.intersects(LineString([a,z])) for a,z in zip(keep,keep[1:]))
route=dict(net=net,width=width,via_diameter=.6,via_drill=.3,path=[[3,*p] for p in keep],tag='wide SYS_SW bridge')
(out/'POWER_BRIDGE.json').write_text(json.dumps({'routes':[route],'failed':[]},indent=2)+'\n')
print('1.5mm supply bridge:',keep,'length_mm',sum(math.dist(a,z) for a,z in zip(keep,keep[1:])))
