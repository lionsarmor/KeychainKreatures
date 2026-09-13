"""Read-only native DSN export of the final routed board for further editing."""
from pathlib import Path
import pcbnew as k,argparse
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['C2','C3','C4'],default='C2');revision=parser.parse_args().revision
root=Path(__file__).resolve().parent.parent
sm=k.SETTINGS_MANAGER();p=str(root/'KK_main_module.kicad_pro');assert sm.LoadProject(p)
b=k.LoadBoard(str(root/'KK_main_module.kicad_pcb'));b.SetProject(sm.GetProject(p));b.SynchronizeNetsAndNetClasses(False)
assert k.ExportSpecctraDSN(b,str(root/f'routing/KK_main_module_{revision}_final.dsn'))
print('Exported final routed board without modifying source.')
