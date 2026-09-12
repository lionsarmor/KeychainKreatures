"""Apply recorded local repairs, and keep starved pads trace-fed for easy soldering."""
from pathlib import Path
import pcbnew as k,json,math,sys
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_main_module/C6_flat_stack'
p=ROOT/'KK_main_module/pcb/c2_apply_local_route.py'
s=p.read_text().replace('root=Path(__file__).resolve().parent.parent','root=OUT')
s=s.replace("root/'routing/KK_main_module_C2_candidate.kicad_pcb'","root/'KK_main_module.kicad_pcb'")
s=s.replace("root/'routing/C2_LOCAL_REPAIRS.json'","root/'reports/LOCAL_REPAIRS.json'")
if '--thermals-only' in sys.argv:
    b=k.LoadBoard(str(OUT/'KK_main_module.kicad_pcb'))
else:
    assert not (OUT/'reports/trace_fed_ground_pads.json').exists(),'Repairs already applied; use --thermals-only'
    exec(compile(s,str(p),'exec'))
# Do not suppress the DRC category or globally remove thermal reliefs. These
# four pads already have explicit routed ground, so omit only their pour join.
fps={f.GetReference():f for f in b.GetFootprints()};audit=[]
for ref,pin in [('SW7','C'),('C18','2'),('C12','2'),('R34','2'),('SW8','C')]:
    pad=next(p for p in fps[ref].Pads() if p.GetNumber()==pin);assert pad.GetNetname()=='/GND'
    t=[t for t in b.GetTracks() if t.GetNetname()=='/GND' and t.GetClass()!='PCB_VIA' and min(math.dist((t.GetStart().x,t.GetStart().y),(pad.GetPosition().x,pad.GetPosition().y)),math.dist((t.GetEnd().x,t.GetEnd().y),(pad.GetPosition().x,pad.GetPosition().y)))<k.FromMM(.001)]
    assert t,'Ground pad lacks explicit route: '+ref+':'+pin
    pad.SetLocalZoneConnection(k.ZONE_CONNECTION_NONE)
    audit.append({'pad':ref+':'+pin,'explicit_ground_tracks':len(t),'reason':'Trace-fed pad; omit ineffective local pour thermal only; no DRC suppression.'})
for f in fps.values():
    if not f.GetReference().startswith('TP'):continue
    for pad in f.Pads():
        if pad.GetNetname()=='/GND':
            pad.SetLocalZoneConnection(k.ZONE_CONNECTION_FULL)
            audit.append({'pad':f.GetReference()+':'+pad.GetNumber(),'reason':'Bare ground probe pad, no fitted component: solid ground-plane connection rather than thermal spokes.'})
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(OUT/'KK_main_module.kicad_pcb'),b)
(OUT/'reports/trace_fed_ground_pads.json').write_text(json.dumps(audit,indent=2)+'\n')
print('Ground joins updated:',len(audit),'pads; no global DRC relaxation.')
