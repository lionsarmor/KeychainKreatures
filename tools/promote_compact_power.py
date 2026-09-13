"""One-shot, guarded P4 promotion. Archives P3 and issued C6/P3 packages intact.

Does not route, modify electrical CAD, order boards, or publish to GitHub.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / 'revisions/2026-09-12_power_compact'
CANDIDATE = WORK / 'P4_candidate'
ARCHIVE = WORK / 'P3_previous'
POWER = ROOT / 'KK_power_module'
MAIN = ROOT / 'KK_main_module'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def write(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, indent=2) + '\n')
def rel(p): return str(p.relative_to(ROOT))

assert not ARCHIVE.exists(), 'Promotion already started; inspect its manifest, do not overwrite'
processes = subprocess.check_output(['ps', '-eo', 'comm='], text=True).splitlines()
assert not {'kicad','pcbnew','eeschema'} & {p.strip() for p in processes}, 'Close KiCad first'
audit = read(CANDIDATE/'reports/COMPACT_CHANGE_AUDIT.json')
assert sha(POWER/'KK_power_module.kicad_pcb') == audit['source_p3_sha256']
assert sha(CANDIDATE/'KK_power_module.kicad_pcb') == audit['candidate_sha256']
assert sha(MAIN/'KK_main_module.kicad_pcb') == audit['main_unchanged_sha256']
for p, h in read(CANDIDATE/'SOURCE_BASELINE.json').items(): assert sha(ROOT/p) == h, p
for board in read(ROOT/'docs/C6_P3_RELEASE_INDEX.json')['boards']:
    assert sha(ROOT/board['zip']) == board['zip_sha256']
    assert sha(ROOT/board['gerbers_zip']) == board['gerbers_sha256']
for filename in ['DRC.json', 'ERC.json']:
    report = read(CANDIDATE/'reports'/filename)
    if filename == 'DRC.json':
        assert not report['violations'] and not report['unconnected_items'] and not report['schematic_parity']
    else: assert all(not s['violations'] for s in report['sheets'])
assert read(CANDIDATE/'release_checks/CAD_AUDIT.json')['status'].startswith('PASS')

manifest = {'state':'archiving', 'reason':'P4 compact power; main CAD unchanged', 'files':[]}
ARCHIVE.mkdir(parents=True)
def archive(source, destination, move=True):
    assert not destination.exists(), destination
    entries = sorted(source.rglob('*')) if source.is_dir() else [source]
    for p in entries:
        if p.is_file() and not p.name.endswith(('.kicad_prl','.lck')):
            q = destination/p.relative_to(source) if source.is_dir() else destination
            manifest['files'].append({'from':rel(p),'to':rel(q),'sha256':sha(p),'operation':'move' if move else 'snapshot'})
    destination.parent.mkdir(parents=True, exist_ok=True)
    if move: shutil.move(str(source), str(destination))
    elif source.is_dir(): shutil.copytree(source, destination)
    else: shutil.copy2(source, destination)
    write(WORK/'PROMOTION.json', manifest)

for p in sorted(POWER.iterdir()): archive(p, ARCHIVE/'KK_power_module'/p.name)
archive(MAIN/'manufacturing', ARCHIVE/'KK_main_module/manufacturing')
# Preserve every current instruction before changing the mechanical pairing.
for name in ['README.md','START_HERE.md','CHANGELOG.md','tools/README.md','revisions/README.md']:
    archive(ROOT/name, ARCHIVE/'instructions'/name, move=False)
for name in ['assembly','README.md','FABRICATION_REQUIREMENTS.md']:
    archive(MAIN/name, ARCHIVE/'instructions/KK_main_module'/name, move=False)
for p in sorted((ROOT/'docs').iterdir()): archive(p, ARCHIVE/'docs'/p.name)
desktop = Path('/home/legion/Desktop/PRINT THIS.pdf')
if desktop.exists(): archive(desktop, ARCHIVE/'PRINT_THIS_PREVIOUS.pdf', move=False) if desktop.is_relative_to(ROOT) else shutil.copy2(desktop, ARCHIVE/'PRINT_THIS_PREVIOUS.pdf')

for p in sorted(CANDIDATE.iterdir()):
    if p.is_dir(): shutil.copytree(p, POWER/p.name)
    else: shutil.copy2(p, POWER/p.name)
baseline = {rel(ARCHIVE/'KK_power_module'/Path(p).relative_to('KK_power_module')): h
            for p,h in read(CANDIDATE/'SOURCE_BASELINE.json').items()}
write(POWER/'SOURCE_BASELINE.json', baseline)
for p,h in baseline.items(): assert sha(ROOT/p)==h
for row in manifest['files']: assert sha(ROOT/row['to'])==row['sha256'], row['to']
manifest.update(state='promoted_pending_release', active_power_sha256=sha(POWER/'KK_power_module.kicad_pcb'),
                unchanged_main_sha256=sha(MAIN/'KK_main_module.kicad_pcb'))
write(WORK/'PROMOTION.json', manifest)
print(json.dumps({'state':manifest['state'],'archived_files':len(manifest['files']),'power_mm':[50,50],'main_mm':[96,105]},indent=2))
