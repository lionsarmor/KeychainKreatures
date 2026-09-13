"""Find local, drill/copper-clear placement for the five C.3 RGB parts."""
from pathlib import Path
import json,math
from shapely import Point,LineString,box,union_all
from shapely.affinity import translate,rotate
root=Path(__file__).resolve().parent.parent
d=json.loads((root/'routing/c3_geometry.json').read_text())
# Reuse only the pure pad-shape definition, not the executable planner.
import ast
tree=ast.parse((root/'pcb/c3_plan_debug.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='padshape'],type_ignores=[]),'<padshape>','exec'))
refs=['U4','D3','R40','R41','C27'];fps={f['ref']:f for f in d['footprints']}
oldpads=[p for p in d['pads'] if p['key'].split(':')[0] not in refs]
oldfps=[f for f in d['footprints'] if f['ref'] not in refs]
placed=[]
inside=box(4,4,76,96).buffer(4).buffer(-.6)
for ref in refs:
    f=fps[ref];ps=[p for p in d['pads'] if p['key'].split(':')[0]==ref]
    body=box(*f['courtyard_mm'])
    neighbors=union_all([box(*g['courtyard_mm']).buffer(.21) for g in oldfps if g['side']==f['side'] and g['courtyard_mm']]+[Point(x,y).buffer(2.8) for x,y in [(4,4),(76,60),(4,96),(76,96)]])
    blocked=[]
    for p in ps:
        net=p['net']
        # Existing track segments may be locally rerouted after placement.
        # Existing component pads and via drills remain immutable obstacles.
        copper=union_all([padshape(q) for q in oldpads if q['net']!=net]+[Point(v['xy']).buffer(v['diameter']/2) for v in d['vias'] if v['net']!=net]).buffer(.21)
        holes=union_all([Point(q['xy']).buffer(max(q['drill'])/2+max(p['drill'])/2+.255) for q in oldpads]+[Point(v['xy']).buffer(v['drill']/2+max(p['drill'])/2+.255) for v in d['vias']])
        blocked.append((p,padshape(p),copper,holes))
    candidates=sorted([(i*.5,j*.5) for i in range(-140,141) for j in range(-170,31)],key=lambda a:a[0]**2+a[1]**2)
    found=None
    for dx,dy in candidates:
        g=translate(body,dx,dy)
        if not inside.contains(g) or neighbors.intersects(g):continue
        if any(g.intersects(padshape(p)) for p in oldpads):continue
        if any(box(*o['courtyard_mm']).intersects(translate(shape,dx,dy)) for o in oldfps if o['courtyard_mm'] for p,shape,copper,holes in blocked):continue
        if any(copper.intersects(translate(shape,dx,dy)) or holes.intersects(Point(p['xy'][0]+dx,p['xy'][1]+dy)) for p,shape,copper,holes in blocked):continue
        found=(dx,dy);break
    assert found,'No safe RGB placement for '+ref
    dx,dy=found
    for p in ps:p['xy']=[p['xy'][0]+dx,p['xy'][1]+dy]
    f['xy']=[f['xy'][0]+dx,f['xy'][1]+dy];f['courtyard_mm']=[f['courtyard_mm'][0]+dx,f['courtyard_mm'][1]+dy,f['courtyard_mm'][2]+dx,f['courtyard_mm'][3]+dy]
    oldpads.extend(ps);oldfps.append(f);placed.append({'ref':ref,'delta':found,'xy':f['xy'],'courtyard_mm':f['courtyard_mm'],'side':f['side']})
    print(placed[-1],flush=True)
(root/'pcb/C3_RGB_PLACEMENT_FINAL.json').write_text(json.dumps(placed,indent=2)+'\n')
