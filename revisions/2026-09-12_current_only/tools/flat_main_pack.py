"""Reuse audited C5 functional objectives with new, larger flat-body envelopes."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'KK_main_module/pcb/c5_pack.py'
s=p.read_text().replace("root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'", "root=ROOT/'KK_main_module';out=root/'C6_flat_stack'")
s=s.replace('W,H=84,95','W,H=96,105')
s=s.replace('shift(kw[\'extra\'],2,0)', 'shift(kw[\'extra\'],8,0)').replace('put(r,x+2,y,a,**kw)', 'put(r,x+8,y,a,**kw)')
s=s.replace("('H2',80,4),('H3',4,91),('H4',80,91)", "('H2',92,4),('H3',4,101),('H4',92,101)")
s=s.replace("[32,0,52,13]", "[38,0,58,13]").replace("[27,0,57,5.25]", "[33,0,63,5.25]")
# Keep SD card access at the right edge; move connectors to the new bottom edge.
s=s.replace("fixed('J3',61.5,52,0,center=False,extra=[59.7,36.3,80,54.9])", "fixed('J3',67.5,52,0,center=False,extra=[65.7,36.3,86,54.9])")
s=s.replace("fixed('J1',49,90,0)", "fixed('J1',49,100,0)").replace("fixed('J4',10,90,0)", "fixed('J4',10,100,0)").replace("fixed('J5',30,90,0)", "fixed('J5',30,100,0)")
s=s.replace('best=None;tx,ty=target(r);tp=', 'best=None;tx,ty=target(r);tx+=6;tp=')
s=s.replace('def hit(a,b,g=.2):','def hit(a,b,g=.19999):')
# Flat bodies have a 0.5mm courtyard border, plus the existing 0.2mm gap.
# Preserve display, controls, connectors, optical parts, sockets and antenna position.
s=s.replace("'UNROUTED ENGINEERING CANDIDATE'", "'C6 FLAT STACK: UNROUTED, NOT FOR FABRICATION'").replace('C.4 unchanged','C5 unchanged')
exec(compile(s,str(p),'exec'))
