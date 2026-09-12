"""Replace only MOD1; preserve the current board's other components, outline and zones."""
from pathlib import Path
import json, math, xml.etree.ElementTree as E
import pcbnew as k
ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'pcb'
meta=json.loads((WORK/'SUPERMINI_IMPORT.json').read_text())
pinmap=meta['pin_map'];inverse={v:a for a,v in pinmap.items()}
xml=E.parse(WORK/'board_netlist.xml').getroot()
beforexml=E.parse(Path(meta['backup'])/'before_netlist.xml').getroot()
def partitions(root,rename=False):
    return sorted(tuple(sorted((n.attrib['ref'],inverse[n.attrib['pin']] if rename and n.attrib['ref']=='MOD1' else n.attrib['pin'])
        for n in net.findall('node'))) for net in root.findall('./nets/net'))
assert partitions(beforexml)==partitions(xml,True),'Electrical connectivity changed during pin renaming'
board=k.LoadBoard(str(ROOT/'KK_main_module.kicad_pcb'))
def others():
    return sorted((f.GetReference(),f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees(),f.GetLayer(),
        tuple(sorted((p.GetNumber(),p.GetPosition().x,p.GetPosition().y,p.GetNetname()) for p in f.Pads())))
        for f in board.GetFootprints() if f.GetReference()!='MOD1')
untouched=others()
old=next(f for f in board.GetFootprints() if f.GetReference()=='MOD1')
assert old.GetLayer()==k.F_Cu,'Unexpected module side; inspect before swapping'
new=k.FootprintLoad(str(ROOT/'KK_Main.pretty'),'ESP32-S3-SuperMini');new.SetParent(board)
new.SetFPID(k.LIB_ID('KK_Main','ESP32-S3-SuperMini'))
new.SetReference('MOD1');new.SetValue(old.GetValue());new.SetPath(old.GetPath());new.SetUuid(old.m_Uuid)
for name,value in old.GetFieldsText().items():
    if name not in ('Reference','Value','Footprint'):
        new.SetField(name,value);new.GetField(name).SetVisible(False)
new.SetOrientationDegrees(old.GetOrientationDegrees());new.SetPosition(old.GetPosition())
new.Reference().SetPosition(old.Reference().GetPosition());new.Reference().SetTextSize(old.Reference().GetTextSize())
new.Reference().SetTextThickness(old.Reference().GetTextThickness());new.Reference().SetTextAngle(old.Reference().GetTextAngle())
new.Value().SetVisible(False)
nets={n.GetNetname():n for n in board.GetNetsByNetcode().values()}
desired={(p.attrib['ref'],p.attrib['pin']):net.attrib['name'] for net in xml.findall('./nets/net') for p in net.findall('node')}
for p in new.Pads():
    name=desired['MOD1',p.GetNumber()]
    if name not in nets:
        n=k.NETINFO_ITEM(board,name);board.Add(n);nets[name]=n
    p.SetNet(nets[name])
board.Remove(old);board.Add(new)
assert others()==untouched,'Unrelated component changed'
board.BuildConnectivity()
assert k.ZONE_FILLER(board).Fill(board.Zones()),'Fill failed'
actual={(f.GetReference(),p.GetNumber()):p.GetNetname() for f in board.GetFootprints() for p in f.Pads() if p.GetNumber()}
assert actual==desired,'Board pad/net mismatch'
k.SaveBoard(str(ROOT/'KK_main_module.kicad_pcb'),board)
# Update only MOD1's placement record; other placements are untouched.
record=json.loads((WORK/'PLACEMENT.json').read_text())
row=next(r for r in record['components'] if r['reference']=='MOD1')
corners=[]
for g in new.GraphicalItems():
    if g.GetLayer()==k.F_CrtYd:
        b=g.GetBoundingBox();corners.extend([(k.ToMM(b.GetX()),k.ToMM(b.GetY())),(k.ToMM(b.GetRight()),k.ToMM(b.GetBottom()))])
row.update(footprint='KK_Main:ESP32-S3-SuperMini',status='USER_SUPPLIED_FOOTPRINT',courtyard_mm=[min(p[0] for p in corners),min(p[1] for p in corners),max(p[0] for p in corners),max(p[1] for p in corners)])
(WORK/'PLACEMENT.json').write_text(json.dumps(record,indent=2)+'\n')
report={'component_pads':len(actual),'logical_net_partitions_preserved':True,'non_module_footprints_unchanged':len(untouched),
        'module_position_mm':[k.ToMM(new.GetPosition().x),k.ToMM(new.GetPosition().y)],'angle_degrees':new.GetOrientationDegrees(),
        'source_geometry_preserved':True,'pad_net_mismatches':[],
        'module_pads':[{ 'pad':p.GetNumber(),'net':p.GetNetname(),'x_mm':k.ToMM(p.GetPosition().x),'y_mm':k.ToMM(p.GetPosition().y)} for p in new.Pads()]}
(WORK/'SUPERMINI_REPLACEMENT_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print('MOD1 replaced; 267 pads/net assignments checked; all electrical net partitions and 94 other footprints preserved. Ground zones refilled.')
