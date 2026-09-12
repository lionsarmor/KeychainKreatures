"""C.5 assembly outputs, explicitly separate from historical C.4 release."""
from pathlib import Path
import csv,json,html,xml.etree.ElementTree as ET,shutil,sys,hashlib
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout';assembly=out/'assembly';assembly.mkdir(exist_ok=True)
x=ET.parse(out/'netlist.xml').getroot();p=json.loads((out/'placement.json').read_text())['positions'];up=set(json.loads((out/'upright_refs.json').read_text()))
rows=[]
for c in x.findall('./components/comp'):
 r=c.get('ref');fields={e.get('name'):e.text or '' for e in c.findall('./fields/field')}
 notes=fields.get('Review','').replace('C.4','C.5')
 if r in up:notes+=' C.5 upright resistor, 2.54mm pitch. Same MPN/value; form long return lead with clearance.'
 if r=='D1':notes+=' C.5 rear top-facing formed leads: nominal lens axis 5mm off rear PCB. Verify optical direction and lead form.'
 rows.append({'Reference':r,'Quantity':1,'Value':c.findtext('value'),'MPN':fields.get('MPN',''),'Footprint':c.findtext('footprint'),'Side':p[r]['side'],'Datasheet':c.findtext('datasheet',''),'Notes':notes.strip()})
def writecsv(file,rr):
 with file.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
writecsv(assembly/'C5_BOM_BY_REFERENCE.csv',rows)
with (root/'assembly/C4_KIT_EXTRAS.csv').open(newline='') as f:extras=list(csv.DictReader(f))
extras=[{k:v.replace('C.4','C.5').replace('80 x 115','84 x 95') for k,v in row.items()} for row in extras]
writecsv(assembly/'C5_KIT_EXTRAS.csv',extras)
shutil.copy2(root/'assembly/C4_BENCH_TEST_RECORD.csv',assembly/'C5_BENCH_TEST_RECORD.csv')
with (root/'assembly/C4_TEST_POINT_MAP.csv').open(newline='') as f:debug=list(csv.DictReader(f))
# Rebuild coordinates from the new board placement, never carry C.4 coordinates.
tp=[]
for r,pos in p.items():
 if r.startswith('TP'):
  pp=pos['pads']['1'];tp.append({'Reference':r,'Net':pp['net'],'X_mm':pp['xy'][0],'Y_mm':pp['xy'][1],'Probe_side':'rear preferred; bare through-hole','Notes':'No fitted posts; see native board for adjacent nets.'})
writecsv(assembly/'C5_TEST_POINT_MAP.csv',sorted(tp,key=lambda r:int(r['Reference'][2:])))
esc=html.escape
def table(rr):
 keys=list(rr[0]);return '<table><thead><tr>'+''.join('<th>'+esc(k)+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(str(r[k]))+'</td>' for k in keys)+'</tr>' for r in rr)+'</tbody></table>'
