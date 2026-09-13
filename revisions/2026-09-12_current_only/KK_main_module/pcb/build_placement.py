"""Create a net-linked, unrouted placement PCB through the native KiCad API.
Run inside the installed KiCad Flatpak. This is NOT a fabrication generator.
"""
from pathlib import Path
import json, math, xml.etree.ElementTree as ET
import pcbnew as k

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / 'pcb'
BOARD_PATH = ROOT / 'KK_main_module.kicad_pcb'
if BOARD_PATH.exists() and list(k.LoadBoard(str(BOARD_PATH)).GetTracks()):
    raise RuntimeError('Historical placement generator refuses to overwrite routed work. Use the C.2 project directly.')
board = k.BOARD()
board.SetCopperLayerCount(2)
board.GetDesignSettings().SetBoardThickness(k.FromMM(1.6))
def vec(x,y): return k.VECTOR2I(k.FromMM(x), k.FromMM(y))
def mm(x): return k.ToMM(x)
data=json.loads((WORK/'footprint_assignments.json').read_text())
netxml=ET.parse(WORK/'board_netlist.xml').getroot()
components={c.attrib['ref']:c for c in netxml.findall('./components/comp')}
net_by_pin={}; nets={}
for el in netxml.findall('./nets/net'):
    name=el.attrib['name']; net=k.NETINFO_ITEM(board,name);board.Add(net);nets[name]=net
    for node in el.findall('node'): net_by_pin[(node.attrib['ref'],node.attrib['pin'])]=net

def shape_line(a,b,layer,width=.15):
    s=k.PCB_SHAPE(board);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(vec(*a));s.SetEnd(vec(*b));s.SetLayer(layer);s.SetWidth(k.FromMM(width));board.Add(s)
def rectangle(x1,y1,x2,y2,layer,width=.15):
    pts=[(x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)]
    for a,b in zip(pts,pts[1:]):shape_line(a,b,layer,width)
def text(label,x,y,layer=k.Dwgs_User,size=1):
    t=k.PCB_TEXT(board);t.SetText(label);t.SetPosition(vec(x,y));t.SetTextSize(vec(size,size));t.SetTextThickness(k.FromMM(.15));t.SetLayer(layer);board.Add(t)
rectangle(0,0,80,100,k.Edge_Cuts,.05)
text('KK MAIN C.1 - PLACEMENT ONLY / DO NOT FABRICATE',40,103,size=1.2)
text('80 x 100 mm / 2 layers / 1.6 mm / THT assembly',40,106,size=1)
rectangle(24,9,55,57,k.Dwgs_User)
text('TFT 31 x 48: envelope only',39.5,32,k.Dwgs_User,.9)
text('Header offset / height NOT verified',39.5,35,k.Dwgs_User,.8)
rectangle(3,35,21,53,k.Dwgs_User)
text('SD envelope',12,43,k.Dwgs_User,.8)
text('NO METAL / ANTENNA',65,3,k.Dwgs_User,.8)
# Conservative antenna area; direction and dimensions depend on sample qualification.
z=k.ZONE(board);z.SetLayerSet(k.LSET.AllCuMask(2));z.SetIsRuleArea(True)
z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowCopperPour(True) if hasattr(z,'SetDoNotAllowCopperPour') else z.SetDoNotAllowZoneFills(True)
z.SetDoNotAllowFootprints(False);z.SetZoneName('PROVISIONAL_SUPERMINI_ANTENNA')
outline=z.Outline();outline.NewOutline()
for x,y in [(51,0),(80,0),(80,7),(51,7)]:outline.Append(k.FromMM(x),k.FromMM(y))
board.Add(z)

occupied=[]; placed={}; positions=[]
def bbox(fp):
    # Courtyard-only bounding box; do not let reference text distort placement.
    pts=[]
    for g in fp.GraphicalItems():
        if g.GetLayer() in (k.F_CrtYd,k.B_CrtYd):
            b=g.GetBoundingBox();pts.extend([(mm(b.GetX()),mm(b.GetY())),(mm(b.GetRight()),mm(b.GetBottom()))])
    if not pts:
        b=fp.GetBoundingBox(False,False);return [mm(b.GetX()),mm(b.GetY()),mm(b.GetRight()),mm(b.GetBottom())]
    return [min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)]
def collides(a,b,gap=.2):return not(a[2]+gap<=b[0] or b[2]+gap<=a[0] or a[3]+gap<=b[1] or b[3]+gap<=a[1])
def centered(fp,x,y,angle,back):
    if back:fp.Flip(vec(0,0),k.FLIP_DIRECTION_LEFT_RIGHT)
    fp.SetOrientationDegrees(angle)
    b=bbox(fp);fp.SetPosition(vec(x-(b[0]+b[2])/2,y-(b[1]+b[3])/2))
def footprint(row):
    name=row['footprint'].split(':')[1]
    fp=k.FootprintLoad(str(ROOT/'KK_Main.pretty'),name)
    if not fp:raise RuntimeError('Cannot load '+name)
    fp.SetParent(board)
    fp.SetFPID(k.LIB_ID('KK_Main',name));fp.SetReference(row['ref']);fp.SetValue(row['value'])
    for field in components[row['ref']].findall('./fields/field'):
        if field.attrib['name'] not in ('Footprint','Value','Reference'):
            fp.SetField(field.attrib['name'],field.text or '')
            fp.GetField(field.attrib['name']).SetVisible(False)
    p=k.KIID_PATH()
    for u in row['path'].strip('/').split('/'):p.push_back(k.KIID(u))
    fp.SetPath(p)
    for pad in fp.Pads():
        net=net_by_pin.get((row['ref'],pad.GetNumber()))
        if net:pad.SetNet(net)
    return fp
