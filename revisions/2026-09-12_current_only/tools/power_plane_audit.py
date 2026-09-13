"""Independent filled-plane connectivity and safe stitching candidates.
Includes all four copper layers. Native DRC remains authoritative.
"""
from pathlib import Path
import json,math,sys
import numpy as np
from shapely import Point,LineString,Polygon,box,union_all,intersects_xy
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_power_module/work/P2_review'
source=(ROOT/'revisions/2026-09-11_cleanup/KK_power_module/p2_local_route.py').read_text().split('planned=[];failed=[]')[0]
source=source.replace("OUT=Path(__file__).resolve().parent/'P2_compact'",'OUT=ROOT/"KK_power_module/work/P2_review"')
exec(compile(source,__file__,'exec'),globals())
layers=['F.Cu','In1.Cu','In2.Cu','B.Cu']
report={};stitches=[]
for net,rootpad in [('/GND','J3:2'),('/SYS_SW','U4:5')]:
    rows=[[] for _ in layers];ports=[];raw=[];holes=[]
    for p,g in shapes:
        ls=[i for i,l in enumerate(layers) if l in p['layers']]
        if p['net']==net:
            for i in ls:rows[i].append(g.buffer(.000002))
            if ls:ports.append((p['xy'],ls,p['key']))
        elif ls:raw.append(g)
        if max(p['drill']):holes.append(Point(p['xy']).buffer(max(p['drill'])/2))
    for t in d['tracks']:
        g=LineString([t['a'],t['b']]).buffer(t['width']/2+.000002)
        if t['net']==net:
            # Screen the load-bearing supply path independently of long, thin
            # signal-router repairs. Short original pad escapes remain included.
            if '--power-width-check' in sys.argv and net=='/SYS_SW' and t['width']<.6 and not (t['locked'] and math.dist(t['a'],t['b'])<=2):continue
            rows[layers.index(t['layer'])].append(g)
        else:raw.append(g)
    for v in d['vias']:
        g=Point(v['xy']).buffer(v['diameter']/2+.000002)
        if v['net']==net:
            for row in rows:row.append(g)
            ports.append((v['xy'],list(range(4)),'via '+v['uuid']))
        else:raw.append(g)
        holes.append(Point(v['xy']).buffer(v['drill']/2))
    for z in d['zones']:
        if z['net']==net:rows[layers.index(z['layer'])].append(Polygon(z['outline'],z['holes']).buffer(.000002))
    groups=[];parent=[]
    for la,row in enumerate(rows):
        merged=union_all(row)
        for g in getattr(merged,'geoms',[merged]):
            if not g.is_empty:groups.append((la,g));parent.append(len(parent))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def member(p,ls):return [i for i,(la,g) in enumerate(groups) if la in ls and g.distance(Point(p))<.00001]
    for p,ls,key in ports:
        ids=member(p,ls)
        for i in ids[1:]:parent[root(i)]=root(ids[0])
    rootport=next(p for p in ports if p[2]==rootpad);mainroot=root(member(rootport[0],rootport[1])[0])
    components={}
    for i,(la,g) in enumerate(groups):components.setdefault(root(i),[]).append((la,g))
    records=[]
    obs=union_all([union_all(raw).buffer(.25+.155),union_all(holes).buffer(.1+.255),box(-3,-3,53,53).difference(inside.buffer(-.655))])
    xs=np.arange(.8,49.2,.1);xx,yy=np.meshgrid(xs,xs);valid=~intersects_xy(obs,xx,yy)
    main_copper=union_all([g for la,g in components[mainroot]])
    for comp,polys in components.items():
        names=[key for p,ls,key in ports if not key.startswith('via ') and any(root(i)==comp for i in member(p,ls))]
        entry={'main':comp==mainroot,'pads':names,'layers':sorted(set(layers[la] for la,g in polys)),'area_sum_mm2':sum(g.area for la,g in polys),'bounds':list(union_all([g for la,g in polys]).bounds)}
        records.append(entry)
        if comp==mainroot:continue
        floating=union_all([g for la,g in polys])
        viable=valid&intersects_xy(floating,xx,yy)&intersects_xy(main_copper,xx,yy)
        iy,ix=np.where(viable)
        if len(ix):
            c=floating.centroid;j=np.argmin((xx[iy,ix]-c.x)**2+(yy[iy,ix]-c.y)**2);pt=[float(xx[iy[j],ix[j]]),float(yy[iy[j],ix[j]])]
            stitches.append(dict(net=net,width=.2,via_diameter=.5,via_drill=.2,path=[[0,*pt],[1,*pt]],tag='plane stitch'))
            valid &= ~intersects_xy(Point(pt).buffer(.455),xx,yy)
            entry['stitch']=pt
        else:entry['stitch']=None
    report[net]=records
suffix='_POWER_WIDTH' if '--power-width-check' in sys.argv else ''
(OUT/('PLANE_AUDIT'+suffix+'.json')).write_text(json.dumps(report,indent=2)+'\n')
if not suffix:(OUT/'GROUND_STITCHES.json').write_text(json.dumps({'routes':stitches,'failed':[]},indent=2)+'\n')
print(json.dumps(report,indent=2));print('Proposed stitching vias:',len(stitches))
