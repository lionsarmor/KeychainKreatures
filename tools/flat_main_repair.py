"""Two bounded C6 repairs using current exported geometry; host Python."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_main_module/C6_flat_stack'
p=ROOT/'KK_main_module/pcb/c2_local_route.py'
s=p.read_text().split('# Final all-net')[0]
s=s.replace('root=Path(__file__).resolve().parent.parent',"root=OUT")
s=s.replace("root/'routing/c2_geometry.json'","root/'reports/copper.json'")
s=s.replace('box(4,4,76,96)','box(4,4,92,101)').replace('box(-5,-5,85,105)','box(-5,-5,101,110)')
s=s.replace('np.arange(0,80.00001,step)','np.arange(0,96.00001,step)').replace('np.arange(0,100.00001,step)','np.arange(0,105.00001,step)')
s=s.replace('box(51,0,80,7),box(59.5,7,72.5,15.5)','box(33,0,63,5.25),box(41.5,5.25,54.5,14.5)')
s=s.replace('step=.2;','step=.1;')
s=s.replace('if abs(x-y)<1e-8:g=Point(0,0).buffer(r,quad_segs=24)','if abs(x-y)<1e-8 and abs(x-2*r)<1e-8:g=Point(0,0).buffer(r,quad_segs=24)')
exec(compile(s,str(p),'exec'))
for a,z in [('R24:2','D1:2'),('Q3:1','R23:1')]:
    assert pads[a]['net']==pads[z]['net']
    route(pads[a]['xy'],pads[z]['xy'],pads[a]['net'],.5,.8,.4)
(OUT/'reports/LOCAL_REPAIRS.json').write_text(json.dumps(repairs,indent=2)+'\n')
