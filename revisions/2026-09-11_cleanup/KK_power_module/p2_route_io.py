"""P.2 routing exchange. Preserve the manually locked critical connections."""
from pathlib import Path
import sys,shutil,json,re,pcbnew as k
out=Path(__file__).resolve().parent/'P2_compact'
path=out/'KK_power_module.kicad_pcb'
sm=k.SETTINGS_MANAGER();pro=str(out/'KK_power_module.kicad_pro');assert sm.LoadProject(pro)
b=k.LoadBoard(str(path));b.SetProject(sm.GetProject(pro));b.SynchronizeNetsAndNetClasses(False)
def signature(t):
    # DSN's 0.1um grid may round KiCad's nanometre coordinates by <=50nm.
    # Direction of an undirected trace is immaterial. Do not waive reroutes.
    q=lambda n:round(n/100)
    ends=sorted([(q(t.GetStart().x),q(t.GetStart().y)),(q(t.GetEnd().x),q(t.GetEnd().y))])
    width=t.GetWidth(k.F_Cu) if t.GetClass()=='PCB_VIA' else t.GetWidth()
    return (t.GetNetname(),t.GetLayer(),*ends[0],*ends[1],q(width),t.GetClass())
if '--export' in sys.argv:
    assert list(b.GetTracks()),'Critical copper must be placed first'
    shutil.copy2(path,out/'P2_critical_before_router.kicad_pcb')
    assert k.ExportSpecctraDSN(b,str(out/'P2_route.dsn'))
    dsn=(out/'P2_route.dsn').read_text()
    for layer in ['In1.Cu','In2.Cu']:
        dsn=dsn.replace('(layer '+layer+'\n      (type signal)', '(layer '+layer+'\n      (type power)')
    # The source-current trunks are explicitly locked in p2_power_paths.py.
    # Width here applies only to remaining bias/sense/test branches, not trunks.
    assert (out/'power_paths.json').exists()
    for cls in ['SOURCE_POWER','USB_CHARGE']:
        dsn,count=re.subn(r'(\(class '+cls+r'\b.*?\(width )\d+(\))',r'\g<1>200\2',dsn,count=1,flags=re.S)
        assert count==1,cls
    (out/'P2_route.dsn').write_text(dsn)
    print('Exported routing DSN, retaining native planes and locked copper.')
elif '--import' in sys.argv:
    original={signature(t) for t in b.GetTracks() if t.IsLocked()}
    shutil.copy2(path,out/'P2_before_ses_import.kicad_pcb')
    ses=out/'P2_route.ses';normal=out/'P2_normalized.ses'
    normal.write_text(ses.read_text().replace('(component \n','(component ""\n'))
    assert k.ImportSpecctraSES(b,str(normal))
    # KiCad's session importer may replace even protected wire objects. Every
    # original critical segment must still exist geometrically before save.
    result={signature(t) for t in b.GetTracks()}
    missing=original-result
    (out/'routing_import_audit.json').write_text(json.dumps({'critical_items':len(original),'missing':list(missing)},indent=2))
    assert not missing,f'Router changed {len(missing)} critical items; refusing save'
    for t in b.GetTracks():
        if signature(t) in original:t.SetLocked(True)
    b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(path),b)
    print('Imported routing; critical copper preserved. Native DRC still required.')
