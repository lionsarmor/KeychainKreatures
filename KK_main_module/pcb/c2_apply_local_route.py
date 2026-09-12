from pathlib import Path
import pcbnew as k,json
root=Path(__file__).resolve().parent.parent
file=root/'routing/KK_main_module_C2_candidate.kicad_pcb';b=k.LoadBoard(str(file))
nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
def v(p):return k.VECTOR2I(k.FromMM(p[0]),k.FromMM(p[1]))
for r in json.loads((root/'routing/C2_LOCAL_REPAIRS.json').read_text()):
    for a,z in zip(r['path'],r['path'][1:]):
        if a[0]!=z[0]:
            t=k.PCB_VIA(b);t.SetPosition(v(a[1:]));t.SetWidth(k.FromMM(r['via_diameter']));t.SetDrill(k.FromMM(r['via_drill']));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu)
        elif a[1:]==z[1:]:continue
        else:
            t=k.PCB_TRACK(b);t.SetStart(v(a[1:]));t.SetEnd(v(z[1:]));t.SetWidth(k.FromMM(r['width']));t.SetLayer(k.F_Cu if a[0]==0 else k.B_Cu)
        t.SetNet(nets[r['net']]);b.Add(t)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(file),b)
print('Applied locally checked repairs; KiCad DRC still required.')
