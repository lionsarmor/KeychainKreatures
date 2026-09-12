"""Deterministic electrical-group packing; courtyard separation across both faces.
Elevated display overlaps rear bodies only, never assumes solder tails are absent.
"""
from pathlib import Path
import json,math,ast
import numpy as np
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
d=json.loads((out/'geometry.json').read_text());W,H=84,95
placed={};occupied=[]
def shift(b,x,y):return [b[0]+x,b[1]+y,b[2]+x,b[3]+y]
def hit(a,b,g=.2):return not(a[2]+g<=b[0] or b[2]+g<=a[0] or a[3]+g<=b[1] or b[3]+g<=a[1])
def put(r,x,y,a,center=True,extra=None):
 q=d[r]['variants'][str(a)];bb=q['box']
 if center:x-=(bb[0]+bb[2])/2;y-=(bb[1]+bb[3])/2
 b=shift(bb,x,y);conf=[n for n,z in occupied if hit(b,z)]
 if conf:raise RuntimeError((r,conf,b))
 pads={p['pin']:{**p,'xy':[p['xy'][0]+x,p['xy'][1]+y]} for p in q['pads']}
 placed[r]={'xy':[x,y],'angle':a,'side':d[r]['side'],'box':b,'pads':pads}
 occupied.append((r,extra or ([b[0]-.75,b[1]-.75,b[2]+.75,b[3]+.75] if r.startswith('TP') else b)))
def fixed(r,x,y,a,**kw):
 if kw.get('extra'):kw['extra']=shift(kw['extra'],2,0)
 put(r,x+2,y,a,**kw)
for r,x,y in [('H1',4,4),('H2',80,4),('H3',4,91),('H4',80,91)]:
 put(r,x,y,0);occupied[-1]=(r,[x-2.5,y-2.5,x+2.5,y+2.5])
# Screen front: 48 x 31 landscape body x16..64, y18..49.
fixed('J2',18,42.39,180,center=False)
fixed('MOD1',40,18,0)
# Antenna + exposed top-edge band. Existing module pads are outside this window.
occupied.append(('ANTENNA',[32,0,52,13]))
occupied.append(('ANTENNA_EDGE',[27,0,57,5.25]))
fixed('D3',72,27,90)
fixed('D1',11,8,0)
fixed('U2',20,5.5,0)
# SD insert/eject to right edge, not buried beneath another rear component.
fixed('J3',61.5,52,0,center=False,extra=[59.7,36.3,80,54.9])
for r,x,y in [('SW1',18,60),('SW2',18,80),('SW3',7,70),('SW4',29,70),
              ('SW5',73,70),('SW6',62,80),('SW7',62,60),('SW8',51,70),('SW9',40,81.5)]:fixed(r,x,y,0)
fixed('U1',9.5,37,0)
fixed('U3',40,47,0)
fixed('U4',65,13,90)
fixed('J1',49,90,0)
fixed('J4',10,90,0)
fixed('J5',30,90,0)
# Extract already documented critical electrical placement objectives.
tree=ast.parse((root/'pcb/c2_placement.py').read_text())
pairs=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='pairs' for t in n.targets))
pairs += [('C27:1','U4:16'),('R40:1','U4:15'),('R41:2','U4:13'),
 ('R39:2','Q6:2'),('R38:1','Q6:2'),('R37:1','Q5:2'),('R36:2','Q5:2'),
 ('R24:2','D1:2'),('Q1:3','D1:1'),('R25:2','Q1:2'),('R26:1','Q1:2')]
def target(r):
 if r in ['Q1','R24','R25','R26','R27','C14','C15']:return (18,14)
 if r in ['D2','Q4','R28','R29','C16','C17']:return (14,87)
 if r in ['C7','C8','C9','R1','R2','R3']:return (16,47)
 if r in ['C10','C11']:return (60,50)
 if r in ['C12','C13']:return (20,25)
 if r in ['Q5','Q6'] or r.startswith('R') and 30<=int(r[1:])<=39 or r.startswith('C') and 18<=int(r[1:])<=26:return (40,50)
 if r in ['C27','R40','R41','R42','R43']:return (64,24)
 if r.startswith('C') and int(r[1:])<=6:return (55,89)
 if r in ['Q2','Q3'] or r.startswith('R') and 14<=int(r[1:])<=23:return (28,31)
 return (35,62)
