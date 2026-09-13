from pathlib import Path
import json,shutil,pcbnew as k
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout';file=out/'KK_main_module.kicad_pcb'
backup=out/'C5_before_repairs.kicad_pcb'
if not backup.exists():shutil.copy2(file,backup)
b=k.LoadBoard(str(backup));fps={f.GetReference():f for f in b.GetFootprints()};nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()}
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
for r in json.loads((out/'REPAIRS.json').read_text()):
 for a,z in zip(r['path'],r['path'][1:]):
  if a==z:continue
  if a[0]==z[0]:
   t=k.PCB_TRACK(b);t.SetStart(v(*a[1:]));t.SetEnd(v(*z[1:]));t.SetWidth(k.FromMM(r['width']));t.SetLayer(k.F_Cu if a[0]==0 else k.B_Cu)
  else:
   t=k.PCB_VIA(b);t.SetPosition(v(*a[1:]));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu);t.SetWidth(k.FromMM(r['via_diameter']));t.SetDrill(k.FromMM(r['via_drill']))
  t.SetNet(nets[r['net']]);b.Add(t)
for ref,pin in [('Q2','1'),('R20','2'),('U1','16'),('C7','2')]:
 p=next(p for p in fps[ref].Pads() if p.GetNumber()==pin);assert p.GetNetname()=='/GND';p.SetLocalZoneConnection(k.ZONE_CONNECTION_NONE)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(file),b)
print('Five native opens repaired; four isolated thermals use explicit ground routes. Recheck required.')
