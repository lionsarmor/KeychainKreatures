"""Read-only C6/P3 release audit, assembly plots and coordinate tables.
Run in KiCad Flatpak Python, one CPU. Never alters routed CAD.
"""
from pathlib import Path
import pcbnew as k
import csv, json, hashlib, sys

ROOT = Path(__file__).resolve().parent.parent
kind = sys.argv[1]
assert kind in ('main', 'power')
src = ROOT / ('KK_main_module/C6_flat_stack' if kind == 'main' else 'KK_power_module/P3_matching_stack')
stem = 'KK_' + kind + '_module'
out = src / 'release_checks'
out.mkdir(exist_ok=True)
sm = k.SETTINGS_MANAGER()
assert sm.LoadProject(str(src / (stem + '.kicad_pro')))
b = k.LoadBoard(str(src / (stem + '.kicad_pcb')))
b.SetProject(sm.GetProject(str(src / (stem + '.kicad_pro'))))
def xy(p): return [round(k.ToMM(p.x), 6), round(k.ToMM(p.y), 6)]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name, headers, rows):
    with (out / name).open('w', newline='') as f:
        w = csv.writer(f); w.writerow(headers); w.writerows(sorted(rows))
fps = {f.GetReference(): f for f in b.GetFootprints()}
if kind == 'main':
    with (src / 'assembly/C6_BOM_BY_REFERENCE.csv').open(newline='') as f: expected = {r['Reference']: r for r in csv.DictReader(f)}
else:
    design = json.loads((src / 'design.json').read_text())
    expected = {p['ref']: p for p in design['components'] if not p['ref'].startswith('TP')}
fitted = {r: f for r, f in fps.items() if not r.startswith(('TP', 'H', 'LOGO'))}
assert fitted.keys() == expected.keys()
rows = []; groups = {}; tests = []; connectors = []; via_pads = []; models = []
vias = [t for t in b.GetTracks() if t.GetClass() == 'PCB_VIA']
for ref, f in fitted.items():
    p = expected[ref]
    value, mpn, fp, ds, notes = ([p[x] for x in ('Value', 'MPN', 'Footprint', 'Datasheet', 'Notes')] if kind == 'main' else [p.get(x, '') for x in ('value', 'mpn', 'footprint', 'datasheet', 'note')])
    assert f.GetValue() == value, (ref, f.GetValue(), value)
    actual_fp = str(f.GetFPID().GetLibNickname()) + ':' + str(f.GetFPID().GetLibItemName())
    assert actual_fp == fp, (ref, actual_fp, fp)
    side = 'Bottom' if f.IsFlipped() else 'Top'
    if kind == 'main': assert p['Side'] == ('back' if f.IsFlipped() else 'front'), ref
    if kind == 'power':
        pins = {pad.GetNumber(): pad.GetNetname().lstrip('/') for pad in f.Pads()}
        for pin, net in p['nets'].items():
            assert pin in pins, (ref, pin)
            assert pins[pin] == net if net is not None else (not pins[pin] or pins[pin].startswith('unconnected-')), (ref, pin)
    method = 'THT/mixed' if any(pad.GetAttribute() == k.PAD_ATTRIB_PTH for pad in f.Pads()) else 'SMT'
    rows.append([ref, value, mpn, fp, *xy(f.GetPosition()), f.GetOrientationDegrees(), side, method, ds, notes])
    groups.setdefault((value, mpn, fp, method, ds), []).append(ref)
    assert len(f.Models()), ref + ' missing 3D'
    for m in f.Models():
        resolved = Path(m.m_Filename.replace('${KIPRJMOD}', str(src)).replace('${KICAD10_3DMODEL_DIR}', '/app/extensions/Library/3dmodels'))
        assert resolved.is_file(), str(resolved)
        models.append({'reference': ref, 'path': m.m_Filename, 'sha256': sha(resolved)})
    for pad in f.Pads():
        if ref.startswith('J'):
            connectors.append([ref, pad.GetNumber(), pad.GetNetname().lstrip('/'), *xy(pad.GetPosition()), side])
        if pad.GetAttribute() == k.PAD_ATTRIB_SMD:
            for via in vias:
                if pad.HitTest(via.GetPosition()):
                    via_pads.append([ref, pad.GetNumber(), *xy(via.GetPosition()), k.ToMM(via.GetDrillValue()), 'Filled/capped/planarized; factory must also evaluate partial overlaps'])
