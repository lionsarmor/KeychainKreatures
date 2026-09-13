"""Generate current C6/P3 release documentation from preserved prior reviews.
Does not modify PCB/schematic geometry, historical revisions, or old ZIPs.
"""
from pathlib import Path
import csv, json, shutil
ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / 'KK_main_module/C6_flat_stack'
POWER = ROOT / 'KK_power_module/P3_matching_stack'
def copy(a, b):
    b.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(a, b)
def table(path, fields, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
# Bring all electrical source references forward without the old placement draft.
for src, dst in [(ROOT/'KK_power_module/P2_compact/datasheets', POWER/'datasheets'), (ROOT/'KK_main_module/component_review/datasheets', MAIN/'datasheets')]:
    for p in src.iterdir():
        if p.is_file() and not (dst/p.name).exists(): copy(p, dst/p.name)
design = json.loads((ROOT/'KK_power_module/P2_compact/design.json').read_text())
design['revision'] = 'P.3 MATCHING STACK PROTOTYPE'
design['mechanical'] = {'outline_mm': [96,105], 'radius_mm': 4, 'thickness_mm': 1.6, 'mounting_centers_mm': [[4,4],[92,4],[4,101],[92,101]], 'prior_core_transform': 'x=51-old_x; y=104-old_y; rotate 180 degrees, layers unchanged', 'note': 'Electrical values retain historical interface names (including C.5 SYS_IN); compatible with C.6. Use native P3 PCB for physical positions, not historical layout generators.'}
(POWER/'design.json').write_text(json.dumps(design, indent=2)+'\n')
copy(ROOT/'KK_power_module/P2_compact/electrical_screening.json', POWER/'electrical_screening.json')
with (MAIN/'assembly/C6_BOM_BY_REFERENCE.csv').open(newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
for r in rows:
    r['Notes']=r['Notes'].replace('C.5:', 'C.6:').replace('custom footprint pending', 'custom footprint included; verify delivered switch fit and A/B versus C/D continuity')
table(MAIN/'assembly/C6_BOM_BY_REFERENCE.csv', fields, rows)
with (ROOT/'KK_main_module/assembly/C5_KIT_EXTRAS.csv').open(newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
for r in rows:
    r['Source / drawing']=r['Source / drawing'].replace('../component_review/datasheets/', '../datasheets/').replace('../component_review/MODULE_SOURCE_NOTES.md', 'ASSEMBLY_GUIDE.md')
    name=r['Part / specification']
    if name.startswith('KK MAIN'):
        r.update({'Part / specification':'KK MAIN C.6 PROTOTYPE', 'Description':'96 x 105 x 1.6 mm, 2-layer, R4, four 2.2 mm M2 holes', 'Source / drawing':'../FABRICATION_REQUIREMENTS.md'})
    elif name=='XHP-4':
        r.update({'Quantity per kit':'2', 'Description':'Two ends of power J3 to main J1 harness', 'Assembly note':'Pin-for-pin 1=5V, 2=GND, 3=3.3V, 4=3.2V. Check both ends with meter.'})
    elif name=='SXH-001T-P0.6':
        r['Quantity per kit']='8'
    elif name.startswith('M2 x 15'):
        r.update({'Part / specification':'M2 x 20 mm nylon female/female standoff', 'Description':'Provisional removable-stack spacing', 'Assembly note':'Four between board faces for MOCK-UP only; verify actual module, JST plug and wire bend clearance.'})
    elif name=='M2 x 5 mm nylon screw': r['Quantity per kit']='8'
    elif name=='M2 nylon flat washer': r['Quantity per kit']='8'
    r['Assembly note']=r['Assembly note'].replace('Future power-board connector at other cable end is deliberately excluded.', '')
def extra(q, part, desc, note, source='Manufacturer drawing / dimensional specification; procurement approval pending'):
    rows.append(dict(zip(fields, [q, part, desc, source, note])))
extra('1','KK POWER P.3 assembled subassembly','96 x 105 x 1.6 mm four-layer power PCB with 108 fitted positions','Separate power BOM covers those 108 positions. Do not double-count them or ask students to assemble its fine-pitch SMT.')
extra('1','VHR-2N','JST VH battery mating housing','J2 pin1 CELL_PLUS; pin2 BAT_NEG, not GND. Cell choice and polarity require approval.')
extra('2','SVH-21T-P1.1','JST VH battery contacts','20 AWG battery pigtails; qualified crimps, check insulation range against JST drawing.')
extra('2 x provisional 150 mm','20 AWG stranded insulated battery pigtails','Battery connector wires','Final length/insulation rating and battery termination await cell/case choice.')
extra('1','103AT-2','Semitec 10k thermistor bonded to cell','Connect to power J4 pin1 NTC, pin2 GND. Insulate/bond to selected cell; do not replace by a fixed resistor.')
extra('1','PHR-2','Power J4 thermistor housing','Additional to the TWO motor/speaker PH housings above.')
extra('2','SPH-002T-P0.5S','Power J4 thermistor crimp contacts','Use suitable 28 AWG insulated pigtails; check exact wire/insulation and crimp tooling.')
extra('2 x provisional 150 mm','28 AWG insulated thermistor pigtails','NTC lead extensions','Insulated splices and strain relief, electrically isolated from cell pouch/can.')
extra('10','0.5 mm nonconductive capacitor supports','Under horizontally mounted electrolytic bodies','Material must tolerate assembly/operating temperature, not obstruct vents and not stress seals; sample qualification required.')
extra('1 set','Insulating inter-board barrier and harness retention','Prevent solder-tail and wiring shorts','Keep RF zone empty; no battery pressed against solder tails. Shape after physical mock-up.')
extra('1, NOT SELECTED','1S 4.2 V maximum Li-ion/LiPo cell','Battery intentionally not frozen','Provisionally >=4 A continuous, >=0.34 A charge allowance. Select documented cell, temperature limits, fit and protection coordination before real-cell testing.')
table(MAIN/'assembly/C6_COMPLETE_KIT_EXTRAS.csv', fields, rows)
bench=(ROOT/'KK_main_module/assembly/C5_BENCH_TEST_RECORD.csv').read_text().replace('80 x 115 mm', '96 x 105 mm').replace('Qualify with future power module', 'Qualify with P.3 power module').replace('RGB formed leads and ED16DT socket', 'RGB formed leads and PPTC041LFBN-RC socket; U4 ED16DT socket')
(MAIN/'assembly/C6_BENCH_TEST_RECORD.csv').write_text(bench)
# Preserve detailed, still-applicable pin mappings and firmware requirements.
old=(ROOT/'KK_main_module/assembly/ASSEMBLY_GUIDE.md').read_text()
orientation=old[old.index('## Parts whose orientation matters'):old.index('## Power and first startup')]
orientation=orientation.replace('The 150 mm cut lengths are a bench allowance; final enclosure lengths and the power-board end of J1 are deferred.', 'The 150 mm cut lengths are a bench allowance; both power J3 and main J1 now use XHP-4 housings. Use eight XH contacts for the complete pin-for-pin harness; final lengths depend on the shell.')
firmware=old[old.index('## Firmware requirements and audio qualification'):old.index('The 3D render now includes D3')]
firmware=firmware.replace('[C5_BENCH_TEST_RECORD.csv](C5_BENCH_TEST_RECORD.csv)', '[C6_BENCH_TEST_RECORD.csv](C6_BENCH_TEST_RECORD.csv)')
intro='''# Main C.6 — prototype assembly and wiring

Use ONLY C.6 CAD/BOM/Gerbers with P.3 power. Both boards are 96 x 105 x 1.6 mm, R4 corners, four 2.2 mm mounting holes. Main is two-layer through-hole student assembly; power is a separately factory-assembled four-layer SMT board. These five samples are for adult-supervised engineering qualification, not finished toys.

## Flat parts and assembly order

1. Dry-fit the actual socketed ESP32, landscape screen, SD module, RGB, switches and plugged JSTs on the actual-size drawings. Print at 100% and measure the calibration line. Seller module revisions and socket retention remain unqualified.
2. Fit ALL R1-R43 horizontally, 10.16 mm pitch. No upright resistors. Fit flat axial D2, ceramic capacitors and empty DIP sockets; verify values before soldering.
3. Form Q1-Q6 to the flat-body outlines, marked flat face up, preserving numbered leads; support leads near the body. Do not swap Q6 LP0701N3-G for BC327.
4. Mount C1/C3/C5/C13/C17/C25 (ECEA1CKA101, 100uF/16V) and C9/C11/C15/C21 (ECEA1CKA100, 10uF/16V) horizontally on 0.5 mm insulating support. Maximum heights including support are 7.3 and 5.0 mm respectively. Full maximum can length is 8 mm. Pad1 positive, striped negative lead pad2. The 10uF part's native 1.5 mm leads must be formed to 2.54 mm; 100uF uses 2.5 mm. Support at the seal; do not cross, twist or pull leads or block the pressure vent.
5. Fit rear JSTs/module sockets, IR emitter D1 and receiver U2 facing the top case window, then front screen/RGB sockets and nine soft switches. Tack one pin and check alignment before completing. IR optics, buttons, connectors and sockets retain functional height; do not flatten them.
6. Trim solder tails to <=2.5 mm and inspect both sides before inserting modules/chips. Debug holes are bare probe points, not tall headers beneath opposite-side parts. Support the display's free edge mechanically.
7. For the first removable stack mock-up, use four 20 mm M2 insulating standoffs between PCB faces. Main display/buttons face front; power component side faces rear cover. Power front-view X is mirrored relative to main front in the assembled stack. Verify plugged connector/wire bends; 20 mm is NOT approved final spacing. Main ESP32 rear envelope is about 15.3 mm; front RGB remains about 22.1 mm. Battery and complete case depth are not frozen.

Keep the marked antenna region free of metal, battery, hardware and loose wiring. Unscrew/unplug the power board for access to main-board solder joints and sockets. Use insulating barriers and strain relief; do not press a cell against solder tails.

'''
power='''## First power and integrated testing

Read the accompanying P3_REVIEW_AND_TEST.md before connecting anything. First qualify the power board alone with current-limited equipment and dummy loads; battery selection remains open. Main J1 is NOT a raw battery input. Do not combine ESP32 USB power and external SYS_IN until exact-module backfeed behavior is proven. Program the removable MCU separately for recovery; Wi-Fi app/game loading requires firmware not provided here.

Power J3 -> main J1: 1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2, pin-for-pin. The charger USB-C carries no data to main. Do not assume the two physically compatible speaker/motor plugs are interchangeable electrically.

P.3 screening load targets are 5 V/0.6 A, 3.3 V/0.4 A and 3.2 V/0.5 A; none is a measured rating. Older main-board reservations included 0.5 A on 3.3 V and additional RGB allowance. Those reservations were estimates, not measurements: the integrated peak budget remains an explicit bench qualification item. Do not silently treat a 0.4 A screening result as proof of a 0.5 A logic requirement. Test combined Wi-Fi, SD, RGB, IR, audio and motor peaks and adjust the design if capacity is insufficient.

Start with socketed loads and actuators disconnected. Check short circuits, pin polarity, rail nominal values, disabled amplifier/motor and unexpected current. Power OFF before changing connections. Scope rail rise/fall and GPIO back-powering before attaching all logic. Increase current limits only as justified by measured startup; stop for heat, oscillation or incorrect rails. R23 stays 100 ohm until the exact display backlight current is measured. Test motor short pulses without stalling, then audio at low volume; neither speaker output is ground. Record results for each sample.

'''
(MAIN/'assembly/ASSEMBLY_GUIDE.md').write_text(intro+orientation+power+firmware)
old=(ROOT/'docs/POWER_PROTOTYPE_REVIEW.md').read_text()
start=old.index('## Electrical review and limits')
body=old[start:]
body=body.replace('Front view left-to-right is 3V2, 3V3, GND, 5V because the header is rotated', 'Use current CONNECTOR_PIN_MAP.csv and pad numbers; do not infer order from an old or mirrored drawing')
body=body.replace('with 22 AWG wire', 'with Alpha 3050 24 AWG stranded wire for this prototype harness (same as main kit list)')
body=body.replace('some stock models remain unavailable', 'all 108 fitted model links resolve, but connector mating volumes and seller modules still need physical checks')
body=body.replace('50 × 50 mm', '96 × 105 mm').replace('R3 corners', 'R4 corners')
body=body.replace('CAD_AUDIT.json lists', 'VIA_IN_PAD_REVIEW.csv lists')
intro='''# P.3 power — five-sample engineering review and first-power-up

Current board: 96 x 105 mm, R4 corners, four layers, 1.6 mm thickness. Four 2.2 mm holes at (4,4), (92,4), (4,101), (92,101) mm match C.6 main. This package is for prototype DFM review; factory process/parts approval and physical/bench qualification remain required. Not a finished student product.

P.3 preserves the P.2 circuit and routed power core by rotating 180 degrees and translating x=51-old_x, y=104-old_y; every electrical pad/net/track/via geometry and layer was checked. Mounting holes, outline, antenna keepout and model attachments were deliberately revised. The wide 1.5 mm SYS_SW bridge on In1 and 0.6 mm C8 feed remain. In1 is NOT a completely uninterrupted ground plane. There are 3,515 track segments, 260 vias, 108 fitted parts and 28 rear bare test pads.

All current coordinates come from the P.3 native PCB. Power component side faces the rear cover; power front-view X is mirrored relative to main front when stacked. USB is near the bottom and the switch near the left edge in native front view: check actual cable overmold and case actuator clearance. Keep the 60 x 38 mm upper RF region free of metal, wiring and battery. Start a fit mock-up with 20 mm insulating spacers; plugged JSTs and wire bends can need more. Clip solder tails to <=2.5 mm and use insulating barriers. The cell and final case spacing are not selected.

TP4 is system GND. TP3 is BAT_NEG, NOT GND. Never bypass battery protection by shorting those returns with grounded test equipment. Use TEST_POINTS.csv rather than old P.2 coordinates.

The included electrical screening was inherited unchanged from P.2 because the circuit did not change. Its calculations are not new measurements or qualified output ratings. Main's older 3.3 V reservation was 0.5 A while this screening target is 0.4 A: reconcile the actual integrated load with bench measurements before approving product use.

'''
(POWER/'assembly/P3_REVIEW_AND_TEST.md').write_text(intro+body)
fab=(ROOT/'docs/POWER_FABRICATION_REQUIREMENTS.md').read_text().replace('P.2', 'P.3').replace('50 × 50 mm', '96 × 105 mm').replace('R3 corners', 'R4 corners').replace('`CAD_AUDIT.json` lists via centers', '`VIA_IN_PAD_REVIEW.csv` lists via centers')
(POWER/'assembly/FABRICATION_REQUIREMENTS.md').write_text(fab)
copy(POWER/'assembly/P3_REVIEW_AND_TEST.md', MAIN/'assembly/P3_REVIEW_AND_TEST.md')
print('Prepared current BOM notes, complete kit extras, portable datasheet references and C6/P3 assembly/test guides; no CAD edits.')
