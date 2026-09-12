"""Apply C.5 mechanical placement to a separate native, net-linked board."""
from pathlib import Path
import pcbnew as k,json,math
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
d=json.loads((out/'placement.json').read_text());W,H,_=d['board_mm']
b=k.LoadBoard(str(out/'C5_blank.kicad_pcb'));fps={f.GetReference():f for f in b.GetFootprints()}
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
def bounds(g):
 z=g.GetBoundingBox();return [k.ToMM(z.GetX()),k.ToMM(z.GetY()),k.ToMM(z.GetRight()),k.ToMM(z.GetBottom())]
for r,p in d['positions'].items():
 f=fps[r]
 if (f.GetLayer()==k.F_Cu)!=(p['side']=='front'):f.Flip(f.GetPosition(),k.FLIP_DIRECTION_LEFT_RIGHT)
 f.SetOrientationDegrees(p['angle']);f.SetPosition(v(*p['xy']));f.Value().SetVisible(False)
 for field in f.GetFields():
  if 'C.4' in field.GetText():field.SetText(field.GetText().replace('C.4','C.5'))
 for pad in f.Pads():pad.SetLocalZoneConnection(k.ZONE_CONNECTION_INHERITED)
 f.Reference().SetVisible(False)
 if r.startswith('H'):continue
 for pin,pp in p['pads'].items():
  actual=next(q for q in f.Pads() if q.GetNumber()==pin)
  assert math.dist(xy(actual.GetPosition()),pp['xy'])<.00001,(r,pin)
  assert actual.GetNetname()==pp['net']
f=fps['D1'];f.Models().clear();m=k.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/3dmodels/TSAL6200_C5_edge_formed.wrl';f.Models().push_back(m)
# New model attachment only; pad geometry/net numbering unchanged.
f.SetFPID(k.LIB_ID('KK_Main','TSAL6200_C5_EdgeFormed'))
lib=k.FootprintLoad(str(root/'KK_Main.pretty'),'TSAL6200_LED5');lib.SetFPID(f.GetFPID());lib.Models().clear();lm=k.FP_3DMODEL();lm.m_Filename=m.m_Filename;lib.Models().push_back(lm)
lib.SetLibDescription('TSAL6200, formed at 5mm rear lens-axis height; optical axis local +Y. Qualification required. Original pad1 K / pad2 A retained.')
k.FootprintSave(str(root/'KK_Main.pretty'),lib)
f.SetLibDescription(lib.GetLibDescription())
r=4;u=r/math.sqrt(2)
for a,z in [((r,0),(W-r,0)),((W,r),(W,H-r)),((W-r,H),(r,H)),((0,H-r),(0,r))]:
 s=k.PCB_SHAPE(b);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s)
for a,c,z in [((W-r,0),(W-r+u,r-u),(W,r)),((W,H-r),(W-r+u,H-r+u),(W-r,H)),((r,H),(r-u,H-r+u),(0,H-r)),((0,r),(r-u,r-u),(r,0))]:
 s=k.PCB_SHAPE(b);s.SetShape(k.SHAPE_T_ARC);s.SetArcGeometry(v(*a),v(*c),v(*z));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s)
net=next(n for n in b.GetNetsByNetcode().values() if n.GetNetname()=='/GND')
for la,name in [(k.F_Cu,'MAIN_GND_FRONT'),(k.B_Cu,'MAIN_GND_BACK')]:
 z=k.ZONE(b);z.SetLayer(la);z.SetNet(net);z.SetZoneName(name);z.SetLocalClearance(k.FromMM(.25));z.SetMinThickness(k.FromMM(.25));z.SetPadConnection(k.ZONE_CONNECTION_THERMAL);z.SetThermalReliefGap(k.FromMM(.3));z.SetThermalReliefSpokeWidth(k.FromMM(.3));z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
 o=z.Outline();o.NewOutline()
 for x,y in [(0,0),(W,0),(W,H),(0,H)]:o.Append(k.FromMM(x),k.FromMM(y))
 b.Add(z)
