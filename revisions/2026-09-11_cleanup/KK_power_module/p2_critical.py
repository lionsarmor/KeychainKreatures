"""Explicit short converter loops and ground/power planes before autorouting.

KiCad Python. No route is accepted solely because this script completes: native
DRC and the independent final net/path audit remain mandatory.
"""
from pathlib import Path
import json,shutil,pcbnew as k
OUT=Path(__file__).resolve().parent/'P2_compact';PATH=OUT/'KK_power_module.kicad_pcb'
sm=k.SETTINGS_MANAGER();pro=str(OUT/'KK_power_module.kicad_pro');assert sm.LoadProject(pro)
b=k.LoadBoard(str(PATH));b.SetProject(sm.GetProject(pro));b.SynchronizeNetsAndNetClasses(False)
assert not list(b.GetTracks()),'Refusing to replace existing routing'
shutil.copy2(PATH,OUT/'P2_unrouted.kicad_pcb')
fps={f.GetReference():f for f in b.GetFootprints()}
def V(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
def pad(key):
    ref,num=key.split(':');return next(p for p in fps[ref].Pads() if p.GetNumber()==num)
def P(key):return xy(pad(key).GetPosition())
audit=[]
def trace(net,points,width=.2,layer=k.F_Cu):
    for a,z in zip(points,points[1:]):
        if a==z:continue
        t=k.PCB_TRACK(b);t.SetStart(V(*a));t.SetEnd(V(*z));t.SetWidth(k.FromMM(width));t.SetLayer(layer);t.SetNet(net);t.SetLocked(True);b.Add(t)
def netpath(key,points,width=.2,layer=k.F_Cu):trace(pad(key).GetNet(),points,width,layer)
def join(a,z,middle=(),width=.2,layer=k.F_Cu):
    assert pad(a).GetNetCode()==pad(z).GetNetCode(),(a,z)
    netpath(a,[P(a),*middle,P(z)],width,layer);audit.append({'from':a,'to':z,'width_mm':width,'layer':b.GetLayerName(layer)})
def via(key,pt,diameter=.5,drill=.2):
    v=k.PCB_VIA(b);v.SetPosition(V(*pt));v.SetWidth(k.FromMM(diameter));v.SetDrill(k.FromMM(drill));v.SetViaType(k.VIATYPE_THROUGH);v.SetLayerPair(k.F_Cu,k.B_Cu);v.SetNet(pad(key).GetNet());v.SetLocked(True);b.Add(v)
for i,ref in enumerate(['U5','U6','U7']):
    x,y=xy(fps[ref].GetPosition());ci=20+i*10;ind='L'+str(i+1)
    # Wide switch paths start after very short, pitch-limited IC-pad necks.
    for pin,lp,sgn in [('1','1',-1),('10','2',1)]:
        neck=[x+sgn*1.975,y-1.5]
        netpath(ref+':'+pin,[P(ref+':'+pin),neck],.2)
        netpath(ref+':'+pin,[neck,[x+sgn*1.185,y-2.29],P(ind+':'+lp)],.55)
    # Input bank and local high-current plane entry.
    neck=[x-2.4,y-.5]
    netpath(ref+':2',[P(ref+':2'),neck],.2)
    netpath(ref+':2',[neck,P(f'C{ci}:1')],.65)
    join(f'C{ci}:1',f'C{ci+1}:1',width=.65)
    inp=P(f'C{ci+1}:1')
    netpath(f'C{ci+1}:1',[inp,[inp[0],inp[1]-2.2]],.6)
    for dy in [1.2,2.2]:via(f'C{ci+1}:1',[inp[0],inp[1]-dy],.6,.3)
    # Output bank. Three closely spaced capacitors share a broad connection.
    neck=[x+2.5,y-.5]
    netpath(ref+':9',[P(ref+':9'),neck],.2)
    netpath(ref+':9',[neck,P(f'C{ci+2}:1'),P(f'C{ci+3}:1'),P(f'C{ci+4}:1')],.65)
    # Kelvin-like local feedback and AUX paths, kept out of switch nodes.
    cfb=f'C{ci+8}:1';rlo=f'R{ci+1}:1';rhi=f'R{ci}:2'
    join(ref+':8',cfb,[[x+2.1,y],[x+2.7,y+.6],[P(cfb)[0],y+.6]],.15)
    if i<2:
        join(cfb,rhi,width=.15);join(rhi,rlo,width=.15)
    else:
        # Series upper resistor R43 is routed separately after pad fanout.
        join(cfb,rlo,[[x+3.5,y+.1],[x+7.1,y+.1]],.15)
    join(ref+':6',f'C{ci+5}:1',[[x+2.1,y+1],[x+2.1,y+2.8],[x+1.4,y+3.5]],.15)
    join(ref+':7',ref+':11',[[x+.6,y+.5]],.2)
    # Exposed-pad vias: assembly notes require review of via tenting/fill and
    # stencil apertures. No thermal performance is inferred from this alone.
    for dx in [-.4,.4]:via(ref+':11',[x+dx,y],.5,.2)
    for n in [ci,ci+1]:
        p=P(f'C{n}:2');pt=[1.55 if i==0 else p[0]-1.1,p[1]]
        netpath(f'C{n}:2',[p,pt],.4);via(f'C{n}:2',pt,.6,.3)
    for n in [ci+2,ci+3,ci+4]:
        p=P(f'C{n}:2');pt=[p[0],p[1]-1.2]
        netpath(f'C{n}:2',[p,pt],.4);via(f'C{n}:2',pt,.6,.3)
    for key,offset in [(f'C{ci+5}:2',(0,1.1)),(f'C{ci+8}:2',(0,1.1)),(f'R{ci+1}:2',(1.05,0))]:
        p=P(key);pt=[p[0]+offset[0],p[1]+offset[1]]
        netpath(key,[p,pt],.2);via(key,pt)
    # Quiet output sense pick-up is intentionally a light-current branch.
    end=P(f'R{ci}:1');src=P(f'C{ci+4}:1')
    # Back-layer quiet branch avoids the adjacent cell's input-ground return.
    # Ground on In1.Cu separates it from front-side switch-node copper.
    a=[src[0],src[1]+1.35];z=[end[0],27.3]
    netpath(f'C{ci+4}:1',[src,a],.2);via(f'C{ci+4}:1',a)
    netpath(f'R{ci}:1',[end,z],.2);via(f'R{ci}:1',z)
    netpath(f'C{ci+4}:1',[a,[a[0]-.35,a[1]+.35],[a[0]-.35,27.3],z],.2,k.B_Cu)
# Limiter WCSP fanout. No vias are placed in the six solder balls.
join('U13:A1','U13:B1',width=.2)
for key,points in [('U13:B1',[[22,4.5]]),('U13:B2',[[24.4,4.5]]),
                   ('U13:A2',[[23.6,3.7],[24.4,3.3]]),
                   ('U13:C2',[[23.6,5.3],[24.4,5.7]]),('U13:C1',[[22.8,6]])]:
    netpath(key,[P(key),*points],.15 if key in ['U13:A2','U13:C2','U13:C1'] else .2)
    via(key,points[-1])
# eFuse high-current output to the inner supply plane, with four parallel vias.
netpath('U4:5',[P('U4:5'),[37.4,12.2]],.2)
netpath('U4:5',[[37.4,12.2],[38.2,13],[39.2,13],[39.2,14],[38.2,14],[38.2,13]],.8)
for x in [38.2,39.2]:
    for y in [13,14]:via('U4:5',[x,y],.6,.3)
for ref,pin,offsets in [('U1','17',[(-.4,0),(.4,0)]),('U4','9',[(0,0)]),('U12','21',[(-.6,-.6),(.6,-.6),(-.6,.6),(.6,.6)])]:
    x,y=P(ref+':'+pin)
    for dx,dy in offsets:via(ref+':'+pin,[x+dx,y+dy])
def zone(key,layer,points):
    z=k.ZONE(b);z.SetLayer(layer);z.SetNet(pad(key).GetNet());z.SetPadConnection(k.ZONE_CONNECTION_FULL)
    z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
    z.SetLocalClearance(k.FromMM(.2));z.SetMinThickness(k.FromMM(.2));z.SetThermalReliefGap(k.FromMM(.25));z.SetThermalReliefSpokeWidth(k.FromMM(.35))
    z.Outline().NewOutline()
    for x,y in points:z.Outline().Append(int(k.FromMM(x)),int(k.FromMM(y)))
    b.Add(z)
zone('J3:2',k.In1_Cu,[(.6,.6),(49.4,.6),(49.4,49.4),(.6,49.4)])
zone('U4:5',k.In2_Cu,[(1,9),(49,9),(49,29),(1,29)])
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(PATH),b)
(OUT/'critical_routes.json').write_text(json.dumps(audit,indent=2)+'\n')
print('Critical converter paths and planes saved. Must pass DRC before routing handoff.')
