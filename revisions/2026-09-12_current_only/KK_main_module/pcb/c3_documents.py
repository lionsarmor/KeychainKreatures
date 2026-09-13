"""Generate current debug/connector BOM and bare-pad service map."""
from pathlib import Path
import json,csv,collections,html,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent.parent;out=root/'assembly'
plan=json.loads((root/'pcb/C3_DEBUG_PLAN.json').read_text())
def writecsv(name,rows):
    with (out/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (out/'C2_BOM_BY_REFERENCE.csv').open() as f:rows=list(csv.DictReader(f))
for r in rows:
    if r['Reference'].startswith('SW'):
        r['Notes']='200 ohm maximum closed contact resistance; custom 8 x 4.5mm ABCD footprint assigned. Dry-fit actual switch height; verify A/B and C/D contact pairs.'
    if r['Reference'] in ['J4','J5']:
        r.update(MPN='B2B-PH-K-S(LF)(SN)',Footprint='KK_Main:JST_PH_B2B_2',Notes='C.3 top-entry JST-PH; not the former right-angle S2B. Mating PHR-2 remains unchanged.')
xml=ET.parse(root/'pcb/c3_netlist.xml').getroot()
new_sides={r['reference']:r['side'] for r in json.loads((root/'pcb/C3_RGB_PLACEMENT.json').read_text())}
for c in xml.findall('./components/comp'):
    ref=c.attrib['ref']
    if ref not in new_sides:continue
    fields={f.attrib['name']:f.text or '' for f in c.findall('./fields/field')}
    rows.append({'Reference':ref,'Quantity':'1','Value':c.findtext('value'),'MPN':fields['MPN'],'Footprint':c.findtext('footprint'),'Side':new_sides[ref],'Datasheet':c.findtext('datasheet') or '', 'Notes':fields.get('Review','')})
assert len(rows)==98 and len({r['Reference'] for r in rows})==98
writecsv('C3_BOM_BY_REFERENCE.csv',rows)
groups=collections.defaultdict(list)
for r in rows:groups[r['MPN'],r['Value'],r['Footprint']].append(r)
grouped=[{'Quantity':len(rs),'References':', '.join(r['Reference'] for r in rs),'MPN':rs[0]['MPN'],'Value':rs[0]['Value'],'Footprint':rs[0]['Footprint'],'Datasheet':rs[0]['Datasheet']} for rs in groups.values()]
writecsv('C3_PCB_BOM.csv',grouped)
with (out/'C2_KIT_EXTRAS.csv').open() as f:extras=list(csv.DictReader(f))
extras[0]['Part / specification']='KK MAIN C.3 RGB PROTOTYPE'
extras[0]['Description']='80 x 115 x 1.6 mm two-layer through-hole prototype PCB'
extras[0]['Assembly note']='Engineering prototype only; powered qualification required.'
extras.insert(4,{'Quantity per kit':'1','Part / specification':'ED16DT','Description':'On Shore 16-pin narrow DIP socket for U4','Source / drawing':'../component_review/datasheets/dip-sockets.pdf','Assembly note':'7.62mm rows, 2.54mm pitch; match the U4 pin-1 notch. Not a wide socket.'})
writecsv('C3_KIT_EXTRAS.csv',extras)
def table(rs):
    keys=list(rs[0]);return '<table><thead><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in keys)+'</tr>' for r in rs)+'</tbody></table>'
intro='C.3 RGB engineering prototype: 98 component positions, 25 bare plated test holes, 80 x 115mm PCB. Includes separate RGB D3 and driver U4; D1 remains infrared. D3 requires lead forming from 1.27mm to 2.54mm pitch; use the assembly guide and by-reference BOM notes. U4 needs the ED16DT socket listed below. J4/J5 use vertical B2B-PH, not side-entry S2B-PH. Power module, battery and enclosure are separate. Exact speaker rating, module revisions and powered qualification remain release holds.'
(out/'C3_BOM_PRINT.html').write_text('<!doctype html><html><meta charset="utf-8"><title>KK C3 RGB prototype BOM</title><style>body{font:12px sans-serif;margin:20px}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{border:1px solid #aaa;padding:5px;text-align:left}thead{display:table-header-group}tr{break-inside:avoid}@media print{@page{size:A4 landscape;margin:10mm}}</style><h1>KK C.3 — RGB ENGINEERING PROTOTYPE</h1><p>'+intro+'</p>'+table(grouped)+table(extras)+'</html>')
service=[{'Pad':i['ref'],'Signal':i['label'],'Net':i['net'],'Same net as':i['source_pin'],'Probe face':i['probe_side'],'X mm':i['xy'][0],'Y mm':i['xy'][1],'Added tap mm':round(i['stub_mm'],3)} for i in plan]
writecsv('C3_TEST_POINT_MAP.csv',service)
lines=['# C.3 debug pads and safe measurements','',
'25 bare plated holes: 2.0 mm exposed copper diameter, 0.8 mm drill. No additional component is purchased or installed. TP numbering deliberately has gaps where no useful, clearly labelled site fitted. Coordinates below use the normal PCB editor front-view axes; the rear print is mirrored.', '',
'## Access and repair limits','',
'- Probe only from the listed face. Front access may require removing the socketed screen, SD reader or MCU. The carrier does not guarantee access through the finished enclosure.',
'- These holes have no fitted wire loops or test-point posts. Some lie beneath a component on the opposite face. Do not push a long lead through into that component; keep any repair solder/wire clear of its body and pins. Prefer a surface-soldered insulated wire on the accessible face.',
'- Pads expose existing nets; they do NOT disconnect miswired traces. Power off before continuity checks or soldering. Correcting a short may still require cutting and verifying a trace.',
'- Never clip an earth-referenced scope ground to speaker outputs, MOTOR_RETURN, BLK or MOSFET gates. Scope ground clips go only to a GND point. Use differential measurement for the bridge speaker.',
'- Do not use these as extra power inputs. No raw battery and no USB plus SYS_IN together. Use the coordinated, current-limited source described in the assembly guide.',
'- MCU TX/RX header positions serve the TFT; they are not a spare debug UART. EN/BOOT remain on the removable MCU. Initial/recovery flashing is performed with that module removed from the carrier.', '',
'## Coverage','',
'Supply rails, three GND access points, I2C, button interrupt/function, SPI clock/MOSI/SD-CS, display controls/backlight, audio PWM/filter output, motor return, IR transmit/receive/filtered supply and expander reset. MISO, amplifier VCC/input/enable, speaker outputs and motor gate/enable retain accessible component solder joints; this pass does not claim a separate test hole for every circuit node.', '',
'| Pad | Signal | Same net as | Probe face | X, Y (mm) |','|---|---|---|---|---|']
for i in plan:lines.append(f"| {i['ref']} | {i['label']} | {i['source_pin']} | {i['probe_side']} | {i['xy'][0]:.2f}, {i['xy'][1]:.2f} |")
lines+=['','## Expected observations','',
'TP1: nominal 5 V. TP2: nominal 3.3 V. TP3: nominal 3.2 V. Ground points read near 0 V relative to J1 pin 2. TP32 is the IR receiver supply after its series resistor, slightly below the logic rail depending on load.',
'Logic pads use 3.3 V signaling; activity and idle states depend on firmware. TP23 carries filtered, DC-biased audio, not a speaker output. TP29 is the switched motor return: not a permanent ground. Do not infer a working firmware protocol from a DC meter reading.', '',
'## CAD review exception','',
'The C.3 custom courtyard rule applies only to bare TP footprints. KiCad normally assumes a physical lead passes through every plated component hole; that assumption does not apply to these unpopulated probe holes. Opposite-face body intersections are deliberately allowed, while copper, drill, mask and edge clearances remain enforced. Never populate these holes with posts or loops without a new mechanical review. No general DRC category was disabled for this addition.']
(out/'C3_DEBUG_GUIDE.md').write_text('\n'.join(lines)+'\n')
print('Generated 98-reference RGB BOM, kit extras and 25-point debug map.')
