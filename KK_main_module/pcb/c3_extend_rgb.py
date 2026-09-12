"""Approved 80x115mm RGB extension, preserving checked 80x100mm circuitry."""
from pathlib import Path
import pcbnew as k,json,xml.etree.ElementTree as ET,ast
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(root/'pcb/backups/pre_c3_rgb/KK_main_module.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
xml=ET.parse(root/'pcb/c3_netlist.xml').getroot();comps={c.attrib['ref']:c for c in xml.findall('./components/comp')}
by_pin={};nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()}
for el in xml.findall('./nets/net'):
    name=el.attrib['name']
    if name not in nets:nets[name]=k.NETINFO_ITEM(b,name);b.Add(nets[name])
    for node in el.findall('node'):by_pin[node.attrib['ref'],node.attrib['pin']]=nets[name]
tree=ast.parse((root/'pcb/c3_add_rgb.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='make'],type_ignores=[]),'<make RGB footprint>','exec'))
for p in fps['U1'].Pads():p.SetNet(by_pin['U1',p.GetNumber()])
for g in b.GetDrawings():
    if g.GetLayer()==k.Edge_Cuts:
        if g.GetShape()==k.SHAPE_T_ARC:
            if min(g.GetStart().y,g.GetEnd().y)>=k.FromMM(96):g.Move(v(0,15))
        else:
            for get,setter in [(g.GetStart,g.SetStart),(g.GetEnd,g.SetEnd)]:
                p=get()
                if p.y>=k.FromMM(96):setter(k.VECTOR2I(p.x,p.y+k.FromMM(15)))
    elif hasattr(g,'GetText'):
        t=g.GetText().replace('80 x 100','80 x 115')
        if 'PROTOTYPE' in t and 'C.3' in t:t='KK MAIN C.3 / RGB PROTOTYPE'
        g.SetText(t)
for f in b.GetFootprints():
    if f.GetReference().startswith('H') and f.GetPosition().y>=k.FromMM(96):f.Move(v(0,15))
for z in b.Zones():
    if z.GetIsRuleArea():continue
    chain=z.Outline().Outline(0)
    for i in range(chain.PointCount()):
        p=chain.CPoint(i)
        if p.y>=k.FromMM(96):chain.SetPoint(i,k.VECTOR2I(p.x,p.y+k.FromMM(15)))
    z.UnFill()
placement=[]
for ref,x,y,angle,side in [('U4',41,106,90,'back'),('D3',16,106,0,'front'),('R40',58,104,0,'back'),('R41',69,106,90,'back'),('C27',54.5,100,0,'back'),('R42',16,101,0,'back'),('R43',16,111,0,'back')]:
    f=make(ref)
    if side=='back':f.Flip(v(0,0),k.FLIP_DIRECTION_LEFT_RIGHT)
    f.SetOrientationDegrees(angle)
    boxes=[g.GetBoundingBox() for g in f.GraphicalItems() if g.GetLayer() in (k.F_CrtYd,k.B_CrtYd)]
    lo=[min(k.ToMM(z.GetX()) for z in boxes),min(k.ToMM(z.GetY()) for z in boxes)]
    hi=[max(k.ToMM(z.GetRight()) for z in boxes),max(k.ToMM(z.GetBottom()) for z in boxes)]
    f.SetPosition(v(x-(lo[0]+hi[0])/2,y-(lo[1]+hi[1])/2))
    f.Reference().SetTextSize(v(1,1));f.Reference().SetTextThickness(k.FromMM(.15));f.Reference().SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T))
    b.Add(f);fps[ref]=f
    placement.append({'reference':ref,'side':side,'center':[x,y],'angle':angle})
b.GetTitleBlock().SetRevision('C.3 RGB')
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(root/'routing/KK_main_module_C3_extended.kicad_pcb'),b)
(root/'pcb/C3_RGB_PLACEMENT.json').write_text(json.dumps(placement,indent=2)+'\n')
print('Added RGB circuitry in approved 15mm extension; original routes retained.')
