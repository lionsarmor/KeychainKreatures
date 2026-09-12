"""Revision labels only; engineering candidates remain on manufacturing hold."""
from pathlib import Path
import pcbnew as k,re
ROOT=Path(__file__).resolve().parent.parent
for relative,stem,revision in [('KK_main_module/C6_flat_stack','KK_main_module','C.6'),('KK_power_module/P3_matching_stack','KK_power_module','P.3')]:
    folder=ROOT/relative;b=k.LoadBoard(str(folder/(stem+'.kicad_pcb')))
    b.GetTitleBlock().SetRevision(revision+' flat stack engineering')
    for t in b.GetDrawings():
        if not isinstance(t,k.PCB_TEXT):continue
        s=t.GetText()
        if revision=='C.6':s=s.replace('C6 UNROUTED MECHANICAL CANDIDATE','C6 ROUTED ENGINEERING CANDIDATE')
        else:s=re.sub(r'\bP\.?2\b','P3',s)
        t.SetText(s)
    k.SaveBoard(str(folder/(stem+'.kicad_pcb')),b)
    p=folder/(stem+'.kicad_sch');s=p.read_text()
    s=re.sub(r'\(rev\s+"[^"]*"\)', '(rev "'+revision+' flat stack engineering")',s,count=1)
    p.write_text(s)
print('Revision metadata updated; no net or component changes.')
