"""Read-only release consistency checks; writes only a derived audit report."""
from pathlib import Path
import csv,json,hashlib,zipfile,re,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent.parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(name):
    with (root/name).open(newline='') as f:return list(csv.DictReader(f))
manifest=json.loads((root/'manufacturing/MANIFEST.json').read_text())
assert manifest['revision']=='C.3'
for name,sha in manifest['source_sha256'].items():assert digest(root/name)==sha,name
for name,sha in manifest['manufacturing_files'].items():assert digest(root/'manufacturing'/name)==sha,name
for key in ['erc_violations','drc_violations','unconnected_items','schematic_parity_issues']:assert manifest[key]==0
with zipfile.ZipFile(root/'manufacturing/KK_MAIN_C3_PROTOTYPE_FAB.zip') as z:
    assert z.testzip() is None
    for name in manifest['manufacturing_files']:
        assert z.read(Path(name).name)==(root/'manufacturing'/name).read_bytes(),name
    for name in ['README.md','MANIFEST.json','DRILL_REPORT.txt']:
        assert z.read(name)==(root/'manufacturing'/name).read_bytes(),name
with zipfile.ZipFile(root/'assembly/C3_DATASHEETS.zip') as z:
    assert z.testzip() is None
    ds=json.loads(z.read('C3_DATASHEET_MANIFEST.json'))
    for d in ds:assert hashlib.sha256(z.read(d['file'])).hexdigest()==d['sha256']
xml=ET.parse(root/'pcb/c3_netlist.xml').getroot()
comps={c.attrib['ref']:c for c in xml.findall('./components/comp')}
bom=rows('assembly/C3_BOM_BY_REFERENCE.csv')
assert len(bom)==98 and {r['Reference'] for r in bom}==set(comps)
for r in bom:
    c=comps[r['Reference']];fields={f.attrib['name']:f.text or '' for f in c.findall('./fields/field')}
    assert r['MPN']==fields['MPN'] and r['Value']==c.findtext('value') and r['Footprint']==c.findtext('footprint')
assert sum(int(r['Quantity']) for r in rows('assembly/C3_PCB_BOM.csv'))==98
extras=rows('assembly/C3_KIT_EXTRAS.csv');assert any(r['Part / specification']=='ED16DT' for r in extras)
assert len(rows('assembly/C3_TEST_POINT_MAP.csv'))==25
assert all(r['Status']=='PENDING' for r in rows('assembly/C3_BENCH_TEST_RECORD.csv'))
checked=[]
for name in ['README.md','C3_PROTOTYPE_REPORT.md','assembly/README.md','assembly/ASSEMBLY_GUIDE.md','pcb/README.md','routing/README.md']:
    p=root/name
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' not in target and not target.startswith('#'):assert (p.parent/target).exists(),(name,target)
    checked.append(name)
report={'status':'PASS','revision':'C.3 RGB','source_and_export_hashes_verified':True,'fabrication_zip_matches_outputs':True,'datasheet_zip_integrity_verified':True,'bom_components':len(bom),'kit_extra_rows':len(extras),'local_document_links_checked':checked,'physical_tests':'PENDING; no hardware test is claimed','board_sha256':digest(root/'KK_main_module.kicad_pcb')}
(root/'pcb/C3_RELEASE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
