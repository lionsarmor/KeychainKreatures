"""Add local routes to approved RGB extension without ripping up old copper."""
from pathlib import Path
import json,math,heapq,itertools,ast
import numpy as np
from shapely import Point,LineString,box,union_all,intersects_xy
from shapely.affinity import rotate,translate
root=Path(__file__).resolve().parent.parent
d=json.loads((root/'routing/c3_geometry.json').read_text());pads={p['key']:p for p in d['pads']}
tree=ast.parse((root/'pcb/c2_local_route.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<local route functions>','exec'))
shapes=[(p['net'],padshape(p),p) for p in d['pads']]
inside=box(4,4,76,111).buffer(4,quad_segs=24).buffer(-.505)
outside=union_all([box(-5,-5,85,120).difference(inside),*[Point(x,y).buffer(2.7) for x,y in [(4,4),(76,60),(4,111),(76,111)]]])
step=.2;xs=np.arange(0,80.00001,step);ys=np.arange(0,115.00001,step)
xx,yy=np.meshgrid(xs,ys);ny,nx=xx.shape;repairs=[]
pairs=[('U4:16','C27:1',.8),('U4:15','R40:1',.25),('U4:13','R41:2',.25),('U4:16','R41:1',.8),('U4:5','D3:1',.25),('U4:6','D3:4',.25),('U4:7','D3:3',.25),('D3:2','C1:1',.8),('C27:1','R5:1',.8),('U1:25','U4:2',.25),('U1:26','U4:3',.25),('U1:27','U4:4',.25),('U1:28','U4:13',.25)]
pairs.extend([('R42:1','U4:2',.25),('R43:1','U4:3',.25)])
for a,z,w in pairs:
    assert pads[a]['net']==pads[z]['net'],(a,z)
    route(pads[a]['xy'],pads[z]['xy'],pads[a]['net'],w,1 if w>=.8 else .6,.5 if w>=.8 else .3)
    (root/'routing/C3_RGB_ROUTES.json').write_text(json.dumps(repairs,indent=2)+'\n')
print('Completed',len(repairs),'routes; GND connected through pours.')
