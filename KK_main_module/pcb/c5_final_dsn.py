from pathlib import Path
import pcbnew as k
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
sm=k.SETTINGS_MANAGER();p=str(root/'KK_main_module.kicad_pro');assert sm.LoadProject(p)
b=k.LoadBoard(str(root/'KK_main_module.kicad_pcb'));b.SetProject(sm.GetProject(p));b.SynchronizeNetsAndNetClasses(False)
assert k.ExportSpecctraDSN(b,str(out/'C5_final_routed.dsn'))
print('Final C.5 DSN exported from promoted root project.')
