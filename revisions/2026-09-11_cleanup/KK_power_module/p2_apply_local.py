"""Import the locally planned connections, preserving a recoverable snapshot."""
from pathlib import Path
import json,shutil,hashlib,pcbnew as k
out=Path(__file__).resolve().parent/'P2_compact';path=out/'KK_power_module.kicad_pcb'
sm=k.SETTINGS_MANAGER();pro=str(out/'KK_power_module.kicad_pro');assert sm.LoadProject(pro)
b=k.LoadBoard(str(path));b.SetProject(sm.GetProject(pro));b.SynchronizeNetsAndNetClasses(False)
plan=json.loads((out/'LOCAL_ROUTES.json').read_text())
assert not any(r.get('critical') for r in plan['failed']),'Load-carrying connection failed'
assert len(list(b.GetTracks()))<350,'Refusing to import twice or over a changed routed board'
shutil.copy2(path,out/'P2_manual_before_local.kicad_pcb')
def V(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
for route in plan['routes']:
    net=b.FindNet(route['net']);assert net and net.GetNetCode()>0,route['net']
    critical=not route['tag'].startswith('branch')
    for a,z in zip(route['path'],route['path'][1:]):
        if a==z:continue
        if a[0]==z[0]:
            t=k.PCB_TRACK(b);t.SetStart(V(*a[1:]));t.SetEnd(V(*z[1:]));t.SetWidth(k.FromMM(route['width']));t.SetLayer(k.F_Cu if a[0]==0 else k.B_Cu)
        else:
            t=k.PCB_VIA(b);t.SetPosition(V(*a[1:]));t.SetWidth(k.FromMM(route['via_diameter']));t.SetDrill(k.FromMM(route['via_drill']));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu)
        t.SetNet(net);t.SetLocked(critical);b.Add(t)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(path),b)
(out/'local_import.json').write_text(json.dumps({'plan_sha256':hashlib.sha256((out/'LOCAL_ROUTES.json').read_bytes()).hexdigest(),'routes':len(plan['routes']),'failed':plan['failed'],'status':'IMPORTED; NATIVE DRC REQUIRED'},indent=2)+'\n')
print('Imported',len(plan['routes']),'connections; native DRC required.')
