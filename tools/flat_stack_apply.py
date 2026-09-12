"""C6/P3 native mechanical candidates. No fabrication export or source promotion."""
from pathlib import Path
import pcbnew as k, json, math, sys
ROOT=Path(__file__).resolve().parent.parent
MAIN=ROOT/'KK_main_module/C6_flat_stack';POWER=ROOT/'KK_power_module/P3_matching_stack'
W,H=96,105
HOLES={'H1':(4,4),'H2':(92,4),'H3':(4,101),'H4':(92,101)}
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
def bounds(g):
    q=g.GetBoundingBox();return [k.ToMM(q.GetX()),k.ToMM(q.GetY()),k.ToMM(q.GetRight()),k.ToMM(q.GetBottom())]
def outline(b):
    r=4;u=r/math.sqrt(2)
    for a,z in [((r,0),(W-r,0)),((W,r),(W,H-r)),((W-r,H),(r,H)),((0,H-r),(0,r))]:
        s=k.PCB_SHAPE(b);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s)
    for a,c,z in [((W-r,0),(W-r+u,r-u),(W,r)),((W,H-r),(W-r+u,H-r+u),(W-r,H)),((r,H),(r-u,H-r+u),(0,H-r)),((0,r),(r-u,r-u),(r,0))]:
        s=k.PCB_SHAPE(b);s.SetShape(k.SHAPE_T_ARC);s.SetArcGeometry(v(*a),v(*c),v(*z));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s)
def keepout(b,name,pts):
    z=k.ZONE(b);z.SetLayerSet(k.LSET.AllCuMask(b.GetCopperLayerCount()));z.SetIsRuleArea(True)
    z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowFootprints(False);z.SetZoneName(name)
    o=z.Outline();o.NewOutline()
    for x,y in pts:o.Append(k.FromMM(x),k.FromMM(y))
    b.Add(z)
def text(b,t,x,y,la=k.F_SilkS,size=.85):
    s=k.PCB_TEXT(b);s.SetText(t);s.SetPosition(v(x,y));s.SetTextSize(v(size,size));s.SetTextThickness(k.FromMM(.13));s.SetLayer(la);s.SetMirrored(la==k.B_SilkS);b.Add(s);return s
def hit(a,z,g=.15):return not(a[2]+g<=z[0] or z[2]+g<=a[0] or a[3]+g<=z[1] or z[3]+g<=a[1])

