"""Generate the P.1 engineering schematic from an explicit pin/net manifest.

Never overwrites the released root project. Run on the host, then export the
netlist/ERC with native KiCad. All CAD edits are reproducible from this file.
"""
from pathlib import Path
import json,re,copy,uuid,csv
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'P1_revision'
META=json.loads((OUT/'stage.json').read_text()); LIB=Path(META['libraries']['Symbols'])
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'kk-power-p1:'+s))
def parse(s):
    t=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s); i=0
    def p():
        nonlocal i
        assert t[i]=='('; i+=1; a=[]
        while t[i]!=')':
            if t[i]=='(': a.append(p())
            else: a.append(t[i]); i+=1
        i+=1; return a
    return p()
def dump(a): return '('+' '.join(map(dump,a))+')' if isinstance(a,list) else str(a)
def val(s): return json.loads(s) if str(s).startswith('"') else s
def kids(a,k):return [x for x in a if isinstance(x,list) and x[0]==k]
def child(a,k):return next((x for x in a if isinstance(x,list) and x[0]==k),None)
q=json.dumps
defs={}; cache={}
DATASHEETS={
 'BQ24074RGTR':'https://www.ti.com/lit/ds/symlink/bq24074.pdf',
 'TUSB320LAIRWBR':'https://www.ti.com/lit/ds/symlink/tusb320lai.pdf',
 'TPS259530DSGR':'https://www.ti.com/lit/ds/symlink/tps2595.pdf',
 'TPS63060DSCR':'https://www.ti.com/lit/ds/symlink/tps63060.pdf',
 'TPS22918DBVR':'https://www.ti.com/lit/ds/symlink/tps22918.pdf',
 'SN74AUP1G17DBVR':'https://www.ti.com/lit/ds/symlink/sn74aup1g17.pdf',
 'TPS386000RGPR':'https://www.ti.com/lit/ds/symlink/tps386000.pdf',
 'TPS22950YBHR':'https://www.ti.com/lit/ds/symlink/tps22950.pdf',
 'TLV75533PDBVR':'https://www.ti.com/lit/ds/symlink/tlv755p.pdf',
 'AO3400A':'https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf',
 'DW01A':'https://hmsemi.com/downfile/DW01A.PDF',
 'FS8205':'https://www.ic-fortune.com/upload/Download/FS8205-DS-19_EN.pdf',
 'XFL4020-102MEC':'https://www.coilcraft.com/getmedia/50632d43-da1b-4cdb-8ab4-3029cab51df3/xfl4020.pdf',
 'JS102011SAQN':'https://www.ckswitches.com/media/1422/js.pdf',
 'HC-TYPE-C-16P-01A':'https://datasheet.lcsc.com/lcsc/2211161000_HCTL-HC-TYPE-C-16P-01A_C2894897.pdf',
}
def stock(lib,name,alias=None):
    if lib not in cache:cache[lib]={val(a[1]):a for a in kids(parse((LIB/(lib+'.kicad_sym')).read_text()),'symbol')}
    def resolve(n):
        d=copy.deepcopy(cache[lib][n]); e=child(d,'extends')
        if e:
            base=resolve(val(e[1])); props={val(x[1]) for x in kids(d,'property')}
            d=[x for x in d if x is not e]
            d.extend(copy.deepcopy(x) for x in base[2:] if isinstance(x,list) and (x[0]!='property' or val(x[1]) not in props))
        return d
    d=resolve(name); alias=alias or name; d[1]=q(alias)
    for j,u in enumerate(kids(d,'symbol')):
        suffix=re.search(r'(_\d+_\d+)$',val(u[1])).group(1)
        u[1]=q(alias+suffix)
    defs[alias]=d;return alias
