"""Legible RGB assembly markings on the routed candidate."""
from pathlib import Path
import pcbnew as k,math,ast,json
root=Path(__file__).resolve().parent.parent
file=root/'routing/KK_main_module_C3_rgb_routed.kicad_pcb'
b=k.LoadBoard(str(file));fps={f.GetReference():f for f in b.GetFootprints()}
# Reuse the checked text-clearance helper with the approved taller board.
source=(root/'pcb/c3_connector_silk.py').read_text().replace('bb[3]>99','bb[3]>114')
tree=ast.parse(source)
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<silk placement>','exec'))
for ref in ['U4','R41','C27']:move(fps[ref].Reference(),xy(fps[ref].GetPosition()))
def label(text,point,side,other=None):
    t=k.PCB_TEXT(b);t.SetText(text);t.SetLayer(k.B_SilkS if side=='back' else k.F_SilkS);b.Add(t);move(t,point,other)
for ref in ['U4','D3']:
    ps={p.GetNumber():p for p in fps[ref].Pads()}
    label('1',xy(ps['1'].GetPosition()),'back' if ref=='U4' else 'front',xy(ps['2'].GetPosition()))
label('RGB MOOD', [16,111], 'front')
label('D3: 1=R 2=+ 3=B 4=G', [17,101], 'front')
label('FORM LEADS TO 2.54mm', [18,98.5], 'front')
label('RGB DRIVER', [41,113], 'back')
label('80 x 115mm / C.3', [62,112], 'front')
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(file),b)
print('RGB pin-1, lead-order and orientation labels added.')