for name,pts in [('EDGE',[(27,0),(57,0),(57,5.25),(27,5.25)]),('UNDER_MODULE',[(35.5,5.25),(48.5,5.25),(48.5,14.5),(35.5,14.5)])]:
 z=k.ZONE(b);z.SetLayerSet(k.LSET.AllCuMask(2));z.SetIsRuleArea(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowFootprints(False);z.SetZoneName('C5_ANTENNA_'+name);o=z.Outline();o.NewOutline()
 for x,y in pts:o.Append(k.FromMM(x),k.FromMM(y))
 b.Add(z)
def text(t,x,y,la=k.F_SilkS,size=.85):
 s=k.PCB_TEXT(b);s.SetText(t);s.SetPosition(v(x,y));s.SetTextSize(v(size,size));s.SetTextThickness(k.FromMM(.13));s.SetLayer(la);s.SetMirrored(la==k.B_SilkS);b.Add(s);return s
text('C.5 - ENGINEERING',42,H-1.4,k.F_SilkS,.8)
text('LANDSCAPE 280 x 240 / SAMPLE FIT REQUIRED',42,104,k.Dwgs_User,1)
text('C.5 UNROUTED - DO NOT FABRICATE',42,107,k.Dwgs_User,1.2)
# Official library artwork; board-only, not circuit components or certification.
for ref,name,x,y in [('LOGO1','KiCad-Logo_6mm_SilkScreen',12,88.5),('LOGO2','OSHW-Logo_5.7x6mm_SilkScreen',72,88.5)]:
 f=k.FootprintLoad('/app/extensions/Library/footprints/Symbol.pretty',name);assert f is not None,name
 f.SetParent(b);f.SetReference(ref);f.SetFPID(k.LIB_ID('Symbol',name));f.SetPosition(v(x,y));f.SetAttributes(k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES|k.FP_BOARD_ONLY);f.Reference().SetVisible(False);f.Value().SetVisible(False)
 padboxes=[bounds(p) for ff in b.GetFootprints() for p in ff.Pads()]
 padboxes += [bounds(ff) for ff in b.GetFootprints() if ff.GetReference().startswith('LOGO')]
 for xx,yy in sorted([(i*.5,j*.5) for i in range(10,int(W*2-10)) for j in range(10,int(H*2-10))],key=lambda q:(q[0]-x)**2+(q[1]-y)**2):
  f.SetPosition(v(xx,yy));bb=bounds(f)
  if not any(not(bb[2]+.3<=p[0] or p[2]+.3<=bb[0] or bb[3]+.3<=p[1] or p[3]+.3<=bb[1]) for p in padboxes):break
 else:raise RuntimeError('No logo room '+ref)
 b.Add(f)
# Legible references/orientation labels, searched against all copper and same-side artwork.
def hit(a,z,g=.23):return not(a[2]+g<=z[0] or z[2]+g<=a[0] or a[3]+g<=z[1] or z[3]+g<=a[1])
obs={la:[] for la in [k.F_SilkS,k.B_SilkS]}
for f in b.GetFootprints():
 for p in f.Pads():
  for la in obs:obs[la].append(bounds(p))
 for g in f.GraphicalItems():
  if g.GetLayer() in obs and (not hasattr(g,'IsVisible') or g.IsVisible()):
   bb=bounds(g)
   if isinstance(g,k.PCB_SHAPE) and g.GetShape()==k.SHAPE_T_RECT:
    x1,y1,x2,y2=bb;t=.15
    obs[g.GetLayer()].extend([[x1,y1,x2,y1+t],[x1,y2-t,x2,y2],[x1,y1,x1+t,y2],[x2-t,y1,x2,y2]])
   else:obs[g.GetLayer()].append(bb)
for g in b.GetDrawings():
 if g.GetLayer() in obs:obs[g.GetLayer()].append(bounds(g))
def label(t,anchor,la,sz=.8,maxshift=12):
 s=text(t,*anchor,la,sz)
 for dx,dy in sorted([(i*.5,j*.5) for i in range(-maxshift*2,maxshift*2+1) for j in range(-maxshift*2,maxshift*2+1)],key=lambda p:p[0]**2+p[1]**2):
  s.SetPosition(v(anchor[0]+dx,anchor[1]+dy));bb=bounds(s)
  if bb[0]<1 or bb[1]<1 or bb[2]>W-1 or bb[3]>H-1:continue
  if not any(hit(bb,z) for z in obs[la]):obs[la].append(bb);return s
 raise RuntimeError('No label space '+t)
for r,p in d['positions'].items():
 if r.startswith('H'):continue
 la=k.F_SilkS if p['side']=='front' else k.B_SilkS;bb=p['box'];anchor=[(bb[0]+bb[2])/2,bb[1]-1]
 label(r,anchor,la)
 if r.startswith('C') and 'Nichicon' in d.get('x',{}).get(r,''):pass
 # Only original polarized footprint graphics are retained; explicit pin 1 added below.
 if r in ['MOD1','J1','J2','J3','J4','J5','U1','U2','U3','U4','D3']:
  pn='5V' if r=='MOD1' else '1';p1=p['pads'][pn]['xy'];label('5V' if r=='MOD1' else '1',p1,la,.8,8)
for t,x,y in [('UP',20,60),('DOWN',20,80),('LEFT',9,70),('RIGHT',31,70),('A',75,70),('B',64,80),('X',64,60),('Y',53,70),('MODE',42,81.5),('RGB',74,27)]:label(t,[x,y],k.F_SilkS,.85)
for r,t in [('J1','SYS_IN'),('J4','MOTOR'),('J5','SPEAKER'),('U2','IR RX'),('D1','IR TX'),('J3','SD OUT >')]:
 pp=d['positions'][r]['box'];label(t,[(pp[0]+pp[2])/2,pp[3]+2],k.B_SilkS,.85)
label('NO METAL',[42,5],k.F_SilkS,.9,3)
label('KEYCHAIN KREATURES',[42,52],k.F_SilkS,1,30)
b.GetTitleBlock().SetRevision('C.5 landscape engineering');b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones())
k.SaveBoard(str(out/'KK_main_module.kicad_pcb'),b)
print('C.5 board written; routing and verification required')
