"""Find copper intersecting the new LED pads and preserve boundary connectivity."""
from pathlib import Path
from shapely import Point,LineString,union_all
import json
root=Path(__file__).resolve().parent.parent;d=json.loads((root/'routing/c3_geometry.json').read_text())
newpads=[p for p in d['pads'] if p['key'].startswith('D3:')]
blocked=union_all([Point(p['xy']).buffer(max(p['size'])/2+.205) for p in newpads])
removed=[t for t in d['tracks'] if LineString([t['a'],t['b']]).buffer(t['width']/2).intersects(blocked)]
removed_ids={t['uuid'] for t in removed};remaining=[t for t in d['tracks'] if t['uuid'] not in removed_ids]
detours=[]
def key(p):return tuple(round(x,6) for x in p)
for net in sorted({t['net'] for t in removed}):
    ts=[t for t in removed if t['net']==net];todo=list(ts)
    while todo:
        group=[todo.pop()];nodes={key(group[0]['a']),key(group[0]['b'])}
        changed=True
        while changed:
            changed=False
            for t in todo[:]:
                if key(t['a']) in nodes or key(t['b']) in nodes:todo.remove(t);group.append(t);nodes.update([key(t['a']),key(t['b'])]);changed=True
        boundary=[]
        for p in sorted(nodes):
            layers=set()
            for t in remaining:
                if t['net']==net and Point(p).distance(LineString([t['a'],t['b']]))<1e-5:layers.add(t['layer'])
            if any(q['net']==net and Point(p).distance(Point(q['xy']))<1e-5 for q in d['pads']):layers.update([0,1])
            if any(q['net']==net and Point(p).distance(Point(q['xy']))<1e-5 for q in d['vias']):layers.update([0,1])
            if layers:boundary.append({'xy':list(p),'layers':sorted(layers)})
        assert len(boundary)>=2,(net,boundary)
        detours.append({'net':net,'width':max(t['width'] for t in group),'terminals':boundary})
report={'removed':removed,'detours':detours}
(root/'routing/C4_CLEARANCE_DETOURS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'removed_segments':len(removed),'detours':detours},indent=2))
