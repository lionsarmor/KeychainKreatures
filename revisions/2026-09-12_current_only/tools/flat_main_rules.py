"""Restore explicit C6 width classes from actual component pin nets, not stale names."""
from pathlib import Path
import json, shutil
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_main_module/C6_flat_stack'
p=OUT/'KK_main_module.kicad_pro';pro=json.loads(p.read_text());g=json.loads((OUT/'geometry.json').read_text())
base=next(c for c in pro['net_settings']['classes'] if c['name']=='Default')
spec=[('Default',.25,.6,.3),('Power',.8,1,.5),('Motor',.8,1,.5),('Speaker',.5,.8,.4),('Audio',.3,.6,.3),('Ground',.6,1,.5),('AuxLoad',.5,.8,.4)]
classes=[{**base,'name':name,'track_width':w,'via_diameter':d,'via_drill':h,'clearance':.2,'priority':2147483647 if name=='Default' else i} for i,(name,w,d,h) in enumerate(spec)]
assigned={}
def assign(c,keys):
    for key in keys:
        ref,pin=key.split(':');net=next(p['net'] for p in g[ref]['variants']['0']['pads'] if p['pin']==pin)
        assert net and not net.startswith('unconnected');assigned[net]=c
assign('Audio',['R30:2','R31:2','C20:2','U3:7','U3:8','U3:5','R34:1','R35:1'])
assign('Speaker',['J5:1','J5:2'])
assign('AuxLoad',['D1:1','D1:2','Q3:1','J2:8'])
assign('Power',['J1:1','J1:3','J1:4','U3:2'])
assign('Motor',['J4:2']);assign('Ground',['J1:2'])
pro['net_settings']['classes']=classes
pro['net_settings']['netclass_assignments']=None
pro['net_settings']['netclass_patterns']=[{'pattern':net,'netclass':cls} for net,cls in assigned.items()]
pro['board']['design_settings']['track_widths']=[.25,.3,.5,.6,.8,1]
pro['board']['design_settings']['via_dimensions']=[{'diameter':d,'drill':h} for d,h in [(.6,.3),(.8,.4),(1,.5)]]
p.write_text(json.dumps(pro,indent=2)+'\n')
(OUT/'reports/ROUTING_RULES.json').write_text(json.dumps({'classes':spec,'assignments':assigned,'note':'Saved source had only Default class; restored from documented C2/C5 functional pin assignments using current native pad nets.'},indent=2)+'\n')
first=OUT/'C6_first_route_NOT_RELEASED.kicad_pcb'
assert not first.exists(),'Reroute already staged; do not overwrite'
shutil.copy2(OUT/'KK_main_module.kicad_pcb',first)
shutil.copy2(OUT/'C6_unrouted.kicad_pcb',OUT/'KK_main_module.kicad_pcb')
shutil.copy2(OUT/'C6_route.ses',OUT/'C6_first_route_NOT_RELEASED.ses')
print('Explicit width classes restored; first route preserved; fresh route required.')
