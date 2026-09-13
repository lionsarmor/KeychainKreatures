"""Native current-copper export for two exact local repairs."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'KK_main_module/pcb/c2_geometry.py'
s=p.read_text().replace('root=Path(__file__).resolve().parent.parent',"root=ROOT/'KK_main_module/C6_flat_stack'")
s=s.replace("root/'routing/KK_main_module_C2_candidate.kicad_pcb'","root/'KK_main_module.kicad_pcb'")
s=s.replace("root/'routing/c2_geometry.json'","root/'reports/copper.json'")
exec(compile(s,str(p),'exec'))
