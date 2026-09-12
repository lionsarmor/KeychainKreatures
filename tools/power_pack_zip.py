"""Finish packaging an already published, hash-checked CAD review.
Preserve any incomplete archive; support reproducible library timestamps.
"""
from pathlib import Path
import hashlib,json,zipfile,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'KK_power_module/manufacturing/P2_5_SAMPLE_REVIEW_2026-09-12'
ARC=ROOT/'revisions/2026-09-12_power_final'
OLD=ROOT/'KK_power_module/manufacturing/P2_5_SAMPLE_REVIEW'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((OUT/'SHA256_MANIFEST.json').read_text())
for entry in manifest['files']:assert sha(OUT/entry['path'])==entry['sha256'],entry['path']
ver=json.loads((OUT/'verification/VERIFICATION.json').read_text())
assert sha(ROOT/'KK_power_module/P2_compact/KK_power_module.kicad_pcb')==ver['PCB_SHA256']
archive=OUT.with_suffix('.zip');incomplete=ARC/'incomplete_review_zip.zip'
if archive.exists():
    assert not incomplete.exists(),'Do not overwrite a preserved archive'
    archive.rename(incomplete)
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=5,strict_timestamps=False) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,str(p.relative_to(OUT.parent)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for entry in manifest['files']:assert hashlib.sha256(z.read(OUT.name+'/'+entry['path'])).hexdigest()==entry['sha256']
(archive.with_suffix('.zip.sha256')).write_text(sha(archive)+'  '+archive.name+'\n')
(ARC/'manufacturing').mkdir(exist_ok=True)
for old in [OLD,OLD.with_suffix('.zip')]:
    dest=ARC/'manufacturing'/old.name
    assert old.exists() and not dest.exists()
    shutil.move(str(old),str(dest))
print(json.dumps({'zip':str(archive),'verified_files':len(manifest['files']),'bytes':archive.stat().st_size,'sha256':sha(archive),'old_release_preserved':str(ARC/'manufacturing')},indent=2))
