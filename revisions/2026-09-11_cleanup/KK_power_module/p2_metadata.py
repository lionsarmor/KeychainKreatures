"""Refresh component metadata only; never alter placement or copper."""
from pathlib import Path
import json,pcbnew as k
out=Path(__file__).resolve().parent/'P2_compact'
path=out/'KK_power_module.kicad_pcb';b=k.LoadBoard(str(path))
d=json.loads((out/'design.json').read_text());parts={p['ref']:p for p in d['components']}
for f in b.GetFootprints():
    if f.GetReference() not in parts:continue
    p=parts[f.GetReference()];f.SetValue(p['value'])
    for field,key in [('MPN','mpn'),('Notes','note'),('Datasheet','datasheet')]:
        f.SetField(field,p[key]);f.GetField(field).SetVisible(False)
k.SaveBoard(str(path),b)