order=['C26','C21','C22','C25','C23','C24','R34','R35','R33','R32','C20','C19','R31','C18','R30',
       'C14','C15','R27','Q1','R24','R25','R26','C16','D2','Q4','C17','C8','C9','C27','R40','R41','C10','C11','C12','C13',
       'Q6','Q5','R38','R39','R36','R37','C1','C2','C3','C4','C5','C6']
order += sorted(set(d)-set(placed)-set(order),key=lambda r:(r.startswith('TP'),not r.startswith('Q'),r))
X,Y=np.meshgrid(np.arange(1.5,W-1.49,.5),np.arange(1.5,H-1.49,.5));X=X.ravel();Y=Y.ravel()
for r in order:
 if r in placed:continue
 best=None;tx,ty=target(r);tp=r.startswith('TP')
 for a,q in d[r]['variants'].items():
  bb=np.array(q['box']);cx=(bb[0]+bb[2])/2;cy=(bb[1]+bb[3])/2;bb-=np.array([cx,cy,cx,cy])
  if tp:bb+=np.array([-.75,-.75,.75,.75])
  valid=(X+bb[0]>=1.5)&(X+bb[2]<=W-1.5)&(Y+bb[1]>=1.5)&(Y+bb[3]<=H-1.5)
  for n,z in occupied:valid&=(X+bb[2]+.2<=z[0])|(X+bb[0]-.2>=z[2])|(Y+bb[3]+.2<=z[1])|(Y+bb[1]-.2>=z[3])
  # Elevated LCD over front solder tails is intentional. Only modules/buttons/RGB on front.
  ix=np.flatnonzero(valid)
  if not len(ix):continue
  x,y=X[ix],Y[ix];score=.3*((x-tx)**2+(y-ty)**2)
  for p in q['pads']:
   dx,dy=p['xy'][0]-cx,p['xy'][1]-cy;key=r+':'+p['pin']
   ends=[]
   for aa,bbkey in pairs:
    other=bbkey if aa==key else aa if bbkey==key else None
    if other:
     rr,pn=other.split(':')
     if rr in placed and pn in placed[rr]['pads']:ends.append(placed[rr]['pads'][pn]['xy'])
   for ex,ey in ends:score+=20*((x+dx-ex)**2+(y+dy-ey)**2)
   net=p['net']
   if net not in ['/GND','/LOGIC_3V3','/ACT_3V2','/MCU_5V'] and not net.startswith('unconnected') or tp:
    ee=[pp['xy'] for ff in placed.values() for pp in ff['pads'].values() if pp['net']==net]
    if ee:score+=np.min([(x+dx-ex)**2+(y+dy-ey)**2 for ex,ey in ee],axis=0)*(2 if tp else 1)
  j=np.argmin(score);s=float(score[j])
  if best is None or s<best[0]:best=(s,float(x[j]),float(y[j]),int(a))
 if best is None:raise RuntimeError('NO ROOM '+r)
 _,x,y,a=best;put(r,x,y,a);print(r,x,y,a,flush=True)
dist=[]
for aa,bb in pairs:
 ar,ap=aa.split(':');br,bp=bb.split(':')
 if ap in placed[ar]['pads'] and bp in placed[br]['pads']:dist.append({'connection':aa+' -> '+bb,'direct_mm':round(math.dist(placed[ar]['pads'][ap]['xy'],placed[br]['pads'][bp]['xy']),3)})
(out/'placement.json').write_text(json.dumps({'status':'UNROUTED ENGINEERING CANDIDATE','board_mm':[W,H,1.6],'positions':placed,'critical_distances':dist},indent=2))
print('Packed',len(placed),'positions; C.4 unchanged')
