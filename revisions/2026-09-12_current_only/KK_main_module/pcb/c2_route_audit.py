"""Read-only route topology/width audit. Lengths exclude vertical via barrels."""
from pathlib import Path
import json, math, heapq, collections, sys
import pcbnew as k
root=Path(__file__).resolve().parent.parent
file=Path(sys.argv[1]) if len(sys.argv)>1 else root/'KK_main_module.kicad_pcb'
b=k.LoadBoard(str(file));fps={f.GetReference():f for f in b.GetFootprints()}
def xy(p):return (round(k.ToMM(p.x),4),round(k.ToMM(p.y),4))
def pad(key):r,n=key.split(':');return next(p for p in fps[r].Pads() if p.GetNumber()==n)
stats=collections.defaultdict(lambda:{'length_mm':0,'widths_mm':set(),'vias':0})
tracks=collections.defaultdict(list);vias=collections.defaultdict(list)
for t in b.GetTracks():
    name=t.GetNetname()
    if t.GetClass()=='PCB_VIA':stats[name]['vias']+=1;vias[name].append(t)
    else:
        stats[name]['length_mm']+=k.ToMM(t.GetLength());stats[name]['widths_mm'].add(k.ToMM(t.GetWidth()));tracks[name].append(t)
def distance(a,z):
    pa,pz=pad(a),pad(z);name=pa.GetNetname();assert name==pz.GetNetname(),(a,z)
    edges=collections.defaultdict(list);points=set()
    ts=tracks[name]
    for t in ts:
        for p in (t.GetStart(),t.GetEnd()):points.add((*xy(p),t.GetLayer()))
    def link(n,m,d):edges[n].append((m,d));edges[m].append((n,d))
    for t in ts:
        aa,zz=xy(t.GetStart()),xy(t.GetEnd());dx,dy=zz[0]-aa[0],zz[1]-aa[1];ll=math.hypot(dx,dy)
        if not ll:continue
        hits=[]
        for p in points:
            if p[2]!=t.GetLayer():continue
            dot=((p[0]-aa[0])*dx+(p[1]-aa[1])*dy)/ll
            cross=abs((p[0]-aa[0])*dy-(p[1]-aa[1])*dx)/ll
            if -.0003<=dot<=ll+.0003 and cross<.0003:hits.append((dot,p))
        hits.sort()
        for (d,n),(dd,m) in zip(hits,hits[1:]):link(n,m,dd-d)
    for v in vias[name]:
        x,y=xy(v.GetPosition());link((x,y,k.F_Cu),(x,y,k.B_Cu),0)
    # Plated pads bridge both layers; include copper travel within each pad.
    for f in fps.values():
        for p in f.Pads():
            if p.GetNetname()!=name:continue
            key=f.GetReference()+':'+p.GetNumber();x,y=xy(p.GetPosition())
            for n in points:
                if p.HitTest(k.VECTOR2I(k.FromMM(n[0]),k.FromMM(n[1]))):link(key,n,math.hypot(n[0]-x,n[1]-y))
    queue=[(0,a)];ds={a:0};visited=set();serial=0
    # Mixed node types need a serial tie-breaker in the priority queue.
    queue=[(0,0,a)]
    while queue:
        d,_,n=heapq.heappop(queue)
        if n in visited:continue
        if n==z:return round(d,3)
        visited.add(n)
        for m,c in edges[n]:
            dd=d+c
            if dd<ds.get(m,float('inf')):
                ds[m]=dd;serial+=1;heapq.heappush(queue,(dd,serial,m))
    return None
pairs=json.loads((root/'pcb/C2_PLACEMENT_DISTANCES.json').read_text())
for a,z in [('C11:1','U1:9'),('J1:1','MOD1:5V'),('J1:3','J2:2'),('J1:3','J3:1'),('J1:4','Q6:1'),('Q6:3','U3:2'),('J1:4','J4:1')]:pairs.append({'connection':a+' -> '+z})
for row in pairs:
    a,z=row['connection'].split(' -> ')
    if pad(a).GetNetname()==pad(z).GetNetname():row['routed_length_mm']=distance(a,z)
for s in stats.values():s['widths_mm']=sorted(s['widths_mm']);s['length_mm']=round(s['length_mm'],3)
result={'source':str(file),'track_segments':sum(len(v) for v in tracks.values()),'vias':sum(len(v) for v in vias.values()),'net_statistics':dict(stats),'path_lengths':pairs,'note':'Shortest trace graph length including in-pad travel; excludes via barrel length and plane shortcuts. Null does not prove disconnection when pours supply a path.'}
(root/'pcb/C2_ROUTE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'tracks':result['track_segments'],'vias':result['vias'],'paths':pairs},indent=2))
