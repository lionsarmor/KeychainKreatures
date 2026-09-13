"""Read-only native CAD audit/plots; manufacturing export fails closed on DRC/ERC.
Run inside the KiCad Flatpak Python, pinned to one CPU. Never edits the PCB.
"""
from pathlib import Path
import json,csv,sys,hashlib,os
import pcbnew as k
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/os.environ.get('KK_POWER_REVIEW_DIR','KK_power_module/work/P2_review')
OUT=SRC/'prototype_package'
OUT.mkdir(exist_ok=True)
sm=k.SETTINGS_MANAGER();pro=str(SRC/'KK_power_module.kicad_pro');assert sm.LoadProject(pro)
b=k.LoadBoard(str(SRC/'KK_power_module.kicad_pcb'));b.SetProject(sm.GetProject(pro))
design=json.loads((SRC/'design.json').read_text());expected={p['ref']:p for p in design['components']}
def xy(p):return [round(k.ToMM(p.x),6),round(k.ToMM(p.y),6)]
errors=[];rows=[];tests=[];connectors={};via_pads=[]
vias=[t for t in b.GetTracks() if t.GetClass()=='PCB_VIA']
for f in b.GetFootprints():
    ref=f.GetReference();fp=str(f.GetFPID().GetLibItemName());part=expected.get(ref)
    if not part:
        if ref.startswith('LOGO'):
            if list(f.Pads()) or not (f.GetAttributes() & k.FP_BOARD_ONLY):errors.append('Logo is not non-electrical board artwork '+ref)
        elif not ref.startswith('H'):errors.append('Unexpected footprint '+ref)
        continue
    if f.GetValue()!=part['value']:errors.append('Value mismatch '+ref)
    if fp!=part['footprint'].split(':')[-1]:errors.append('Footprint mismatch '+ref)
    pins={}
    for p in f.Pads():
        number=p.GetNumber()
        if not number:continue
        net=p.GetNetname().lstrip('/');pins[number]=net
        if ref.startswith('J'):connectors.setdefault(ref,[]).append(dict(pin=number,net=net,xy=xy(p.GetPosition())))
        if p.GetAttribute()==k.PAD_ATTRIB_SMD and p.IsOnLayer(k.F_Cu):
            for v in vias:
                if p.HitTest(v.GetPosition()):via_pads.append(dict(ref=ref,pin=number,xy=xy(v.GetPosition()),drill_mm=k.ToMM(v.GetDrillValue())))
    for pin,want in part['nets'].items():
        got=pins.get(pin)
        if got is None:errors.append('Missing pad '+ref+':'+pin)
        elif want is None:
            if got and not got.startswith('unconnected-'):errors.append('NC connected '+ref+':'+pin)
        elif got!=want:errors.append('Pad/net mismatch '+ref+':'+pin)
    if ref.startswith('TP'):
        tests.append([ref,part['value'],*xy(f.GetPosition()),b.GetLayerName(f.GetLayer())]);continue
    rows.append([ref,part['value'],part['mpn'],part['footprint'],*xy(f.GetPosition()),f.GetOrientationDegrees(),'Bottom' if f.IsFlipped() else 'Top','THT/mixed' if any(p.GetAttribute()==k.PAD_ATTRIB_PTH for p in f.Pads()) else 'SMT',part.get('datasheet',''),part.get('note','')])
assert len(rows)==108 and len(tests)==28,(len(rows),len(tests))
audit=dict(errors=errors,fitted_components=len(rows),bare_test_pads=len(tests),board_size_mm=[50,50],copper_layers=b.GetCopperLayerCount(),tracks=sum(t.GetClass()!='PCB_VIA' for t in b.GetTracks()),vias=len(vias),connectors=connectors,via_in_smd_pad=via_pads,PCB_SHA256=hashlib.sha256((SRC/'KK_power_module.kicad_pcb').read_bytes()).hexdigest(),scope='Native pad-number/net/value/footprint identity and geometry audit; not independent package-drawing or powered qualification')
(OUT/'CAD_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
assert not errors,errors
def csvwrite(name,header,data):
    with (OUT/name).open('w',newline='') as fh:
        w=csv.writer(fh);w.writerow(header);w.writerows(sorted(data,key=lambda r:r[0]))
csvwrite('BOM_AND_PLACEMENT.csv',['Reference','Value','Selected MPN (availability/substitution approval required)','Footprint','CAD X mm','CAD Y mm (down-positive)','KiCad rotation degrees','Side','Assembly','Datasheet','Notes'],rows)
grouped={}
for r in rows:
    key=(r[1],r[2],r[3],r[8],r[9])
    grouped.setdefault(key,[]).append(r[0])
csvwrite('BOM_GROUPED_5_BOARDS.csv',['References','Value','Selected MPN','Footprint','Assembly','Datasheet','Quantity per board','Quantity for 5 (excludes assembly attrition)'],[[', '.join(sorted(refs)),*key,len(refs),5*len(refs)] for key,refs in grouped.items()])
csvwrite('TEST_POINTS.csv',['Reference','Signal','CAD X mm','CAD Y mm (down-positive)','Layer'],tests)
plots=OUT/'drawings';plots.mkdir(exist_ok=True)
# Separate external silkscreen labels from fab-body references to avoid
# double-printed designators. No footprint graphics or saved CAD are altered.
pc=k.PLOT_CONTROLLER(b);po=pc.GetPlotOptions();po.SetOutputDirectory(str(plots));po.SetPlotFrameRef(False);po.SetAutoScale(False);po.SetScale(1);po.SetPlotReference(True);po.SetPlotValue(False)
for name,layers in [('assembly_top',[k.Edge_Cuts,k.F_SilkS]),('assembly_bottom',[k.Edge_Cuts,k.B_SilkS]),('component_bodies_top',[k.Edge_Cuts,k.F_Fab]),('component_bodies_bottom',[k.Edge_Cuts,k.B_Fab]),('copper_front',[k.F_Cu,k.Edge_Cuts]),('copper_inner1',[k.In1_Cu,k.Edge_Cuts]),('copper_inner2',[k.In2_Cu,k.Edge_Cuts]),('copper_back',[k.B_Cu,k.Edge_Cuts])]:
    po.SetMirror(name.endswith('_bottom'));pc.SetLayer(layers[0]);assert pc.OpenPlotfile(name,k.PLOT_FORMAT_SVG,name)
    for la in layers:pc.SetLayer(la);pc.PlotLayer()
    pc.ClosePlot()
if '--manufacturing' in sys.argv:
    drc=json.loads((SRC/'review_drc.json').read_text());erc=json.loads((SRC/'final_erc.json').read_text())
    assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity'],'DRC must be completely clean'
    assert all(not s['violations'] for s in erc['sheets']),'ERC must be completely clean'
    print('PASS: native audit and clean report gate; CLI Gerbers/drill exports may follow.')
print(json.dumps({k:audit[k] for k in ['errors','fitted_components','bare_test_pads','tracks','vias']}))