def box(name,pins):
    # Pins specified explicitly from manufacturer numbering, not physical sides.
    left=[p for p in pins if p[2] not in ('output','power_out','open_collector')]
    right=[p for p in pins if p not in left]
    h=max(10.16,(max(len(left),len(right))+1)*2.54); w=25.4
    s=f'(symbol {q(name)} (pin_names(offset 0.6))(in_bom yes)(on_board yes)(property "Reference" "U"(at 0 0 0)(effects(font(size 1.27 1.27))))(property "Value" {q(name)}(at 0 0 0)(effects(font(size 1.27 1.27))))(symbol {q(name+"_0_1")}(rectangle(start {-w/2} {h/2})(end {w/2} {-h/2})(stroke(width 0.254)(type default))(fill(type background))))(symbol {q(name+"_1_1")}'
    for side,ps in [(-1,left),(1,right)]:
        for i,(n,label,typ) in enumerate(ps):
            y=(len(ps)-1)/2*2.54-i*2.54
            s+=f'(pin {typ} line(at {side*(w/2+5.08)} {y} {0 if side<0 else 180})(length 5.08)(name {q(label)}(effects(font(size 1.1 1.1))))(number {q(str(n))}(effects(font(size 1.1 1.1)))))'
    defs[name]=parse(s+'))');return name
def fpof(sym):return val(next(p for p in kids(defs[sym],'property') if val(p[1])=='Footprint')[2])
for lib,n in [('Device','R'),('Device','C'),('Device','L'),('Device','LED'),('Device','D_Schottky'),('Device','D'),('Device','Fuse'),('Transistor_FET','2N7002'),('Switch','SW_SPDT'),('Battery_Management','BQ24074RGT'),('Battery_Management','DW01A'),('Regulator_Switching','TPS63060')]:stock(lib,n)
stock('Connector','USB_C_Receptacle_USB2.0_16P','USB_C_Receptacle_USB2.0')
stock('Regulator_Linear','TLV75533PDBV')
stock('Transistor_FET','AO3400A')
for unit in kids(defs['USB_C_Receptacle_USB2.0'],'symbol'):
    for pin in kids(unit,'pin'):
        if val(child(pin,'number')[1])=='SH':child(pin,'number')[1]='"S1"'
# Manufacturer specifies open-drain PG; the stock symbol uses generic output.
for unit in kids(defs['TPS63060'],'symbol'):
    for pin in kids(unit,'pin'):
        if val(child(pin,'number')[1])=='5':pin[1]='open_collector'
box('TUSB320LAI',[(1,'CC1','bidirectional'),(2,'CC2','bidirectional'),(3,'PORT = SINK','input'),(4,'VBUS_DET','input'),(5,'ADDR = NC','input'),(6,'OUT3','open_collector'),(7,'OUT1','open_collector'),(8,'OUT2','open_collector'),(9,'ID','open_collector'),(10,'GND','power_in'),(11,'EN_N','input'),(12,'VDD','power_in')])
box('FS8205',[(1,'S1','passive'),(2,'D1','passive'),(3,'S2','passive'),(4,'G2 / OC','input'),(5,'D2','passive'),(6,'G1 / OD','input')])
box('TPS259530',[(1,'dVdt','passive'),(2,'EN / UVLO','input'),(3,'IN','power_in'),(4,'IN','power_in'),(5,'OUT','power_out'),(6,'FAULT_N','open_collector'),(7,'ILM','passive'),(8,'GND','power_in'),(9,'EP / GND','power_in')])
box('TPS22918',[(1,'VIN','power_in'),(2,'GND','power_in'),(3,'ON','input'),(4,'CT','passive'),(5,'QOD','passive'),(6,'VOUT','power_out')])
box('TPS22950', [('A1','ON','input'),('A2','FLT_N','open_collector'),('B1','VIN','power_in'),('B2','VOUT','power_out'),('C1','GND','power_in'),('C2','ILIM','passive')])
box('SN74AUP1G17',[(1,'NC','no_connect'),(2,'A','input'),(3,'GND','power_in'),(4,'Y','output'),(5,'VCC','power_in')])
box('TPS386000',[(1,'MR_N','input'),(2,'CT4','passive'),(3,'CT3','passive'),(4,'CT2','passive'),(5,'CT1','passive'),(6,'SENSE4H','input'),(7,'SENSE4L','input'),(8,'SENSE3','input'),(9,'SENSE2','input'),(10,'SENSE1','input'),(11,'NC / GND','passive'),(12,'GND','power_in'),(13,'VREF','output'),(14,'VDD','power_in'),(15,'RESET1_N','open_collector'),(16,'RESET2_N','open_collector'),(17,'RESET3_N','open_collector'),(18,'RESET4_N','open_collector'),(19,'WDO_N','open_collector'),(20,'WDI','input'),(21,'EP / GND','power_in')])
for name,labels in [('Battery',['CELL+','CELL-']),('Temperature',['NTC','GND']),('Output',['5V','GND','3V3','3V2']),('Status',['PGOOD_N','CHARGE_N','FAULT_N','GND','VBAT'])]:
    box(name,[(i+1,label,'passive') for i,label in enumerate(labels)])
