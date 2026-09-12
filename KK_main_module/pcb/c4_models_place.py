"""Attach project-local 3D assemblies and move socketed RGB in a candidate only."""
from pathlib import Path
import pcbnew as k,json,math,ast
root=Path(__file__).resolve().parent.parent
b=k.LoadBoard(str(root/'routing/KK_main_module_C4_stage.kicad_pcb'));fps={f.GetReference():f for f in b.GetFootprints()}
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
modelmap={'KEMET_C315_P2p54':'KEMET_C315_max','Nichicon_UVR_D5_P2':'Nichicon_UVR_D5_H11','Adafruit3101_ABCD':'Adafruit3101_soft','ED08DT_DIP8_Socket':'Socketed_DIP8','ED16DT_DIP16_Socket':'Socketed_DIP16','ED281DT_DIP28_Socket':'Socketed_DIP28','TSOP38238_Vertical':'TSOP38238','TSAL6200_LED5':'TSAL6200_IR','ESP32-S3-SuperMini':'SuperMini_socketed_envelope','Sullins_PPTC081_LFB':'XIITIA_screen_socketed_envelope','Sullins_PPTC061_LFB':'GODIYMODULES_SD_socketed_envelope','RGB_CA_5mm_LeadFormed':'Kingbright_RGB_socketed'}
library=root/'KK_Main.pretty'
def attach(f,name):
    f.Models().clear();m=k.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/3dmodels/'+name+'.wrl';f.Models().push_back(m)
def socketize(f):
    f.SetFPID(k.LIB_ID('KK_Main','RGB_CA_5mm_Socketed'))
    f.SetLibDescription('Kingbright RGB in Sullins PPTC041LFBN-RC socket. Confirm actual LED contact retention. Pin1 R,2 A+,3 B,4 G.')
    for p in f.Pads():p.SetSize(v(1.85,1.85));p.SetDrillSize(v(1.05,1.05))
    edges=[((-1.525,-1.5),(-1.525,1.5)),((-1.525,-1.5),(9.145,-1.5)),((9.145,-1.5),(9.145,1.5)),((9.145,1.5),(-1.525,1.5))]
    i=0
    for g in f.GraphicalItems():
        if g.GetLayer()==k.F_SilkS and isinstance(g,k.PCB_SHAPE):
            g.SetStart(v(*edges[i][0]));g.SetEnd(v(*edges[i][1]));i+=1
        elif g.GetLayer()==k.F_CrtYd:
            g.SetStart(v(-1.8,-1.775));g.SetEnd(v(9.42,1.775))
for item,name in modelmap.items():
    assert (root/'3dmodels'/f'{name}.wrl').exists()
    f=k.FootprintLoad(str(library),item);assert f is not None;attach(f,name)
    if item=='RGB_CA_5mm_LeadFormed':
        socketize(f)
    k.FootprintSave(str(library),f)
for f in fps.values():
    name=modelmap.get(str(f.GetFPID().GetLibItemName()))
    if name:attach(f,name)
d3=fps['D3'];d3.SetPosition(v(0,0));socketize(d3)
d3.SetOrientationDegrees(90);d3.SetPosition(v(69,41.56))
# Existing D3 labels are moved, not left at their old bottom position.
source=(root/'pcb/c3_connector_silk.py').read_text().replace('bb[3]>99','bb[3]>114').replace('range(-24,25)','range(-48,49)')
exec(compile(ast.Module(body=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<label helpers>','exec'))
for g in b.GetDrawings():
    if not hasattr(g,'GetText'):continue
    t=g.GetText()
    if t=='USB END':move(g,[62,33])
    elif t=='TP29':move(g,[74,42.5])
    elif t=='MOTOR' and g.GetLayer()==k.B_SilkS:move(g,[73,33])
    elif t=='K' and g.GetLayer()==k.B_SilkS and math.dist(xy(g.GetPosition()),[70,42.83])<1:move(g,[67,44])
    elif t=='RGB MOOD':move(g,[73,44.5])
    elif t.startswith('D3: 1=R'):g.SetText('D3: 1=R 2=+ 3=B 4=G');move(g,[64,47])
    elif t.startswith('FORM LEADS'):g.SetText('D3 SOCKET: FORM LEADS');move(g,[20,104])
    elif t=='1' and g.GetLayer()==k.F_SilkS and math.dist(xy(g.GetPosition()),[12.19,106])<5:move(g,[69,41.56],[69,39.02])
    elif 'C.3' in t or 'C3' in t:g.SetText(t.replace('C.3','C.4').replace('C3','C4'))
move(d3.Reference(),[73,37])
move(fps['D2'].Reference(),[65.5,42.5])
b.GetTitleBlock().SetRevision('C.4 top RGB / populated 3D')
b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(root/'routing/KK_main_module_C4_unfinished.kicad_pcb'),b)
(root/'pcb/C4_LED_PLACEMENT.json').write_text(json.dumps({'reference':'D3','center_mm':[69,37.75],'pad1_mm':[69,41.56],'angle_degrees':90,'socket':'PPTC041LFBN-RC','socket_contact_qualification':'PENDING actual LED retention and lead-dimension check'},indent=2)+'\n')
print('C4 candidate: RGB below MCU, project-local models attached; four branches await reroute.')
