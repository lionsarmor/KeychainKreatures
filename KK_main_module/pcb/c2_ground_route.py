"""Second routing pass: explicit ground connectivity, not assumed plane contacts."""
from pathlib import Path
import pcbnew as k
root=Path(__file__).resolve().parent.parent
sm=k.SETTINGS_MANAGER();p=str(root/'KK_main_module.kicad_pro');assert sm.LoadProject(p)
b=k.LoadBoard(str(root/'routing/KK_main_module_C2_candidate.kicad_pcb'))
b.SetProject(sm.GetProject(p));b.SynchronizeNetsAndNetClasses(False)
for z in list(b.Zones()):
    if not z.GetIsRuleArea():b.Remove(z)
assert k.ExportSpecctraDSN(b,str(root/'routing/KK_main_module_C2_ground.dsn'))
print('Ground-explicit repair DSN exported; original candidate pours retained.')
