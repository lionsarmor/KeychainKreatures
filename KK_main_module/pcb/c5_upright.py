"""Same resistor MPNs, alternate lead form; only candidate footprints changed."""
from pathlib import Path
import json,pcbnew as k
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
b=k.LoadBoard(str(out/'C5_blank.kicad_pcb'));fps={f.GetReference():f for f in b.GetFootprints()}
refs=json.loads((out/'upright_refs.json').read_text())
name='R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical'
lib=k.FootprintLoad('/app/extensions/Library/footprints/Resistor_THT.pretty',name)
assert lib is not None
lib.SetFPID(k.LIB_ID('KK_Main','MFR25_Upright_P2p54'));k.FootprintSave(str(root/'KK_Main.pretty'),lib)
for r in refs:
 old=fps[r];f=k.FootprintLoad(str(root/'KK_Main.pretty'),'MFR25_Upright_P2p54');f.SetParent(b);f.SetFPID(lib.GetFPID());f.SetReference(r);f.SetValue(old.GetValue());f.SetPath(old.GetPath());f.SetUuid(old.m_Uuid)
 for field in old.GetFields():
  if field.GetName() not in ['Reference','Value','Footprint']:f.SetField(field.GetName(),field.GetText());f.GetField(field.GetName()).SetVisible(False)
 pads={p.GetNumber():p for p in old.Pads()}
 for p in f.Pads():p.SetNet(pads[p.GetNumber()].GetNet())
 f.Value().SetVisible(False);b.Remove(old);b.Add(f)
k.SaveBoard(str(out/'C5_blank.kicad_pcb'),b)
print('Candidate upright low-current resistors:',len(refs))
