"""P.2 compact prototype circuit. Preserve P.1 and the legacy root project."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'P2_compact'
OUT.mkdir(exist_ok=True);(OUT/'datasheets').mkdir(exist_ok=True)
if not (OUT/'stage.json').exists():shutil.copy2(ROOT/'P1_revision/stage.json',OUT/'stage.json')
s=(ROOT/'p1_design.py').read_text()
def replace(old,new):
    global s
    assert old in s,old
    s=s.replace(old,new)
replace("OUT=ROOT/'P1_revision'","OUT=ROOT/'P2_compact'")
replace('kk-power-p1:','kk-power-p2:')
replace('P.1 ENGINEERING','P.2 PROTOTYPE DRAFT')
replace('POWER P.1','POWER P.2')
replace("stock('Regulator_Linear','TLV75533PDBV')","stock('Regulator_Linear','TLV75533PDBV')\nstock('Battery_Management','BQ24075RGT','BQ24075T')")
replace("# Freeze project-local copies",'''# P.2: voltage-based battery temperature monitoring permits a deliberately
# narrower charging window with the cell-bonded Semitec 103AT-2 sensor.
DATASHEETS['BQ24075TRGTR']='https://www.ti.com/lit/ds/symlink/bq24075t.pdf'
DATASHEETS['103AT-2']='https://www.semitec-global.com/uploads/2022/01/P12-13-AT-Thermistor.pdf'
u=next(p for p in PARTS if p['ref']=='U1')
u.update(symbol='BQ24075T',value='BQ24075TRGTR',mpn='BQ24075TRGTR',datasheet=DATASHEETS['BQ24075TRGTR'],note='Voltage-based TS network; only the T variant is valid. SYSOFF pin 15 grounded. Approx. 300mA charge target. No NTC bypass.')
u['nets']['15']='GND'
p=next(p for p in PARTS if p['ref']=='R1')
p.update(value='887k',mpn='RC0603FR07887KL',note='1%; standard E96 value. TUSB320LAI rev D recommended VBUS resistor range 855..920kohm, nominal 887kohm.')
p=next(p for p in PARTS if p['ref']=='R4')
p.update(value='2.94k',mpn='RT0603BRD072K94L',note='0.1%; below the 3kohm maximum programming resistance including tolerance.')
p=next(p for p in PARTS if p['ref']=='R71')
p.update(value='634',mpn='RT0603BRD07634RL',note='0.1%; high-mode external limiter near 2A, above the charger internal 1.23A limit. Prevents two current limiters fighting. Charger sets the advertised-source ceiling.')
g='CELL CHARGER / POWER PATH'
R('R74','31.6k','USB_CHG','NTC',g,True)
R('R75','20k','NTC','GND',g,True)
# The TI reference design already uses two input and three output ceramics.
# Remove the six redundant extra bypasses; retain each AUX capacitor.
removed={'C26','C27','C36','C37','C46','C47','J5'}
PARTS[:]=[p for p in PARTS if p['ref'] not in removed]
for group in GROUPS:GROUPS[group][:]=[p for p in GROUPS[group] if p['ref'] not in removed]
for i,net in enumerate(['PGOOD_N','CHARGE_N','VOLTAGES_OK'],26):
    add('TP'+str(i),'TestPoint',net,'BARE PCB PAD',{1:net},'MAIN BOARD HARNESS / DEBUG','TestPoint:TestPoint_Pad_D1.5mm','Backside bare probe pad; replaces bulky service header.')
for ref,u in [('C28','U5'),('C38','U6'),('C48','U7')]:
    p=next(p for p in PARTS if p['ref']==ref)
    p.update(nets={'1':u+'_FB','2':'GND'},note='10pF across the lower feedback resistor per TPS63060 datasheet, not an upper-divider feedforward capacitor.')
for p in PARTS:
    if p['ref'] in ['U5','U6','U7']:
        p['footprint']='Package_SON:Texas_S-PWSON-N10'
# Freeze project-local copies''')
exec(compile(s,str(ROOT/'p1_design.py'),'exec'),globals())
import json
p=json.loads((OUT/'KK_power_module.kicad_pro').read_text())
rules=p['board']['design_settings']['rules']
rules.update(min_track_width=.15,min_clearance=.1,min_hole_clearance=.2,min_hole_to_hole=.25,min_via_diameter=.5,min_through_hole_diameter=.2,min_via_annular_width=.15,min_copper_edge_clearance=.4)
for cls in p['net_settings']['classes']:
    cls.update(clearance=.15,via_diameter=.5,via_drill=.2)
    if cls['name']=='Default':cls['track_width']=.2
p['board']['design_settings']['drc_exclusions']=[]
(OUT/'KK_power_module.kicad_pro').write_text(json.dumps(p,indent=2)+'\n')
