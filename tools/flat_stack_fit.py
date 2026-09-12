"""Actual-size, unrouted-pad/body fit PDFs from C6; never moves saved design."""
from pathlib import Path
import pcbnew as k,subprocess,tempfile
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_main_module/C6_flat_stack'
b=k.LoadBoard(str(OUT/'KK_main_module.kicad_pcb'))
removed=list(b.GetTracks())
for t in removed:b.Remove(t)
for z in b.Zones():
    if not z.GetIsRuleArea():z.UnFill()
for group in [b.GetFootprints(),b.GetDrawings(),b.Zones()]:
    for item in group:item.Move(k.VECTOR2I(k.FromMM(15),k.FromMM(15)))
with tempfile.TemporaryDirectory(prefix='kk-c6-paper-fit-') as temp:
    source=str(Path(temp)/'C6_PAPER_FIT_ONLY.kicad_pcb');k.SaveBoard(source,b)
    for side,prefix in [('front','F'),('back','B')]:
        args=['kicad-cli','pcb','export','pdf','--layers',f'{prefix}.Cu,{prefix}.Silkscreen,{prefix}.Fab,Edge.Cuts','--mode-single','--black-and-white','--scale','1','--no-property-popups','--exclude-value','--output',str(OUT/'assembly'/f'C6_{side}_FIT_100_PERCENT.pdf')]
        if side=='back':args.append('--mirror')
        subprocess.run(args+[source],check=True)
print('Two actual-size C6 fit PDFs exported; print at 100%, no fit-to-page. Original CAD untouched.')
