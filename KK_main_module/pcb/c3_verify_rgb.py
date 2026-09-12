"""Independent pin/net, retained-route, geometry and population release checks."""
from pathlib import Path
import pcbnew as k,json,hashlib,xml.etree.ElementTree as ET
from collections import Counter
root=Path(__file__).resolve().parent.parent;b=k.LoadBoard(str(root/'KK_main_module.kicad_pcb'))
old=k.LoadBoard(str(root/'pcb/backups/pre_c3_rgb/KK_main_module.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
xml=ET.parse(root/'pcb/c3_netlist.xml').getroot();comps={c.attrib['ref']:c for c in xml.findall('./components/comp')}
expected={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
def pos(p):return(p.x,p.y)
def copper(t):
    if t.GetClass()=='PCB_VIA':return('via',t.GetNetname(),pos(t.GetPosition()),t.GetWidth(k.F_Cu),t.GetDrillValue())
    return('track',t.GetNetname(),pos(t.GetStart()),pos(t.GetEnd()),t.GetWidth(),t.GetLayer())
assert not Counter(copper(t) for t in old.GetTracks())-Counter(copper(t) for t in b.GetTracks()), 'Original copper changed'
for f in old.GetFootprints():
    n=fps[f.GetReference()];delta=k.FromMM(15) if f.GetReference().startswith('H') and f.GetPosition().y>=k.FromMM(96) else 0
    assert pos(n.GetPosition())==(f.GetPosition().x,f.GetPosition().y+delta)
    assert n.GetOrientationDegrees()==f.GetOrientationDegrees()
    a={p.GetNumber():p for p in f.Pads()};z={p.GetNumber():p for p in n.Pads()}
    assert set(a)==set(z)
    for number,p in a.items():
        q=z[number];assert pos(q.GetPosition())==(p.GetPosition().x,p.GetPosition().y+delta)
        assert pos(q.GetSize())==pos(p.GetSize()) and pos(q.GetDrillSize())==pos(p.GetDrillSize())
        if not(f.GetReference()=='U1' and number in ['25','26','27','28']):assert p.GetNetname()==q.GetNetname()
for ref,c in comps.items():
    f=fps[ref];assert f.GetValue()==c.findtext('value'),ref
    assert str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())==c.findtext('footprint'),ref
    assert f.Reference().IsVisible(),ref+' hidden reference'
    for p in f.Pads():
        assert p.GetNetname()==expected[ref,p.GetNumber()],ref+':'+p.GetNumber()
        assert p.GetAttribute()==k.PAD_ATTRIB_PTH
    fields={e.attrib['name']:e.text or '' for e in c.findall('./fields/field')}
    assert f.GetField('MPN').GetText()==fields['MPN'],ref
plan=json.loads((root/'pcb/C3_DEBUG_PLAN.json').read_text())
for i in plan:
    f=fps[i['ref']];p=next(iter(f.Pads()))
    assert f.GetAttributes()&k.FP_BOARD_ONLY and f.GetAttributes()&k.FP_EXCLUDE_FROM_BOM
    assert f.GetFPID().GetLibItemName()=='Debug_PTH_2mm' and p.GetNetname()==i['net']
assert len(comps)==98 and len(plan)==25 and len(fps)==127
edge=b.GetBoardEdgesBoundingBox();assert abs(k.ToMM(edge.GetWidth())-80)<.1 and abs(k.ToMM(edge.GetHeight())-115)<.1
zones=[{'rule_area':z.GetIsRuleArea(),'name':z.GetZoneName(),'filled':z.IsFilled(),'net':z.GetNetname()} for z in b.Zones()]
assert sum(z['rule_area'] for z in zones)==2
assert sum(not z['rule_area'] and z['filled'] and z['net']=='/GND' for z in zones)==2
rules=json.loads((root/'pcb/C2_ROUTING_RULES.json').read_text());widths={n:w for n,w,_,_ in rules['classes']}
for t in b.GetTracks():
    if t.GetClass()!='PCB_VIA':assert k.ToMM(t.GetWidth())+1e-6>=widths[rules['assignments'].get(t.GetNetname(),'Default')]
via_count=sum(t.GetClass()=='PCB_VIA' for t in b.GetTracks())
report={'revision':'C.3 RGB ENGINEERING PROTOTYPE','board_mm':[80,115,1.6],'schematic_components':len(comps),'test_points':len(plan),'original_routes_and_electrical_placements_retained':True,'mounting_hole_change':'bottom two holes moved 15mm down','track_segments':len(list(b.GetTracks()))-via_count,'vias':via_count,'plated_holes':sum(p.GetAttribute()==k.PAD_ATTRIB_PTH for f in fps.values() for p in f.Pads())+via_count,'npth_holes':sum(p.GetAttribute()==k.PAD_ATTRIB_NPTH for f in fps.values() for p in f.Pads()),'zones':zones,'board_sha256':hashlib.sha256((root/'KK_main_module.kicad_pcb').read_bytes()).hexdigest()}
(root/'pcb/C3_FINAL_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