if '--main' in sys.argv:
    b=k.LoadBoard(str(MAIN/'C6_blank.kicad_pcb'));d=json.loads((MAIN/'placement.json').read_text());fps={f.GetReference():f for f in b.GetFootprints()}
    assert d['board_mm']==[W,H,1.6]
    for r,p in d['positions'].items():
        f=fps[r]
        if (f.GetLayer()==k.F_Cu)!=(p['side']=='front'):f.Flip(f.GetPosition(),k.FLIP_DIRECTION_LEFT_RIGHT)
        f.SetOrientationDegrees(p['angle']);f.SetPosition(v(*p['xy']));f.Value().SetVisible(False);f.Reference().SetVisible(False)
        for pad in f.Pads():
            assert math.dist(xy(pad.GetPosition()),p['pads'][pad.GetNumber()]['xy'])<.00001
            assert pad.GetNetname()==p['pads'][pad.GetNumber()]['net']
    outline(b)
    net=next(n for n in b.GetNetsByNetcode().values() if n.GetNetname()=='/GND')
    for la in [k.F_Cu,k.B_Cu]:
        z=k.ZONE(b);z.SetLayer(la);z.SetNet(net);z.SetZoneName('C6_GND');z.SetLocalClearance(k.FromMM(.25));z.SetMinThickness(k.FromMM(.25));z.SetPadConnection(k.ZONE_CONNECTION_THERMAL);z.SetThermalReliefGap(k.FromMM(.3));z.SetThermalReliefSpokeWidth(k.FromMM(.3));z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
        o=z.Outline();o.NewOutline()
        for x,y in [(0,0),(W,0),(W,H),(0,H)]:o.Append(k.FromMM(x),k.FromMM(y))
        b.Add(z)
    keepout(b,'C6_ANTENNA_EDGE',[(33,0),(63,0),(63,5.25),(33,5.25)])
    keepout(b,'C6_ANTENNA_UNDER_MODULE',[(41.5,5.25),(54.5,5.25),(54.5,14.5),(41.5,14.5)])
    obs={k.F_SilkS:[],k.B_SilkS:[]}
    for r,p in d['positions'].items():
        for pp in p['pads'].values():
            # Recompute absolute pad bounds; geometry JSON stores local bounds.
            pad=next(q for q in fps[r].Pads() if q.GetNumber()==pp['pin'])
            for la in obs:obs[la].append(bounds(pad))
        if not r.startswith('TP'):
            # Reference text may be inside its assembly outline (visible before
            # insertion), but not across the outline or a solder pad.
            la=k.F_SilkS if p['side']=='front' else k.B_SilkS;x1,y1,x2,y2=p['box'];t=.2
            obs[la].extend([[x1,y1,x2,y1+t],[x1,y2-t,x2,y2],[x1,y1,x1+t,y2],[x2-t,y1,x2,y2]])
    for la in obs:obs[la].extend([[x-2.5,y-2.5,x+2.5,y+2.5] for x,y in HOLES.values()])
    labels=[]
    def label(t,anchor,la,sz=.8,maxshift=12):
        s=text(b,t,*anchor,la,sz)
        for dx,dy in sorted([(i*.5,j*.5) for i in range(-maxshift*2,maxshift*2+1) for j in range(-maxshift*2,maxshift*2+1)],key=lambda p:p[0]**2+p[1]**2):
            s.SetPosition(v(anchor[0]+dx,anchor[1]+dy));bb=bounds(s)
            if bb[0]<1 or bb[1]<1 or bb[2]>W-1 or bb[3]>H-1:continue
            if not any(hit(bb,z) for z in obs[la]):
                obs[la].append(bb);labels.append({'label':t,'xy':xy(s.GetPosition()),'anchor':anchor,'offset_mm':math.hypot(dx,dy),'side':b.GetLayerName(la)});return
        raise RuntimeError('No accessible silkscreen space: '+t)
    # Critical identification gets priority over passive references.
    for r,t in [('J1','SYS IN'),('J4','MOTOR'),('J5','SPEAKER'),('U2','IR RX'),('D1','IR TX'),('J3','SD >')]:
        p=d['positions'][r];bb=p['box'];label(t,[(bb[0]+bb[2])/2,bb[3]+1.5],k.B_SilkS)
    for r,p in d['positions'].items():
        if r.startswith('H'):continue
        bb=p['box'];la=k.F_SilkS if p['side']=='front' else k.B_SilkS
        label(r,[(bb[0]+bb[2])/2,bb[1]-1],la)
        if r in ['MOD1','J1','J2','J3','J4','J5','U1','U2','U3','U4','D3']:
            pin='5V' if r=='MOD1' else '1';label(pin,p['pads'][pin]['xy'],la,.8)
    for r,t in [('SW1','UP'),('SW2','DOWN'),('SW3','LEFT'),('SW4','RIGHT'),('SW5','A'),('SW6','B'),('SW7','X'),('SW8','Y'),('SW9','MODE'),('D3','RGB')]:
        p=d['positions'][r]['box'];label(t,[(p[0]+p[2])/2,p[3]+1],k.F_SilkS,.85)
    label('KEYCHAIN KREATURES',[48,53],k.F_SilkS,1,25)
    label('C6 FLAT - PROTOTYPE',[48,103],k.F_SilkS,.85)
    label('ANTENNA - NO METAL',[48,3],k.F_SilkS,.85,3)
    # Official non-certification logos; retain physical-component DRC checks.
    retained=[]
    for ref,name,anchor in [('LOGO1','KiCad-Logo_6mm_SilkScreen',(15,87)),('LOGO2','OSHW-Logo_5.7x6mm_SilkScreen',(81,88))]:
        f=k.FootprintLoad('/app/extensions/Library/footprints/Symbol.pretty',name);f.SetParent(b);f.SetReference(ref);f.SetFPID(k.LIB_ID('Symbol',name));f.SetAttributes(k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES);f.SetAllowMissingCourtyard(True);f.Reference().SetVisible(False);f.Value().SetVisible(False)
        for xx,yy in sorted([(i,j) for i in range(5,W-5) for j in range(5,H-5)],key=lambda p:(p[0]-anchor[0])**2+(p[1]-anchor[1])**2):
            f.SetPosition(v(xx,yy));q=f.GetBoundingBox(False,False);bb=[k.ToMM(q.GetX()),k.ToMM(q.GetY()),k.ToMM(q.GetRight()),k.ToMM(q.GetBottom())]
            if not any(hit(bb,z,.3) for z in obs[k.F_SilkS]):break
        else:raise RuntimeError('No room for logo '+ref)
        obs[k.F_SilkS].append(bb);b.Add(f);retained.append(f)
    text(b,'C6 UNROUTED MECHANICAL CANDIDATE - DO NOT FABRICATE',W/2,H+4,k.Dwgs_User,1)
    b.GetTitleBlock().SetRevision('C.6 flat stack - UNROUTED')
    b.BuildConnectivity();k.SaveBoard(str(MAIN/'KK_main_module.kicad_pcb'),b)
    (MAIN/'reports/silkscreen_labels.json').write_text(json.dumps(labels,indent=2))
    print('C6 placed: 96 x 105mm, R4, common M2 holes, full flat-body courtyards. ROUTING PENDING.')

