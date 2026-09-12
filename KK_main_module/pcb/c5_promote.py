"""Promote only the checked C.5 snapshot; refuse to overwrite new user edits."""
from pathlib import Path
import shutil,json,hashlib
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout';backup=root/'pcb/backups/pre_c5_relayout'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((out/'DRC.json').read_text());assert not d['violations'] and not d['unconnected_items'] and not d['schematic_parity']
v=json.loads((out/'VERIFICATION.json').read_text());assert v['board_sha256']==sha(out/'KK_main_module.kicad_pcb') and v['track_segments']>0
m=json.loads((out/'manufacturing/MANIFEST.json').read_text());assert m['revision']=='C.5'
for name,h in m['source_sha256'].items():assert sha(out/name)==h,name
for ext in ['kicad_pcb','kicad_sch','kicad_pro','kicad_dru']:
 name='KK_main_module.'+ext;assert sha(root/name)==sha(backup/name),'Root changed since snapshot; preserve and inspect '+name
for name in ['README.md','KK_main_module.pdf']:
 if (root/name).exists() and not (backup/name).exists():shutil.copy2(root/name,backup/name)
for ext in ['kicad_pcb','kicad_sch','kicad_pro','kicad_dru','pdf']:shutil.copy2(out/('KK_main_module.'+ext),root/('KK_main_module.'+ext))
archive=root/'archive/C4_manufacturing_superseded';archive.mkdir(exist_ok=True)
assert not (archive/'manufacturing').exists(),'Do not overwrite an archive'
shutil.move(str(root/'manufacturing'),str(archive/'manufacturing'))
shutil.copytree(out/'manufacturing',root/'manufacturing')
for name in ['front-fit-check.pdf','back-fit-check.pdf']:
 shutil.copy2(root/'pcb'/name,backup/name);shutil.copy2(out/name,root/'pcb'/name)
for name in ['ASSEMBLY_GUIDE.md','README.md']:
 if (root/'assembly'/name).exists():shutil.copy2(root/'assembly'/name,backup/('assembly_'+name))
for file in (out/'assembly').iterdir():
 if file.is_file() and file.name!='ASSEMBLY_GUIDE.md':shutil.copy2(file,root/'assembly'/file.name)
guide=(out/'assembly/ASSEMBLY_GUIDE.md').read_text().replace('../CIRCUIT_REVIEW.md','../C5_relayout/CIRCUIT_REVIEW.md').replace('../../component_review/','../component_review/')
(root/'assembly/ASSEMBLY_GUIDE.md').write_text(guide)
print('C.5 promoted. C.4 native sources and fabrication directory remain recoverable in backups/archive.')
