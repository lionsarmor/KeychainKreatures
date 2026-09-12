"""Reuse the C3 table generator with explicit C4 output and socket addition."""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
s=(root/'pcb/c3_documents.py').read_text().replace('pcb/c3_netlist.xml','pcb/c4_netlist.xml')
for name in ['BOM_BY_REFERENCE','PCB_BOM','KIT_EXTRAS','BOM_PRINT','TEST_POINT_MAP','DEBUG_GUIDE']:
    s=s.replace('C3_'+name,'C4_'+name)
s=s.replace('C.3','C.4').replace('KK C3','KK C4')
s=s.replace("writecsv('C4_KIT_EXTRAS.csv',extras)","extras.insert(5,{'Quantity per kit':'1','Part / specification':'PPTC041LFBN-RC','Description':'Sullins four-pin socket for removable D3 RGB LED','Source / drawing':'../component_review/datasheets/sullins-female-headers.pdf','Assembly note':'Prototype contact fit/retention with actual LED leads is PENDING; do not force or tin mating leads. 8.5mm housing; formed LED leads to 2.54mm pitch. Pin1 R,2 A+,3 B,4 G.'})\nwritecsv('C4_KIT_EXTRAS.csv',extras)")
s=s.replace('D3 requires lead forming','D3 is socketed below the ESP32 on the right; socket retention must be tested. D3 requires lead forming')
exec(compile(s,'<C4 table generator>','exec'))
