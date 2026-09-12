"""Plan removal of the known obsolete NTC dead-end, stopping at a branch.
No PCB writes. Native DRC must verify the result.
"""
from pathlib import Path
import json,math
from shapely import Point,LineString
out=Path(__file__).resolve().parent.parent/'KK_power_module/work/P2_review'
d=json.loads((out/'geometry.json').read_text())
tracks={t['uuid']:t for t in d['tracks'] if t['net']=='/NTC' and t['layer']=='B.Cu'}
current='de5274e8-35f6-48e6-b3ed-7ef274c743a8';point=[27.4,4.6];remove=[]
while current:
    t=tracks[current];assert not t['locked']
    other=t['b'] if math.dist(point,t['a'])<1e-5 else t['a']
    assert math.dist(point,t['a'])<1e-5 or math.dist(point,t['b'])<1e-5
    remove.append(current)
    if any(v['net']=='/NTC' and math.dist(v['xy'],other)<.26 for v in d['vias']):break
    if any(p['net']=='/NTC' and 'B.Cu' in p['layers'] and math.dist(p['xy'],other)<max(p['size'])/2 for p in d['pads']):break
    neighbors=[q for key,q in tracks.items() if key not in remove and LineString([q['a'],q['b']]).distance(Point(other))<1e-5]
    if len(neighbors)!=1:break
    q=neighbors[0]
    if min(math.dist(other,q['a']),math.dist(other,q['b']))>1e-5:break
    current=q['uuid'];point=other
assert 1<=len(remove)<=60
(out/'unblock.json').write_text(json.dumps({'routes':[{'net':'/NTC','uuids':remove,'reason':'Known obsolete dead-end, stop at first junction'}]},indent=2)+'\n')
print('Prune',len(remove),'obsolete signal segments; stop at',other)
