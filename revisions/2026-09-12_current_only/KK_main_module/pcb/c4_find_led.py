"""Find a pad/courtyard-safe socket site below MCU using actual copper obstacles."""
from pathlib import Path
import json,ast,math
from shapely import Point,LineString,box,union_all
from shapely.affinity import rotate,translate
root=Path(__file__).resolve().parent.parent;d=json.loads((root/'routing/c3_geometry.json').read_text())
exec(compile(ast.Module(body=[n for n in ast.parse((root/'pcb/c2_local_route.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='padshape'],type_ignores=[]),'<pad shapes>','exec'))
pads=[p for p in d['pads'] if not p['key'].startswith('D3:')]
copper=union_all([padshape(p) for p in pads]+[LineString([t['a'],t['b']]).buffer(t['width']/2) for t in d['tracks']]+[Point(v['xy']).buffer(v['diameter']/2) for v in d['vias']]).buffer(.205)
front=union_all([box(*f['courtyard_mm']) for f in d['footprints'] if f['side']=='front' and f['ref']!='D3' and f['courtyard_mm']])
back=union_all([box(*f['courtyard_mm']) for f in d['footprints'] if f['side']=='back' and f['courtyard_mm']])
leadobs=union_all([padshape(p) for p in pads])
result=[]
for a in [0,90]:
    for ix in range(224,306):
        for iy in range(132,201):
            x,y=ix/4,iy/4
            # Socket body courtyard, not elevated lens projection.
            court=translate(rotate(box(-5.61,-1.795,5.61,1.795),-a,origin=(0,0)),x,y)
            if court.bounds[2]>79.5 or court.intersects(front) or court.intersects(leadobs):continue
            ps=[(x+(i-1.5)*2.54*math.cos(math.radians(a)),y-(i-1.5)*2.54*math.sin(math.radians(a))) for i in range(4)]
            shapes=[Point(p).buffer(.925) for p in ps]
            if any(s.intersects(back) or s.intersects(copper) for s in shapes):continue
            result.append({'center':[x,y],'angle':a,'score':math.dist((x,y),(69,37.75))})
result.sort(key=lambda x:x['score']);print(json.dumps(result[:15],indent=2))
(root/'pcb/C4_LED_SITES.json').write_text(json.dumps(result,indent=2)+'\n')
