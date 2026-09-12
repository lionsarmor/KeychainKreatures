"""Small deterministic copper repair router; uses actual pad and track obstacles.
Generated routes MUST pass KiCad DRC before use. Host Python + Shapely/numpy.
"""
from pathlib import Path
import json, math, heapq, itertools
import numpy as np
from shapely import Point,LineString,box,union_all,intersects_xy
from shapely.affinity import rotate,translate
root=Path(__file__).resolve().parent.parent
d=json.loads((root/'routing/c2_geometry.json').read_text())
pads={p['key']:p for p in d['pads']}
def padshape(p):
    x,y=p['size'];s=p['shape'];r=p['radius'] if s==4 else min(x,y)/2 if s==2 else 0
    if s==0:g=Point(0,0).buffer(x/2,quad_segs=24)
    elif r:
        if abs(x-y)<1e-8:g=Point(0,0).buffer(r,quad_segs=24)
        elif abs(min(x,y)-2*r)<1e-8:
            g=LineString([(-x/2+r,-y/2+r),(x/2-r,y/2-r)]).buffer(r,quad_segs=24)
        else:g=box(-x/2+r,-y/2+r,x/2-r,y/2-r).buffer(r,quad_segs=16)
    else:g=box(-x/2,-y/2,x/2,y/2)
    return translate(rotate(g,-p['angle'],origin=(0,0)),*p['xy'])
shapes=[(p['net'],padshape(p),p) for p in d['pads']]
# Board edge clearance >=0.5 mm; radius 4 mm; no antenna copper.
inside=box(4,4,76,96).buffer(4,quad_segs=24).buffer(-.505)
outside=box(-5,-5,85,105).difference(inside)
step=.2;xs=np.arange(0,80.00001,step);ys=np.arange(0,100.00001,step)
xx,yy=np.meshgrid(xs,ys);ny,nx=xx.shape
repairs=[]
def route(start,end,net,width,vd,dh,end_layers=(0,1)):
    raw=[[],[]]
    for _,g,p in shapes:
        if p['net']!=net:
            for layer in raw:layer.append(g)
    for t in d['tracks']: 
        if t['net']!=net:raw[t['layer']].append(LineString([t['a'],t['b']]).buffer(t['width']/2,quad_segs=12))
    for v in d['vias']:
        if v['net']!=net:
            for layer in raw:layer.append(Point(v['xy']).buffer(v['diameter']/2,quad_segs=16))
    copper=[union_all(r) for r in raw]
    rf=union_all([box(51,0,80,7),box(59.5,7,72.5,15.5)])
    obstacles=[union_all([g.buffer(.205+width/2),outside,rf.buffer(width/2+.205)]) for g in copper]
    valid=np.stack([~intersects_xy(g,xx,yy) for g in obstacles])
    viaobs=union_all([g.buffer(.205+vd/2) for g in copper]+[outside.buffer(vd/2),rf.buffer(vd/2+.205)]+[Point(p['xy']).buffer(max(p['drill'])/2+dh/2+.255) for p in d['pads']]+[Point(v['xy']).buffer(v['drill']/2+dh/2+.255) for v in d['vias']])
    viavalid=~intersects_xy(viaobs,xx,yy)
    def links(pt,layers):
        result={}
        for la in layers:
            ix,iy=round(pt[0]/step),round(pt[1]/step)
            for dy in range(-3,4):
                for dx in range(-3,4):
                    x,y=ix+dx,iy+dy
                    if 0<=x<nx and 0<=y<ny and valid[la,y,x] and not obstacles[la].intersects(LineString([pt,(xs[x],ys[y])])):result[(la,y,x)]=math.dist(pt,(xs[x],ys[y]))
        return result
    starts=links(start,(0,1));ends=links(end,end_layers)
    assert starts and ends,('No legal pad escape',start,end)
    dist={};prev={};serial=itertools.count();q=[]
    def heur(n):return math.dist((xs[n[2]],ys[n[1]]),end)
    for n,c in starts.items():dist[n]=c;prev[n]=None;heapq.heappush(q,(c+heur(n),next(serial),c,n))
    closed=set();finish=None
    while q:
        _,_,cost,n=heapq.heappop(q)
        if n in closed:continue
        closed.add(n)
        if n in ends:finish=n;break
        la,y,x=n
        candidates=[]
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            a,c=x+dx,y+dy
            if not (0<=a<nx and 0<=c<ny and valid[la,c,a]):continue
            if dx and dy and not(valid[la,y,a] and valid[la,c,x]):continue
            candidates.append(((la,c,a),step*math.hypot(dx,dy)))
        if viavalid[y,x]:candidates.append(((1-la,y,x),4))
        for m,w in candidates:
            nc=cost+w
            if nc<dist.get(m,float('inf')):
                dist[m]=nc;prev[m]=n;heapq.heappush(q,(nc+heur(m),next(serial),nc,m))
    if finish is None:raise RuntimeError('No local route '+net)
    nodes=[];n=finish
    while n is not None:nodes.append(n);n=prev[n]
    nodes.reverse();pts=[(nodes[0][0],*start)]+[(la,float(xs[x]),float(ys[y])) for la,y,x in nodes]+[(nodes[-1][0],*end)]
    # Collapse straight grid steps, retaining exact pad endpoint stubs.
    keep=[pts[0]]
    for i in range(1,len(pts)-1):
        a,b,c=keep[-1],pts[i],pts[i+1]
        if a[0]==b[0]==c[0] and abs((b[1]-a[1])*(c[2]-b[2])-(b[2]-a[2])*(c[1]-b[1]))<1e-8:continue
        keep.append(b)
    keep.append(pts[-1])
    r={'net':net,'width':width,'via_diameter':vd,'via_drill':dh,'path':keep}
    for a,b in zip(keep,keep[1:]):
        if a[0]==b[0]:
            assert not obstacles[a[0]].intersects(LineString([a[1:],b[1:]])), 'Generated segment touches obstacle'
            d['tracks'].append({'net':net,'a':a[1:],'b':b[1:],'width':width,'layer':a[0]})
        else:d['vias'].append({'net':net,'xy':a[1:],'diameter':vd,'drill':dh})
    repairs.append(r);print(net,'route length',sum(math.dist(a[1:],b[1:]) for a,b in zip(keep,keep[1:])),'vertices',len(keep),flush=True)
# Final all-net route is connected. Only add the short shared bulk-cap branch.
route(pads['C11:1']['xy'],pads['U1:9']['xy'],pads['C11:1']['net'],.8,1,.5)
(root/'routing/C2_LOCAL_REPAIRS.json').write_text(json.dumps(repairs,indent=2)+'\n')
