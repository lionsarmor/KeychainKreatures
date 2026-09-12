"""Single-process, time-bounded signal repairs. No native PCB edits.

Reuses the preserved planner definitions, fixes inner-copper via obstacles,
permits sparse In2 signal escapes, and never routes over the In1 ground plane.
Native refill/DRC and power-plane connectivity checks remain mandatory.
"""
from pathlib import Path
import sys,json,re,math,signal
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'KK_power_module/work/P2_review'
s=(ROOT/'revisions/2026-09-11_cleanup/KK_power_module/p2_local_route.py').read_text().split("for a,z in [('C24:1'")[0]
def change(a,z):
    global s
    assert a in s,a
    s=s.replace(a,z)
change("OUT=Path(__file__).resolve().parent/'P2_compact'",'OUT=ROOT/"KK_power_module/work/P2_review"')
change("layers=['F.Cu','B.Cu']","layers=['F.Cu','B.Cu','In2.Cu']")
change('raw=[[],[]]','raw=[[],[],[]]')
change('range(2)','range(3)')
change("candidates.append(((la,c,a),step*math.hypot(dx,dy)))","candidates.append(((la,c,a),step*math.hypot(dx,dy)*(1.25 if la==2 else 1)))")
change("if viavalid[y,x]:candidates.append(((1-la,y,x),3))","if viavalid[y,x]:\n            for other in range(3):\n                if other!=la:candidates.append(((other,y,x),5))")
change("OUT/'LOCAL_ROUTES.json'","OUT/'REPAIR_ROUTES.json'")
change('return math.dist((xs[n[2]],ys[n[1]]),end)','return 1.5*math.dist((xs[n[2]],ys[n[1]]),end)')
exec(compile(s,str(__file__),'exec'),globals())
def timeout(_sig,_frame):raise RuntimeError('Per-route CPU time limit (20 seconds)')
signal.signal(signal.SIGPROF,timeout)
def allowed(item):
    desc=item['description']
    if desc.startswith(('Via','PTH')) or 'on all copper layers' in desc:return [0,1,2]
    for i,name in enumerate(layers):
        if 'on '+name in desc:return [i]
    return []
report=json.loads((OUT/'review_drc.json').read_text())
todo=[q for q in report['unconnected_items'] if not any(i['description'].startswith('Zone') for i in q['items'])]
if any(i['description'].startswith('Zone') for q in report['unconnected_items'] for i in q['items']):
    for key in ['C72:2','U9:2','U11:3']:
        p=pads[key];v=min([v for v in d['vias'] if v['net']=='/GND'],key=lambda v:math.dist(p['xy'],v['xy']))
        todo.append({'items':[{'description':'Pad '+key+' [/GND] on F.Cu','pos':dict(zip(['x','y'],p['xy']))},{'description':'Via [/GND] on F.Cu - B.Cu','pos':dict(zip(['x','y'],v['xy']))}]})
priority=['/CC1','/CC2','/EF_UVLO','/SENSE_3V3','/NTC','/REG_ENABLE','/SYS_SW']
def rank(q):
    name=re.search(r'\[([^]]+)\]',q['items'][0]['description']).group(1)
    return (priority.index(name) if name in priority else len(priority),math.dist(list(q['items'][0]['pos'].values()),list(q['items'][1]['pos'].values())))
todo.sort(key=rank)
def anchors(pt,net,allowed_layers):
    # Start at a connected existing via/pad, not behind the IC pin again.
    # Existing via holes cannot legally receive a second new via; treating
    # them merely as obstacles would defeat deliberate pin fanout.
    shapes_by_layer=[[] for _ in layers];ports=[]
    for p,g in shapes:
        if p['net']!=net:continue
        ls=[i for i,name in enumerate(layers) if name in p['layers']]
        for i in ls:shapes_by_layer[i].append(g)
        if ls:ports.append((p['xy'],ls))
    for t in d['tracks']:
        if t['net']==net and t['layer'] in layers:shapes_by_layer[layers.index(t['layer'])].append(LineString([t['a'],t['b']]).buffer(t['width']/2+.000002))
    for v in d['vias']:
        if v['net']!=net:continue
        for row in shapes_by_layer:row.append(Point(v['xy']).buffer(v['diameter']/2+.000002))
        ports.append((v['xy'],list(range(len(layers)))))
    groups=[];parents=[]
    for la,row in enumerate(shapes_by_layer):
        g=union_all(row)
        for poly in getattr(g,'geoms',[g]):
            if not poly.is_empty:groups.append((la,poly));parents.append(len(parents))
    def root(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    def membership(p,ls):return [i for i,(la,g) in enumerate(groups) if la in ls and g.distance(Point(p))<.00001]
    for p,ls in ports:
        ids=membership(p,ls)
        for i in ids[1:]:parents[root(i)]=root(ids[0])
    ids=membership(pt,allowed_layers);roots={root(i) for i in ids}
    result=[(pt,allowed_layers)]
    for p,ls in ports:
        if any(root(i) in roots for i in membership(p,ls)):result.append((p,ls))
    return result
def position(item):
    m=re.search(r'pad (\S+) .*? of (\w+)',item['description'],re.I)
    if m and m.group(2)+':'+m.group(1) in pads:return pads[m.group(2)+':'+m.group(1)]['xy']
    return [item['pos']['x'],item['pos']['y']]
for idx,item in enumerate(todo):
    a,z=item['items'];net=re.search(r'\[([^]]+)\]',a['description']).group(1)
    sl,el=allowed(a),allowed(z)
    if not sl or not el:failed.append({'items':item,'reason':'Unsupported layer'});continue
    start=position(a);end=position(z)
    starts,ends=anchors(start,net,sl),anchors(end,net,el)
    starts=[p for p in starts if len(p[1])>1] or starts
    ends=[p for p in ends if len(p[1])>1] or ends
    pa,pz=min(((pa,pz) for pa in starts for pz in ends),key=lambda pp:math.dist(pp[0][0],pp[1][0]))
    start,sl=pa;end,el=pz
    if math.dist(start,end)<.00001:continue
    nt,nv=len(d['tracks']),len(d['vias'])
    try:
        signal.setitimer(signal.ITIMER_PROF,20)
        route(start,end,net,.15,sl,el,'repair '+str(idx),.5,.2)
    except RuntimeError as e:
        d['tracks'][nt:]=[];d['vias'][nv:]=[]
        failed.append({'items':item,'reason':str(e)});print('FAILED',net,e,flush=True)
    finally:signal.setitimer(signal.ITIMER_PROF,0)
(OUT/'REPAIR_ROUTES.json').write_text(json.dumps({'routes':planned,'failed':failed},indent=2)+'\n')
print('Candidate repairs:',len(planned),'failed:',len(failed),flush=True)