for ref, f in fps.items():
    if ref.startswith('TP'):
        pads = list(f.Pads()); assert len(pads) == 1
        tests.append([ref, pads[0].GetNetname().lstrip('/'), *xy(f.GetPosition()), b.GetLayerName(f.GetLayer())])
table('BOM_AND_PLACEMENT.csv', ['Reference', 'Value', 'MPN', 'Footprint', 'CAD X mm', 'CAD Y mm (down-positive)', 'KiCad rotation degrees', 'Side', 'Assembly', 'Datasheet', 'Notes'], rows)
table('BOM_GROUPED_5_BOARDS.csv', ['References', 'Value', 'MPN', 'Footprint', 'Assembly', 'Datasheet', 'Quantity per board', 'Quantity for 5 (no attrition)'], [[', '.join(sorted(refs)), *key, len(refs), 5 * len(refs)] for key, refs in groups.items()])
table('TEST_POINTS.csv', ['Reference', 'Signal', 'CAD X mm', 'CAD Y mm (down-positive)', 'Layer'], tests)
table('CONNECTOR_PIN_MAP.csv', ['Reference', 'Pin', 'Signal', 'CAD X mm', 'CAD Y mm (down-positive)', 'Side'], connectors)
table('VIA_IN_PAD_REVIEW.csv', ['Reference', 'Pad', 'CAD X mm', 'CAD Y mm (down-positive)', 'Drill mm', 'Process'], via_pads)
# Native SVG plots with a single set of references, then host converts to PDF.
plots = out / 'drawings'; plots.mkdir(exist_ok=True)
pc = k.PLOT_CONTROLLER(b); po = pc.GetPlotOptions()
po.SetOutputDirectory(str(plots)); po.SetPlotFrameRef(False); po.SetAutoScale(False); po.SetScale(1)
po.SetPlotReference(True); po.SetPlotValue(False)
for name, layers in [('assembly_top', [k.Edge_Cuts, k.F_SilkS]), ('assembly_bottom', [k.Edge_Cuts, k.B_SilkS]), ('bodies_top', [k.Edge_Cuts, k.F_Fab]), ('bodies_bottom', [k.Edge_Cuts, k.B_Fab])]:
    po.SetMirror(name.endswith('_bottom')); pc.SetLayer(layers[0]); assert pc.OpenPlotfile(name, k.PLOT_FORMAT_SVG, name)
    for layer in layers: pc.SetLayer(layer); pc.PlotLayer()
    pc.ClosePlot()
audit = {'source_sha256': {stem + '.' + ext: sha(src / (stem + '.' + ext)) for ext in ['kicad_pcb', 'kicad_sch', 'kicad_pro']}, 'fitted': len(rows), 'test_pads': len(tests), 'copper_layers': b.GetCopperLayerCount(), 'tracks': sum(t.GetClass() != 'PCB_VIA' for t in b.GetTracks()), 'vias': len(vias), 'models': models, 'via_centers_in_smd_pads': len(via_pads), 'holes': {r: {'xy_mm': xy(f.GetPosition()), 'drill_mm': xy(next(iter(f.Pads())).GetDrillSize())} for r, f in fps.items() if r.startswith('H')}, 'outline_mm': [96, 105], 'status': 'PASS; static geometry/BOM/net checks, not physical or powered qualification'}
assert len(rows) == (98 if kind == 'main' else 108)
assert len(tests) == (25 if kind == 'main' else 28)
(out / 'CAD_AUDIT.json').write_text(json.dumps(audit, indent=2) + '\n')
print(json.dumps({x: audit[x] for x in ['fitted', 'test_pads', 'tracks', 'vias', 'via_centers_in_smd_pads', 'status']}))
