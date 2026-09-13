"""Generate current C6/P4 assembly docs from archived C6/P3 text.

Preserves the electrical qualification instructions; explicitly replaces mechanics.
Run before sealing the new release, not over an issued package.
"""
from pathlib import Path
import csv, shutil
ROOT=Path(__file__).resolve().parent.parent
OLD=ROOT/'revisions/2026-09-12_power_compact/P3_previous'
MAIN=ROOT/'KK_main_module'; POWER=ROOT/'KK_power_module'
def put(p,t): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t)
def revised(t):
    return t.replace('C6_P3_RELEASE_INDEX.json','CURRENT_RELEASE_INDEX.json').replace('C6_P3_STATIC_AUDIT.json','CURRENT_STATIC_AUDIT.json').replace('C6_P3_STACK_REVIEW.pdf','C6_P4_MECHANICAL_REVIEW.pdf').replace('P.3','P.4').replace('P3_REVIEW_AND_TEST','P4_REVIEW_AND_TEST').replace('KK_POWER_P3_','KK_POWER_P4_').replace('KK_MAIN_C6_5_PROTOTYPE','KK_MAIN_C6_P4_PAIRING_5_PROTOTYPE').replace('KK_MAIN_C6_GERBERS','KK_MAIN_C6_P4_PAIRING_GERBERS')
def paragraphs(t, replacements):
    result=[]
    for p in t.split('\n\n'):
        for start,new in replacements.items():
            if p.startswith(start):p=new;break
        result.append(p)
    return '\n\n'.join(result)

t=revised((OLD/'KK_power_module/assembly/P3_REVIEW_AND_TEST.md').read_text())
t=paragraphs(t,{
 'Current board:':'Current board: **50 x 50 x 1.6 mm**, R3 corners, four layers. Four 2.2 mm M2 holes at (3,3), (47,3), (3,47), (47,47) mm. Main C.6 remains 96 x 105 mm: the holes DO NOT match. Use separate removable case supports. This package is for prototype DFM review; factory process/parts approval and physical/bench qualification remain required. Not a finished student product.',
 'P.4 preserves':'P.4 restores the original compact routed geometry from P.2 while retaining the repaired P.3 3D assets. Relative to P.3, every electrical pad/net/track/via is rigidly transformed by x=51-old_x, y=104-old_y (180 degrees, same layers). Outline and mounting holes are restored to 50 x 50 mm/R3; the oversized-board antenna keepout is removed. The complete compact board must instead be positioned clear of the main antenna. The wide 1.5 mm SYS_SW bridge on In1 and 0.6 mm C8 feed remain. In1 is NOT an uninterrupted ground plane. There are 3,515 track segments, 260 vias, 108 fitted parts and 28 rear bare test pads.',
 'All current coordinates':'All current coordinates come from the P.4 native PCB. In its native front view USB is at the top edge, the switch at the right edge and the harness connectors toward the bottom. Final case placement and orientation behind the main board are not frozen. Use independent supports; the old shared 20 mm four-standoff stack is superseded. Keep the entire power PCB, battery, harness and hardware clear of the main antenna region. Verify actual plugged JSTs, cable overmolds, wire bends and access to test pads. Clip solder tails to <=2.5 mm, inspect the joints and use insulating barriers. Cell position and board spacing still require a physical mock-up.',
 'TP4 is':'TP4 is system GND. TP3 is BAT_NEG, NOT GND. Never bypass battery protection by shorting those returns with grounded test equipment. Use the current P.4 TEST_POINTS.csv rather than old revision coordinates.'})
t=t.replace('four copper layers, 96 × 105 mm, 1.6 mm nominal thickness, R4 corners','four copper layers, 50 × 50 mm, 1.6 mm nominal thickness, R3 corners')
put(POWER/'assembly/P4_REVIEW_AND_TEST.md',t)
t=revised((OLD/'KK_power_module/assembly/FABRICATION_REQUIREMENTS.md').read_text()).replace('96 × 105 mm, 1.6 mm nominal, R4 corners','50 × 50 mm, 1.6 mm nominal, R3 corners')
t += '\nMounting centers in native top-left-origin coordinates: (3,3), (47,3), (3,47), (47,47) mm. Do not enlarge the outline to match main C.6. P.4 needs separate case supports.\n'
for p in [POWER/'FABRICATION_REQUIREMENTS.md',POWER/'assembly/FABRICATION_REQUIREMENTS.md']:put(p,t)

