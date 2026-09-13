"""Reuse trace-graph audit without changing historical C.2 reports."""
from pathlib import Path
import sys
root=Path(__file__).resolve().parent.parent
s=(root/'pcb/c2_route_audit.py').read_text().replace("root/'pcb/C2_PLACEMENT_DISTANCES.json'","root/'C5_relayout/critical_pairs.json'").replace("root/'pcb/C2_ROUTE_AUDIT.json'","root/'C5_relayout/ROUTE_AUDIT.json'")
sys.argv=[sys.argv[0],str(root/'C5_relayout/KK_main_module.kicad_pcb')]
exec(compile(s,str(root/'pcb/c2_route_audit.py'),'exec'))
