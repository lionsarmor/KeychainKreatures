from pathlib import Path
import sys
root=Path(__file__).resolve().parent.parent
s=(root/'pcb/c3_geometry.py').read_text().replace("root/'routing/c3_geometry.json'","root/'C5_relayout/copper.json'")
sys.argv=[sys.argv[0],str(root/'C5_relayout/KK_main_module.kicad_pcb')]
exec(compile(s,str(root/'pcb/c3_geometry.py'),'exec'))