t=revised((OLD/'instructions/KK_main_module/assembly/ASSEMBLY_GUIDE.md').read_text())
t=t.replace('Both boards are 96 x 105 x 1.6 mm, R4 corners, four 2.2 mm mounting holes.','Main is 96 x 105 x 1.6 mm/R4; power is 50 x 50 x 1.6 mm/R3. Both have four 2.2 mm holes, but their mounting patterns DO NOT match.')
lines=t.splitlines()
for i,l in enumerate(lines):
    if l.startswith('7. For the first removable stack'):
        lines[i]='7. Mount the smaller power board behind main on independent removable case supports, not shared four-hole standoffs. Keep the power PCB, cell, wires and hardware clear of the main antenna. Main display/buttons face the user; final power orientation and board spacing need a mock-up with plugged connectors and wire bends. Main ESP32 rear envelope is about 15.3 mm; front RGB remains about 22.1 mm. Battery, fastener lengths and case depth are not frozen.'
put(MAIN/'assembly/ASSEMBLY_GUIDE.md','\n'.join(lines)+'\n')
put(MAIN/'FABRICATION_REQUIREMENTS.md',revised((OLD/'instructions/KK_main_module/FABRICATION_REQUIREMENTS.md').read_text())+'\nC.6 copper, drill and native CAD are unchanged. This refreshed package updates documentation for the compact P.4 pairing; separate mounting supports are required.\n')
with (OLD/'instructions/KK_main_module/assembly/C6_COMPLETE_KIT_EXTRAS.csv').open(newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
for r in rows:
    if r['Part / specification']=='M2 x 20 mm nylon female/female standoff':
        r.update({'Quantity per kit':'8 mounting points; hardware TBD','Part / specification':'Independent M2 insulating case supports; lengths TBD','Description':'Four main mounts and four separate compact-power mounts','Assembly note':'No common mounting pattern. Select removable supports and fasteners after the case mock-up; do not buy four shared 20 mm spacers.'})
    if r['Part / specification']=='M2 x 5 mm nylon screw':
        r.update({'Quantity per kit':'TBD after case design','Part / specification':'M2 nylon screws; lengths TBD','Description':'Fasteners for independent board supports','Assembly note':'Four 2.2 mm holes per board; confirm engagement and component clearance with chosen supports.'})
    if 'KK POWER P.3' in r['Part / specification']:
        r['Part / specification']='KK POWER P.4 assembled subassembly'
        r['Description']='50 x 50 x 1.6 mm four-layer R3 power PCB with 108 fitted positions'
with (MAIN/'assembly/C6_COMPLETE_KIT_EXTRAS.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

for name in ['README.md','START_HERE.md']:
    t=revised((OLD/'instructions'/name).read_text())
    t=t.replace('C.6/P.3','C.6/P.4').replace('C.6 / P.3','C.6 / P.4')
    t=t.replace('Both boards are 96 × 105 × 1.6 mm with matching mounting holes for a removable stack.','Main is 96 × 105 × 1.6 mm; power is now 50 × 50 × 1.6 mm. The power board needs independent removable case supports; mounting patterns do not match.')
    t=t.replace('Both boards use a **96 × 105 × 1.6 mm** outline with R4 corners and matching M2 mounting holes.','Main C.6 is **96 × 105 × 1.6 mm**, R4. Compact power P.4 is **50 × 50 × 1.6 mm**, R3. Each has four 2.2 mm M2 holes, but they require separate supports.')
    t=t.replace('The proposed 20 mm inter-board spacing is for a mock-up, not an approved enclosure dimension.','The previous common-hole 20 mm spacer plan is superseded. Power placement, antenna clearance and independent support heights need a physical mock-up.')
    t=t.replace('[matching drill audit](docs/C6_P3_DRILL_ALIGNMENT_AUDIT.json)','[individual outline/hole audit](docs/CURRENT_STATIC_AUDIT.json)')
    t=t.replace('The `manufacturing/` subfolders retain the issued full review packages and Gerber/drill ZIPs unchanged.','The `manufacturing/` subfolders contain the new C6/P4 review packages and Gerber/drill ZIPs. Prior issued packages remain unchanged in the compact-revision archive.')
    t=t.replace('This cleanup changes local paths and documentation only; no circuit, issued ZIP, Git commit or GitHub push is part of the move.','The current P.4 promotion changes the power outline and its absolute placement coordinates, not the circuit. Main C.6 CAD stays unchanged. Both review packages are refreshed; see the current release index. Historical move manifests remain recovery evidence.')
    put(ROOT/name,t)

t=revised((OLD/'docs/README.md').read_text())
t=t.replace(' · [Drill alignment](C6_P3_DRILL_ALIGNMENT_AUDIT.json)','')
t=t.replace('Do not mix older upright-resistor instructions, 84 × 95 mm main or 50 × 50 mm power Gerbers into the current 96 × 105 mm stack.','Use only current C.6 main and P.4 power packages. P.4 is 50 × 50 mm, but old P.2 files of the same size are not the current release. Main remains 96 × 105 mm; use separate mounting supports.')
t += '\nThe previous oversized P.3 board, C6/P3 packages and shared-hole reports are preserved in [the compact-revision archive](../revisions/2026-09-12_power_compact/P3_previous/). Main C.6 CAD and fabrication geometry are unchanged; its new review package replaces obsolete shared-stack documentation.\n'
put(ROOT/'docs/README.md',t)

t=revised((OLD/'KK_power_module/README.md').read_text())
t=t.replace('current P.4 matching stack','current P.4 compact module').replace('96 × 105 × 1.6 mm, four copper layers, R4 corners, matching C.6 mounting holes.','50 × 50 × 1.6 mm, four copper layers, R3 corners, four 2.2 mm holes at (3,3), (47,3), (3,47), (47,47) mm. It needs independent case supports; main C.6 remains 96 × 105 mm.')
put(POWER/'README.md',t)
put(MAIN/'README.md',revised((OLD/'instructions/KK_main_module/README.md').read_text()).replace('rounded corners and mounting holes matching power P.4','R4 rounded corners and its own mounting pattern. Compact power P.4 is 50 × 50 mm and needs separate supports'))
t=revised((OLD/'instructions/tools/README.md').read_text())
t=t.replace('C.6/P.3','C.6/P.4').replace('printable four-page stack review','printable four-page review with separate actual-size mounting templates')
t=t.replace('Issued review/Gerber ZIPs are unchanged snapshots. Their recorded original source paths remain historical metadata; docs/CURRENT_RELEASE_INDEX.json points to current source locations and verifies the same bytes.','New C6/P4 review/Gerber ZIPs are hash-bound snapshots. Main C.6 CAD and fabrication geometry are unchanged; power P.4 is compact. docs/CURRENT_RELEASE_INDEX.json lists the new packages; old snapshots are archived intact.')
t += '\n- `promote_compact_power.py`: completed guarded one-time promotion; refuses to overwrite its archive.\n- `compact_release_docs.py`: generates current guides from preserved pre-promotion text; run only before sealing a release.\n- `current_release.py`: fresh sequential native checks and immutable C6/P4 packages; refuses existing outputs.\n- `power_compact_candidate.py`: historical one-shot candidate builder, not a current routing command. Its source assumptions refer to the pre-promotion P.3 root.\n'
put(ROOT/'tools/README.md',t)
put(ROOT/'CHANGELOG.md','''# Release notes

## 2026-09-12 — compact P.4 power / unchanged C.6 main

- Restored power to 50 × 50 × 1.6 mm, R3 corners and its original four mounting holes. Main stays 96 × 105 mm/R4; separate case supports replace the shared-hole stack plan.
- Preserved the routed electrical core and repaired P.3 models. All electrical pad/net/track/via geometry matches the original compact core after rigid transformation; no circuit redesign or global autoroute.
- Archived the oversized P.3 source and previous issued packages intact. Current native projects are directly at the two module roots.
- Refreshed both manufacturing review packages, BOM/placement/maps, native checks, mechanical print sheet and assembly documentation. Main CAD and manufacturing geometry remain unchanged.
- Hardware is still an engineering prototype: factory DFM/process approval, physical fit, battery selection and bench qualification remain open. No order or production approval is implied.

Previous release notes are preserved in [the pre-promotion instructions](revisions/2026-09-12_power_compact/P3_previous/instructions/CHANGELOG.md).
''')
put(ROOT/'revisions/2026-09-12_power_compact/README.md','''# Compact power revision — recovery map

Current projects are at the repository's KK_main_module and KK_power_module roots, not here.

- P4_candidate: preserved compact candidate and its original audit context, before promotion/export.
- P3_previous/KK_power_module: oversized P.3 source, supporting files and issued packages, unchanged.
- P3_previous/KK_main_module/manufacturing: previous issued C.6 packages, unchanged.
- P3_previous/instructions and P3_previous/docs: superseded instructions and shared-hole reports.
- PROMOTION.json: SHA-256 recovery map from original paths to preserved copies. Candidate audit status records its pre-promotion stage; current source-bound checks are in the active release package.

Old files are historical evidence, not current assembly instructions. Restore to a scratch directory, never over the active boards. The former matching-outline and 20 mm shared-standoff instructions no longer apply.
''')
put(ROOT/'revisions/README.md',(OLD/'instructions/revisions/README.md').read_text()+'\n## Compact power P.4\n\nSee [2026-09-12_power_compact](2026-09-12_power_compact/) for the preserved P.3 projects, prior packages, source snapshots and promotion hash map. Current power is 50 × 50 mm with separate mounts; main C.6 remains unchanged.\n')
print('Current assembly, BOM extras and navigation generated; packages not sealed yet.')
