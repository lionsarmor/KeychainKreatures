"""Bounded KiCad edits on the disposable P.2 review candidate only."""
from pathlib import Path
import sys,json,shutil,pcbnew as k
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'KK_power_module/work/P2_review'
PATH=OUT/'KK_power_module.kicad_pcb'
sm=k.SETTINGS_MANAGER();pro=str(OUT/'KK_power_module.kicad_pro');assert sm.LoadProject(pro)
b=k.LoadBoard(str(PATH));b.SetProject(sm.GetProject(pro));b.SynchronizeNetsAndNetClasses(False)
def V(pt):return k.VECTOR2I(k.FromMM(pt[0]),k.FromMM(pt[1]))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
command=sys.argv[1]
if command=='fill':
    for z in b.Zones():
        if not z.GetIsRuleArea():z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
    b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(PATH),b)
    print('Refilled candidate pours; isolated copper islands removed.')
elif command=='import-archived-plan':
    assert len(list(b.GetTracks()))<350,'Candidate already routed; refusing duplicate import'
    plan=json.loads((ROOT/'revisions/2026-09-11_cleanup/KK_power_module/P2_compact/LOCAL_ROUTES.json').read_text())
    assert not any(r.get('critical') for r in plan['failed'])
    route_items=[]
    for route in plan['routes']:
        net=b.FindNet(route['net']);assert net and net.GetNetCode()>0
        ids=[]
        for a,z in zip(route['path'],route['path'][1:]):
            if a==z:continue
            if a[0]==z[0]:
                t=k.PCB_TRACK(b);t.SetStart(V(a[1:]));t.SetEnd(V(z[1:]));t.SetWidth(k.FromMM(route['width']));t.SetLayer([k.F_Cu,k.B_Cu][a[0]])
            else:
                t=k.PCB_VIA(b);t.SetPosition(V(a[1:]));t.SetWidth(k.FromMM(route['via_diameter']));t.SetDrill(k.FromMM(route['via_drill']));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu)
            t.SetNet(net);t.SetLocked(not route['tag'].startswith('branch'));b.Add(t);ids.append(t.m_Uuid.AsString())
        route_items.append(dict(tag=route['tag'],net=route['net'],uuids=ids))
    (OUT/'imported_plan_items.json').write_text(json.dumps(route_items,indent=2)+'\n')
    b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(PATH),b)
    print('Imported candidate only:',len(plan['routes']),'paths; native DRC is mandatory.')
elif command=='geometry':
    data={'pads':[],'tracks':[],'vias':[],'zones':[]};layers=list(b.GetEnabledLayers().CuStack())
    for f in b.GetFootprints():
        for p in f.Pads():
            data['pads'].append(dict(key=f.GetReference()+':'+p.GetNumber(),net=p.GetNetname(),xy=xy(p.GetPosition()),size=xy(p.GetSize()),shape=int(p.GetShape()),angle=p.GetOrientationDegrees(),radius=k.ToMM(p.GetRoundRectCornerRadius()),drill=xy(p.GetDrillSize()),layers=[b.GetLayerName(l) for l in layers if p.IsOnLayer(l)]))
    for t in b.GetTracks():
        if t.GetClass()=='PCB_VIA':data['vias'].append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),xy=xy(t.GetPosition()),diameter=k.ToMM(t.GetWidth(k.F_Cu)),drill=k.ToMM(t.GetDrillValue()),layers=[b.GetLayerName(l) for l in layers]))
        else:data['tracks'].append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),a=xy(t.GetStart()),b=xy(t.GetEnd()),width=k.ToMM(t.GetWidth()),layer=b.GetLayerName(t.GetLayer()),locked=t.IsLocked()))
    for z in b.Zones():
        if z.GetIsRuleArea():continue
        for layer in layers:
            if not z.IsOnLayer(layer):continue
            polys=z.GetFilledPolysList(layer)
            for i in range(polys.OutlineCount()):
                def coords(r):return [xy(r.CPoint(j)) for j in range(r.PointCount())]
                data['zones'].append(dict(net=z.GetNetname(),layer=b.GetLayerName(layer),outline=coords(polys.COutline(i)),holes=[coords(polys.CHole(i,j)) for j in range(polys.HoleCount(i))]))
    (OUT/'geometry.json').write_text(json.dumps(data,indent=2)+'\n');print(len(data['tracks']),'tracks',len(data['vias']),'vias',len(data['zones']),'filled zone polygons')
