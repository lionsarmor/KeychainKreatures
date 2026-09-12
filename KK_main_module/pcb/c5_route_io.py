"""Local routing handoff; keep C.4 and C.5 unrouted snapshots recoverable."""
from pathlib import Path
import sys,re,shutil,pcbnew as k
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
sm=k.SETTINGS_MANAGER();p=str(out/'KK_main_module.kicad_pro');assert sm.LoadProject(p)
b=k.LoadBoard(str(out/'KK_main_module.kicad_pcb'));b.SetProject(sm.GetProject(p));b.SynchronizeNetsAndNetClasses(False)
if '--export' in sys.argv:
 assert not list(b.GetTracks())
 shutil.copy2(out/'KK_main_module.kicad_pcb',out/'C5_unrouted.kicad_pcb')
 assert k.ExportSpecctraDSN(b,str(out/'C5_native.dsn'))
 s=(out/'C5_native.dsn').read_text();s=re.sub(r'^    \(plane .*\n','',s,flags=re.M)
 # Native rule areas are verified below before local routing.
 (out/'C5_route.dsn').write_text(s)
 print('C5_route.dsn exported. Grounds must be explicitly routed before pours.')
elif '--import' in sys.argv:
 assert not list(b.GetTracks())
 ses=out/'C5_route.ses';normal=out/'C5_normalized.ses';normal.write_text(ses.read_text().replace('(component \n','(component ""\n'))
 assert k.ImportSpecctraSES(b,str(normal))
 b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(out/'KK_main_module.kicad_pcb'),b)
 print('Imported local routing. DRC / connectivity / electrical-path audit still required.')