stock('Connector','TestPoint')
PARTS=[]; GROUPS={}
def add(ref,sym,value,mpn,nets,group,footprint=None,note=''):
    pins={val(child(p,'number')[1]) for u in kids(defs[sym],'symbol') for p in kids(u,'pin')}
    nets={str(k):v for k,v in nets.items()};assert set(nets)==pins,(ref,pins,set(nets))
    d=dict(ref=ref,symbol=sym,value=value,mpn=mpn,nets=nets,group=group,footprint=footprint or fpof(sym),note=note,uuid=uid(ref),datasheet=DATASHEETS.get(mpn,''))
    PARTS.append(d);GROUPS.setdefault(group,[]).append(d);return d
RC='Resistor_SMD:R_0603_1608Metric'; CC='Capacitor_SMD:C_0805_2012Metric'; CSM='Capacitor_SMD:C_0603_1608Metric'
def R(ref,value,a,b,g,precision=False):
    # Yageo resistance code (e.g. 470RL, 1K3L, 100KL). Purchasing audit pending.
    if value.endswith('k') and float(value[:-1])>=1000:
        code=format(float(value[:-1])/1000,'g').replace('.','M')
        if 'M' not in code:code+='M'
        code+='L'
    elif value.endswith('k'):
        whole,sep,frac=value[:-1].partition('.')
        code=whole+'K'+frac+'L'
    else:code=value.replace('.','R')+('' if '.' in value else 'R')+'L'
    add(ref,'R',value,('RT0603BRD07' if precision else 'RC0603FR07')+code,{1:a,2:b},g,RC,'0.1% thin film' if precision else '1% thick film')
def C(ref,value,a,b,g):
    mpn={'100n':'GRM188R71C104KA01D','10u':'GRM21BR61C106KE15L','22u':'GRM21BR61C226ME44L','1u':'GRM188R71C105KA12D','10p':'GRM1885C1H100JA01D','10n':'GRM188R71H103KA01D','22n':'GRM188R71H223KA01D','47n':'GRM188R71H473KA01D','4.7u':'GRM21BR71C475KA73L'}[value]
    add(ref,'C',value,mpn,{1:a,2:b},g,CC if value in ['10u','22u','4.7u'] else CSM,'Check effective capacitance at operating bias; 16V minimum for bulk.')
g='USB-C CHARGING ONLY'
usb={p:None for p in ['A1','A4','A5','A6','A7','A8','A9','A12','B1','B4','B5','B6','B7','B8','B9','B12','S1']}
# Stock USB symbol has combined power/ground contacts, unlike its footprint.
usb={val(child(p,'number')[1]):None for u in kids(defs['USB_C_Receptacle_USB2.0'],'symbol') for p in kids(u,'pin')}
for n in usb:
    if n in ['A1','B1','A12','B12','S1']:usb[n]='GND'
    if n in ['A4','A9','B4','B9']:usb[n]='VBUS'
