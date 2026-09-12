"""Explicit current-carrying source paths. Remaining source-net branches are
sense/control/test connections; autorouter may use their lighter widths.
Requires filled/capped vias at the listed component-pad via arrays.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=(ROOT/'p2_critical.py').read_text().split("for i,ref in enumerate")[0]
s=s.replace("assert not list(b.GetTracks()),'Refusing to replace existing routing'", "assert len(list(b.GetTracks())) < 250, 'Refusing to overwrite an autorouted board'")
s=s.replace("shutil.copy2(PATH,OUT/'P2_unrouted.kicad_pcb')", "shutil.copy2(PATH,OUT/'P2_before_power_paths.kicad_pcb')")
exec(compile(s,str(ROOT/'p2_critical.py'),'exec'),globals())
for ref,point in {'TP4':(15.8,28.5),'TP5':(20,29),'TP25':(5,39),'TP26':(8,39),'TP27':(14,39),'TP28':(17,39)}.items():
    fps[ref].SetPosition(V(*point))
def array(key,dx=.3,dy=0,diam=.5,drill=.2):
    x,y=P(key)
    for sign in [-1,1]:via(key,[x+sign*dx,y+sign*dy],diam,drill)
    netpath(key,[[x-dx,y-dy],[x+dx,y+dy]],min(diam,.5))
for ref in ['Q1','Q2','Q3']:
    array(ref+':1');array(ref+':3')
    join(ref+':2',ref+':5',width=.5)
join('Q1:5','Q2:2',width=.5);join('Q2:5','Q3:2',width=.5)
join('Q1:1','Q2:1',width=1.5,layer=k.B_Cu)
join('Q2:1','Q3:1',width=1.5,layer=k.B_Cu)
join('J2:2','Q2:1',[[10.8,40.77],[10.8,34.55]],1.5,k.B_Cu)
# Four parallel plated vias at each fuse pad; filled/capped for assembly.
for key in ['F1:1','F1:2']:
    x,y=P(key)
    for dx in [-.3,.3]:
        for dy in [-.3,.3]:via(key,[x+dx,y+dy],.6,.3)
    for layer in [k.F_Cu,k.B_Cu,k.In2_Cu]:
        netpath(key,[[x-.3,y],[x+.3,y]],1.2,layer)
join('F1:1','J2:1',[[11.35,38],[12.48,39.13]],1.5,k.In2_Cu)
for key in ['U1:2','U1:3']:
    netpath(key,[P(key),[25.7,7]],.2)
for point in [[25.7,7],[25.45,6.25]]:via('U1:2',point,.5,.2)
netpath('U1:2',[[25.7,7],[25.45,6.75],[25.45,6.25]],.35)
netpath('F1:2',[P('F1:2'),[18,30.5],[18,10.6],[20.6,8],[25.7,8],[25.7,7]],1.5,k.B_Cu)
array('C4:1')
netpath('C4:1',[P('C4:1'),[24.5,8]],.8,k.B_Cu)
# Charger OUT to eFuse IN: short chip-pad necks, then a broad rear trunk.
for key in ['U1:10','U1:11']:netpath(key,[P(key),[30.2,7]],.2)
netpath('U1:10',[[30.2,7],[30.7,7.5],P('C5:1')],.6)
array('C5:1')
for key in ['U4:3','U4:4']:netpath(key,[P(key),[34.25,11.5]],.2)
for point in [[34.25,11.5],[34.6,12.2]]:via('U4:3',point,.5,.2)
netpath('U4:3',[[34.25,11.5],[34.6,12.2]],.5)
netpath('C5:1',[P('C5:1'),[34.25,10.7],[34.25,11.5]],1.5,k.B_Cu)
# USB power contacts and limiter feed: neither CC nor USB data carries power.
for key in ['J1:A4','J1:A9']:
    x,y=P(key);netpath(key,[[x,y],[x,8.2]],.4);via(key,[x,8.2],.6,.3)
netpath('J1:A4',[[9.6,8.2],[18.3,8.2],[22,4.5]],.8,k.B_Cu)
via('U13:B1',[22,3.7],.6,.3);netpath('U13:B1',[[22,4.5],[22,3.7]],.5)
via('U13:B2',[25.2,4.5],.6,.3);netpath('U13:B2',[[24.4,4.5],[25.2,4.5]],.5)
array('C3:1')
netpath('U1:13',[P('U1:13'),[28.75,4.85]],.2)
netpath('U1:13',[[28.75,4.85],[28.05,4.15],P('C3:1')],.45)
netpath('U13:B2',[[24.4,4.5],[25.2,4.5],P('C3:1')],.8,k.B_Cu)
array('D1:1',.5,0,.6,.3);array('D1:2',.5,0,.6,.3)
netpath('D1:1',[P('D1:1'),[6,13],[9.6,9.4],[9.6,8.2]],.8,k.B_Cu)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(PATH),b)
(OUT/'power_paths.json').write_text(json.dumps({'connections':audit,'note':'Filled/capped component-pad vias required; geometry still subject to native DRC.'},indent=2)+'\n')
print('Explicit source-current paths saved; native DRC required.')
