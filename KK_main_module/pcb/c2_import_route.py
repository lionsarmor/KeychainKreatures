"""Import local FreeRouting SES into a candidate, refill copper, preserve source."""
from pathlib import Path
import pcbnew as k, sys
root=Path(__file__).resolve().parent.parent
stem=sys.argv[1] if len(sys.argv)>1 else 'KK_main_module_C2'
board=k.LoadBoard(str(root/'routing/KK_main_module_C2_unrouted.kicad_pcb'))
assert not list(board.GetTracks())
if stem.endswith('_antenna'):
    z=k.ZONE(board);z.SetLayerSet(k.LSET.AllCuMask(2));z.SetIsRuleArea(True)
    z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowFootprints(False)
    z.SetZoneName('SUPERMINI_ANTENNA_UNDER_MODULE');o=z.Outline();o.NewOutline()
    for x,y in [(59.5,7),(72.5,7),(72.5,15.5),(59.5,15.5)]:o.Append(k.FromMM(x),k.FromMM(y))
    board.Add(z)
# FreeRouting 2.3 drops the empty quoted footprint identifier of board-only
# mounting holes. Restore that token only; preserve the original SES verbatim.
ses=root/('routing/'+stem+'.ses')
normalized=root/('routing/'+stem+'_normalized.ses')
normalized.write_text(ses.read_text().replace('(component \n','(component ""\n'))
assert k.ImportSpecctraSES(board,str(normalized))
board.BuildConnectivity();k.ZONE_FILLER(board).Fill(board.Zones())
k.SaveBoard(str(root/'routing/KK_main_module_C2_candidate.kicad_pcb'),board)
print('Imported candidate:',len(list(board.GetTracks())),'tracks/vias. Not yet promoted.')
