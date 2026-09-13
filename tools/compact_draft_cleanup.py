"""One-time preservation of unissued export draft and superseded live P3 guide."""
from pathlib import Path
import shutil,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
DEST=ROOT/'revisions/2026-09-12_power_compact/unissued_export_1'
assert not DEST.exists()
assert not (ROOT/'docs/CURRENT_RELEASE_INDEX.json').exists(),'Issued outputs must not be altered'
paths=[
 'KK_main_module/manufacturing/KK_MAIN_C6_P4_PAIRING_5_PROTOTYPE_REVIEW_2026-09-12',
 'KK_main_module/release_checks/fabrication_P4_pairing',
 'KK_main_module/release_checks/fabrication',
 'KK_main_module/assembly/P3_REVIEW_AND_TEST.md',
]
rows=[]
for name in paths:
    p=ROOT/name;assert p.exists(),p
    target=DEST/name;target.parent.mkdir(parents=True,exist_ok=True)
    for f in sorted(p.rglob('*')) if p.is_dir() else [p]:
        if f.is_file():rows.append({'from':str(f.relative_to(ROOT)),'to':str((target/f.relative_to(p) if p.is_dir() else target).relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    shutil.move(str(p),str(target))
shutil.copy2(ROOT/'KK_power_module/assembly/P4_REVIEW_AND_TEST.md',ROOT/'KK_main_module/assembly/P4_REVIEW_AND_TEST.md')
(DEST/'MOVE_MANIFEST.json').write_text(json.dumps({'status':'unissued draft; superseded during documentation preflight','files':rows},indent=2)+'\n')
print('Preserved unissued draft and superseded live P3 guide; current live guides now P4.')
