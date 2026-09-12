"""Explicit pin escapes, checked against copper on all four layers.
This is a candidate planner, not a substitute for native DRC.
"""
from pathlib import Path
import json,math,sys
from shapely import Point,LineString,union_all
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_power_module/work/P2_review'
source=(ROOT/'revisions/2026-09-11_cleanup/KK_power_module/p2_local_route.py').read_text().split('planned=[];failed=[]')[0]
source=source.replace("OUT=Path(__file__).resolve().parent/'P2_compact'",'OUT=ROOT/"KK_power_module/work/P2_review"')
exec(compile(source,__file__,'exec'),globals())
plans=[];failed=[];obstacle_cache={};union_cache={}
def attempt(key,pts,via=True,width=.15):
    if sys.argv[1:] and key not in sys.argv[1:]:return False
    p=pads[key];net=p['net'];pts=[p['xy'],*pts];blocking=[]
    stamp=(len(d['tracks']),len(d['vias']))
    if stamp not in obstacle_cache:
        tracks=[(t['net'],LineString([t['a'],t['b']]).buffer(t['width']/2),[t['layer']]) for t in d['tracks']]
        tracks += [(v['net'],Point(v['xy']).buffer(v['diameter']/2),['F.Cu','In1.Cu','In2.Cu','B.Cu']) for v in d['vias']]
        obstacle_cache[stamp]=[(q['net'],g,q['layers']) for q,g in shapes if q['layers']]+tracks
    obs=obstacle_cache[stamp]
    cachekey=stamp+(net,)
    if cachekey not in union_cache:
        union_cache[cachekey]=(union_all([g for name,g,ls in obs if name!=net and 'F.Cu' in ls]),union_all([g for name,g,ls in obs if name!=net]),union_all([Point(q['xy']).buffer(max(q['drill'])/2+.355) for q in d['pads'] if max(q['drill'])]+[Point(q['xy']).buffer(q['drill']/2+.355) for q in d['vias']]))
    front,allcopper,holearea=union_cache[cachekey]
    trace=LineString(pts).buffer(width/2+.151)
    if trace.intersects(front):blocking.append(('track','foreign front copper'))
    if via:
        disk=Point(pts[-1]).buffer(.25+.151)
        if disk.intersects(allcopper):blocking.append(('via','foreign copper'))
        if holearea.intersects(Point(pts[-1])):blocking.append(('hole','existing drill'))
    if blocking:
        failed.append({'pin':key,'points':pts,'blocking':sorted(set(blocking))});return False
    route=dict(net=net,width=width,via_diameter=.5,via_drill=.2,path=[[0,*pt] for pt in pts]+([[1,*pts[-1]]] if via else []),tag='explicit '+key)
    plans.append(route)
    for a,z in zip(pts,pts[1:]):d['tracks'].append(dict(net=net,a=a,b=z,width=width,layer='F.Cu'))
    if via:d['vias'].append(dict(net=net,xy=pts[-1],diameter=.5,drill=.2))
    return True
attempt('U7:3',[pads['U7:4']['xy']],False,.2)
attempt('U5:3',[pads['U5:4']['xy']],False,.2)
attempt('U6:3',[pads['U6:4']['xy']],False,.2)
attempt('U4:2',[[34.4,10.75],[34.4,9.5],[35.0,9.5]])
attempt('U1:1',[[25.95,6.25],[25.95,5.7],[24.8,5.7],[24.8,6.1],[24.45,6.6]])
attempt('U12:8',[[41,33.6],[40.75,34.0]])
attempt('U12:9',[[41.5,33.8]])
attempt('U12:10',[[42,33.6],[42.25,34.0]])
attempt('C72:2',[[21.6,9.75]])
attempt('U9:2',[[27.0,33.0]])
attempt('U11:3',[[40.8,36.95]])
attempt('U1:16',[[27.25,4.8],[26.8,4.8]])
attempt('C8:1',[[38.75,12.0],[38.2,13.0]],False,.6)
if 'R66:2' in sys.argv:
    p=pads['R66:2']['xy'];found=False
    candidates=sorted([[round(p[0]+i*.1,3),round(p[1]+j*.1,3)] for i in range(-22,23) for j in range(-22,23)],key=lambda q:math.dist(p,q))
    for q in candidates:
        if math.dist(p,q)<.3:continue
        if attempt('R66:2',[q],True,.2):found=True;break
    if found:failed=[f for f in failed if f['pin']!='R66:2']
    else:failed=[f for f in failed if f['pin']!='R66:2']+[{'pin':'R66:2','blocking':'No short straight escape fits'}]
(OUT/'FANOUT_ROUTES.json').write_text(json.dumps({'routes':plans,'failed':failed},indent=2)+'\n')
print('Accepted fanouts:',[p['tag'] for p in plans]);print('Blocked:',json.dumps(failed,indent=2))