if '--power' in sys.argv:
    # Always start from preserved P2, never transform P3 twice.
    b=k.LoadBoard(str(ROOT/'KK_power_module/P2_compact/KK_power_module.kicad_pcb'))
    def signature(board, transformed=False):
        def pos(p):
            x,y=xy(p);return [round(51-x if transformed else x,6),round(104-y if transformed else y,6)]
        pads=sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),pos(p.GetPosition()),xy(p.GetSize()),xy(p.GetDrillSize())) for f in board.GetFootprints() if not f.GetReference().startswith('H') for p in f.Pads())
        tracks=sorted((t.GetClass(),t.GetNetname(),pos(t.GetStart()),pos(t.GetEnd()),int(t.GetLayer()),t.GetWidth(k.F_Cu) if t.GetClass()=='PCB_VIA' else t.GetWidth(),t.GetDrillValue() if t.GetClass()=='PCB_VIA' else 0) for t in board.GetTracks())
        return {'pads':pads,'tracks':tracks}
    expected=signature(b,True);retained=list(b.GetFootprints())+list(b.GetTracks())+list(b.Zones())+list(b.GetDrawings())
    for g in retained:
        if g.GetLayer()==k.Edge_Cuts:b.Remove(g);continue
        g.Rotate(v(0,0),k.EDA_ANGLE(180,k.DEGREES_T));g.Move(v(51,104))
    for f in b.GetFootprints():
        if f.GetReference() in HOLES:f.SetPosition(v(*HOLES[f.GetReference()]));f.SetOrientationDegrees(0)
    assert signature(b)==expected,'Power pad/track transform mismatch'
    outline(b)
    # Do not expand existing power planes. Entire upper section stays copper-free.
    keepout(b,'P3_MAIN_ANTENNA_CLEARANCE',[(18,0),(78,0),(78,38),(18,38)])
    text(b,'P3 MATCHING STACK - ENGINEERING',48,43,k.F_SilkS,1)
    text(b,'KEEP BATTERY / WIRING / METAL OUT OF ANTENNA AREA',48,18,k.F_SilkS,.8)
    text(b,'96 x 105 / COMMON M2 MOUNTS / REMOVE TO SERVICE MAIN',48,46,k.B_SilkS,.8)
    text(b,'MECHANICAL CANDIDATE - NOT RELEASED FOR FABRICATION',48,H+4,k.Dwgs_User,1)
    b.GetTitleBlock().SetRevision('P.3 matching stack - ENGINEERING')
    b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(POWER/'KK_power_module.kicad_pcb'),b)
    report={'result':'PASS: rigid power pad/trace transform preserved','transform_mm':'x = 51 - old_x; y = 104 - old_y; rotation 180 degrees; layers unchanged','board_mm':[W,H,1.6],'mounting_holes':HOLES,'tracks_and_vias':len(expected['tracks']),'component_pads':len(expected['pads']),'scope':'Pad/net/size/drill identity and every trace/via coordinate, layer, width, drill. Hole relocation and zone refills require native DRC. Not powered qualification.'}
    (POWER/'reports/rigid_core_preservation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('P3 power core preserved and repositioned; matching 96 x 105 outline and holes. Native DRC pending.')