usb['A5']='CC1';usb['B5']='CC2'
add('J1','USB_C_Receptacle_USB2.0','USB-C CHARGE ONLY','HC-TYPE-C-16P-01A',usb,g,'KK_Power:USB_C_HCTL','All USB D+/D- and SBU pins intentionally NC. Shield grounded.')
add('U14','TLV75533PDBV','TLV75533PDBVR','TLV75533PDBVR',{1:'VBUS',2:'GND',3:'VBUS',4:None,5:'CC_3V3'},g,note='Dedicated USB-powered CC supply: TUSB320 VDD recommended maximum is 5V, so do not feed it raw USB. Not connected to main-board 3V3.')
C('C72','1u','CC_3V3','GND',g)
add('U3','TUSB320LAI','TUSB320LAIRWBR','TUSB320LAIRWBR',{1:'CC1',2:'CC2',3:'GND',4:'VBUS_DET',5:None,6:None,7:'CC_DEFAULT_N',8:None,9:None,10:'GND',11:'GND',12:'CC_3V3'},g,'Package_DFN_QFN:Texas_X2QFN-12_1.6x1.6mm_P0.4mm','Sink/GPIO mode; internal Rd. Pullups use the same regulated supply to avoid backpowering. Not a USB data controller.')
R('R1','900k','VBUS','VBUS_DET',g);R('R2','4.7k','CC_3V3','CC_DEFAULT_N',g)
add('Q4','AO3400A','AO3400A','AO3400A',{1:'CC_DEFAULT_N',2:'GND',3:'USB_HIGH_CURRENT'},g,note='Logic-level FET specified at 2.5V gate drive; clamps high-current request in default/unattached state.')
R('R3','10k','CC_3V3','USB_HIGH_CURRENT',g);C('C1','1u','VBUS','GND',g);C('C2','100n','CC_3V3','GND',g)
add('D1','D','SMAJ5.0A','SMAJ5.0A',{1:'VBUS',2:'GND'},g,'Diode_SMD:D_SMA','Unidirectional input TVS; pin 1 cathode.')
g='CELL CHARGER / POWER PATH'
add('U1','BQ24074RGT','BQ24074RGTR','BQ24074RGTR',{1:'NTC',2:'VBAT',3:'VBAT',4:'GND',5:'USB_HIGH_CURRENT',6:'GND',7:'PGOOD_N',8:'GND',9:'CHARGE_N',10:'SYS_RAW',11:'SYS_RAW',12:'CHG_ILIM',13:'USB_CHG',14:None,15:None,16:'CHG_ISET',17:'GND'},g,note='Up to ~300mA charging on capable USB-C. Legacy input is ~50mA nominal, so charging is slow with toy off. Default timer/termination; EP solder required.')
R('R4','3k','CHG_ISET','GND',g);R('R5','1.3k','CHG_ILIM','GND',g)
C('C3','4.7u','USB_CHG','GND',g);C('C4','10u','VBAT','GND',g);C('C5','22u','SYS_RAW','GND',g)
add('J4','Temperature','BATTERY NTC','B2B-PH-K-S(LF)(SN)',{1:'NTC',2:'GND'},g,'Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical','10k NTC thermally bonded to cell. No fitted NO_NTC bypass.')
for ref,net,value,mpn in [('LED1','PGOOD_N','POWER GOOD','APT3216LZGCK'),('LED2','CHARGE_N','CHARGING','APT3216SURCK')]:
    add(ref,'LED',value,mpn,{1:ref+'_K',2:'VBUS'},g,'LED_SMD:LED_1206_3216Metric')
    R('R6' if ref=='LED1' else 'R7','4.7k',ref+'_K',net,g)
