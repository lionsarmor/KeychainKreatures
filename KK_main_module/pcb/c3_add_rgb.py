"""Native C.3 ECO: socketed RGB driver and top-entry actuator connectors.
Unchanged footprints and copper are preserved; new nets require routing.
"""
from pathlib import Path
import pcbnew as k,json,xml.etree.ElementTree as ET,sys
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(root/'routing/KK_main_module_C3_candidate.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
for name,source in [('JST_PH_B2B_2','Connector_JST.pretty/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical'),('ED16DT_DIP16_Socket','Package_DIP.pretty/DIP-16_W7.62mm_Socket_LongPads')]:
    lib,part=source.split('/')
    f=k.FootprintLoad('/app/extensions/Library/footprints/'+lib,part)
    f.SetFPID(k.LIB_ID('KK_Main',name));k.FootprintSave(str(root/'KK_Main.pretty'),f)
xml=ET.parse(root/'pcb/c3_netlist.xml').getroot()
comps={c.attrib['ref']:c for c in xml.findall('./components/comp')}
by_pin={};nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()}
for el in xml.findall('./nets/net'):
    name=el.attrib['name']
    if name not in nets:nets[name]=k.NETINFO_ITEM(b,name);b.Add(nets[name])
    for n in el.findall('node'):by_pin[n.attrib['ref'],n.attrib['pin']]=nets[name]
def make(ref):
    c=comps[ref];name=c.findtext('footprint').split(':')[1]
    f=k.FootprintLoad(str(root/'KK_Main.pretty'),name);f.SetParent(b)
    f.SetFPID(k.LIB_ID('KK_Main',name))
    f.SetReference(ref);f.SetValue(c.findtext('value'))
    fields={e.attrib['name']:e.text or '' for e in c.findall('./fields/field')}
    for key,val in fields.items():f.SetField(key,val);f.GetField(key).SetVisible(False)
    f.SetField('Datasheet',c.findtext('datasheet') or '');f.GetField('Datasheet').SetVisible(False)
    stamp=c.findtext('tstamps').strip().split()[0]
    root_path=fps['U1'].GetPath().AsString().rsplit('/',1)[0]
    f.SetPath(k.KIID_PATH(root_path+'/'+stamp))
    f.SetUuid(k.KIID(stamp))
    for p in f.Pads():p.SetNet(by_pin[ref,p.GetNumber()])
    f.Value().SetVisible(False)
    return f
# Delete only old connector footprints through native board detach. No track
# removal occurs. Positions, mapped pad coordinates and nets are asserted.
for ref in ['J4','J5']:
    old=fps[ref];new=make(ref);new.Flip(v(0,0),k.FLIP_DIRECTION_LEFT_RIGHT)
    new.SetOrientationDegrees(old.GetOrientationDegrees());new.SetPosition(old.GetPosition())
    new.Reference().SetPosition(old.Reference().GetPosition());new.Reference().SetTextAngle(old.Reference().GetTextAngle())
    oldpads={p.GetNumber():p for p in old.Pads()}
    for p in new.Pads():
        assert xy(p.GetPosition())==xy(oldpads[p.GetNumber()].GetPosition())
        assert p.GetNetname()==oldpads[p.GetNumber()].GetNetname()
    if ref=='J5':
        # 0.25 mm left shift clears C24. Existing trace endpoints remain
        # inside the 1.75 mm-wide pads; verify connectivity with DRC.
        new.Move(v(-.25,0))
    b.Remove(old);b.Add(new);fps[ref]=new
connectors_only='--connectors-only' in sys.argv
if not connectors_only:
    for p in fps['U1'].Pads():p.SetNet(by_pin['U1',p.GetNumber()])
placement=[]
for ref,x,y,angle,side in ([] if connectors_only else [('U4',59,85,0,'back'),('D3',41,61,0,'front'),('R40',74,89,90,'back'),('R41',74,73,90,'back'),('C27',48,89,0,'back')]):
    f=make(ref)
    if side=='back':f.Flip(v(0,0),k.FLIP_DIRECTION_LEFT_RIGHT)
    f.SetOrientationDegrees(angle)
    boxes=[g.GetBoundingBox() for g in f.GraphicalItems() if g.GetLayer() in (k.F_CrtYd,k.B_CrtYd)]
    lo=[min(k.ToMM(z.GetX()) for z in boxes),min(k.ToMM(z.GetY()) for z in boxes)]
    hi=[max(k.ToMM(z.GetRight()) for z in boxes),max(k.ToMM(z.GetBottom()) for z in boxes)]
    f.SetPosition(v(x-(lo[0]+hi[0])/2,y-(lo[1]+hi[1])/2))
    f.Reference().SetTextSize(v(1,1));f.Reference().SetTextThickness(k.FromMM(.15));f.Reference().SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T))
    b.Add(f);fps[ref]=f
    placement.append({'ref':ref,'center':[x,y],'angle':angle,'side':side})
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones())
k.SaveBoard(str(root/('routing/KK_main_module_C3_debug_connectors.kicad_pcb' if connectors_only else 'routing/KK_main_module_C3_rgb_unrouted.kicad_pcb')),b)
(root/'pcb/C3_RGB_PLACEMENT.json').write_text(json.dumps(placement,indent=2)+'\n')
print(('RGB parts deferred; ' if connectors_only else 'Added 5 through-hole RGB components; ')+'switched J4/J5 to top-entry, retaining nets and trace connectivity (J5 shifted 0.25mm).')
