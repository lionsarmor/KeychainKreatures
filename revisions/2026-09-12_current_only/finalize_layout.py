"""One-time local cleanup finalization; no circuit, Git or issued-package edits."""
from pathlib import Path
import json, hashlib, shutil, subprocess, re
ROOT=Path(__file__).resolve().parents[2]
ARC=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
index=read(ROOT/'docs/C6_P3_RELEASE_INDEX.json')
move=read(ARC/'MOVE_MANIFEST.json')
report={'scope':'Current-only relocation; exact CAD/issued ZIP hashes preserved; fresh native checks at new paths', 'sources':{}, 'archive':str(ARC.relative_to(ROOT)), 'checks':{}, 'no_circuit_edits':True, 'no_git_commit_or_push':True}
for p,h in move['protected_current_files'].items():
    assert sha(ROOT/p)==h,p
report['protected_file_count']=len(move['protected_current_files'])
for b in index['boards']:
    src=ROOT/b['source'];stem='KK_'+b['kind']+'_module'
    assert not (src/('C6_flat_stack' if b['kind']=='main' else 'P3_matching_stack')).exists()
    drc=read(src/'reports/POST_MOVE_DRC.json');erc=read(src/'reports/POST_MOVE_ERC.json')
    assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
    assert all(not s['violations'] for s in erc['sheets'])
    report['sources'][b['kind']]=str(src.relative_to(ROOT)/(stem+'.kicad_pro'))
    report['checks'][b['kind']]={'erc':0,'drc':0,'opens':0,'parity':0,'pcb_sha256':sha(src/(stem+'.kicad_pcb')),'drc_report_sha256':sha(src/'reports/POST_MOVE_DRC.json'),'erc_report_sha256':sha(src/'reports/POST_MOVE_ERC.json')}
# Preserve earlier print bytes, update only the live convenience sheets.
doc=ROOT/'docs/C6_P3_STACK_REVIEW.pdf'
backup=ARC/'metadata/C6_P3_STACK_REVIEW_before_cleanup.pdf'
assert not backup.exists(),'Finalization already performed'
shutil.copy2(doc,backup)
desktop=ROOT.parent/'PRINT THIS.pdf'
if desktop.exists():shutil.copy2(desktop,ARC/'metadata/PRINT_THIS_before_current_only.pdf')
subprocess.run(['python3',str(ROOT/'tools/flat_stack_report.py')],check=True)
shutil.copy2(doc,desktop)
report['print_sheet']=str(desktop);report['print_sheet_sha256']=sha(doc)
# Check current navigation only; archived/package snapshots keep original locations.
docs=['README.md','START_HERE.md','CONTRIBUTING.md','CHANGELOG.md','docs/README.md','docs/FLAT_STACK_REWORK.md','tools/README.md','KK_main_module/README.md','KK_power_module/README.md','revisions/README.md']
links=[]
for name in docs:
    p=ROOT/name
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if re.match(r'^(https?:|mailto:|#)',target):continue
        target=target.split('#')[0]
        resolved=(p.parent/target).resolve()
        assert resolved.is_relative_to(ROOT) and resolved.exists(),(name,target)
        links.append([name,target])
report['current_links_checked']=len(links)
report['preserved_archive_files']=sum(r['to'].startswith(str(ARC.relative_to(ROOT))+'/') for r in move['files'])
for p,h in move['protected_current_files'].items():assert sha(ROOT/p)==h,p
(ROOT/'docs/CURRENT_LAYOUT_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