g='CELL PROTECTION / FUSE'
add('J2','Battery','1S CELL / VH','B2P-VH(LF)(SN)',{1:'CELL_PLUS',2:'BAT_NEG'},g,'Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical','Higher-current polarity-controlled cell harness. Requires a cell rated at least 4A continuous; not interchangeable with old PH or main-board XH harnesses.')
add('F1','Fuse','4A FAST','0451004.MRL',{1:'CELL_PLUS',2:'VBAT'},g,'Fuse:Fuse_1206_3216Metric','Secondary fault fuse; not a substitute for cell protection. Cell and fuse I-squared-t coordination still required.')
add('U2','DW01A','DW01A / H&M','DW01A',{1:'OD',2:'PROTECT_CS',3:'OC',4:None,5:'PROTECT_VCC',6:'BAT_NEG'},g,note='H&M Semiconductor DW01A per linked manufacturer sheet. No generic substitutions. Parallel-FET trip thresholds, cell limits and fuse coordination remain release holds.')
for i in [1,2,3]:add('Q'+str(i),'FS8205','FS8205','FS8205',{1:'BAT_NEG',2:'DRAIN_COMMON',3:'GND',4:'OC',5:'DRAIN_COMMON',6:'OD'},g,'KK_Power:FS8205','Three parallel matched dual-MOSFET banks. Must qualify current sharing and trip thresholds.')
R('R8','470','VBAT','PROTECT_VCC',g);R('R9','1k','GND','PROTECT_CS',g);C('C6','100n','PROTECT_VCC','BAT_NEG',g)
g='SYSTEM SWITCH / INRUSH / UVLO'
add('SW1','SW_SPDT','OFF / ON','JS102011SAQN',{1:'GND',2:'RUN_CTL',3:'SYS_RAW'},g,'Button_Switch_SMD:SW_SPDT_CK_JS102011SAQN','Signal-level switch only; charging remains on when toy off.')
add('U4','TPS259530','TPS259530DSGR','TPS259530DSGR',{1:'EF_SLEW',2:'EF_UVLO',3:'SYS_RAW',4:'SYS_RAW',5:'SYS_SW',6:'EF_FAULT_N',7:'EF_ILIM',8:'GND',9:'GND'},g,'Package_SON:Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm','Latch-off on thermal fault; cycle switch to recover.')
R('R10','182k','RUN_CTL','EF_UVLO',g,True);R('R11','100k','EF_UVLO','GND',g,True);R('R12','620','EF_ILIM','GND',g)
C('C7','10n','EF_SLEW','GND',g);C('C8','22u','SYS_SW','GND',g);C('C9','100n','SYS_RAW','GND',g)
R('R13','100k','SYS_RAW','EF_FAULT_N',g);R('R14','10k','RUN_CTL','REG_ENABLE',g)
for index,(rail,top,bottom,regout) in enumerate([('MCU_5V','909k','101k','REG_5V'),('LOGIC_3V3','560k','100k','REG_3V3'),('ACT_3V2','540k','100k','REG_3V2')]):
    g=['5 V BUCK-BOOST','3.3 V BUCK-BOOST','3.2 V BUCK-BOOST'][index]; u='U'+str(5+index); k=20+index*10
    add(u,'TPS63060','TPS63060DSCR','TPS63060DSCR',{1:u+'_L1',2:'SYS_SW',3:'REG_ENABLE',4:'REG_ENABLE',5:'PG_ALL',6:u+'_AUX',7:'GND',8:u+'_FB',9:regout,10:u+'_L2',11:'GND'},g,note='Forced PWM for controlled rail accuracy/ripple. PG shared open-drain.')
    add('L'+str(index+1),'L','1uH','XFL4020-102MEC',{1:u+'_L1',2:u+'_L2'},g,'Inductor_SMD:L_Coilcraft_XxL4020','TI-recommended family; 5.1A Isat at 20% loss, manufacturer limits apply.')
    C('C'+str(k),'10u','SYS_SW','GND',g);C('C'+str(k+1),'10u','SYS_SW','GND',g)
    for j in range(3):C('C'+str(k+2+j),'22u',regout,'GND',g)
    C('C'+str(k+5),'100n',u+'_AUX','GND',g);C('C'+str(k+6),'100n','SYS_SW','GND',g);C('C'+str(k+7),'100n',regout,'GND',g)
    if index==2:
        R('R'+str(k),'270k',regout,u+'_FB_MID',g,True);R('R'+str(k+3),'270k',u+'_FB_MID',u+'_FB',g,True)
    else:R('R'+str(k),top,regout,u+'_FB',g,True)
    R('R'+str(k+1),bottom,u+'_FB','GND',g,True);C('C'+str(k+8),'10p',regout,u+'_FB',g)
g='ALL-RAIL READY / SOFT OUTPUTS'
add('U11','SN74AUP1G17','SN74AUP1G17DBVR','SN74AUP1G17DBVR',{1:None,2:'VOLTAGES_OK',3:'GND',4:'RAILS_EN',5:'REG_3V3'},g,'Package_TO_SOT_SMD:SOT-23-5','Buffers the independent voltage-supervisor outputs; not converter current-limit PG.')
R('R50','470k','REG_3V3','PG_ALL',g);C('C51','100n','REG_3V3','GND',g);R('R51','100k','RAILS_EN','GND',g)
for i,(raw,rail) in enumerate([('REG_5V','MCU_5V'),('REG_3V3','LOGIC_3V3'),('REG_3V2','ACT_3V2')]):
    u='U'+str(8+i);ct=u+'_CT'
    add(u,'TPS22918','TPS22918DBVR','TPS22918DBVR',{1:raw,2:'GND',3:'RAILS_EN',4:ct,5:u+'_QOD',6:rail},g,'Package_TO_SOT_SMD:SOT-23-6','Resistor-limited output discharge. Qualify ramp/fall timing with actual C.5 load capacitance.')
    R('R'+str(52+i),'100',rail,u+'_QOD',g)
    C('C'+str(52+i),'10n',ct,'GND',g)
