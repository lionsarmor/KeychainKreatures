"""Independent checks against KiCad's exported electrical connectivity.

Static checks and calculations only. Does not simulate a battery or switcher.
"""
from pathlib import Path
import json,hashlib,re,math,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'P1_revision';d=json.loads((OUT/'design.json').read_text())
def readnets(path):
    tree=ET.parse(path).getroot();lookup={};membership={}
    for net in tree.findall('./nets/net'):
        name=net.attrib['name'].removeprefix('/')
        for node in net.findall('node'):
            key=(node.attrib['ref'],node.attrib['pin'])
            assert key not in lookup,('Duplicate pin in native netlist',key)
            lookup[key]=name;membership.setdefault(name,set()).add(key)
    return lookup,membership
lookup,members=readnets(OUT/'netlist.xml');issues=[]
for p in d['components']:
    for pin,expected in p['nets'].items():
        actual=lookup.get((p['ref'],pin))
        if expected is None:
            if actual is not None and not actual.startswith('unconnected-'):issues.append(f'{p["ref"]}.{pin}: NC unexpectedly on {actual}')
        elif actual!=expected:issues.append(f'{p["ref"]}.{pin}: expected {expected}, got {actual}')
main,_=readnets(ROOT.parent/'KK_main_module/C5_relayout/netlist.xml')
for pin in ['1','2','3','4']:
    if lookup.get(('J3',pin))!=main.get(('J1',pin)):issues.append('Main harness mismatch on pin '+pin)
# Explicit design invariants independent of the generator's part definitions.
assert lookup['J3','1']=='MCU_5V' and lookup['J3','2']=='GND'
assert lookup['J3','3']=='LOGIC_3V3' and lookup['J3','4']=='ACT_3V2'
assert lookup['J2','2']=='BAT_NEG' and lookup['U1','8']=='GND'
assert lookup['U2','6']=='BAT_NEG' and lookup['J4','2']=='GND'
assert members['BAT_NEG'].isdisjoint(members['GND'])
for pin in ['A6','A7','B6','B7','A8','B8']:
    assert lookup.get(('J1',pin),'unconnected-').startswith('unconnected-')
assert lookup['SW1','2']=='RUN_CTL'
assert lookup['U1','10']=='SYS_RAW' and lookup['U4','3']=='SYS_RAW'
# No direct charger bypass around the dedicated low-current USB input path.
assert lookup['U1','13']=='USB_CHG'
assert lookup['U13','B1']=='VBUS' and lookup['U13','B2']=='USB_CHG'
assert lookup['U13','C2']==lookup['R70','1']==lookup['R71','1']=='USB_PORT_ILIM'
assert lookup['R70','2']=='GND'
assert lookup['R71','2']==lookup['Q5','3']=='USB_PORT_ILIM_FAST'
assert lookup['Q5','1']==lookup['U1','5']=='USB_HIGH_CURRENT'
assert lookup['Q5','2']=='GND' and lookup['U1','6']=='GND'
# CC controller must not be powered or pulled up above its recommended supply.
assert lookup['U3','12']==lookup['U14','5']==lookup['R2','1']=='CC_3V3'
assert lookup['U14','1']==lookup['U14','3']=='VBUS'
assert lookup['U14','2']=='GND' and lookup['U3','3']==lookup['U3','11']=='GND'
assert lookup['R3','1']=='CC_3V3' and lookup['R72','2']=='GND'
assert lookup['U12','15']==lookup['U12','16']==lookup['U12','17']=='VOLTAGES_OK'
assert lookup['U12','14']==lookup['C60','1']==lookup['SW1','3']=='SYS_RAW'
assert lookup['U12','1']==lookup['SW1','2']=='RUN_CTL'
assert lookup['U11','2']=='VOLTAGES_OK'
for u in ['U8','U9','U10']:
    assert lookup[u,'5']!=lookup[u,'6'],'Output discharge must have series resistor'
for u in ['U5','U6','U7']:
    assert lookup[u,'3']==lookup[u,'4']=='REG_ENABLE'
