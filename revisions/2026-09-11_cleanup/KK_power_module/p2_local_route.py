"""Deterministic outer-layer connection planner. No native board edits.
First routes the six actual load-carrying rail connections at 0.6mm, before
any sense/debug branches. Every resulting candidate must pass native DRC.
"""
from pathlib import Path
import json,math,heapq,itertools,re
import numpy as np
from shapely import Point,LineString,box,union_all,intersects_xy
from shapely.affinity import rotate,translate
OUT=Path(__file__).resolve().parent/'P2_compact'
d=json.loads((OUT/'geometry.json').read_text());pads={p['key']:p for p in d['pads']}
layers=['F.Cu','B.Cu'];step=.1
xs=np.arange(0,50.0001,step);ys=xs;xx,yy=np.meshgrid(xs,ys);ny,nx=xx.shape
inside=box(3,3,47,47).buffer(3,quad_segs=32)
def padshape(p):
    x,y=p['size'];s=p['shape'];r=p['radius'] if s==4 else min(x,y)/2 if s==2 else 0
    if s==0:g=Point(0,0).buffer(x/2,quad_segs=24)
    elif r and s==2:
        g=Point(0,0).buffer(r,quad_segs=24) if abs(x-y)<1e-8 else LineString([(-x/2+r,-y/2+r),(x/2-r,y/2-r)]).buffer(r,quad_segs=24)
    elif r:g=box(-x/2+r,-y/2+r,x/2-r,y/2-r).buffer(r,quad_segs=24)
    else:g=box(-x/2,-y/2,x/2,y/2)
    return translate(rotate(g,-p['angle'],origin=(0,0)),*p['xy'])
shapes=[(p,padshape(p)) for p in d['pads']]
planned=[];failed=[]
def route(start,end,net,width,sl,el,tag,vd=.6,dh=.3):
    raw=[[],[]];holes=[];inner_copper=[]
    for p,g in shapes:
        if max(p['drill'])>0:
            h=Point(p['xy']).buffer(max(p['drill'])/2,quad_segs=24)
            holes.append(h)
            if p['net']!=net:
                for row in raw:row.append(h.buffer(.205-.155))
        if p['net']==net:continue
        for la in range(2):
            if layers[la] in p['layers']:raw[la].append(g)
    for t in d['tracks']:
        if t['net']!=net and t['layer'] in layers:raw[layers.index(t['layer'])].append(LineString([t['a'],t['b']]).buffer(t['width']/2,quad_segs=16))
        elif t['net']!=net:inner_copper.append(LineString([t['a'],t['b']]).buffer(t['width']/2,quad_segs=16))
    for v in d['vias']:
        holes.append(Point(v['xy']).buffer(v['drill']/2,quad_segs=16))
        if v['net']!=net:
            for row in raw:row.append(Point(v['xy']).buffer(v['diameter']/2,quad_segs=24))
    copper=[union_all(r) for r in raw]
    outside=box(-3,-3,53,53).difference(inside.buffer(-(.405+width/2)))
    obs=[union_all([g.buffer(.155+width/2),outside]) for g in copper]
    valid=np.stack([~intersects_xy(g,xx,yy) for g in obs])
    viaobs=union_all([g.buffer(.155+vd/2) for g in copper+inner_copper]+[box(-3,-3,53,53).difference(inside.buffer(-(.405+vd/2))),union_all(holes).buffer(dh/2+.255)])
    viavalid=~intersects_xy(viaobs,xx,yy)
    def links(pt,allowed):
        result={};ix,iy=round(pt[0]/step),round(pt[1]/step)
        for la in allowed:
            for dy in range(-5,6):
                for dx in range(-5,6):
                    x,y=ix+dx,iy+dy
                    if 0<=x<nx and 0<=y<ny and valid[la,y,x] and not obs[la].intersects(LineString([pt,(xs[x],ys[y])])):result[(la,y,x)]=math.dist(pt,(xs[x],ys[y]))
        return result
    starts=links(start,sl);ends=links(end,el)
    if not starts or not ends:raise RuntimeError('No legal pad escape')
    q=[];dist={};prev={};serial=itertools.count()
    def heuristic(n):return math.dist((xs[n[2]],ys[n[1]]),end)
    for n,c in starts.items():dist[n]=c;prev[n]=None;heapq.heappush(q,(c+heuristic(n),next(serial),c,n))
    closed=set();finish=None
    while q:
        _,_,cost,n=heapq.heappop(q)
        if n in closed:continue
        closed.add(n)
        if n in ends:finish=n;break
        la,y,x=n;candidates=[]
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            a,c=x+dx,y+dy
            if not(0<=a<nx and 0<=c<ny and valid[la,c,a]):continue
            if dx and dy and not(valid[la,y,a] and valid[la,c,x]):continue
            candidates.append(((la,c,a),step*math.hypot(dx,dy)))
        if viavalid[y,x]:candidates.append(((1-la,y,x),3))
        for m,w in candidates:
            nc=cost+w
            if nc<dist.get(m,float('inf')):dist[m]=nc;prev[m]=n;heapq.heappush(q,(nc+heuristic(m),next(serial),nc,m))
    if finish is None:raise RuntimeError('No path through current copper')
    nodes=[];n=finish
    while n is not None:nodes.append(n);n=prev[n]
    nodes.reverse();pts=[(nodes[0][0],*start)]+[(la,float(xs[x]),float(ys[y])) for la,y,x in nodes]+[(nodes[-1][0],*end)]
    keep=[pts[0]]
    for i in range(1,len(pts)-1):
        a,z,c=keep[-1],pts[i],pts[i+1]
        if a[0]==z[0]==c[0] and abs((z[1]-a[1])*(c[2]-z[2])-(z[2]-a[2])*(c[1]-z[1]))<1e-8:continue
        keep.append(z)
    keep.append(pts[-1])
    for a,z in zip(keep,keep[1:]):
        if a==z:continue
        if a[0]==z[0]:
            if obs[a[0]].intersects(LineString([a[1:],z[1:]])):raise RuntimeError('Simplification clearance failed')
            d['tracks'].append(dict(net=net,a=a[1:],b=z[1:],width=width,layer=layers[a[0]]))
        else:d['vias'].append(dict(net=net,xy=a[1:],diameter=vd,drill=dh))
    planned.append(dict(net=net,width=width,via_diameter=vd,via_drill=dh,path=keep,tag=tag))
    (OUT/'LOCAL_ROUTES.json').write_text(json.dumps({'routes':planned,'failed':failed},indent=2)+'\n')
    print(tag,net,width,'mm',len(keep),'vertices',flush=True)
