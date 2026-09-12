from pathlib import Path
import pcbnew as k
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout';file=out/'KK_main_module.kicad_pcb';b=k.LoadBoard(str(file))
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
for a,z,layer in [((18,18),(66,49),k.F_Fab),((62,36.7),(79.9,54.6),k.B_Fab)]:
 g=k.PCB_SHAPE(b);g.SetShape(k.SHAPE_T_RECT);g.SetStart(v(*a));g.SetEnd(v(*z));g.SetLayer(layer);g.SetWidth(k.FromMM(.15));b.Add(g)
b.GetTitleBlock().SetRevision('C.5 compact landscape prototype');b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(file),b)
print('Filled final candidate with nominal module outlines on assembly layers.')
