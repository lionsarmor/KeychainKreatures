"""Post-route physical finishing: labels, outer ground pours, portable models.

Never changes signal routing. Re-run native DRC after running this script.
"""
from pathlib import Path
import json,shutil,pcbnew as k
out=Path(__file__).resolve().parent/'P2_compact';path=out/'KK_power_module.kicad_pcb'
sm=k.SETTINGS_MANAGER();pro=str(out/'KK_power_module.kicad_pro');assert sm.LoadProject(pro)
b=k.LoadBoard(str(path));b.SetProject(sm.GetProject(pro));b.SynchronizeNetsAndNetClasses(False)
def V(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
fps={f.GetReference():f for f in b.GetFootprints()}
drawing_text=set()
for g in list(b.GetDrawings()):
    if isinstance(g,k.PCB_TEXT) and g.GetText() in ['1 + / 2 -','5V GND 3V3 3V2']:
        g.SetLayer(k.Dwgs_User);continue
    if isinstance(g,k.PCB_TEXT):drawing_text.add(g.GetText())
    if isinstance(g,k.PCB_TEXT) and g.GetText() in ['KK POWER P.2','USB CHARGE']:
        g.SetLayer(k.B_SilkS);g.SetMirrored(True)
        g.SetPosition(V(25,2) if g.GetText()=='KK POWER P.2' else V(12,8.9))
def label(text,x,y,size=.65):
    g=k.PCB_TEXT(b);g.SetText(text);g.SetLayer(k.F_SilkS);g.SetPosition(V(x,y))
    g.SetTextSize(V(size,size));g.SetTextThickness(k.FromMM(.1));b.Add(g)
# Labels follow the actual rotated header pad positions, not an assumed
# left-to-right pin order. J3 pin 1 is on the right in the top view.
existing_text=drawing_text
if '3V2' not in existing_text:
    for text,x in [('3V2',31.75),('3V3',34.25),('GND',36.75),('5V',39.25)]:label(text,x,48.5,.8)
    label('2 -',8.52,47.7,.8);label('1 +',12.48,47.7,.8)
fps['C1'].Reference().SetLayer(k.F_Fab)
fps['C1'].Reference().SetPosition(fps['C1'].GetPosition())
# Each device is explicitly identified at its body on the assembly layer, even
# when a crowded silk label had to be placed farther away or omitted.
for f in b.GetFootprints():
    f.SetField('AssemblyRef',f.GetReference());field=f.GetField('AssemblyRef')
    field.SetText(f.GetReference());field.SetVisible(True)
    field.SetLayer(k.F_Fab if f.GetLayer()==k.F_Cu else k.B_Fab)
    field.SetTextSize(V(.65,.65));field.SetTextThickness(k.FromMM(.08))
    field.SetPosition(f.GetPosition());field.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T))
    field.SetMirrored(f.GetLayer()==k.B_Cu)
    for model in f.Models():
        prefix='${KICAD10_3DMODEL_DIR}/'
        if model.m_Filename.startswith(prefix):
            name=model.m_Filename[len(prefix):]
            if (out/'3dmodels'/name).exists():model.m_Filename='${KIPRJMOD}/3dmodels/'+name
    if f.GetReference() in ['Q1','Q2','Q3'] and not list(f.Models()):
        model=k.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/3dmodels/Package_TO_SOT_SMD.3dshapes/SOT-23-6.step';f.Models().push_back(model)
# An uninterrupted inner ground plane is the primary return. Outer ground
# pours add shielding/thermal copper; remove detached islands automatically.
ground=next(p for p in fps['J3'].Pads() if p.GetNumber()=='2').GetNet()
existing={z.GetLayer() for z in b.Zones() if z.GetNetname()==ground.GetNetname()}
for layer in [k.F_Cu,k.B_Cu]:
    if layer in existing:continue
    z=k.ZONE(b);z.SetLayer(layer);z.SetNet(ground);z.SetPadConnection(k.ZONE_CONNECTION_FULL)
    z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
    z.SetLocalClearance(k.FromMM(.2));z.SetMinThickness(k.FromMM(.2))
    z.Outline().NewOutline()
    for x,y in [(.6,.6),(49.4,.6),(49.4,49.4),(.6,49.4)]:z.Outline().Append(k.FromMM(x),k.FromMM(y))
    b.Add(z)
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(path),b)
print('Post-route labels/models/pours updated. Final DRC required.')
