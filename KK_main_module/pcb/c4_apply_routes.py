"""Apply only recorded LED routes to the staged, modeled C4 candidate."""
from pathlib import Path
import pcbnew as k,json,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(root/'routing/KK_main_module_C4_unfinished.kicad_pcb'))
def v(p):return k.VECTOR2I(k.FromMM(p[0]),k.FromMM(p[1]))
nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()}
routes=json.loads((root/'routing/C4_LED_ROUTES.json').read_text())
gp=root/'routing/C4_GROUND_REPAIRS.json'
if gp.exists():routes+=json.loads(gp.read_text())
for r in routes:
    for a,z in zip(r['path'],r['path'][1:]):
        if a[0]==z[0]:
            if a[1:]==z[1:]:continue
            t=k.PCB_TRACK(b);t.SetStart(v(a[1:]));t.SetEnd(v(z[1:]));t.SetWidth(k.FromMM(r['width']));t.SetLayer(k.F_Cu if a[0]==0 else k.B_Cu)
        else:
            t=k.PCB_VIA(b);t.SetPosition(v(a[1:]));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu);t.SetWidth(k.FromMM(r['via_diameter']));t.SetDrill(k.FromMM(r['via_drill']))
        t.SetNet(nets[r['net']]);b.Add(t)
if gp.exists():
    for f in b.GetFootprints():
        for p in f.Pads():
            if f.GetReference()+':'+p.GetNumber() in ['SW7:C','SW9:D','C4:2']:p.SetLocalZoneConnection(k.ZONE_CONNECTION_NONE)
xml=root/'pcb/c4_netlist.xml'
if xml.exists():
    fs={f.GetReference():f for f in b.GetFootprints()}
    for c in ET.parse(xml).getroot().findall('./components/comp'):
        f=fs[c.attrib['ref']]
        for field in c.findall('./fields/field'):
            if field.attrib['name'] not in ['Reference','Value','Footprint']:
                f.SetField(field.attrib['name'],field.text or '');f.GetField(field.attrib['name']).SetVisible(False)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(root/'routing/KK_main_module_C4_routed.kicad_pcb'),b)
print('Saved rerouted C4 candidate.')
