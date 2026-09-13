"""C4 export, document-link, BOM and archive consistency checks."""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
s=(root/'pcb/c3_release_audit.py').read_text().replace('C3','C4').replace('C.3','C.4').replace('c3_netlist','c4_netlist')
exec(compile(s,'<C4 release consistency checks>','exec'))
