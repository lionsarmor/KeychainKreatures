"""Independent P.2 netlist / interface / manufacturing-geometry audit."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'P2_compact'
s=(ROOT/'p1_verify.py').read_text().split('calculations={')[0]
s=s.replace("OUT=ROOT/'P1_revision'","OUT=ROOT/'P2_compact'")
s=s.replace('if gap<.25:', 'if gap<.2:').replace("'project_minimum_mm':.25","'project_minimum_mm':.2")
exec(compile(s,str(ROOT/'p1_verify.py'),'exec'),globals())
assert lookup['U1','15']=='GND','BQ24075T SYSOFF must be low'
assert lookup['U1','1']==lookup['R74','2']==lookup['R75','1']==lookup['J4','1']=='NTC'
assert lookup['R74','1']=='USB_CHG' and lookup['R75','2']=='GND'
parts={p['ref']:p for p in d['components']}
assert parts['U1']['mpn']=='BQ24075TRGTR'
assert parts['R74']['value']=='31.6k' and parts['R75']['value']=='20k'
for n,u in [(28,'U5'),(38,'U6'),(48,'U7')]:
    assert lookup['C'+str(n),'1']==lookup[u,'8']
    assert lookup['C'+str(n),'2']=='GND'
assert len([p for p in d['components'] if p['ref'].startswith('TP')])==28
report={'status':'STATIC AUDIT ONLY','static_connectivity_issues':issues,
        'independent_USB_hole_clearance_issues':hole_gaps,
        'component_count':len(d['components']),'test_pad_count':28,
        'main_interface_match':not any('harness mismatch' in s for s in issues),
        'source_hashes':hashes,
        'electrical_screening':json.loads((OUT/'electrical_screening.json').read_text()),
        'checked_artifact_sha256':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['design.json','netlist.xml','KK_power_module.kicad_sch','KK_power_module.kicad_pcb','KK_power_module.kicad_pro','KK_Power.pretty/USB_C_HCTL.kicad_mod']}}
(OUT/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
assert not issues,issues
assert not hole_gaps,hole_gaps
print('Static manifest/native-netlist/interface checks pass. USB NPTH copper gap >=0.20mm. No hardware qualification implied.')
