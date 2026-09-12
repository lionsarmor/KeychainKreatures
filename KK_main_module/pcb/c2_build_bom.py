"""Generate purchasing and reference BOMs from the authoritative C.2 netlist."""
from pathlib import Path
import csv,json,xml.etree.ElementTree as ET,collections,html,hashlib
root=Path(__file__).resolve().parent.parent;out=root/'assembly';out.mkdir(exist_ok=True)
xml=ET.parse(root/'pcb/board_netlist.xml').getroot()
positions={r['reference']:r for r in json.loads((root/'pcb/PLACEMENT.json').read_text())['components']}
rows=[]
for c in xml.findall('./components/comp'):
    ref=c.attrib['ref'];fields={f.attrib['name']:f.text or '' for f in c.findall('./fields/field')}
    rows.append({'Reference':ref,'Quantity':1,'Value':c.findtext('value'),'MPN':fields.get('MPN',''),'Footprint':c.findtext('footprint'),'Side':positions[ref]['side'],'Datasheet':c.findtext('datasheet',''),'Notes':fields.get('Review','')})
assert len(rows)==91 and len({r['Reference'] for r in rows})==91
def writecsv(name,rs):
    with (out/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
writecsv('C2_BOM_BY_REFERENCE.csv',rows)
groups=collections.defaultdict(list)
for r in rows:groups[(r['MPN'],r['Value'],r['Footprint'])].append(r)
grouped=[]
for (_,_,_),rs in groups.items():
    r=rs[0];grouped.append({'Quantity':len(rs),'References':', '.join(x['Reference'] for x in rs),'MPN':r['MPN'],'Value':r['Value'],'Footprint':r['Footprint'],'Datasheet':r['Datasheet']})
writecsv('C2_PCB_BOM.csv',grouped)
extras=[]
def add(q,part,description,source,note=''):extras.append({'Quantity per kit':q,'Part / specification':part,'Description':description,'Source / drawing':source,'Assembly note':note})
base='../component_review/datasheets/'
add('1','KK MAIN C.2','80 x 100 x 1.6 mm two-layer prototype PCB','../manufacturing/README.md','Do not fabricate until release checks pass.')
add('2','PPTC091LFBN-RC','Sullins 1x9 MCU sockets',base+'sullins-female-headers.pdf','MOD1 is already counted in the PCB BOM; these sockets are additional.')
add('1','ED281DT','On Shore narrow 28-pin DIP socket',base+'dip-sockets.pdf','For U1; 7.62 mm rows, not wide ED28DT.')
add('1','ED08DT','On Shore 8-pin DIP socket',base+'dip-sockets.pdf','For U3; notch matches pin-1 marking.')
add('1','XIITIA / Amazon B0DFWL25RB','240 x 280 ST7789V2 screen module','https://www.amazon.com/dp/B0DFWL25RB','J2 socket is already counted. Retain R23=100 ohm until BLK current is measured.')
add('1','GODIYMODULES / Amazon B0F82XWT4F','3.3 V six-pin microSD module','https://www.amazon.com/dp/B0F82XWT4F','J3 socket is already counted. Card not included with reader.')
add('1','TS32GUSD300S','Transcend 32 GB microSDHC card',base+'transcend-usd300s.pdf','FAT32; actual SPI-mode read/write and power-loss tests required. Not extra RAM.')
add('1','LCM0827A3038F','LEADER 3 V coin vibration motor',base+'motor.pdf','Prepare wired harness before giving kit to students; do not crimp 24-AWG terminals onto its AWG32 leads.')
add('1','FS1511P08-H3.0 wired / 8 ohm','FUET prototype speaker','../component_review/MODULE_SOURCE_NOTES.md','Prototype selection only: exact continuous power rating remains undocumented. Start volume low; do not release a student product on a guessed rating.')
add('2 if absent from MCU bundle','TSW-109-07-G-S','Samtec 1x9 male module headers','https://www.samtec.com/products/tsw-109-07-g-s','Optional replacement, do not count twice. Check contact engagement in the selected female sockets.')
add('1 if absent from screen bundle','TSW-108-07-G-S','Samtec 1x8 male screen header','https://www.samtec.com/products/tsw-108-07-g-s','Optional replacement. Solder on the correct side of the display module.')
add('1 if absent from SD bundle','TSW-106-07-G-S','Samtec 1x6 male SD header','https://www.samtec.com/products/tsw-106-07-g-s','Optional replacement, do not count twice.')
add('1','XHP-4','JST-XH four-way mating SYS_IN housing',base+'jst-xh.pdf','For J1. Future power-board connector at other cable end is deliberately excluded.')
add('4','SXH-001T-P0.6','JST-XH crimp contacts',base+'jst-xh.pdf','For 24-AWG SYS_IN wires. Use specified crimp tool and pull-test, not solder-filled crimps.')
add('2','PHR-2','JST-PH motor and speaker mating housings',base+'jst-ph.pdf','Label MOTOR and SPEAKER; identical keys do not prevent swapping.')
add('4','SPH-002T-P0.5S','JST-PH contacts for 24-AWG pigtails',base+'jst-ph.pdf','These go on added Alpha 3050 pigtails, NOT directly on the motor AWG32 leads.')
add('8 x 150 mm cut lengths','Alpha Wire 3050, 24 AWG stranded, color-coded','SYS_IN 4 conductors; speaker 2; motor 2','https://www.alphawire.com/products/wire/hook-up-wire/premium/3050','1.2 m total before trimming; OD 0.056 +/-0.002 in fits selected PH/XH contact ranges. Prototype harness lengths, adjust to shell later.')
add('4 x 15 mm cut lengths','RNF-100-1/16-0-STK / TE 5052892055','Insulation for four actuator-lead/pigtail splices','https://www.te.com/en/product-5052892055.html','Adult-prepared harnesses. Check sleeve fits joint, covers insulation at both ends, and add separate strain relief; not battery insulation.')
add('4','M2 x 15 mm nylon female/female standoff','Prototype bench supports','Commodity dimensional specification','Provides rear-component clearance; not final enclosure hardware.')
add('4','M2 x 5 mm nylon screw','Attach board to bench standoffs','Commodity dimensional specification','Four 2.2 mm NPTH mounting holes. Do not overtighten.')
add('4','M2 nylon flat washer','Mounting washers','Commodity dimensional specification','Keep hardware within reserved mounting area.')
add('As fitted','Nonconductive display support and motor/speaker retention','Prototype mechanical support / strain relief','Measure assembled stack','Do not suspend screen mechanically by its header alone. Final shell/support dimensions remain an enclosure task.')
writecsv('C2_KIT_EXTRAS.csv',extras)
def table(rs):
    keys=list(rs[0]);return '<table><thead><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in keys)+'</tr>' for r in rs)+'</tbody></table>'
intro='C.2 engineering-prototype BOM. All 91 schematic positions are accounted for. J2/J3 already include their female sockets; do not buy them twice. Power module, battery and enclosure are outside this main-board release. Speaker rating, delivered module revisions and powered qualification remain release holds.'
(out/'C2_BOM_PRINT.html').write_text('<!doctype html><html><meta charset="utf-8"><title>KK Main C.2 BOM</title><style>body{font:12px sans-serif;margin:20px}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{border:1px solid #aaa;padding:5px;text-align:left;overflow-wrap:anywhere}thead{display:table-header-group}tr{break-inside:avoid}@media print{@page{size:A4 landscape;margin:10mm}}</style><h1>Keychain Kreatures — C.2 prototype BOM</h1><p>'+intro+'</p><h2>PCB population</h2>'+table(grouped)+'<h2>Additional kit materials</h2>'+table(extras)+'</html>')
(out/'README.md').write_text('# C.2 prototype assembly packet\n\n'+intro+'\n\n- [Print the complete BOM](C2_BOM_PRINT.html)\n- [Grouped PCB purchasing BOM](C2_PCB_BOM.csv)\n- [Every reference and its board side](C2_BOM_BY_REFERENCE.csv)\n- [Sockets, modules, mating plugs and wiring](C2_KIT_EXTRAS.csv)\n- [Assembly and bring-up guide](ASSEMBLY_GUIDE.md)\n\nOlder BOMs elsewhere in the project are historical and must not be combined with C.2. Optional bundled headers are not extra required purchases. Order at most a small engineering prototype batch before electrical tests.\n')
print(f'{len(rows)} PCB references, {len(grouped)} purchasing groups, {len(extras)} kit-material rows.')
