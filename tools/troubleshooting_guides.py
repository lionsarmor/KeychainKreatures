"""Build student troubleshooting HTML/PDF/worksheets; never edits CAD/releases.

Uses existing MarkdownIt and a temporary isolated LibreOffice profile. Run sequentially
with nice -n 15 taskset -c 0. PDFs are documentation, not new fabrication files.
"""
from pathlib import Path
import csv, hashlib, json, re, shutil, subprocess, tempfile, zipfile
import xml.etree.ElementTree as ET
from urllib.parse import quote
from markdown_it import MarkdownIt

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'docs/troubleshooting'
OUT.mkdir(parents=True,exist_ok=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rel(p):return str(p.relative_to(ROOT))
def rows(p):
    with p.open(newline='') as f:return list(csv.DictReader(f))
def write_csv(p,header,data):
    with p.open('w',newline='') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(data)

index=read(ROOT/'docs/CURRENT_RELEASE_INDEX.json')
baseline={}
for b in index['boards']:
    ver=read(ROOT/b['directory']/'RELEASE_VERIFICATION.json')
    for n,h in ver['source_sha256'].items():
        p=ROOT/b['source']/n;assert sha(p)==h,'Source differs from released revision: '+str(p)
        baseline[rel(p)]=h
    for key,hashkey in [('zip','zip_sha256'),('gerbers_zip','gerbers_sha256')]:
        assert sha(ROOT/b[key])==b[hashkey]
        baseline[b[key]]=b[hashkey]

def netmap(p):
    out={}
    for n in ET.parse(p).findall('./nets/net'):
        for node in n.findall('node'):out[node.attrib['ref']+'.'+node.attrib['pin']]=n.attrib['name'].lstrip('/')
    return out
main=netmap(ROOT/'KK_main_module/netlist.xml');power=netmap(ROOT/'KK_power_module/netlist.xml')
expected_main={'J1.1':'MCU_5V','J1.2':'GND','J1.3':'LOGIC_3V3','J1.4':'ACT_3V2',
 'U1.9':'LOGIC_3V3','U1.10':'GND','U1.18':'Net-(U1-RESET_N)','U1.5':'AMP_EN','U1.6':'MOTOR_EN','U1.7':'TFT_RST_N',
 'U1.25':'RGB_DATA','U1.26':'RGB_CLK','U1.27':'RGB_LATCH','U1.28':'RGB_OE_N',
 'U3.1':'Net-(J5-+)','U3.3':'Net-(J5--)','U3.4':'GND','U3.2':'Net-(Q6-D)',
 'Q6.1':'ACT_3V2','Q6.3':'Net-(Q6-D)','U2.1':'IR_RX','U2.2':'GND','U2.3':'Net-(U2-VS)',
 'D3.2':'MCU_5V','J3.5':'SPI_MISO','MOD1.TX':'TFT_DC','MOD1.RX':'TFT_CS'}
expected_power={'J2.1':'CELL_PLUS','J2.2':'BAT_NEG','J3.1':'MCU_5V','J3.2':'GND','J3.3':'LOGIC_3V3','J3.4':'ACT_3V2','J4.1':'NTC','J4.2':'GND',
 'TP3.1':'BAT_NEG','TP4.1':'GND','U5.9':'REG_5V','U6.9':'REG_3V3','U7.9':'REG_3V2',
 'U8.6':'MCU_5V','U9.6':'LOGIC_3V3','U10.6':'ACT_3V2','U11.2':'VOLTAGES_OK','U11.4':'RAILS_EN','U12.15':'VOLTAGES_OK',
 'U3.7':'CC_DEFAULT_N','Q4.1':'CC_DEFAULT_N','Q4.3':'USB_HIGH_CURRENT','U13.B2':'USB_CHG'}
for actual,expected in [(main,expected_main),(power,expected_power)]:
    for p,n in expected.items():assert actual[p]==n,(p,actual[p],n)

main_notes={
1:'Main 5 V input; nominal 5.0 V.',2:'Logic supply; nominal 3.3 V.',3:'Actuator supply; nominal 3.2 V. NOT power-board BAT_NEG.',
4:'System ground reference.',6:'Alternate system ground.',8:'Alternate system ground.',
9:'I2C SDA; normally idle high with valid logic power.',10:'I2C SCL; normally idle high with valid logic power.',
11:'Active-low expander interrupt; requires firmware interrupt configuration.',12:'Function button; released high, pressed low.',
13:'Shared SPI clock; activity only during transfers.',14:'Shared SPI MOSI; activity during transfers.',
16:'SD chip select; normally high when deselected.',17:'Display chip select; normally high when deselected.',
18:'Display command/data selection; state depends on transfer.',19:'Display reset, active-low; controlled by U1 GPB6.',
20:'Backlight PWM before driver; meter shows only an average.',21:'Display BLK after switching/current-limiting path; load/PWM dependent.',
22:'Audio PWM before filter; inspect with scope and known test program.',23:'Second low-pass filter node, C19 pad 1/C20 input; waveform and DC bias depend on PWM. C19 is nonpolarized.',
29:'Switched motor return; near GND during ON, may float unloaded when OFF.',
30:'IR transmit logic; valid carrier bursts, not continuous DC test.',31:'IR receive output; normally high, low-going demodulated bursts.',
32:'IR receiver filtered supply; normally close to LOGIC_3V3.',33:'Expander reset; should rise high after startup.'}
power_notes={
1:'Raw USB VBUS; nominal 5 V when attached.',2:'Fused battery positive; interpret with protection state/reference.',
3:'BAT_NEG, cell-side return. Never use as a spare system GND.',4:'System GND; usual rail-measurement reference.',
5:'Charger/system power path output; varies with source and operating state.',6:'After eFuse; near SYS_RAW when enabled and healthy.',
7:'User run command; OFF near GND, ON near SYS_RAW.',8:'eFuse analog undervoltage divider; do not drive externally.',
9:'eFuse current-programming node; no universal digital level.',10:'Active-low eFuse fault; pull-up is to SYS_RAW, not fixed 3.3 V.',
11:'Regulator status, pulled toward REG_3V3; not independent supervisor output.',12:'Common output-gate enable; high after valid supervision.',
13:'Pre-gate 5 V regulator output.',14:'Pre-gate 3.3 V regulator output.',15:'Pre-gate 3.2 V regulator output.',
16:'Gated MCU_5V to J3 pin 1.',17:'Gated LOGIC_3V3 to J3 pin 3.',18:'Gated ACT_3V2 to J3 pin 4.',
19:'Analog thermistor node; depends on source and sensor. No forced logic levels.',
20:'CC-mode OUT1: high for default, low for 1.5/3 A attached advertisement.',
21:'Inverted mode control: low default, high for 1.5/3 A advertisement.',22:'USB supply after U13 current limiter, before charger.',
23:'USB current-limit programming node; do not drive externally.',24:'Active-low U13 fault; pull-up to VBUS. Use voltage-rated probe.',
25:'Dedicated CC supply, nominal 3.3 V with USB input.',26:'Charger input-good status, active-low via VBUS LED path; not 3.3 V logic.',
27:'Charge status, active-low via VBUS LED path; read with charge conditions.',28:'Independent supervisor result; high after valid rails and delay.'}

style='''
@page { size: A4; margin: 15mm 14mm 17mm; }
* { box-sizing: border-box; }
body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.4; color:#17202a; max-width: 185mm; margin: 0 auto; }
h1 { font-size: 24pt; line-height:1.15; border-bottom:3px solid #176b71; padding-bottom:5mm; }
h2 { font-size:16pt; color:#13585d; border-top:1px solid #bbc7cb; padding-top:4mm; margin-top:7mm; break-after:avoid; }
h3 { font-size:12pt; break-after:avoid; }
p,li { orphans:3; widows:3; }
li { margin-bottom:2mm; }
table { border-collapse:collapse; width:100%; font-size:9.5pt; line-height:1.3; margin:4mm 0; table-layout:auto; }
thead { display:table-header-group; background:#e6f1f2; }
tr { break-inside:avoid; }
th,td { border:1px solid #adbac2; padding:2mm; text-align:left; vertical-align:top; overflow-wrap:anywhere; }
td:first-child { min-width:15mm; }
code { font-family:monospace; background:#f0f2f3; overflow-wrap:anywhere; }
a { color:#13585d; overflow-wrap:anywhere; }
blockquote { border-left:4px solid #b86916; padding-left:4mm; margin-left:0; }
.printnote { background:#e6f1f2; padding:3mm; font-size:10pt; }
@media screen { body { padding:8mm; } }
'''
md=MarkdownIt('commonmark',{'html':False}).enable('table')
generated=[]
for kind,rev,notes in [('main','C6',main_notes),('power','P4',power_notes)]:
    src=ROOT/f'KK_{kind}_module';guide=src/'assembly'/f'TROUBLESHOOTING_{kind.upper()}_{rev}.md'
    item=next(b for b in index['boards'] if b['kind']==kind)
    issued=ROOT/item['directory']
    tp_hash=read(issued/'SHA256_MANIFEST.json')['files']['assembly/TEST_POINTS.csv']
    assert sha(src/'release_checks/TEST_POINTS.csv')==tp_hash
    assert sha(issued/'assembly/TEST_POINTS.csv')==tp_hash
    tp=rows(src/'release_checks/TEST_POINTS.csv')
    assert len(tp)==(25 if kind=='main' else 28)
    assert {int(r['Reference'][2:]) for r in tp}==set(notes)
    table=['| TP | Signal | What to expect / use | CAD X, Y mm |','|---|---|---|---|']
    measurement=[]
    for r in sorted(tp,key=lambda r:int(r['Reference'][2:])):
        assert r['Layer']=='B.Cu'
        number=int(r['Reference'][2:]);description=notes[number]
        # Main bare debug pads are board-only; their map is hash-checked against
        # the issued native PCB audit export above, not invented schematic pins.
        if kind=='power':
            actual=power[r['Reference']+'.1']
            assert actual==r['Signal'],(r['Reference'],actual,r['Signal'])
        table.append(f"| {r['Reference']} | `{r['Signal']}` | {description} | {r['CAD X mm']}, {r['CAD Y mm (down-positive)']} |")
        reference='Main TP4 GND' if kind=='main' else 'Power TP4 GND unless cell-side differential measurement explicitly specified'
        measurement.append(['',r['Reference'],r['Signal'],'',reference,description,'NOT RUN','','','',''])
    start='<!-- GENERATED_TEST_POINT_TABLE -->';end='<!-- END_GENERATED_TEST_POINT_TABLE -->'
    text=guide.read_text();block=start+'\n\n'+'\n'.join(table)+'\n\n'+end
    if end in text:text=re.sub(re.escape(start)+r'[\s\S]*?'+re.escape(end),lambda m:block,text)
    else:
        assert text.count(start)==1
        text=text.replace(start,block)
    guide.write_text(text)
    html=guide.with_suffix('.html')
    title=f'{rev} {kind} board troubleshooting'
    rendered=md.render(re.sub(r'<!--[\s\S]*?-->','',text))
    def published_link(m):
        href=m.group(1)
        if re.match(r'^(https?:|mailto:|#)',href):return m.group(0)
        target=(guide.parent/href).resolve()
        assert target.is_relative_to(ROOT) and target.exists(),target
        location='tree' if target.is_dir() else 'blob'
        return 'href="https://github.com/lionsarmor/KeychainKreatures/'+location+'/'+commit+'/'+quote(rel(target))+'"'
    rendered=re.sub(r'href="([^"]+)"',published_link,rendered)
    html.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>'+title+'</title><style>'+style+'</style></head><body><p class="printnote">Student/instructor engineering-prototype guide. Follow the safety gates; record unperformed tests as NOT RUN or BLOCKED.</p>'+rendered+'</body></html>')
    pdf=guide.with_suffix('.pdf')
    subprocess.run(['python3',str(ROOT/'tools/print_guide_pdf.py'),str(html),str(pdf),title],check=True,timeout=60)
    measure=src/'assembly'/f'TROUBLESHOOTING_{rev}_MEASUREMENTS.csv'
    write_csv(measure,['Board serial','Test point','Signal','Power / firmware / load state','Reference point used','Expected context','Status','Measured value and units','Instrument / range','Action / observations','Initials / date'],measurement)
    tests=[]
    for heading in re.findall(r'^## \d+\. ((?:M|P)\d+) — (.+)$',text,re.M):
        tests.append(['',heading[0],heading[1],'Instructor for live power / probes; supervised students where permitted','NOT RUN','','','',''])
    if kind=='main':
        for i,name in enumerate(['Up','Down','Left','Right','A','B','X','Y','Function'],1):
            tests.append(['',f'M5-SW{i}',name+': ten presses, hold, release; raw state and debounced event','Supervised test fixture','NOT RUN','','','',''])
        for test in ['Display colors/border/text/movement','SD file checksum before and after restart','RGB OFF/red/green/blue/reset','IR known receive and external transmit confirmation','Motor short pulse and rail dip','Audio differential DC / low-level tone / pops','Combined load and repeated cold starts']:
            tests.append(['','FUNCTION',test,'Instructor-approved setup','NOT RUN','','','',''])
    else:
        for test in ['Isolation / earth path reviewed','Default USB mode','USB-C 1.5 A mode','USB-C 3 A mode','Both USB-C plug orientations','Charge current / termination / recharge','NTC open / short / temperature response on emulator','Protection fault testing with approved fixture','Startup and shutdown sequencing','USB / GPIO backfeed qualification','One-rail loads then approved combined loads','Low-voltage cutoff / recovery on emulator']:
            tests.append(['','QUALIFICATION',test,'Qualified technician only','NOT RUN','','','',''])
    worksheet=src/'assembly'/f'TROUBLESHOOTING_{rev}_CHECKLIST.csv'
    write_csv(worksheet,['Board serial','Step','Test','Responsibility','Status','Setup / source / load / firmware','Measured evidence','Fault / action / retest','Initials / date'],tests)
    generated.extend([guide,html,pdf,measure,worksheet])

# No CAD, issued package or protected manufacturing output may have changed.
for p,h in baseline.items():assert sha(ROOT/p)==h,p
report={'scope':'Documentation-only supplement; no tests on physical boards performed','guide_version':1,'revisions':['C6','P4'],
        'source_and_issued_packages_unchanged':baseline,'critical_pin_net_assertions':len(expected_main)+len(expected_power),
        'test_points_cross_checked':{'main':25,'power':28},'artifacts':{rel(p):sha(p) for p in generated},
        'physical_tests_performed':False,'diagnostic_firmware_supplied':False,'status':'PASS — documentation generation and source-reference checks only'}
(OUT/'GUIDE_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'generated':[rel(p) for p in generated],'pin_checks':report['critical_pin_net_assertions'],'CAD_and_manufacturing_unchanged':True},indent=2))
