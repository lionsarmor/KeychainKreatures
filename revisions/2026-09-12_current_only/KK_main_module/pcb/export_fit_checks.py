"""Export actual-size fit sheets with printer margins, without moving the design PCB."""
from pathlib import Path
import subprocess, tempfile
import pcbnew as k
ROOT=Path(__file__).resolve().parent.parent
board=k.LoadBoard(str(ROOT/'KK_main_module.kicad_pcb'))
# Paper fit sheets show holes and bodies, not solid copper. The design retains its fills.
for zone in board.Zones():
    if not zone.GetIsRuleArea():zone.UnFill()
offset=k.VECTOR2I(k.FromMM(15),k.FromMM(15))
for collection in (board.GetFootprints(),board.GetDrawings(),board.Zones(),board.GetTracks()):
    for item in collection:item.Move(offset)
note=k.PCB_TEXT(board);note.SetText('KK MAIN C.4 - REAR FIT CHECK / 80 x 115mm / PROTOTYPE')
note.SetLayer(k.B_Fab);note.SetPosition(k.VECTOR2I(k.FromMM(55),k.FromMM(133)))
note.SetTextSize(k.VECTOR2I(k.FromMM(1.1),k.FromMM(1.1)));note.SetTextThickness(k.FromMM(.15));note.SetMirrored(True);board.Add(note)
with tempfile.TemporaryDirectory(prefix='kk-fit-print-') as temp:
    source=str(Path(temp)/'FIT_CHECK_ONLY.kicad_pcb')
    k.SaveBoard(source,board)
    for side in ('front','back'):
        letter='F' if side=='front' else 'B'
        layers=f'{letter}.Cu,{letter}.Silkscreen,{letter}.Fab,Edge.Cuts'+(',Dwgs.User' if side=='front' else '')
        args=['kicad-cli','pcb','export','pdf','--layers',layers,
              '--mode-single','--black-and-white','--scale','1','--no-property-popups',
              '--output',str(ROOT/'pcb'/f'{side}-fit-check.pdf')]
        if side=='back':args.append('--mirror')
        subprocess.run(args+[source],check=True)
