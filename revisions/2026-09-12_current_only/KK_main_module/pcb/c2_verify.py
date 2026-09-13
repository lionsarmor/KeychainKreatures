"""Read-only checks of the promoted board against schematic and placement."""
from pathlib import Path
import json,xml.etree.ElementTree as ET,hashlib
import pcbnew as k
root=Path(__file__).resolve().parent.parent;b=k.LoadBoard(str(root/'KK_main_module.kicad_pcb'))
xml=ET.parse(root/'pcb/board_netlist.xml').getroot()
expected={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'] for net in xml.findall('./nets/net') for n in net.findall('node')}
rows=json.loads((root/'pcb/footprint_assignments.json').read_text());fps={f.GetReference():f for f in b.GetFootprints()}
errors=[];pads=0
for r in rows:
    f=fps[r['ref']];ps={p.GetNumber():p for p in f.Pads()}
    if f.GetValue()!=r['value'] or f.GetField('MPN').GetText()!=r['mpn']:errors.append(r['ref']+' population metadata')
    if f.GetPath().AsString()!=r['path']:errors.append(r['ref']+' schematic UUID path')
    want={n for ref,n in expected if ref==r['ref']}
    if set(ps)!=want:errors.append(r['ref']+' pin numbers')
    for n,p in ps.items():
        pads+=1
        if p.GetNetname()!=expected.get((r['ref'],n)):errors.append(r['ref']+':'+n+' net')
        if p.GetAttribute()!=k.PAD_ATTRIB_PTH:errors.append(r['ref']+':'+n+' not PTH')
before=k.LoadBoard(str(root/'routing/KK_main_module_C2_unrouted.kicad_pcb'));old={f.GetReference():f for f in before.GetFootprints()}
rounding=[]
for ref,f in fps.items():
    dx=f.GetPosition().x-old[ref].GetPosition().x;dy=f.GetPosition().y-old[ref].GetPosition().y
    if dx or dy:rounding.append({'ref':ref,'delta_nm':[dx,dy]})
    if max(abs(dx),abs(dy))>100 or f.GetOrientationDegrees()!=old[ref].GetOrientationDegrees():errors.append(ref+' moved beyond DSN 0.1um quantization')
rules=json.loads((root/'pcb/C2_ROUTING_RULES.json').read_text());widths={n:w for n,w,_,_ in rules['classes']}
for t in b.GetTracks():
    if t.GetClass()!='PCB_VIA':
        name=rules['assignments'].get(t.GetNetname(),'Default')
        if k.ToMM(t.GetWidth())+1e-6<widths[name]:errors.append('Undersized '+t.GetNetname())
zones=[{'name':z.GetZoneName(),'rule_area':z.GetIsRuleArea(),'net':z.GetNetname(),'layers':list(z.GetLayerSet().Seq()),'filled':z.IsFilled()} for z in b.Zones()]
assert len([z for z in zones if z['rule_area']])==2
assert len([z for z in zones if not z['rule_area'] and z['net']=='/GND' and z['filled']])==2
npth=sum(p.GetAttribute()==k.PAD_ATTRIB_NPTH for f in fps.values() for p in f.Pads())
assert len(rows)==91 and pads==267 and npth==4
report={'status':'C.2 ROUTED ENGINEERING PROTOTYPE','schematic_components':len(rows),'component_pads':pads,'npth_mounting_holes':npth,'mismatches':errors,'import_coordinate_rounding':rounding,'zones':zones,'board_sha256':hashlib.sha256((root/'KK_main_module.kicad_pcb').read_bytes()).hexdigest(),'tracks_and_vias':len(list(b.GetTracks()))}
(root/'pcb/C2_FINAL_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
assert not errors,errors
print(json.dumps(report,indent=2))