hashes={};staged=json.loads((OUT/'stage.json').read_text())['source_sha256']
for file,expected in staged.items():
    actual=hashlib.sha256((ROOT/file).read_bytes()).hexdigest();hashes[file]=actual
    if actual!=expected:issues.append('Original changed since backup: '+file)
mainpcb=ROOT.parent/'KK_main_module/KK_main_module.kicad_pcb'
hashes['main_pcb']=hashlib.sha256(mainpcb.read_bytes()).hexdigest()
if hashes['main_pcb']!='b840262c37afad89ec5307568ace5b6acb4406f89c44c91f1579771642a89003':issues.append('C.5 main PCB changed')
# Rotation-invariant independent check: native DRC reported the USB NPTH gap
# before rotation but did not report it afterward. Do not interpret that as a
# geometry fix. Audit the unchanged local footprint directly.
def sexpr(text):
    tokens=iter(re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text))
    def node():
        result=[]
        for t in tokens:
            if t==')':return result
            result.append(node() if t=='(' else json.loads(t) if t.startswith('"') else t)
        raise ValueError('Unclosed expression')
    assert next(tokens)=='('
    return node()
def child(a,key):return next(x for x in a if isinstance(x,list) and x[0]==key)
usb=sexpr((OUT/'KK_Power.pretty/USB_C_HCTL.kicad_mod').read_text())
pads=[x for x in usb if isinstance(x,list) and x[0]=='pad']
hole_gaps=[]
for hole in [x for x in pads if x[2:4]==['np_thru_hole','circle']]:
    hx,hy=map(float,child(hole,'at')[1:3]);hr=float(child(hole,'drill')[1])/2
    for pad in [x for x in pads if x[2:4]==['smd','roundrect']]:
        px,py=map(float,child(pad,'at')[1:3]);sx,sy=map(float,child(pad,'size')[1:3])
        radius=min(sx,sy)*float(child(pad,'roundrect_rratio')[1])
        gap=math.hypot(max(abs(px-hx)-(sx/2-radius),0),max(abs(py-hy)-(sy/2-radius),0))-radius-hr
        if gap<.25:hole_gaps.append({'pad':pad[1],'npth_center_mm':[hx,hy],'copper_to_hole_mm':gap,'project_minimum_mm':.25})
