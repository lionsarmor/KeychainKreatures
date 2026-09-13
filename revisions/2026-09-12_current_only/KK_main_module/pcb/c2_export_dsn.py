"""Export actual KiCad netclasses; no cloud service involved."""
from pathlib import Path
import json, pcbnew as k
root=Path(__file__).resolve().parent.parent
manager=k.SETTINGS_MANAGER()
project=str(root/'KK_main_module.kicad_pro')
assert manager.LoadProject(project)
board=k.LoadBoard(str(root/'KK_main_module.kicad_pcb'))
board.SetProject(manager.GetProject(project))
board.SynchronizeNetsAndNetClasses(False)
out=root/'routing';out.mkdir(exist_ok=True)
assert k.ExportSpecctraDSN(board,str(out/'KK_main_module_C2.dsn'))
k.SaveBoard(str(out/'KK_main_module_C2_unrouted.kicad_pcb'),board)
print('Exported DSN with project settings:',out)
