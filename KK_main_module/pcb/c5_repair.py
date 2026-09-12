"""Route the exact native-DRC opens with current geometry, not assumed connectivity."""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
s=(root/'pcb/c2_local_route.py').read_text().split('# Final all-net')[0]
s=s.replace("root/'routing/c2_geometry.json'","root/'C5_relayout/copper.json'")
s=s.replace('box(4,4,76,96)','box(4,4,80,91)').replace('box(-5,-5,85,105)','box(-5,-5,89,100)').replace('np.arange(0,80.00001,step)','np.arange(0,84.00001,step)').replace('np.arange(0,100.00001,step)','np.arange(0,95.00001,step)')
s=s.replace('box(51,0,80,7),box(59.5,7,72.5,15.5)','box(27,0,57,5.25),box(35.5,5.25,48.5,14.5)')
s=s.replace('step=.2;','step=.1;')
s=s.replace('if abs(x-y)<1e-8:g=Point(0,0).buffer(r,quad_segs=24)','if abs(x-y)<1e-8 and abs(x-2*r)<1e-8:g=Point(0,0).buffer(r,quad_segs=24)')
exec(compile(s,str(root/'pcb/c2_local_route.py'),'exec'))
pads['Q3_STUB']={'net':'Net-(Q3-C)','xy':[30.1656,17.3639]}
for a,z,w,vd,dh in [('R23:1','Q3_STUB',.5,.8,.4),('J5:2','U3:3',.5,.8,.4),('MOD1:11','J3:3',.25,.6,.3),('TP9:1','MOD1:4',.25,.6,.3),('TP32:1','U2:3',.25,.6,.3)]:
 assert pads[a]['net']==pads[z]['net']
 route(pads[a]['xy'],pads[z]['xy'],pads[a]['net'],w,vd,dh)
(root/'C5_relayout/REPAIRS.json').write_text(json.dumps(repairs,indent=2)+'\n')
