"""One-shot, non-destructive C6/P3 engineering staging (host Python)."""
from pathlib import Path
import shutil, hashlib, json, re, csv

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / 'KK_main_module'
OUT = MAIN / 'C6_flat_stack'
POWER = ROOT / 'KK_power_module/P3_matching_stack'
assert not OUT.exists() and not POWER.exists(), 'Candidates already exist; do not overwrite work.'
sources = [(MAIN, OUT, 'KK_main_module', ['KK_Main.pretty', '3dmodels', 'KK_Main.kicad_sym', 'fp-lib-table', 'sym-lib-table']),
           (ROOT / 'KK_power_module/P2_compact', POWER, 'KK_power_module', ['KK_Power.pretty', '3dmodels', 'KK_Power.kicad_sym', 'fp-lib-table', 'sym-lib-table'])]
manifest = {}
for source, target, stem, extras in sources:
    target.mkdir(parents=True)
    manifest[stem] = {}
    for ext in ['kicad_pcb', 'kicad_sch', 'kicad_pro', 'kicad_dru']:
        p = source / (stem + '.' + ext)
        if p.exists():
            shutil.copy2(p, target / p.name)
            manifest[stem][str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    for name in extras:
        p = source / name
        if p.is_dir(): shutil.copytree(p, target / name, symlinks=False)
        elif p.exists(): shutil.copy2(p, target / name)
    (target / 'reports').mkdir()
    (target / 'assembly').mkdir()
    (target / 'datasheets').mkdir()
    (target / 'SOURCE_BASELINE.json').write_text(json.dumps(manifest[stem], indent=2) + '\n')

# Preserve schematic formatting: edit only placed-symbol property blocks.
cap100 = {'C1','C3','C5','C13','C17','C25'}
cap10 = {'C9','C11','C15','C21'}
changes = {}
for row in csv.DictReader((MAIN / 'assembly/C5_BOM_BY_REFERENCE.csv').open()):
    ref = row['Reference']
    change = {}
    if re.fullmatch(r'R\d+', ref):
        change = {'Footprint': 'KK_Main:MFR25_10p16', 'Assembly': 'Horizontal axial body; 10.16mm pitch. No upright resistors.'}
    if ref in cap100 | cap10:
        change = {'Footprint': 'KK_Main:KA_100u_Flat' if ref in cap100 else 'KK_Main:KA_10u_Flat',
                  'MPN': 'ECEA1CKA101' if ref in cap100 else 'ECEA1CKA100',
                  'Datasheet': 'https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1050.pdf',
                  'Assembly': '16V Panasonic KA-A, body horizontal on 0.5mm insulating support. Form leads with support at seal. Square pad 1 = positive. Maximum can envelope D6.8 x L8mm (100u) or D4.5 x L8mm (10u).'}
    if re.fullmatch(r'Q[1-6]', ref):
        change = {'Footprint': 'KK_Main:TO92_Flat_P2p54', 'Assembly': 'Horizontal TO-92, flat marked face up; formed 2.54mm lead spacing. Check actual device pinout; no pin swaps.'}
    if change: changes[ref] = change

def blocks(s):
    depth = 0; start = None; quoted = False; escaped = False
    for i, c in enumerate(s):
        if quoted:
            if escaped: escaped = False
            elif c == '\\': escaped = True
            elif c == '"': quoted = False
            continue
        if c == '"': quoted = True
        elif c == '(':
            depth += 1
            if depth == 2: start = i
        elif c == ')':
            if depth == 2: yield start, i + 1
            depth -= 1

p = OUT / 'KK_main_module.kicad_sch'; s = p.read_text()
for a, z in reversed(list(blocks(s))):
    block = s[a:z]
    if not re.match(r'\(symbol\s', block): continue
    ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if not ref or ref[1] not in changes: continue
    for name, val in changes[ref[1]].items():
        pattern = r'(\(property\s+' + re.escape(json.dumps(name)) + r'\s+)"(?:\\.|[^"\\])*"'
        if re.search(pattern, block): block = re.sub(pattern, lambda m: m[1] + json.dumps(val), block, count=1)
        elif name != 'Assembly':
            block = block[:-1] + f'\n(property {json.dumps(name)} {json.dumps(val)} (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n)'
    s = s[:a] + block + s[z:]
p.write_text(s.replace('(rev "C.5")', '(rev "C.6 engineering")'))
(OUT / 'component_changes.json').write_text(json.dumps(changes, indent=2) + '\n')
rows = list(csv.DictReader((MAIN / 'assembly/C5_BOM_BY_REFERENCE.csv').open()))
for row in rows:
    c = changes.get(row['Reference'], {})
    for field in ['Footprint', 'MPN', 'Datasheet']:
        if field in c: row[field] = c[field]
    if c: row['Notes'] = c['Assembly']
with (OUT / 'assembly/C6_BOM_BY_REFERENCE.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print('Staged independent C6/P3 candidates; active C5/P2 and existing manufacturing ZIPs unchanged.')
