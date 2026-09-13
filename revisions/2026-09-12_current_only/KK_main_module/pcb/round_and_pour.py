"""Round the existing outline and fill both GND layers; preserve placement and tracks.
Run using KiCad Python. Module-fit holds and unrouted signals remain in force.
"""
from pathlib import Path
from datetime import datetime, timezone
import math, shutil
import pcbnew as k

ROOT=Path(__file__).resolve().parent.parent
BOARD_PATH=ROOT/'KK_main_module.kicad_pcb'
POURS={'MAIN_GND_FRONT':k.F_Cu,'MAIN_GND_BACK':k.B_Cu}
def vec(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))

def update_board(board):
    edges=[s for s in board.GetDrawings() if s.GetLayer()==k.Edge_Cuts]
    # Refuse to replace a changed board outline or cutouts with this fixed geometry.
    b=board.GetBoardEdgesBoundingBox()
    if len(edges) not in (4,8) or any(abs(a-z)>.1 for a,z in zip(
        [k.ToMM(b.GetX()),k.ToMM(b.GetY()),k.ToMM(b.GetWidth()),k.ToMM(b.GetHeight())],[0,0,80,100])):
        raise RuntimeError('Outline changed; inspect it before applying the 80 x 100 mm rounding.')
    for edge in edges:board.Remove(edge)
    r=4;d=r/math.sqrt(2)
    lines=[((r,0),(80-r,0)),((80,r),(80,100-r)),
           ((80-r,100),(r,100)),((0,100-r),(0,r))]
    arcs=[((76,0),(76+d,4-d),(80,4)),((80,96),(76+d,96+d),(76,100)),
          ((4,100),(4-d,96+d),(0,96)),((0,4),(4-d,4-d),(4,0))]
    for a,b in lines:
        s=k.PCB_SHAPE(board);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(vec(*a));s.SetEnd(vec(*b))
        s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));board.Add(s)
    for a,m,b in arcs:
        s=k.PCB_SHAPE(board);s.SetShape(k.SHAPE_T_ARC);s.SetArcGeometry(vec(*a),vec(*m),vec(*b))
        s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));board.Add(s)

    ground=[n for n in board.GetNetsByNetcode().values() if n.GetNetname()=='/GND']
    if len(ground)!=1:raise RuntimeError('Expected the schematic /GND net.')
    for z in list(board.Zones()):
        if z.GetZoneName() in POURS and not z.GetIsRuleArea():board.Remove(z)
    # The original antenna keepout is retained; KiCad clips pours to it and the outline.
    for name,layer in POURS.items():
        z=k.ZONE(board);z.SetZoneName(name);z.SetLayer(layer);z.SetNet(ground[0])
        z.SetLocalClearance(k.FromMM(.25));z.SetMinThickness(k.FromMM(.25))
        z.SetPadConnection(k.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(k.FromMM(.3));z.SetThermalReliefSpokeWidth(k.FromMM(.3))
        z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
        p=z.Outline();p.NewOutline()
        for x,y in [(0,0),(80,0),(80,100),(0,100)]:p.Append(k.FromMM(x),k.FromMM(y))
        board.Add(z)
    board.BuildConnectivity()
    if not k.ZONE_FILLER(board).Fill(board.Zones()):raise RuntimeError('Zone fill failed.')

if __name__=='__main__':
    backup=ROOT/'pcb'/'backups';backup.mkdir(exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    shutil.copy2(BOARD_PATH,backup/f'before-round-and-pour-{stamp}.kicad_pcb.bak')
    board=k.LoadBoard(str(BOARD_PATH))
    update_board(board)
    k.SaveBoard(str(BOARD_PATH),board)
    print('Saved 4 mm corner radii and filled front/back GND pours. Placement, tracks and antenna keepout preserved.')
