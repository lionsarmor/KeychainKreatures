"""Join isolated front-ground components to the intact inner ground plane.
Plan only, using real copper/holes on every layer; native DRC required.
"""
from pathlib import Path
import json
import numpy as np
from shapely import Point,LineString,Polygon,box,union_all,intersects_xy
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_power_module/work/P2_review'
source=(ROOT/'revisions/2026-09-11_cleanup/KK_power_module/p2_local_route.py').read_text().split('planned=[];failed=[]')[0]
source=source.replace("OUT=Path(__file__).resolve().parent/'P2_compact'",'OUT=ROOT/"KK_power_module/work/P2_review"')
exec(compile(source,__file__,'exec'),globals())
ground='/GND';raw=[];holes=[];front=[];inner=[];anchors=[]
for p,g in shapes:
    if p['net']!=ground:raw.append(g)
    elif 'F.Cu' in p['layers']:
        front.append(g)
        if max(p['drill']):anchors.append(g)
    if max(p['drill']):holes.append(Point(p['xy']).buffer(max(p['drill'])/2))
for t in d['tracks']:
    g=LineString([t['a'],t['b']]).buffer(t['width']/2)
    if t['net']!=ground:raw.append(g)
    elif t['layer']=='F.Cu':front.append(g)
for v in d['vias']:
    g=Point(v['xy']).buffer(v['diameter']/2)
    if v['net']!=ground:raw.append(g)
    else:front.append(g);anchors.append(g)
    holes.append(Point(v['xy']).buffer(v['drill']/2))
for z in d['zones']:
    if z['net']!=ground:continue
    g=Polygon(z['outline'],z['holes']).buffer(0)
    if z['layer']=='F.Cu':front.append(g)
    if z['layer']=='In1.Cu':inner.append(g)
obs=union_all([union_all(raw).buffer(.155+.25),union_all(holes).buffer(.1+.255),box(-3,-3,53,53).difference(inside.buffer(-.655))])
inner=union_all(inner);anchors=union_all(anchors);front=union_all(front)
xs=np.arange(.8,49.2,.1);xx,yy=np.meshgrid(xs,xs)
valid=~intersects_xy(obs,xx,yy)&intersects_xy(inner,xx,yy)
routes=[];failed=[]
for g in getattr(front,'geoms',[front]):
    if anchors.intersects(g):continue
    viable=valid&intersects_xy(g,xx,yy)
    iy,ix=np.where(viable)
    if not len(ix):failed.append({'bounds':list(g.bounds),'reason':'No legal ground stitch in this component'});continue
    c=g.centroid;idx=np.argmin((xx[iy,ix]-c.x)**2+(yy[iy,ix]-c.y)**2)
    pt=[float(xx[iy[idx],ix[idx]]),float(yy[iy[idx],ix[idx]])]
    routes.append(dict(net=ground,width=.2,via_diameter=.5,via_drill=.2,path=[[0,*pt],[1,*pt]],tag='ground stitch'))
    valid &= ~intersects_xy(Point(pt).buffer(.455),xx,yy)
(OUT/'GROUND_STITCHES.json').write_text(json.dumps({'routes':routes,'failed':failed},indent=2)+'\n')
print('Ground stitch candidates:',len(routes),'unresolved components:',failed)