calculations={
 'usb_legacy_limiter_A_datasheet_at_exact_19k2':[.034,.05,.066],
 'usb_legacy_limiter_A_screen_max_including_R_tolerance':.066*.999**-1.072,
 'usb_high_mode_parallel_ILIM_R_kohm':19.2*1.24/(19.2+1.24),
 'usb_high_mode_limiter_A_typical_formula':1.18*(19.2*1.24/(19.2+1.24))**-1.072,
 'usb_high_mode_logic_V_screen_min':3.3*.985*(100*.99)/(100*.99+10*1.01),
 'usb_upstream_overhead_A_allocation_not_guarantee':.010,
 'usb_legacy_total_A_screen_with_overhead_allocation':.066*.999**-1.072+.010,
 'charge_A_nominal':890/3000,'charge_A_max_with_R_tolerance':975/(3000*.99),
 'usb_advertised_mode_input_limit_A_nominal':1610/1300,
 'usb_advertised_mode_input_limit_A_max_with_R_tolerance':1720/(1300*.99),
 'efuse_limit_A_nominal':2000/620+.04,
 'efuse_limit_A_screen_low':(2000/(620*1.01)+.04)*.925,
 'efuse_limit_A_screen_high':(2000/(620*.99)+.04)*1.075,
 'uvlo_rise_V_nominal':1.2*(1+182/100),
 'uvlo_rise_V_low':1.13*(1+182*.999/(100*1.001)),
 'uvlo_rise_V_high':1.27*(1+182*1.001/(100*.999)),
 'uvlo_fall_V_nominal':1.1*(1+182/100),
 'uvlo_fall_V_low':1.03*(1+182*.999/(100*1.001)),
 'uvlo_fall_V_high':1.17*(1+182*1.001/(100*.999)),
 'screening_output_power_W':5*.6+3.3*.4+3.2*.5,
 'input_current_A_3V_85percent':(5*.6+3.3*.4+3.2*.5)/(3*.85),
 'input_current_A_2V7_80percent':(5*.6+3.3*.4+3.2*.5)/(2.7*.8),
 'raw_output_nominal_V':[.5*(1+909/101),.5*(1+560/100),.5*(1+540/100)],
 'supervisor_falling_threshold_V_nominal':[.4*(1+1060/100),.4*(1+665/100),.4*(1+649/100)],
 'load_gate_rise_ms_typical_estimate':[x*(.55*10000+30)/1000 for x in [5,3.3,3.2]],
 'three_parallel_FET_pairs_R_ohm_25C_max_at_VGS_2V5':2*.037/3,
}
holds=[
 'This is an unrouted placement study, not a finished power board. No manufacturing release.',
 'Full simultaneous 5.92 W screening load needs about 2.74 A at 2.7 V and 80% efficiency. The revised eFuse screening minimum is about 2.99 A; actual load/efficiency/drop/thermal envelope must still be closed before layout freeze.',
 'H&M DW01A is selected, but parallel-FET current sharing, protection trip thresholds versus temperature, fuse coordination and cell discharge/pulse ratings remain unqualified.',
 'Battery must be 1S 4.2 V Li-ion/LiPo rated at least 4 A continuous with an isolated cell-bonded 10k NTC; capacity, charge limits, connector polarity and temperature curve must be approved before fitting a cell. VH connector replaces the old PH/XH battery connector.',
 'Legacy/default USB input is now limited separately, nominally 50mA. The 10mA upstream overhead allocation must be verified including TVS leakage, CC controller, LDO and LEDs; the screening total is not a guaranteed maximum. Verify plug-in inrush, attach/detach and current-advertisement transitions on the bench.',
 'D+/D- remain unconnected: no enumeration, BC1.2 detection or USB suspend detection. Charging from an active powered USB-A port is targeted, not guaranteed from sleeping/disabled ports. No universal USB-host compatibility or USB certification claim.',
 'The added CC LDO and pullup arrangement correct the raw-VBUS supply-range issue. Probe the high-current request during cold start: it must remain default-limited until a valid higher-current advertisement is decoded.',
 'BQ24074 with a bare 103AT-2 NTC has a nominal charge-temperature window around 0 to 50C, with threshold/NTC tolerance. That is not approval for a cell requiring a narrower window: qualify or adjust before battery charging.',
 'Three soft-start outputs do not prove safe ESP32/peripheral rail sequencing. Actual SuperMini regulator, GPIO backfeed, restart and brownout behavior need measurements. Never power the socketed ESP32 USB and main supply simultaneously before reverse-feed qualification.',
 'Motor rail static tolerance, ripple and startup overshoot must remain within the actual motor rating; the nominal 3.2 V calculation alone does not guarantee this.',
 'Manufacturer land-pattern dimensions, bulk-capacitance bias derating, component MPNs, USB ESD and thermal layout remain purchasing/layout review items.',
 '3D models are incomplete; current rendering is not a complete assembly or enclosure-fit approval.',
 'The 0.4mm-pitch TPS22950 WCSP, thermal-pad soldering and USB footprint drill clearances need explicit assembler/fabricator approval; this power board is factory SMT, not a student hand-soldering kit.',
 'Independent USB footprint geometry check finds approximately 0.185mm copper-to-NPTH spacing, below the present 0.25mm project minimum. Native DRC no longer reports this after connector rotation; the physical gap did not change. This remains a manual manufacturing hold, not a waived or fixed clearance.',
]
report={'status':'ENGINEERING ONLY / RELEASE HELD','static_connectivity_issues':issues,'static_connectivity_pass':not issues,'independent_USB_hole_clearance_issues':hole_gaps,'component_count':len(d['components']),'test_pad_count':sum(p['ref'].startswith('TP') for p in d['components']),'source_hashes':hashes,'calculations_not_measurements':calculations,'release_holds':holds,'checked_artifact_sha256':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['design.json','netlist.xml','KK_power_module.kicad_sch','KK_power_module.kicad_pcb','KK_power_module.kicad_pro','KK_Power.pretty/USB_C_HCTL.kicad_mod']}}
(OUT/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'static_connectivity_issues':issues,'status':report['status'],'calculations':calculations},indent=2))
if issues:raise SystemExit(1)
