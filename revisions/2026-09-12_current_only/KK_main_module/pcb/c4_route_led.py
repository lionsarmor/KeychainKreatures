"""Offline reroute of only four relocated LED connections."""
from pathlib import Path
import json,math,heapq,itertools,ast,sys
import numpy as np
from shapely import Point,LineString,box,union_all,intersects_xy
from shapely.affinity import rotate,translate
root=Path(__file__).resolve().parent.parent
ground='--ground' in sys.argv
outfile=root/'routing'/('C4_GROUND_REPAIRS.json' if ground else 'C4_LED_ROUTES.json')
d=json.loads((root/'routing/c3_geometry.json').read_text());pads={p['key']:p for p in d['pads']}
source=(root/'pcb/c2_local_route.py').read_text().replace('end_layers=(0,1)):', 'end_layers=(0,1),start_layers=(0,1)):').replace('starts=links(start,(0,1))','starts=links(start,start_layers)')
tree=ast.parse(source)
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<local route functions>','exec'))
shapes=[(p['net'],padshape(p),p) for p in d['pads']]
inside=box(4,4,76,111).buffer(4,quad_segs=24).buffer(-.505)
outside=union_all([box(-5,-5,85,120).difference(inside),*[Point(x,y).buffer(2.7) for x,y in [(4,4),(76,60),(4,111),(76,111)]]])
step=.2;xs=np.arange(0,80.00001,step);ys=np.arange(0,115.00001,step)
xx,yy=np.meshgrid(xs,ys);ny,nx=xx.shape;repairs=[]
for detour in ([] if ground else json.loads((root/'routing/C4_CLEARANCE_DETOURS.json').read_text())['detours']):
    a=detour['terminals'][0];w=detour['width']
    for z in detour['terminals'][1:]:
        route(a['xy'],z['xy'],detour['net'],w,1 if w>=.8 else .6,.5 if w>=.8 else .3,end_layers=z['layers'],start_layers=a['layers'])
        outfile.write_text(json.dumps(repairs,indent=2)+'\n')
pairs=[('SW7:C','SW7:D',.6),('SW9:D','SW9:C',.6),('C4:2','C6:2',.6)] if ground else [('D3:2','MOD1:5V',.8),('U4:5','D3:1',.25),('U4:6','D3:4',.25),('U4:7','D3:3',.25)]
for a,z,w in pairs:
    assert pads[a]['net']==pads[z]['net'],(a,z)
    route(pads[a]['xy'],pads[z]['xy'],pads[a]['net'],w,1 if w>=.8 else .6,.5 if w>=.8 else .3)
    outfile.write_text(json.dumps(repairs,indent=2)+'\n')
print('Completed',len(repairs),'routes.')
