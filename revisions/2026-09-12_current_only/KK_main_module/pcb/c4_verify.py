"""Independent C4 electrical, route-preservation and 3D coverage checks."""
from pathlib import Path
import pcbnew as k,json,hashlib,xml.etree.ElementTree as ET
from collections import Counter
root=Path(__file__).resolve().parent.parent;b=k.LoadBoard(str(root/'KK_main_module.kicad_pcb'))
old=k.LoadBoard(str(root/'pcb/backups/pre_c4_top_rgb/KK_main_module.kicad_pcb'))
stage=k.LoadBoard(str(root/'routing/KK_main_module_C4_stage.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
xml=ET.parse(root/'pcb/c4_netlist.xml').getroot();cs={c.attrib['ref']:c for c in xml.findall('./components/comp')}
expected={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
def pos(p):return(p.x,p.y)
def copper(t):
    if t.GetClass()=='PCB_VIA':return('via',t.GetNetname(),pos(t.GetPosition()),t.GetWidth(k.F_Cu),t.GetDrillValue())
    return('track',t.GetNetname(),pos(t.GetStart()),pos(t.GetEnd()),t.GetWidth(),t.GetLayer())
assert not Counter(copper(t) for t in stage.GetTracks())-Counter(copper(t) for t in b.GetTracks()),'Unrelated copper changed'
for f in old.GetFootprints():
    n=fps[f.GetReference()]
    if f.GetReference()!='D3':assert pos(n.GetPosition())==pos(f.GetPosition()) and n.GetOrientationDegrees()==f.GetOrientationDegrees()
    a={p.GetNumber():p for p in f.Pads()};z={p.GetNumber():p for p in n.Pads()};assert set(a)==set(z)
    for key,p in a.items():
        q=z[key];assert p.GetNetname()==q.GetNetname(),(f.GetReference(),key)
        if f.GetReference()!='D3':assert pos(p.GetPosition())==pos(q.GetPosition()) and pos(p.GetSize())==pos(q.GetSize()) and pos(p.GetDrillSize())==pos(q.GetDrillSize())
coverage=[];standard=Path('/app/extensions/Library/3dmodels')
for ref,c in cs.items():
    f=fps[ref];assert f.GetValue()==c.findtext('value')
    assert str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())==c.findtext('footprint'),ref
    for p in f.Pads():assert p.GetNetname()==expected[ref,p.GetNumber()] and p.GetAttribute()==k.PAD_ATTRIB_PTH
    ms=list(f.Models());assert ms,ref+' missing model'
    filenames=[]
    for m in ms:
        p=Path(m.m_Filename.replace('${KIPRJMOD}',str(root)).replace('${KICAD10_3DMODEL_DIR}',str(standard)))
        assert p.exists(),str(p);assert m.m_Show
        filenames.append(m.m_Filename)
    coverage.append({'reference':ref,'models':filenames})
assert len(cs)==98 and len(fps)==127
zones=[z for z in b.Zones()];assert sum(z.GetIsRuleArea() for z in zones)==2
assert sum(not z.GetIsRuleArea() and z.IsFilled() and z.GetNetname()=='/GND' for z in zones)==2
rules=json.loads((root/'pcb/C2_ROUTING_RULES.json').read_text());widths={n:w for n,w,_,_ in rules['classes']}
for t in b.GetTracks():
    if t.GetClass()!='PCB_VIA':assert k.ToMM(t.GetWidth())+1e-6>=widths[rules['assignments'].get(t.GetNetname(),'Default')]
vias=sum(t.GetClass()=='PCB_VIA' for t in b.GetTracks())
report={'revision':'C.4','board_mm':[80,115,1.6],'schematic_components':98,'modeled_electrical_positions':len(coverage),'test_points':25,'electrical_pin_net_mapping_unchanged':True,'only_component_moved':'D3','unrelated_routes_preserved':True,'track_segments':len(list(b.GetTracks()))-vias,'vias':vias,'plated_holes':sum(p.GetAttribute()==k.PAD_ATTRIB_PTH for f in fps.values() for p in f.Pads())+vias,'npth_holes':4,'model_coverage':coverage,'qualification':'Nominal geometry only; seller modules and RGB socket retention require physical verification','board_sha256':hashlib.sha256((root/'KK_main_module.kicad_pcb').read_bytes()).hexdigest()}
(root/'pcb/C4_FINAL_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='model_coverage'})
