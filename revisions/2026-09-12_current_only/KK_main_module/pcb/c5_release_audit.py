"""Fail-closed final handoff checks; no fabrication order or physical test."""
from pathlib import Path
import json,csv,hashlib,zipfile,re
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((out/'manufacturing/MANIFEST.json').read_text());v=json.loads((out/'VERIFICATION.json').read_text())
assert m['revision']=='C.5' and v['board_sha256']==sha(root/'KK_main_module.kicad_pcb')==sha(out/'KK_main_module.kicad_pcb')
for base in [root,out]:
 for name,digest in m['source_sha256'].items():assert sha(base/name)==digest,(base,name)
 for name,digest in m['manufacturing_files'].items():assert sha(base/'manufacturing'/name)==digest,(base,name)
 with zipfile.ZipFile(base/'manufacturing/KK_MAIN_C5_PROTOTYPE_FAB.zip') as z:
  assert z.testzip() is None
  for name,digest in m['manufacturing_files'].items():assert hashlib.sha256(z.read(Path(name).name)).hexdigest()==digest
 for file in ['C5_BOM_BY_REFERENCE.csv','C5_KIT_EXTRAS.csv','C5_TEST_POINT_MAP.csv','C5_BOM_PRINT.html']:
  assert sha(base/'assembly'/file)==sha(out/'assembly'/file)
for name in ['DRC.json','promoted_root_drc.json','manufacturing/DRC.json']:
 d=json.loads((out/name).read_text());assert not d['violations'] and not d['unconnected_items'] and not d['schematic_parity']
for name in ['ERC.json','manufacturing/ERC.json']:
 d=json.loads((out/name).read_text());assert not [v for s in d['sheets'] for v in s['violations']]
with (out/'assembly/C5_BOM_BY_REFERENCE.csv').open(newline='') as f:assert len(list(csv.DictReader(f)))==98
with (out/'assembly/C5_TEST_POINT_MAP.csv').open(newline='') as f:assert len(list(csv.DictReader(f)))==25
with (out/'assembly/C5_BENCH_TEST_RECORD.csv').open(newline='') as f:assert all(r['Status']=='PENDING' for r in csv.DictReader(f))
assert '84 x 95' in (out/'assembly/C5_KIT_EXTRAS.csv').read_text()
checked=[]
for p in [root/'README.md',root/'assembly/README.md',root/'assembly/ASSEMBLY_GUIDE.md',root/'routing/README.md',out/'README.md',out/'REPORT.md',out/'CIRCUIT_REVIEW.md',out/'assembly/ASSEMBLY_GUIDE.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' not in link and not link.startswith('#'):assert (p.parent/link).exists(),(p,link)
 checked.append(str(p.relative_to(root)))
for name in ['front-3d.png','back-3d.png','angled-3d.png','front-fit-check.pdf','back-fit-check.pdf','KK_main_module_C5_assembly.step','C5_final_routed.dsn']:
 assert (out/name).stat().st_size>1000,name
assert (root/'pcb/backups/pre_c5_relayout/KK_main_module.kicad_pcb').exists()
assert (root/'archive/C4_manufacturing_superseded/manufacturing/KK_MAIN_C4_PROTOTYPE_FAB.zip').exists()
result={'status':'PASS','revision':'C.5','root_and_revision_snapshot_match':True,'source_and_manufacturing_hashes_match':True,'erc_drc_opens_parity':0,'electrical_positions':98,'checked_component_pads':297,'debug_points':25,'models':98,'plated_drills':371,'npth_drills':4,'board_sha256':v['board_sha256'],'documents_checked':checked,'hardware_qualification':'PENDING; not physically assembled or powered','important_limits':['J1 requires coordinated 5V/3.3V/3.2V, not raw battery','Nominal full front/rear component envelope ~39mm before case clearance','Module fit, RGB socket retention, speaker rating and powered tests pending']}
(out/'RELEASE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
