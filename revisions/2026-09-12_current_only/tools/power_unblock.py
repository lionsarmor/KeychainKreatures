"""Identify removable signal branches that fence in unrouted IC pins."""
from pathlib import Path
import json,math,sys
from shapely import LineString,Point
ROOT=Path(__file__).resolve().parent.parent;out=ROOT/'KK_power_module/work/P2_review'
d=json.loads((out/'geometry.json').read_text());pads={p['key']:p for p in d['pads']}
origins={p['ref']:p['position_mm'] for p in json.loads((out/'placement.json').read_text())['components']}
routes=json.loads((out/'imported_plan_items.json').read_text())
targets=sys.argv[1:] or ['U3:1','U3:2','U4:2','U12:7','U12:9','U7:3','U7:4','U1:1']
blocked=set();audit=[]
extra=[]
for key in targets:
    p=pads[key];o=origins[key.split(':')[0]];a=p['xy'];dx,dy=a[0]-o[0],a[1]-o[1]
    if abs(dx)>abs(dy):end=[a[0]+math.copysign(1.1,dx),a[1]]
    else:end=[a[0],a[1]+math.copysign(1.1,dy)]
    corridor=LineString([a,end]).buffer(.075+.151)
    for t in d['tracks']:
        if t['layer']!='F.Cu' or t['net']==p['net']:continue
        if corridor.intersects(LineString([t['a'],t['b']]).buffer(t['width']/2)):
            r=next((r for r in routes if t['uuid'] in r['uuids']),None)
            if r and r['tag'].startswith('branch'):
                blocked.add(r['tag']);audit.append({'pin':key,'blocking_net':t['net'],'branch':r['tag']})
            elif r is None and not t['locked']:
                extra.append({'tag':'local '+t['uuid'],'net':t['net'],'uuids':[t['uuid']]})
                audit.append({'pin':key,'blocking_net':t['net'],'segment':t['uuid']})
selected=[r for r in routes if r['tag'] in blocked]+extra
(out/'unblock.json').write_text(json.dumps({'routes':selected,'audit':audit},indent=2)+'\n')
print('Proposed rip-up of',len(selected),'signal branches:',[(r['tag'],r['net']) for r in selected])
