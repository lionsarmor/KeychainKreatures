"""C6 native routing I/O. Existing C5/P2 boards are never modified."""
from pathlib import Path
import pcbnew as k, sys, re, shutil
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_main_module/C6_flat_stack'
sm=k.SETTINGS_MANAGER();p=str(OUT/'KK_main_module.kicad_pro');assert sm.LoadProject(p)
b=k.LoadBoard(str(OUT/'KK_main_module.kicad_pcb'));b.SetProject(sm.GetProject(p));b.SynchronizeNetsAndNetClasses(False)
if '--export' in sys.argv:
    assert not list(b.GetTracks()), 'Do not overwrite routed work'
    shutil.copy2(OUT/'KK_main_module.kicad_pcb',OUT/'C6_unrouted.kicad_pcb')
    assert k.ExportSpecctraDSN(b,str(OUT/'C6_native.dsn'))
    s=(OUT/'C6_native.dsn').read_text();s=re.sub(r'^    \(plane .*\n','',s,flags=re.M)
    (OUT/'C6_route.dsn').write_text(s)
    print('Exported C6 DSN; explicitly route grounds; board RF rule areas retained.')
elif '--import' in sys.argv:
    assert not list(b.GetTracks()), 'Import starts from unrouted candidate only'
    s=(OUT/'C6_route.ses').read_text().replace('(component \n','(component ""\n')
    (OUT/'C6_normalized.ses').write_text(s)
    assert k.ImportSpecctraSES(b,str(OUT/'C6_normalized.ses'))
    b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(OUT/'KK_main_module.kicad_pcb'),b)
    print('Imported C6 routes; engineering status remains until native checks pass.')