g='VOLTAGE SUPERVISION / STARTUP'
add('U12','TPS386000','TPS386000RGPR','TPS386000RGPR',{1:'RUN_CTL',2:None,3:None,4:None,5:None,6:'GND',7:'SYS_SW',8:'SENSE_3V2',9:'SENSE_3V3',10:'SENSE_5V',11:'GND',12:'GND',13:None,14:'SYS_RAW',15:'VOLTAGES_OK',16:'VOLTAGES_OK',17:'VOLTAGES_OK',18:None,19:None,20:'GND',21:'GND'},g,'Package_DFN_QFN:Texas_RGP0020D_VQFN-20-1EP_4x4mm_P0.5mm_EP2.7x2.7mm','Powered before the eFuse so MR does not exceed its recommended VDD limit during normal switching. CT floating: default delay. MR switches off output gates. Unused channel 4/watchdog do not drive enables.')
R('R60','10k','REG_3V3','VOLTAGES_OK',g)
for i,(raw,sense,top) in enumerate([('REG_5V','SENSE_5V','1060k'),('REG_3V3','SENSE_3V3','665k'),('REG_3V2','SENSE_3V2','649k')]):
    R('R'+str(61+2*i),top,raw,sense,g,True);R('R'+str(62+2*i),'100k',sense,'GND',g,True)
C('C60','100n','SYS_RAW','GND',g)
g='USB-A / USB-C INPUT CURRENT'
add('U13','TPS22950','TPS22950YBHR','TPS22950YBHR',{'A1':'VBUS','A2':'USB_LIMIT_FAULT_N','B1':'VBUS','B2':'USB_CHG','C1':'GND','C2':'USB_PORT_ILIM'},g,'KK_Power:TPS22950_YBH','Use base TPS22950, not C/L variants: only base supports 50mA setting. Factory-assembled 0.4mm-pitch six-ball WCSP.')
R('R70','19.2k','USB_PORT_ILIM','GND',g,True)
R('R71','1.24k','USB_PORT_ILIM','USB_PORT_ILIM_FAST',g,True)
add('Q5','AO3400A','AO3400A','AO3400A',{1:'USB_HIGH_CURRENT',2:'GND',3:'USB_PORT_ILIM_FAST'},g,note='Logic-level FET specified at 2.5V gate drive; enables the extra ILIM resistor only in advertised higher-current mode.')
R('R72','100k','USB_HIGH_CURRENT','GND',g);R('R73','100k','VBUS','USB_LIMIT_FAULT_N',g)
C('C70','100n','VBUS','GND',g);C('C71','1u','USB_CHG','GND',g)
g='MAIN BOARD HARNESS / DEBUG'
add('J3','Output','C.5 SYS_IN / XH','B4B-XH-A(LF)(SN)',{1:'MCU_5V',2:'GND',3:'LOGIC_3V3',4:'ACT_3V2'},g,'Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical','Straight pin-number-to-pin-number four-wire harness; do not trust wire colors.')
add('J5','Status','SERVICE / NOT MCU SAFE','TSW-105-07-G-S',{1:'PGOOD_N',2:'CHARGE_N',3:'EF_FAULT_N',4:'GND',5:'VBAT'},g,'Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical','Status nets can reach USB/battery voltage. Not a direct ESP32 interface.')
for i,net in enumerate(['VBUS','VBAT','BAT_NEG','GND','SYS_RAW','SYS_SW','RUN_CTL','EF_UVLO','EF_ILIM','EF_FAULT_N','PG_ALL','RAILS_EN','REG_5V','REG_3V3','REG_3V2','MCU_5V','LOGIC_3V3','ACT_3V2','NTC','CC_DEFAULT_N','USB_HIGH_CURRENT','USB_CHG','USB_PORT_ILIM','USB_LIMIT_FAULT_N','CC_3V3'],1):
    add('TP'+str(i),'TestPoint',net,'BARE PCB PAD',{1:net},g,'TestPoint:TestPoint_Pad_D1.5mm','Bare pad, not a purchased component.')
# Freeze project-local copies, avoiding dependence on global library tables.
for p in PARTS:
    p['source_footprint']=p['footprint']
    p['footprint']='KK_Power:'+p['footprint'].split(':')[1]
