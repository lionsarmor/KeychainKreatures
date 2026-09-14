"""Prepare a local PCBWay submission snapshot; never edit CAD or place orders.

Run sequentially with nice/taskset. Existing differing outputs are not overwritten.
Use --verify for read-only source/copy, inventory and centroid validation.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'PCBWay'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rel(p):
    return p.relative_to(ROOT).as_posix()


def emit(name, data):
    p = OUT / name
    data = data.encode() if isinstance(data, str) else data
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        if p.read_bytes() != data:
            raise RuntimeError(f'Refusing to overwrite changed output: {p}')
    else:
        p.write_bytes(data)
    return p


def emit_json(name, data):
    return emit(name, json.dumps(data, indent=2) + '\n')


def emit_csv(name, headers, rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=headers, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return emit(name, stream.getvalue())


def rows(p):
    with p.open(newline='') as f:
        return list(csv.DictReader(f))


def check_centroid():
    base = OUT / '02_Power_P4/03_Pick_and_Place_Upload'
    native = rows(base / 'REFERENCE_ALL_108_NATIVE_POSITIONS.csv')
    smt = rows(base / 'UPLOAD_SMT_CENTROID_MM.csv')
    mixed = rows(base / 'ATTACH_THT_MIXED_OPERATIONS_MM.csv')
    bom = rows(OUT / '02_Power_P4/02_BOM_Upload/UPLOAD_POWER_P4_BOM.csv')
    refs = {}
    for group in bom:
        group_refs = [r.strip() for r in group['References'].split(',')]
        assert len(group_refs) == int(group['Quantity per board'])
        assert len(group_refs) * 5 == int(group['Quantity for 5 (no attrition)'])
        for ref in group_refs:
            assert ref not in refs, ref
            refs[ref] = group['Assembly']
    assert len(refs) == len(native) == 108
    assert len({r['Ref'] for r in native}) == 108
    expected = {r['Ref']: r for r in native}
    assert set(expected) == set(refs)
    assert len(smt) == 104 and len(mixed) == 4
    assert {r['Ref'] for r in mixed} == {'J1', 'J2', 'J3', 'J4'}
    assert {r['Ref'] for r in smt}.isdisjoint(r['Ref'] for r in mixed)
    for group, assembly in [(smt, 'SMT'), (mixed, 'THT/mixed')]:
        for row in group:
            assert row == expected[row['Ref']], row['Ref']
            assert refs[row['Ref']] == assembly
            assert row['Side'] == 'top'
    return {'fitted_per_board': 108, 'SMT': 104, 'THT_mixed': 4,
            'THT_mixed_refs': sorted(r['Ref'] for r in mixed),
            'coordinate_transform': 'NONE; original native mm/Y-up/origin/rotation retained',
            'status': 'PASS reference sets and exact native field preservation; NOT machine calibration'}


def verify():
    inventory = json.loads((OUT / 'PACKAGE_MANIFEST.json').read_text())
    for name, digest in inventory['files'].items():
        assert sha(OUT / name) == digest, name
    copies = json.loads((OUT / 'SOURCE_COPY_MANIFEST.json').read_text())['files']
    for item in copies:
        assert sha(ROOT / item['source']) == item['sha256'], item['source']
        assert sha(OUT / item['destination']) == item['sha256'], item['destination']
    for name in inventory['files']:
        p = OUT / name
        if p.suffix == '.zip':
            with zipfile.ZipFile(p) as archive:
                assert archive.testzip() is None, p
    link_count = 0
    for p in OUT.rglob('*.md'):
        # Authored portal instructions only; copied release guides intentionally
        # retain source-package-relative links and ship with full reference ZIPs.
        if p.name not in {'README.md', 'START_HERE.md'}:
            continue
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if target.startswith(('https:', 'http:', '#')):
                continue
            assert (p.parent / target.split('#')[0]).exists(), (p, target)
            link_count += 1
    for item in rows(OUT / '00_Order_Setup/UPLOAD_MAP.csv'):
        assert (OUT / item['File relative to PCBWay']).exists(), item
    return {'files_in_snapshot': len(inventory['files']),
            'byte_identical_source_copies': len(copies), 'instruction_links': link_count,
            'centroid': check_centroid(), 'order_placed': False,
            'manufacturer_approved': False, 'physical_or_powered_test': False,
            'status': 'PASS — local submission snapshot only'}


def build():
    if (OUT / 'PACKAGE_MANIFEST.json').exists():
        return verify()
    result = subprocess.run(['node', str(ROOT / 'tools/check_project.mjs'), '--published'],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    check = json.loads(result.stdout)
    assert check['errors'] == []
    emit_json('00_Order_Setup/RELEASE_CONSISTENCY_CHECK.json', check)
    index = json.loads((ROOT / 'docs/CURRENT_RELEASE_INDEX.json').read_text())
    copies = []

    def copy(source, destination):
        source = ROOT / source if isinstance(source, str) else source
        data = source.read_bytes()
        target = emit(destination, data)
        assert sha(source) == sha(target)
        copies.append({'source': rel(source), 'destination': destination, 'sha256': sha(source)})

    for item in index['boards']:
        main = item['kind'] == 'main'
        label = 'MAIN_C6' if main else 'POWER_P4'
        board = '01_Main_C6' if main else '02_Power_P4'
        package = ROOT / item['directory']
        assert sha(ROOT / item['zip']) == item['zip_sha256']
        assert sha(ROOT / item['gerbers_zip']) == item['gerbers_sha256']
        copy(item['gerbers_zip'], f'{board}/01_Gerber_Upload/UPLOAD_{label}_GERBERS.zip')
        copy(package / 'FABRICATION_REQUIREMENTS.md', f'{board}/01_Gerber_Upload/FABRICATION_REQUIREMENTS.md')
        full_name = 'FULL_MAIN_C6_REVIEW.zip' if main else 'FULL_POWER_P4_REVIEW.zip'
        copy(item['zip'], f'{board}/05_Full_Review_Package/{full_name}')
        copy(package / 'RELEASE_VERIFICATION.json', f'{board}/05_Full_Review_Package/RELEASE_VERIFICATION.json')
        drawing_dir = f'{board}/02_Drawings_and_Reference' if main else f'{board}/04_Assembly_Drawings'
        for p in sorted((package / 'drawings').iterdir()):
            if p.suffix in {'.pdf', '.png'}:
                copy(p, f'{drawing_dir}/{p.name}')
        for name in ['SCHEMATIC.pdf', 'CONNECTOR_PIN_MAP.csv', 'ASSEMBLY_GUIDE.md']:
            copy(package / 'assembly' / name, f'{drawing_dir}/{name}')
        if main:
            for name in ['C6_front_FIT_100_PERCENT.pdf', 'C6_back_FIT_100_PERCENT.pdf']:
                copy(package / 'assembly' / name, f'{drawing_dir}/{name}')
        else:
            bompath = package / 'assembly/BOM_GROUPED_5_BOARDS.csv'
            copy(bompath, f'{board}/02_BOM_Upload/UPLOAD_POWER_P4_BOM.csv')
            base = f'{board}/03_Pick_and_Place_Upload'
            nativepath = package / 'assembly/POSITIONS_NATIVE.csv'
            copy(nativepath, f'{base}/REFERENCE_ALL_108_NATIVE_POSITIONS.csv')
            copy(package / 'assembly/BOM_AND_PLACEMENT.csv', f'{base}/REFERENCE_CAD_Y_DOWN_BOM_AND_PLACEMENT.csv')
            assembly = {ref.strip(): row['Assembly'] for row in rows(bompath)
                        for ref in row['References'].split(',')}
            native = rows(nativepath)
            headers = list(native[0])
            for filename, kind in [('UPLOAD_SMT_CENTROID_MM.csv', 'SMT'),
                                   ('ATTACH_THT_MIXED_OPERATIONS_MM.csv', 'THT/mixed')]:
                emit_csv(f'{base}/{filename}', headers, [r for r in native if assembly[r['Ref']] == kind])
            emit_json(f'{base}/CENTROID_VERIFICATION.json', check_centroid())
            copy(package / 'assembly/VIA_IN_PAD_REVIEW.csv', f'{board}/01_Gerber_Upload/VIA_IN_PAD_REVIEW.csv')
            copy(package / 'assembly/VIA_IN_PAD_REVIEW.csv', '03_Factory_DFM_and_Questions/POWER_VIA_IN_PAD_REVIEW.csv')
        copy(package / 'FABRICATION_REQUIREMENTS.md', f'03_Factory_DFM_and_Questions/{label}_FABRICATION_REQUIREMENTS.md')

    for source, name in [
        ('KK_main_module/assembly/TROUBLESHOOTING_MAIN_C6.pdf', 'MAIN_TROUBLESHOOTING.pdf'),
        ('KK_power_module/assembly/TROUBLESHOOTING_POWER_P4.pdf', 'POWER_TROUBLESHOOTING.pdf'),
        ('KK_main_module/assembly/TROUBLESHOOTING_C6_CHECKLIST.csv', 'MAIN_BLANK_CHECKLIST.csv'),
        ('KK_main_module/assembly/TROUBLESHOOTING_C6_MEASUREMENTS.csv', 'MAIN_BLANK_MEASUREMENTS.csv'),
        ('KK_power_module/assembly/TROUBLESHOOTING_P4_CHECKLIST.csv', 'POWER_BLANK_CHECKLIST.csv'),
        ('KK_power_module/assembly/TROUBLESHOOTING_P4_MEASUREMENTS.csv', 'POWER_BLANK_MEASUREMENTS.csv'),
        ('KK_power_module/assembly/P4_REVIEW_AND_TEST.md', 'P4_REVIEW_AND_TEST.md'),
        ('KK_main_module/assembly/C6_COMPLETE_KIT_EXTRAS.csv', 'KIT_EXTRAS_FOR_LOCAL_BUILD.csv'),
        ('docs/troubleshooting/FACTORY_FAULT_REPORT.pdf', 'FACTORY_FAULT_REPORT.pdf'),
        ('docs/C6_P4_MECHANICAL_REVIEW.pdf', 'MECHANICAL_REVIEW_PRINT_100_PERCENT.pdf'),
    ]:
        copy(source, '05_Delivery_and_Testing/' + name)

    settings = [
        ('Job scope', '5 bare PCBs', '5 assembled boards', 'Confirm fabrication attrition separately for power'),
        ('Revision', 'C.6', 'P.4', 'Do not mix older revisions'),
        ('Dimensions mm', '96 x 105', '50 x 50', 'Preserve actual Gerber outline; do not scale'),
        ('Copper layers', '2', '4', 'Power F.Cu/In1.Cu/In2.Cu/B.Cu'),
        ('Thickness mm', '1.6 nominal', '1.6 nominal', 'Confirm final stackup'),
        ('Material', 'FR-4', 'FR-4', 'Confirm manufacturer grade and process'),
        ('Copper', '35 um CAD nominal', '35 um CAD nominal layers', 'Confirm finished copper/plating; not a fabricated stackup approval'),
        ('Mask/silkscreen', 'Green / white proposed', 'Green / white proposed', 'Cosmetic proposal; both supplied silk sides retained'),
        ('Finish', 'Lead-free HASL proposed', 'ENIG proposed', 'Power flatness must suit 0.4 mm WCSP; assembler approval required'),
        ('Via process', 'Review normal vias against files', 'Filled capped planarized component-pad vias REQUIRED', 'Tenting is not a substitute on power'),
        ('Assembly', 'NO', 'YES: 108 positions per board', 'Power 104 SMT + 4 mixed/THT connectors'),
        ('Stencil', 'Not requested', 'Assembler to quote/approve', 'Do not guess stencil thickness'),
        ('Electrical test', 'Request bare-board net test', 'Request bare-board net test and assembly inspection', 'Functional testing is separate agreed scope'),
        ('Battery / firmware / case', 'Not included', 'Not included', 'Do not attach an unspecified cell'),
        ('Release status', 'Hold pending DFM/customer approval', 'Hold pending DFM/customer approval', 'No purchase or factory submission performed'),
    ]
    emit_csv('00_Order_Setup/ORDER_SETTINGS.csv', ['Field', 'Main C6', 'Power P4', 'Notes'],
             [dict(zip(['Field', 'Main C6', 'Power P4', 'Notes'], r)) for r in settings])
    uploads = [
        ('Main PCB quote', 'Gerber upload', '01_Main_C6/01_Gerber_Upload/UPLOAD_MAIN_C6_GERBERS.zip', 'Five bare main boards only'),
        ('Power PCB + assembly quote', 'Gerber upload', '02_Power_P4/01_Gerber_Upload/UPLOAD_POWER_P4_GERBERS.zip', 'Five assembled power boards; four layers'),
        ('Power assembly', 'BOM upload', '02_Power_P4/02_BOM_Upload/UPLOAD_POWER_P4_BOM.csv', 'Per-board and five-board quantities; no attrition'),
        ('Power assembly', 'Centroid upload', '02_Power_P4/03_Pick_and_Place_Upload/UPLOAD_SMT_CENTROID_MM.csv', '104 SMT; native mm/Y-up'),
        ('Power assembly', 'Supplemental operations', '02_Power_P4/03_Pick_and_Place_Upload/ATTACH_THT_MIXED_OPERATIONS_MM.csv', 'J1-J4 still fitted; J1 mixed SMT contacts'),
        ('Power DFM', 'Special requirements', '02_Power_P4/01_Gerber_Upload/FABRICATION_REQUIREMENTS.md', 'Required process approval'),
        ('Main review', 'Supplemental engineering attachment', '01_Main_C6/05_Full_Review_Package/FULL_MAIN_C6_REVIEW.zip', 'Not another order or Gerber upload'),
        ('Power review', 'Supplemental engineering attachment', '02_Power_P4/05_Full_Review_Package/FULL_POWER_P4_REVIEW.zip', 'Not another order or Gerber upload'),
        ('Both jobs', 'Message / correspondence', '00_Order_Setup/QUOTE_REQUEST.txt', 'Request review only, hold production'),
    ]
    fields = ['Job', 'Step', 'File relative to PCBWay', 'Notes']
    emit_csv('00_Order_Setup/UPLOAD_MAP.csv', fields, [dict(zip(fields, row)) for row in uploads])
    questions = [
        'Confirm two separate jobs and quantities: 5 main bare, 5 power assembled; attrition separate',
        'Confirm correct dimensions, drill/outline registration and two/four copper layers',
        'Approve actual finished copper/plating and four-layer stackup',
        'Approve filled capped planarized via-in-pad; evaluate full and partial pad overlaps',
        'Approve U13 TPS22950YBHR base variant WCSP and other fine-pitch packages',
        'Approve finish, mask registration, paste apertures, stencil and panel tooling',
        'Confirm every actual manufacturer/orderable MPN and all sourcing proposals',
        'Approve each proposed substitution individually before purchasing',
        'Validate native mm/Y-up origin, rotation and polarity against component drawings',
        'Confirm 104 SMT plus J1-J4 mixed/THT operations; no omitted connectors',
        'Confirm IPC-D-356 bare-board electrical test and retained reports',
        'Agree hidden-joint/X-ray inspection method and cost',
        'Agree any powered-test scope separately; no unspecified battery or firmware',
        'Approve total cost, attrition, tooling, shipping/taxes and lead time',
        'Customer explicitly releases final approved files and quote in writing',
    ]
    emit_csv('03_Factory_DFM_and_Questions/DFM_RESPONSE_CHECKLIST.csv',
             ['ID', 'Question', 'Status', 'Supplier response / file', 'Customer decision'],
             [{'ID': f'DFM-{i:02}', 'Question': q, 'Status': 'PENDING',
               'Supplier response / file': '', 'Customer decision': ''}
              for i, q in enumerate(questions, 1)])
    emit_json('SOURCE_COPY_MANIFEST.json', {'scope': 'Byte-identical copies; source CAD/release unchanged', 'files': copies})
    files = {p.relative_to(OUT).as_posix(): sha(p) for p in sorted(OUT.rglob('*')) if p.is_file()}
    emit_json('PACKAGE_MANIFEST.json', {'scope': 'Local PCBWay submission snapshot; not approval or test results',
                                      'files': files})
    return verify()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1:] != ['--verify']:
        raise SystemExit('Usage: package_pcbway.py [--verify]')
    print(json.dumps(verify() if '--verify' in sys.argv else build(), indent=2))