def accept(row,fp):
    b=bbox(fp);occupied.append((row['ref'],b));board.Add(fp);placed[row['ref']]=fp
    ref=fp.Reference();ref.SetVisible(True);ref.SetTextSize(vec(.85,.85));ref.SetTextThickness(k.FromMM(.13));ref.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T))
    ref.SetPosition(vec((b[0]+b[2])/2,b[1]-1.0));ref.SetLayer(k.B_SilkS if fp.GetLayer()==k.B_Cu else k.F_SilkS)
    fp.Value().SetVisible(False)
    positions.append({'reference':row['ref'],'footprint':row['footprint'],'side':'back' if fp.GetLayer()==k.B_Cu else 'front','courtyard_mm':b,'angle':fp.GetOrientationDegrees(),'status':row['status']})

fixed={
 'MOD1':(66,20,180,False),
 'J2':(39,11,90,False),'J3':(5,44,0,False),
 'D1':(8,12,0,False),'U2':(18,10,180,False),
 'SW1':(19,67,0,False),'SW2':(19,91,0,False),'SW3':(7,79,0,False),'SW4':(31,79,0,False),
 'SW5':(73,79,0,False),'SW6':(61,91,0,False),'SW7':(61,67,0,False),'SW8':(49,79,0,False),'SW9':(40,94,0,False),
 'U1':(14,35,0,True),'U3':(43,57,0,True),
 'J1':(68,52,0,True),'J4':(71,39,90,True),'J5':(6,61,270,True),
 'Q1':(26,17,0,True),'Q2':(44,17,0,True),'Q3':(51,24,0,True),
 'Q4':(62,44,0,True),'Q5':(50,48,0,True),'Q6':(55,57,0,True),
 'C2':(53,30,0,True),'C8':(5,29,0,True),'C14':(15,4.5,0,True),
 'C12':(45,7,0,True),'C10':(5,33,0,True),'C26':(33,57,90,True),
}
# Mechanical holes consume physical area on both sides; excluded from schematic parity/BOM.
for i,(x,y) in enumerate([(4,4),(76,60),(4,96),(76,96)],1):
    fp=k.FOOTPRINT(board);fp.SetReference('H'+str(i));fp.SetValue('M2 2.2mm NPTH');fp.SetAttributes(k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES|k.FP_BOARD_ONLY)
    pad=k.PAD(fp);pad.SetNumber('');pad.SetAttribute(k.PAD_ATTRIB_NPTH);pad.SetShape(k.PAD_SHAPE_CIRCLE);pad.SetSize(vec(2.2,2.2));pad.SetDrillSize(vec(2.2,2.2));pad.SetLayerSet(k.LSET.AllCuMask(2));fp.Add(pad);fp.SetPosition(vec(x,y));fp.Reference().SetVisible(False);fp.Value().SetVisible(False);board.Add(fp);occupied.append(('H'+str(i),[x-2.7,y-2.7,x+2.7,y+2.7]))
for row in data:
    if row['ref'] not in fixed:continue
    fp=footprint(row);centered(fp,*fixed[row['ref']]);b=bbox(fp)
    conflicts=[r for r,c in occupied if collides(b,c)]
    if conflicts:raise RuntimeError(f'Fixed placement overlap {row["ref"]}: {conflicts}')
    accept(row,fp)
# Initial packing uses circuit-block proximity, never permits opposite-side body/pad overlap.
# This is only a placement study: decoupling distance and routing still require refinement.
def target(ref):
    if ref.startswith('R'):
        n=int(ref[1:]);return (22,52) if n<=13 else (47,25) if n<=23 else (23,17) if n<=27 else (66,40) if n<=29 else (42,57)
    if ref.startswith('C'):
        n=int(ref[1:]);return (64,56) if n<=6 else (23,36) if n<=9 else (42,22) if n<=13 else (26,18) if n<=15 else (66,40) if n<=17 else (42,57)
    return {'Q1':(20,16),'Q2':(47,28),'Q3':(53,27),'Q4':(66,39),'Q5':(50,57),'Q6':(56,57),'D2':(66,42)}.get(ref,(40,45))
todo=[r for r in data if r['ref'] not in placed]
# Largest bodies first prevents the capacitors and driver packages becoming stranded.
def area(row):
    b=bbox(footprint(row));return (b[2]-b[0])*(b[3]-b[1])
todo.sort(key=area,reverse=True)
for row in todo:
    tx,ty=target(row['ref']);best=None
    for angle in [0,90]:
        base=footprint(row);centered(base,0,0,angle,True);bb=bbox(base)
        for ix in range(8,154):
            x=ix*.5
            for iy in range(20,192):
                y=iy*.5
                b=[bb[0]+x,bb[1]+y,bb[2]+x,bb[3]+y]
                if b[0]<1 or b[1]<1 or b[2]>79 or b[3]>99:continue
                if collides(b,[51,0,80,7]):continue
                if any(collides(b,c) for _,c in occupied):continue
                score=(x-tx)**2+(y-ty)**2 + (2 if angle else 0)
                if best is None or score<best[0]:best=(score,x,y,angle)
    if best is None:raise RuntimeError('Does not fit: '+row['ref'])
    _,x,y,a=best;fp=footprint(row);centered(fp,x,y,a,True);accept(row,fp)
board.BuildConnectivity()
from round_and_pour import update_board
update_board(board)
k.SaveBoard(str(BOARD_PATH),board)
(WORK/'PLACEMENT.json').write_text(json.dumps({'status':'UNROUTED placement study; module geometry holds','outline_mm':[80,100],'corner_radius_mm':4,'ground_pour_layers':['F.Cu','B.Cu'],'components':positions},indent=2)+'\n')
print(f'Saved {BOARD_PATH}: {len(placed)} net-linked components, 4 NPTH holes; no tracks or manufacturing output.')