# Deterministic, grouped A1 schematic. ICs use functional pin order; passives
# retain conventional resistor/capacitor/diode symbols and visible wire stubs.
items=[]; rootid=uid('sheet'); used={p['symbol'] for p in PARTS}; instances=[]
def text(s,x,y,size=1.27):items.append(f'(text {q(s)}(at {x} {y} 0)(effects(font(size {size} {size}))(justify left top))(uuid "{uid(s+str(x)+str(y))}"))')
def line(a,b):items.append(f'(polyline(pts(xy {a[0]} {a[1]})(xy {b[0]} {b[1]}))(stroke(width 0.25)(type default))(uuid "{uid(str(a)+str(b))}"))')
def sympins(name):
    return [(val(child(p,'number')[1]),*[float(z) for z in child(p,'at')[1:]]) for u in kids(defs[name],'symbol') for p in kids(u,'pin')]
def place(p,x,y):
    x=round(x/1.27)*1.27;y=round(y/1.27)*1.27
    name=p['symbol']; ps=sympins(name); angle=0; p.update(sch_x=x,sch_y=y)
    compact=name in ['R','C','L','D','D_Schottky','Fuse','LED']; tx=x+3 if compact else x; ty=y-3 if compact else y-max((z[2] for z in ps),default=0)-5
    props=''
    for key,value,yy,hidden in [('Reference',p['ref'],ty,False),('Value',p['value'],ty+1.8,False),('Footprint',p['footprint'],y,True),('Datasheet',p.get('datasheet',''),y,True),('MPN',p['mpn'],y,True),('Notes',p['note'],y,True)]:
        props+=f'(property {q(key)} {q(value)}(at {tx} {yy} 0)(effects(font(size 1.15 1.15))'+('(hide yes)' if hidden else '')+'))'
    pinstr=''.join(f'(pin {q(n)}(uuid "{uid(p["ref"]+n)}"))' for n,*_ in ps)
    bom='no' if p['ref'].startswith(('TP','#')) else 'yes'
    items.append(f'(symbol(lib_id "KK_Power:{name}")(at {x} {y} 0)(unit 1)(in_bom {bom})(on_board yes)(dnp no)(uuid "{p["uuid"]}"){props}{pinstr}(instances(project "KK_power_module"(path "/{rootid}"(reference "{p["ref"]}")(unit 1)))))')
    for n,dx,dy,a in ps:
        px=round(x+dx,5);py=round(y-dy,5);net=p['nets'][n]
        if net is None:items.append(f'(no_connect(at {px} {py})(uuid "{uid(p["ref"]+n+"NC")}"))');continue
        import math
        ex=round(px-5.08*math.cos(math.radians(a)),5);ey=round(py+5.08*math.sin(math.radians(a)),5)
        items.append(f'(wire(pts(xy {px} {py})(xy {ex} {ey}))(stroke(width 0)(type default))(uuid "{uid(p["ref"]+n+"wire")}"))')
        items.append(f'(label {q(net)}(at {ex} {ey} {int(a)%180})(effects(font(size 1 1))(justify '+('right' if a==0 else 'left')+f' bottom))(uuid "{uid(p["ref"]+n+"label")}"))')
