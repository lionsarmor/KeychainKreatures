"""Run existing fail-closed exporter in the separate C.5 revision workspace."""
from pathlib import Path
import sys
root=Path(__file__).resolve().parent.parent
s=(root/'pcb/c2_manufacture.py').read_text()
s=s.replace("choices=['C2','C3','C4']","choices=['C2','C3','C4','C5']").replace("['C3','C4']","['C3','C4','C5']")
s=s.replace('root=Path(__file__).resolve().parent.parent',"root=Path(__file__).resolve().parent.parent/'C5_relayout'")
s=s.replace("f'pcb/{revision}_FINAL_VERIFICATION.json'","'VERIFICATION.json'")
sys.argv=[sys.argv[0],'--revision','C5']
exec(compile(s,str(root/'pcb/c2_manufacture.py'),'exec'))