for a,z in [('C24:1','U8:1'),('U8:6','J3:1'),('C34:1','U9:1'),('U9:6','J3:3'),('C44:1','U10:1'),('U10:6','J3:4')]:
    p,q=pads[a],pads[z]
    try:route(p['xy'],q['xy'],p['net'],.6,[0],[0,1] if max(q['drill']) else [0],a+' -> '+z)
    except RuntimeError as e:failed.append({'connection':[a,z],'reason':str(e),'critical':True});print('FAILED CRITICAL',a,z,e,flush=True)
# Additional branches use the actual KiCad disconnected-item list. Native
# connectivity is re-evaluated after importing this candidate; no completion
# claim is based on a count of planned paths alone.
report=json.loads((OUT/'finish_drc.json').read_text())
for idx,item in enumerate(sorted(report['unconnected_items'],key=lambda q:math.dist(list(q['items'][0]['pos'].values()),list(q['items'][1]['pos'].values())))):
    a,z=item['items'];m=re.search(r'\[([^]]+)\]',a['description'])
    if not m:continue
    net=m.group(1);start=[a['pos']['x'],a['pos']['y']];end=[z['pos']['x'],z['pos']['y']]
    def allowed(q):
        text=q['description']
        if text.startswith('Via') or 'on all copper layers' in text:return [0,1]
        if 'on F.Cu' in text:return [0]
        if 'on B.Cu' in text:return [1]
        return []
    sl,el=allowed(a),allowed(z)
    if not sl or not el:failed.append({'connection':[a,z],'reason':'Unsupported endpoint layer'});continue
    for width in [.2,.15]:
        try:route(start,end,net,width,sl,el,'branch '+str(idx),.5,.2);break
        except RuntimeError as e:
            if width==.15:failed.append({'connection':[a,z],'reason':str(e)});print('FAILED',net,e,flush=True)
(OUT/'LOCAL_ROUTES.json').write_text(json.dumps({'routes':planned,'failed':failed},indent=2)+'\n')
print('Planned',len(planned),'failed',len(failed),flush=True)