for gi,(g,parts) in enumerate(GROUPS.items()):
    x=10+(gi%4)*204;y=20+(gi//4)*180
    for a,b in [((x,y),(x+198,y)),((x+198,y),(x+198,y+170)),((x+198,y+170),(x,y+170)),((x,y+170),(x,y))]:line(a,b)
    text(g,x+4,y+3,1.8)
    major=[p for p in parts if p['ref'].startswith(('U','J')) and not p['ref'].startswith('TP')]
    minor=[p for p in parts if p not in major]
    for i,p in enumerate(major):place(p,x+44+(i%2)*100,y+36+(i//2)*55)
    start=80 if len(major)<=2 else 120
    if g=='CELL PROTECTION / FUSE':
        fets=[p for p in minor if p['symbol']=='FS8205']
        for i,p in enumerate(fets):place(p,x+45+i*62,y+92)
        minor=[p for p in minor if p not in fets];start=135
    row_step=18 if g=='MAIN BOARD HARNESS / DEBUG' else 21
    for i,p in enumerate(minor):place(p,x+22+(i%5)*36,y+start+(i//5)*row_step)
text('KEYCHAIN KREATURES / POWER P.1 - ENGINEERING, NOT RELEASED',14,14,3)
# Electrical-source markers, limited to actual externally powered / regulated nets.
stock('power','PWR_FLAG'); used.add('PWR_FLAG')
for i,net in enumerate(['GND','BAT_NEG','VBUS','PROTECT_VCC']):
    p=dict(ref='#FLG'+str(i+1).zfill(3),symbol='PWR_FLAG',value='PWR_FLAG',mpn='',nets={'1':net},footprint='',note='',uuid=uid('flag'+net));place(p,22+i*60,569)
cached=[]
for n in sorted(used):
    d=copy.deepcopy(defs[n]);d[1]=q('KK_Power:'+n);cached.append(dump(d))
s=f'(kicad_sch(version 20250114)(generator "eeschema")(uuid "{rootid}")(paper "A1")(title_block(title "Charging-only, regulated three-rail power module")(date "2026-09-11")(rev "P.1 ENGINEERING")(comment 1 "NOT FOR FABRICATION: review and prototype qualification required"))(lib_symbols '+''.join(cached)+')'+''.join(items)+'(sheet_instances(path "/"(page "1"))))'
(OUT/'KK_power_module.kicad_sch').write_text(s+'\n')
(OUT/'KK_Power.kicad_sym').write_text('(kicad_symbol_lib(version 20250114)(generator "kicad_symbol_editor")'+''.join(dump(defs[n]) for n in sorted(used))+')\n')
(OUT/'sym-lib-table').write_text('(sym_lib_table\n  (version 7)\n  (lib (name "KK_Power") (type "KiCad") (uri "${KIPRJMOD}/KK_Power.kicad_sym") (options "") (descr "P.1 power symbols"))\n)\n')
(OUT/'design.json').write_text(json.dumps({'revision':'P.1 ENGINEERING','sheet_uuid':rootid,'components':PARTS,'groups':list(GROUPS)},indent=2)+'\n')
with (OUT/'BOM_DRAFT.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['Reference','Value','Candidate MPN - purchasing audit pending','Footprint','Group','Datasheet','Notes'])
    for p in PARTS:
        if not p['ref'].startswith('TP'):writer.writerow([p[k] for k in ['ref','value','mpn','footprint','group','datasheet','note']])
pro=json.loads((ROOT/'backups/pre_P1/KK_power_module.kicad_pro').read_text())
pro['meta']['filename']='KK_power_module.kicad_pro';pro['erc']['erc_exclusions']=[]
pro['net_settings']['classes']=[dict(name='Default',clearance=.2,track_width=.25,via_diameter=.6,via_drill=.3,microvia_diameter=.3,microvia_drill=.1,diff_pair_width=.2,diff_pair_gap=.25,diff_pair_via_gap=.25,wire_width=6,bus_width=12,line_style=0,pcb_color='',schematic_color='')]
pro['net_settings']['netclass_patterns']=[]
base=pro['net_settings']['classes'][0]
for name,width,names in [('SOURCE_POWER',1.5,['VBUS','CELL_PLUS','VBAT','BAT_NEG','DRAIN_COMMON','SYS_RAW','SYS_SW']),('USB_CHARGE',.6,['USB_CHG']),('RAIL_0A6',.6,['REG_5V','REG_3V3','REG_3V2','MCU_5V','LOGIC_3V3','ACT_3V2']),('SWITCH_NODE',.5,['U5_L1','U5_L2','U6_L1','U6_L2','U7_L1','U7_L2'])]:
    cls=copy.deepcopy(base);cls.update(name=name,track_width=width);pro['net_settings']['classes'].append(cls)
    pro['net_settings']['netclass_patterns'].extend({'netclass':name,'pattern':'/'+n} for n in names)
# Keep physical/parity checks enabled for the new project, not inherited suppressions.
for key in ['extra_footprint','footprint_type_mismatch','missing_courtyard']:
    pro['board']['design_settings']['rule_severities'][key]='error'
pro['board']['design_settings']['rules']['min_text_height']=.8
pro['board']['design_settings']['rules']['min_silk_clearance']=.1
(OUT/'KK_power_module.kicad_pro').write_text(json.dumps(pro,indent=2)+'\n')
print('Generated',len(PARTS),'parts in',len(GROUPS),'groups; schematic and manifest only, not fabrication-ready.')