(assembly/'C5_BOM_PRINT.html').write_text('<!doctype html><meta charset="utf-8"><title>C.5 prototype kit BOM</title><style>body{font:12px sans-serif}table{border-collapse:collapse;width:100%;margin-bottom:24px}th,td{border:1px solid #aaa;padding:4px;text-align:left;overflow-wrap:anywhere}thead{display:table-header-group}tr{break-inside:avoid}@media print{@page{size:A4 landscape;margin:10mm}}</style><h1>Keychain Kreatures C.5 — engineering prototype</h1><p>84 × 95 mm. 98 circuit positions; 25 upright resistors, rear MCU/SD/IR, landscape screen. No powered qualification. Supply, speaker, LED socket and physical-fit holds: see CIRCUIT_REVIEW.md and ASSEMBLY_GUIDE.md.</p><h2>PCB population</h2>'+table(rows)+'<h2>Kit extras, sockets and mating plugs</h2>'+table(extras))
guide=(root/'assembly/ASSEMBLY_GUIDE.md').read_text().replace('C.4','C.5').replace('C4_','C5_')
# Relative links in the inherited guide are retargeted to the original evidence folder.
guide=guide.replace('../component_review/','../../component_review/').replace('../pcb/','../')
guide=guide[guide.index('## Parts whose orientation matters'):]
guide=guide.split('C.5 reroutes four LED connections')[0]
prefix='''# C.5 layout-specific assembly instructions — read first

The following C.5 instructions supersede old C.4 positions, fit sheets and front/back assignments. Use only the C.5 board and BOM together.

- Board is **84 × 95 × 1.6 mm**, rounded corners. Screen is landscape on the front; D-pad left, four actions right and one mode button in the center, all below the screen.
- **Rear:** ESP32 socket, SD socket, IR emitter/receiver, DIP sockets, power/motor/speaker JSTs and supporting circuitry. **Front:** screen socket, nine soft buttons and socketed RGB. Passives and small transistors are soldered.
- ESP32 antenna points to the top; its USB faces the board interior. Service it with the rear cover removed or the module unplugged. Keep metal and wiring away from the marked antenna area on both sides.
- IR D1 is the same TSAL6200, but its leads are formed so the lens points toward the top edge, alongside U2. Proposed optical-axis height is 5 mm off the rear surface. Do not bend immediately at the epoxy or reverse the cathode/anode; use the pin-1 mark and meter check. Physical qualification is pending.
- Upright resistors use **2.54 mm hole pitch**, not the old 10.16 mm flat footprint. Form them with a jig, insulate the return lead if necessary, and inspect for shorts before power. No resistor value or MPN changed. Upright references: **UPRIGHT_REFS**.
- Trim rear-component leads before fitting the screen. Check clearance under both screen and socketed modules. Support the display's free edge with shell features/spacers; the single socket must not take button or drop loads.
- SD insertion is toward the right edge as viewed from the front (left when looking at the rear). Keep the card/eject path clear. Use the socket, not soldered permanent module pins.
- RGB socket grip on the actual LED leads remains unqualified. Do not tin pins to force a fit. Its proposed front height is 22.1 mm; combined front/back components can require about **39 mm depth before shell clearance**.
- J1 requires coordinated **5 V / GND / 3.3 V / 3.2 V**, not raw battery power. Never assume the unfinished power module or simultaneous module USB is safe.
- Pin-1 squares, polarity marks and front/back fit sheets govern orientation. Some legends are beneath installed parts and are meant to be read during assembly. Bare test holes must not be populated with posts beneath opposite-side assemblies.
- Physical fit, powered bring-up, audio limits, firmware, optical windows, enclosure and battery are not qualified by the PCB checks. See [circuit review](../CIRCUIT_REVIEW.md) and fill in the bench record with real measurements.

---

'''.replace('UPRIGHT_REFS',', '.join(sorted(up,key=lambda r:int(r[1:]))))
(assembly/'ASSEMBLY_GUIDE.md').write_text(prefix+'''## Soldering order

1. Sort all 43 resistors with a meter. Populate flat resistors and D2 first, then ceramics and empty DIP sockets.
2. Populate the marked upright resistors and small transistors using their correct lead forms; do not confuse the two resistor pitches.
3. Fit rear electrolytics, JSTs and module sockets, followed by rear IR parts and front screen/RGB sockets and buttons. Check alignment after soldering one pin.
4. Trim and inspect both faces. Perform the unpowered continuity/polarity checks before inserting ICs, modules or the RGB LED.
5. Attach separately checked harnesses and mechanical supports, then proceed through the current-limited bring-up gates.

'''+guide)
print('C5 BOM, kit extras, debug map and pending bench/assembly guides generated.')
if '--sync-root' in sys.argv:
 assert hashlib.sha256((root/'KK_main_module.kicad_pcb').read_bytes()).digest()==hashlib.sha256((out/'KK_main_module.kicad_pcb').read_bytes()).digest(),'Root has new edits; do not overwrite assembly files.'
 for file in assembly.iterdir():
  if file.is_file() and file.name!='ASSEMBLY_GUIDE.md':shutil.copy2(file,root/'assembly'/file.name)
 text=(assembly/'ASSEMBLY_GUIDE.md').read_text().replace('../CIRCUIT_REVIEW.md','../C5_relayout/CIRCUIT_REVIEW.md').replace('../../component_review/','../component_review/')
 (root/'assembly/ASSEMBLY_GUIDE.md').write_text(text)
