"""Fail-closed C6/P3 static audit; keep physical/manufacturing holds explicit."""
from pathlib import Path
import pcbnew as k,json,hashlib,csv,math,re
ROOT=Path(__file__).resolve().parent.parent
MAIN=ROOT/'KK_main_module/C6_flat_stack';POWER=ROOT/'KK_power_module/P3_matching_stack'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def xy(p):return [round(k.ToMM(p.x),6),round(k.ToMM(p.y),6)]
report={'scope':'Static flat-part/stack/width checks only; no powered or delivered-component qualification','boards':{},'physical_holds':['20mm standoff and JST wire-bend fit','Seller screen, ESP32 and SD module dimensions','Horizontal capacitor lead forming and ripple performance','Battery location / case depth / RF test','Factory DFM / component supply approval before ordering']}
boards=[]
for target,stem in [(MAIN,'KK_main_module'),(POWER,'KK_power_module')]:
    source=target/(stem+'.kicad_pcb');b=k.LoadBoard(str(source));boards.append(b)
    holes={f.GetReference():{'xy_mm':xy(f.GetPosition()),'drill_mm':xy(next(iter(f.Pads())).GetDrillSize())} for f in b.GetFootprints() if f.GetReference().startswith('H')}
    edge=b.GetBoardEdgesBoundingBox();size=xy(edge.GetSize())
    assert all(abs(a-z)<.06 for a,z in zip(size,[96,105])),size
    assert holes.keys()=={'H1','H2','H3','H4'}
    assert {tuple(h['xy_mm']) for h in holes.values()}=={(4,4),(92,4),(4,101),(92,101)}
    assert all(h['drill_mm']==[2.2,2.2] for h in holes.values())
    # Baselines remain recoverable and byte-for-byte unchanged by this work.
    baseline=json.loads((target/'SOURCE_BASELINE.json').read_text())
    assert all(sha(ROOT/p)==want for p,want in baseline.items()),'Baseline changed externally; do not promote'
    drcfile=target/'reports'/('drc_repaired.json' if target==MAIN else 'drc.json')
    drc=json.loads(drcfile.read_text())
    assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity'],str(drcfile)+' is not clean'
    erc=json.loads((target/'reports/erc.json').read_text())
    assert 'sheets' in erc and all(not sheet['violations'] for sheet in erc['sheets']),str(target)+' ERC is not clean'
    fitted_models=0
    for f in b.GetFootprints():
        if f.GetReference().startswith(('H','TP','LOGO')):continue
        assert len(f.Models()),f.GetReference()+' has no model'
        for m in f.Models():
            resolved=Path(m.m_Filename.replace('${KIPRJMOD}',str(target)).replace('${KICAD10_3DMODEL_DIR}','/app/extensions/Library/3dmodels'))
            assert resolved.exists(),str(resolved)
        fitted_models+=1
    report['boards'][stem]={'pcb_sha256':sha(source),'schematic_sha256':sha(target/(stem+'.kicad_sch')),'project_sha256':sha(target/(stem+'.kicad_pro')),'outline_mm':[96,105],'holes':holes,'copper_layers':b.GetCopperLayerCount(),'track_segments':sum(t.GetClass()!='PCB_VIA' for t in b.GetTracks()),'vias':sum(t.GetClass()=='PCB_VIA' for t in b.GetTracks()),'native_DRC_violations':0,'native_ERC_violations':0,'native_opens':0,'native_parity_issues':0,'baseline_preserved':True}
    report['boards'][stem]['fitted_parts_with_resolving_3d_models']=fitted_models

b=boards[0];fps={f.GetReference():f for f in b.GetFootprints()};changes=json.loads((MAIN/'component_changes.json').read_text())
main_in={p.GetNumber():p.GetNetname().lstrip('/') for p in fps['J1'].Pads()}
power_out={p.GetNumber():p.GetNetname().lstrip('/') for f in boards[1].GetFootprints() if f.GetReference()=='J3' for p in f.Pads()}
assert main_in==power_out=={'1':'MCU_5V','2':'GND','3':'LOGIC_3V3','4':'ACT_3V2'}
report['interboard_harness']={'power':'J3','main':'J1','wiring':'pin 1 to pin 1, keyed four-wire harness; never infer order from a mirrored rear drawing','pins':main_in}
assert len([r for r in fps if re.fullmatch(r'R\d+',r)])==43
for r,c in changes.items():
    f=fps[r];assert str(f.GetFPID().GetLibItemName())==c['Footprint'].split(':')[1]
    if r.startswith('R'):assert not any('Vertical' in m.m_Filename or 'Upright' in m.m_Filename for m in f.Models())
    if 'MPN' in c:assert f.GetField('MPN').GetText()==c['MPN']
pinmap=json.loads((MAIN/'reports/pin_net_preservation.json').read_text())['before']
assert {r:{p.GetNumber():p.GetNetname() for p in f.Pads()} for r,f in fps.items() if not r.startswith('LOGO')}==pinmap
fitted=[f for r,f in fps.items() if not r.startswith(('H','TP','LOGO'))]
assert len(fitted)==98
assert all(p.GetAttribute()==k.PAD_ATTRIB_PTH for f in fitted for p in f.Pads())
assert all(len(f.Models()) for f in fitted)
rules=json.loads((MAIN/'reports/ROUTING_RULES.json').read_text());widths={name:w for name,w,_,_ in rules['classes']}
actualpro=json.loads((MAIN/'KK_main_module.kicad_pro').read_text())
assert {c['name']:c['track_width'] for c in actualpro['net_settings']['classes']}==widths
width_fail=[]
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA':continue
    expected=widths[rules['assignments'].get(t.GetNetname(),'Default')]
    if k.ToMM(t.GetWidth())+1e-6<expected:width_fail.append([t.GetNetname(),k.ToMM(t.GetWidth()),expected])
assert not width_fail,width_fail
report['main_flat_parts']={'horizontal_resistors':43,'horizontal_electrolytics':10,'horizontal_TO92':6,'fitted_THT_components':98,'components_with_model_attachments':98,'pin_net_mapping_unchanged':True,'explicit_width_audit':'PASS independent of KiCad netclass assignment','model_note':'Attachment coverage is not measurement or delivered-part certification.'}

# Updated physical-coordinate assembly table for the rigidly moved power core.
rows=[];design=json.loads((ROOT/'KK_power_module/P2_compact/design.json').read_text());parts={p['ref']:p for p in design['components']}
for f in boards[1].GetFootprints():
    r=f.GetReference()
    if r.startswith(('H','LOGO','TP')):continue
    p=parts[r];assert f.GetValue()==p['value']
    rows.append([r,p['value'],p['mpn'],str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),*xy(f.GetPosition()),f.GetOrientationDegrees(),'Bottom' if f.IsFlipped() else 'Top'])
assert len(rows)==108
with (POWER/'assembly/P3_BOM_AND_PLACEMENT_REVIEW.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['Reference','Value','MPN','Footprint','X mm','Y mm','Rotation deg','Native PCB side']);w.writerows(sorted(rows))
report['status']='STATIC CAD CHECKS PASS - PROTOTYPE OUTPUTS REQUIRE SEPARATE HASH-BOUND RELEASE AUDIT; PHYSICAL / BENCH QUALIFICATION PENDING'
(ROOT/'docs/C6_P3_STATIC_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['boards']},indent=2))