elif command=='remove-bad-routes':
    report=json.loads((OUT/'review_drc.json').read_text())
    short_ids={i['uuid'] for v in report['violations'] if v['type']=='shorting_items' for i in v['items']}
    routes=json.loads((OUT/'imported_plan_items.json').read_text())
    bad=[r for r in routes if set(r['uuids'])&short_ids]
    assert all(r['tag'].startswith('branch') for r in bad),'Never remove a critical rail automatically'
    remove={i for r in bad for i in r['uuids']}
    remove|={i['uuid'] for v in report['violations'] if v['type']=='via_dangling' for i in v['items']}
    removed=[]
    for t in list(b.GetTracks()):
        if t.m_Uuid.AsString() in remove:removed.append(t.m_Uuid.AsString());b.Remove(t)
    (OUT/'rejected_routes.json').write_text(json.dumps(bad,indent=2)+'\n')
    k.SaveBoard(str(PATH),b);print('Rejected',len(bad),'shorted signal routes;',len(removed),'candidate copper items removed.')
elif command=='remove':
    ids=set(sys.argv[2:]);found=[]
    for t in list(b.GetTracks()):
        if t.m_Uuid.AsString() in ids:found.append(t.m_Uuid.AsString());b.Remove(t)
    assert set(found)==ids,(found,ids)
    k.SaveBoard(str(PATH),b);print('Removed from candidate:',len(found),'copper items; original P.2 preserved.')
elif command=='unblock':
    selected=json.loads((OUT/'unblock.json').read_text())['routes']
    ids={i for r in selected for i in r['uuids']};n=0
    for t in list(b.GetTracks()):
        if t.m_Uuid.AsString() in ids:
            assert not t.IsLocked(),'Do not rip up critical power routes'
            b.Remove(t);n+=1
    k.SaveBoard(str(PATH),b);print('Removed',n,'signal copper items to unblock IC escapes.')
elif command=='rip-nets':
    nets=set(sys.argv[2:]);n=0
    for t in list(b.GetTracks()):
        if t.GetNetname() in nets and not t.IsLocked():b.Remove(t);n+=1
    k.SaveBoard(str(PATH),b);print('Removed',n,'noncritical signal items on selected nets.')
elif command=='move-debug':
    fps={f.GetReference():f for f in b.GetFootprints()}
    for ref,point in [('TP19',(22,41)),('TP18',(29,47)),('TP10',(44,40))]:
        fps[ref].SetPosition(V(point))
    k.SaveBoard(str(PATH),b);print('Moved NTC/actuator debug pads near their connectors, clear of IC ground escapes.')
elif command in ['apply','stitch','fanout','bridge']:
    plan=json.loads((OUT/({'bridge':'POWER_BRIDGE.json','stitch':'GROUND_STITCHES.json','fanout':'FANOUT_ROUTES.json'}.get(command,'REPAIR_ROUTES.json'))).read_text())
    for route in plan['routes']:
        if route['net'] in sys.argv[2:]:continue
        net=b.FindNet(route['net']);assert net and net.GetNetCode()>0
        for a,z in zip(route['path'],route['path'][1:]):
            if a==z:continue
            if a[0]==z[0]:
                t=k.PCB_TRACK(b);t.SetStart(V(a[1:]));t.SetEnd(V(z[1:]));t.SetWidth(k.FromMM(route['width']));t.SetLayer([k.F_Cu,k.B_Cu,k.In2_Cu,k.In1_Cu][a[0]])
            else:
                t=k.PCB_VIA(b);t.SetPosition(V(a[1:]));t.SetWidth(k.FromMM(route['via_diameter']));t.SetDrill(k.FromMM(route['via_drill']));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu)
            t.SetNet(net);t.SetLocked(command=='bridge');b.Add(t)
    b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(PATH),b);print('Applied',len(plan['routes']),'candidate repair paths; DRC required.')
else:raise SystemExit('Unknown command')
