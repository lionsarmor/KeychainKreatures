"""Independent pin/net/value, model, placement and route-width verification."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,collections,math
import pcbnew as k
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
b=k.LoadBoard(str(out/'KK_main_module.kicad_pcb'));old=k.LoadBoard(str(root/'pcb/backups/pre_c5_relayout/KK_main_module.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()};before={f.GetReference():f for f in old.GetFootprints()}
x=ET.parse(out/'netlist.xml').getroot();comps={c.get('ref'):c for c in x.findall('./components/comp')}
def pmap(f):return {p.GetNumber():p.GetNetname() for p in f.Pads()}
def fid(f):return str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())
expected={(n.get('ref'),n.get('pin')):net.get('name') for net in x.findall('./nets/net') for n in net.findall('node')}
count=0;models=[];changes=[]
for r,c in comps.items():
 f=fps[r];assert pmap(f)==pmap(before[r]),r;assert f.GetValue()==before[r].GetValue()==c.findtext('value'),r
 assert fid(f)==c.findtext('footprint'),r
 for p in f.Pads():
  assert p.GetNetname()==expected[(r,p.GetNumber())],(r,p.GetNumber())
  assert p.GetAttribute()==k.PAD_ATTRIB_PTH,r
  count+=1
 assert len(list(f.Models()))>0,r
 for m in f.Models():
  name=m.m_Filename.replace('${KIPRJMOD}',str(out)).replace('${KICAD10_3DMODEL_DIR}','/app/extensions/Library/3dmodels').replace('${KICAD9_3DMODEL_DIR}','/app/extensions/Library/3dmodels')
  assert Path(name).exists() and m.m_Show,(r,name)
  models.append({'ref':r,'model':m.m_Filename})
 if fid(f)!=fid(before[r]):changes.append(r)
for r,f in fps.items():
 if r.startswith('TP'):assert pmap(f)==pmap(before[r])
rules=json.loads((out/'ROUTING_RULES.json').read_text());widths={c[0]:c[1] for c in rules['classes']};assignment=rules['assignments'];bad=[]
for t in b.GetTracks():
 if t.GetClass()!='PCB_VIA':
  width=k.ToMM(t.GetWidth());minimum=widths[assignment.get(t.GetNetname(),'Default')]
  if width+1e-6<minimum:bad.append([t.GetNetname(),width,minimum])
assert not bad,bad
placement=json.loads((out/'placement.json').read_text());assert len(placement['positions'])==127
for r,pos in placement['positions'].items():
 f=fps[r];pt=f.GetPosition();assert math.dist([k.ToMM(pt.x),k.ToMM(pt.y)],pos['xy'])<.001,r
 assert (f.GetLayer()==k.F_Cu)==(pos['side']=='front'),r
assert len([f for r,f in fps.items() if r.startswith('LOGO')])==2
bb=b.GetBoardEdgesBoundingBox();size=[k.ToMM(bb.GetWidth()),k.ToMM(bb.GetHeight())]
assert all(abs(a-z)<.1 for a,z in zip(size,[84,95]))
result={'status':'STATIC_CHECKS_PASS; see DRC and physical holds','electrical_positions':len(comps),'checked_component_pads':count,'pin_net_value_mapping_unchanged':True,'all_component_pads_through_hole':True,'model_coverage':len(set(m['ref'] for m in models)),'models':models,'footprint_changes':sorted(changes),'test_points':sum(r.startswith('TP') for r in fps),'board_mm':[84,95,1.6],'area_reduction_percent':round((1-84*95/(80*115))*100,2),'track_segments':sum(t.GetClass()!='PCB_VIA' for t in b.GetTracks()),'vias':sum(t.GetClass()=='PCB_VIA' for t in b.GetTracks()),'track_width_violations':bad,'ground_pours':sum(not z.GetIsRuleArea() for z in b.Zones()),'antenna_rule_areas':sum(z.GetIsRuleArea() for z in b.Zones()),'board_sha256':hashlib.sha256((out/'KK_main_module.kicad_pcb').read_bytes()).hexdigest(),'physical_tests':'NOT PERFORMED'}
(out/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='models'})
