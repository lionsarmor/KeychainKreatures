// Revision C engineering capture. Run explicitly; do not overwrite GUI edits blindly.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url));
const uuid=s=>{const h=createHash('sha256').update(s).digest('hex');return `${h.slice(0,8)}-${h.slice(8,12)}-4${h.slice(13,16)}-a${h.slice(17,20)}-${h.slice(20,32)}`;};
const root=uuid('KK-main-revC-root'), project='KK_main_module';
const q=JSON.stringify, n=x=>Number(x.toFixed(4));
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){let a=[];if(t[i++]!=='(')throw Error('parse');while(t[i]!==')'){a.push(t[i]==='('?p():t[i++]);}i++;return a;}return p();}
const dump=a=>Array.isArray(a)?`(${a.map(dump).join(' ')})`:a;
const val=s=>s?.startsWith('"')?JSON.parse(s):s;
const child=(a,k)=>a.find(x=>Array.isArray(x)&&x[0]===k);
function all(a,k){return a.filter(x=>Array.isArray(x)&&x[0]===k);}
const libPath=execFileSync('flatpak',['info','--show-location','org.kicad.KiCad.Library.Symbols'],{encoding:'utf8'}).trim()+'/files/symbols/Device.kicad_sym';
const device=parse(fs.readFileSync(libPath,'utf8'));
const definitions=new Map();
function standard(name){if(definitions.has(name))return name;const a=structuredClone(all(device,'symbol').find(x=>val(x[1])===name));if(!a)throw Error(name);a[1]=q('KK_Draft:'+name);definitions.set(name,a);return name;}
const effects=(size=1)=>`(effects(font(size ${size} ${size})))`;
function box(name,pins,width=30){width=n(Math.round(width/2.54)*2.54);const h=Math.ceil(pins.length/2)*5.08+5.08;
 let s=`(symbol ${q('KK_Draft:'+name)} (pin_names(offset 0.8)) (in_bom yes)(on_board yes)
 (property "Reference" "U" (at 0 ${h/2+4} 0) ${effects()}) (property "Value" ${q(name)} (at 0 ${h/2+2} 0) ${effects()})
 (symbol ${q(name+'_0_1')} (rectangle(start ${-width/2} ${h/2})(end ${width/2} ${-h/2})(stroke(width 0.254)(type default))(fill(type background))))
 (symbol ${q(name+'_1_1')}`;
 pins.forEach(([number,label,type='passive'],i)=>{const right=i>=Math.ceil(pins.length/2),j=right?i-Math.ceil(pins.length/2):i;const x=(width/2+5.08)*(right?1:-1),y=h/2-5.08-j*5.08;
 s+=`(pin ${type} line(at ${x} ${y} ${right?180:0})(length 5.08)(name ${q(label)} ${effects()})(number ${q(String(number))} ${effects()}))`;});
 definitions.set(name,parse(s+'))'));return name;
}
// Transistor graphics use generic KiCad pin identifiers B/C/E or G/D/S;
// remap to the exact package's numeric pinout, never infer TO-92 order.
function transistor(name,base,mapping){standard(base);const a=structuredClone(definitions.get(base));a[1]=q('KK_Draft:'+name);for(const unit of all(a,'symbol')){unit[1]=q(val(unit[1]).replace(base,name));for(const pin of all(unit,'pin')){const num=child(pin,'number');num[1]=q(String(mapping[val(num[1])]))}}
 definitions.set(name,a);return name;}
const sources=Object.fromEntries(JSON.parse(fs.readFileSync(path.join(dir,'../component_review/datasheet_sources.json'),'utf8')));
sources['tn0702.pdf']='https://ww1.microchip.com/downloads/en/DeviceDoc/TN0702-N-Channel-Enhancement-Mode-Vertical-DMOS-FET-Data-Sheet-20005941A.pdf';
sources['jst-xh.pdf']='https://www.jst-mfg.com/product/pdf/eng/eXH.pdf';
const pages=[],components=[];
function page(file,title,notes){const p={file,title,notes,id:uuid(file),items:[],used:new Set()};pages.push(p);return p;}
function text(p,s,x,y,size=1.27){p.items.push(`(text ${q(s)} (at ${x} ${y} 0) (effects(font(size ${size} ${size}))(justify left top)) (uuid ${q(uuid(p.file+s+x+y))}))`);}
function pinsOf(name){return all(definitions.get(name),'symbol').flatMap(u=>all(u,'pin')).map(p=>{const a=child(p,'at');return{number:val(child(p,'number')[1]),x:Number(a[1]),y:Number(a[2]),angle:Number(a[3]),type:p[1]};});}
function part(p,ref,name,value,mpn,x,y,nets,doc='',footprint='',note=''){
 x=n(Math.round(x/1.27)*1.27);y=n(Math.round(y/1.27)*1.27);
 if(components.some(c=>c.ref===ref))throw Error('duplicate '+ref);
 const pins=pinsOf(name);if(Object.keys(nets).length!==pins.length)throw Error('pin count '+ref);
 p.used.add(name);const id=uuid(ref),sheetPath=p===pages[0]?`/${root}`:`/${root}/${p.id}`;
 const ys=pins.map(k=>k.y);const top=y-Math.max(...ys)-10.16;
 let s=`(symbol(lib_id ${q('KK_Draft:'+name)})(at ${x} ${y} 0)(unit 1)(in_bom yes)(on_board yes)(dnp no)(uuid ${q(id)})
 (property "Reference" ${q(ref)}(at ${x+4} ${top} 0) ${effects()})
 (property "Value" ${q(value)}(at ${x+4} ${top+2.54} 0) ${effects()})
 (property "Footprint" ${q(footprint)}(at ${x} ${y} 0)(hide yes) ${effects()})
 (property "Datasheet" ${q(sources[doc]||doc)}(at ${x} ${y} 0)(hide yes) ${effects()})
 (property "MPN" ${q(mpn)}(at ${x} ${y} 0)(hide yes) ${effects()})
 (property "Review" ${q(note)}(at ${x} ${y} 0)(hide yes) ${effects()})`;
 for(const pin of pins){if(!Object.hasOwn(nets,pin.number))throw Error('unmapped '+ref+':'+pin.number);s+=`(pin ${q(pin.number)}(uuid ${q(uuid(ref+':'+pin.number))}))`;
 const px=n(x+pin.x),py=n(y-pin.y),net=nets[pin.number];
 if(net===null){p.items.push(`(no_connect(at ${px} ${py})(uuid ${q(uuid(ref+pin.number+'nc'))}))`);continue;}
 const angle=pin.angle*Math.PI/180, ex=n(px-5.08*Math.cos(angle)),ey=n(py+5.08*Math.sin(angle));
 p.items.push(`(wire(pts(xy ${px} ${py})(xy ${ex} ${ey}))(stroke(width 0)(type default))(uuid ${q(uuid(ref+pin.number+'wire'))}))`);
 // Global labels deliberately join the functional sheets. Small text keeps dense IC pinouts readable.
 const la=pin.angle===0?0:pin.angle===180?180:0;
 p.items.push(`(global_label ${q(net)}(shape input)(at ${ex} ${ey} ${la}) (effects(font(size 0.9 0.9))(justify ${la===180?'left':'right'})) (uuid ${q(uuid(ref+pin.number+'label'))})
 (property "Intersheetrefs" "${'${INTERSHEET_REFS}'}"(at ${ex} ${ey} ${la})(hide yes) ${effects()}))`);
 }
 s+=`(instances(project ${q(project)}(path ${q(sheetPath)}(reference ${q(ref)})(unit 1)))))`;p.items.push(s);
 components.push({ref,page:p.file,value,mpn,symbol:name,nets,datasheet:sources[doc]||doc,footprint,note});
}
const R=standard('R'),C=standard('C'),CP=standard('C_Polarized'),LED=standard('LED'),D=standard('D_Schottky');
const NPN=transistor('KSP2222ABU','Q_NPN',{E:1,B:2,C:3});
const PNP=transistor('BC32725BU','Q_PNP',{C:1,B:2,E:3});
const FET=transistor('TN0702N3_G','Q_NMOS',{S:1,G:2,D:3});
const conn=(count)=>box('Header'+count,Array.from({length:count},(_,i)=>[i+1,'P'+(i+1)]),15.24);
const H2=conn(2),H4=conn(4),H6=conn(6),H8=conn(8);
const SW=box('SoftSwitch3101', [['A','A / contact 1'],['B','B / contact 1'],['C','C / contact 2'],['D','D / contact 2']],30.48);
const MC=box('SuperMini_ASSUMED',[[1,'5V','power_in'],[2,'GND','power_in'],[3,'3V3 OUT','power_out'],[4,'GPIO1','input'],[5,'GPIO2','input'],[6,'GPIO3 STRAP','bidirectional'],[7,'GPIO4','bidirectional'],[8,'GPIO5','output'],[9,'GPIO6','input'],[10,'GPIO7','output'],[11,'GPIO8','output'],[12,'GPIO9','output'],[13,'GPIO10','output'],[14,'GPIO11','output'],[15,'GPIO12','input'],[16,'GPIO13','output'],[17,'TX GPIO43','output'],[18,'RX GPIO44','output']],40.64);
const MCP=box('MCP23017_E_SP',Array.from({length:28},(_,i)=>{const num=i+1,labels={9:'VDD',10:'VSS',11:'NC',12:'SCL',13:'SDA',14:'NC',15:'A0',16:'A1',17:'A2',18:'RESET_N',19:'INTB',20:'INTA'};const label=labels[num]||(num<=8?'GPB'+i:'GPA'+(num-21));const type=[9,10].includes(num)?'power_in':[11,14].includes(num)?'no_connect':[12,15,16,17,18].includes(num)?'input':[19,20].includes(num)?'open_collector':[8,28].includes(num)?'output':'bidirectional';return[num,label,type]}),40.64);
const IR=box('TSOP38238',[[1,'OUT','output'],[2,'GND','power_in'],[3,'VS','power_in']],20.32);
const AMP=box('TDA2822_DIP8',[[1,'OUT1','output'],[2,'VCC','power_in'],[3,'OUT2','output'],[4,'GND','power_in'],[5,'NP2','input'],[6,'IN2','input'],[7,'IN1','input'],[8,'NP1','input']],30.48);
let ri=0,ci=0;
function resistor(p,v,a,b,x,y,note=''){const code={'4.7':'4R7','39':'39R','100':'100R','220':'220R','680':'680R','1k':'1K','4.7k':'4K7','10k':'10K','100k':'100K'}[v];if(!code)throw Error(v);part(p,'R'+(++ri),R,v,'MFR-25FBF52-'+code,x,y,{1:a,2:b},'mfr-resistors.pdf','Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',note);}
function cap(p,v,a,b,x,y,note=''){const specs={'100n':['C315C104K5R5TA','kemet-100nf.pdf'], '10n':['C315C103J1G5TA','kemet-10nf.pdf'], '1u':['C315C105K5R5TA','kemet-1uf.pdf'],'10u':['UVR1C100MDD','nichicon-uvr.pdf'],'100u':['UVR1C101MDD','nichicon-uvr.pdf']};const [mpn,doc]=specs[v];part(p,'C'+(++ci),['10u','100u'].includes(v)?CP:C,v,mpn,x,y,{1:a,2:b},doc,'',note);}
function passives(p,list,x=45,y=160,cols=4,dx=90,dy=32){list.forEach(([type,v,a,b,note],i)=>(type==='R'?resistor:cap)(p,v,a,b,x+(i%cols)*dx,y+Math.floor(i/cols)*dy,note||''));}
const core=page('KK_main_module','01 / MCU and external power interface',[
 'REV C ENGINEERING DRAFT - NOT FOR FABRICATION. No battery, charging or added regulators here.',
 'J1 is a NEW power-module contract: 1=5V_MCU, 2=GND, 3=3V3_PERIPH, 4=3V2_ACT. Old SYS_OUT is NOT compatible.',
 'MOD1 uses ASSUMED header mapping from seller photos/reference. Symbol numbers are carrier IDs, NOT released pad numbers.',
 'Leave module 3V3 output, battery pads and GPIO3 unused. Do not parallel its regulator with 3V3_PERIPH.',
 'USB recovery: remove the socketed MCU and program it separately until dual-source/backfeed tests pass.'
]);
part(core,'MOD1',MC,'ESP32-S3 SuperMini','Teyleten B0D47HBFDY',85,95,{1:'MCU_5V',2:'GND',3:null,4:'BUTTON_INT_N',5:'BUTTON_FN_N',6:null,7:'I2C_SDA',8:'I2C_SCL',9:'IR_RX',10:'IR_TX',11:'AUDIO_PWM',12:'BL_PWM',13:'SD_CS',14:'SPI_MOSI',15:'SPI_MISO',16:'SPI_SCK',17:'TFT_DC',18:'TFT_CS'},'esp32-s3.pdf','','Carrier pad numbering/voltage path requires delivered-module qualification');
part(core,'J1',H4,'SYS_IN / JST-XH','B4B-XH-A(LF)(SN)',235,65,{1:'MCU_5V',2:'GND',3:'LOGIC_3V3',4:'ACT_3V2'},'jst-xh.pdf','','4-rail-interface pins include ground; future supply must sequence rails together');
passives(core,[['C','100u','MCU_5V','GND'],['C','100n','MCU_5V','GND'],['C','100u','LOGIC_3V3','GND'],['C','100n','LOGIC_3V3','GND'],['C','100u','ACT_3V2','GND'],['C','100n','ACT_3V2','GND']],45,190,4);
text(core,'Supply design targets at J1:\n5.0 V +/-5%, reserve 0.6 A for MCU\n3.3 V +/-3%, reserve 0.5 A for display / SD / logic\n3.2 V +/-1%, reserve 0.4 A for audio / motor\nThese are design budgets, not measured consumption.\nNo live mating; common ground; current-limited bring-up.',175,110);
const controls=page('controls','02 / Nine soft buttons and GPIO expander',[
 'A/B are the same physical contact; C/D are the other. Four terminals captured, not abstract switch contacts.',
 'MCP23017: address 0x20; initialize outputs low before direction writes; GPA7/GPB7 are output-only.',
 'Set IOCON MIRROR=1 / ODR=1; INTA reports both button banks. Debounce in firmware. RESET_N has local RC.',
 'GPB4=AMP_EN, GPB5=MOTOR_EN, GPB6=TFT_RST_N. Unused GPIO set outputs low. FN directly wakes ESP32.'
]);
const mcpN={1:'BTN_A_N',2:'BTN_B_N',3:'BTN_X_N',4:'BTN_Y_N',5:'AMP_EN',6:'MOTOR_EN',7:'TFT_RST_N',8:null,9:'LOGIC_3V3',10:'GND',11:null,12:'I2C_SCL',13:'I2C_SDA',14:null,15:'GND',16:'GND',17:'GND',18:'EXP_RESET_N',19:null,20:'BUTTON_INT_N',21:'BTN_UP_N',22:'BTN_DOWN_N',23:'BTN_LEFT_N',24:'BTN_RIGHT_N',25:null,26:null,27:null,28:null};
part(controls,'U1',MCP,'MCP23017-E/SP','MCP23017-E/SP',75,85,mcpN,'mcp23017.pdf','Package_DIP:DIP-28_W7.62mm');
const buttons=['UP','DOWN','LEFT','RIGHT','A','B','X','Y','FN'];
buttons.forEach((b,i)=>{const net=b==='FN'?'BUTTON_FN_N':`BTN_${b}_N`;part(controls,'SW'+(i+1),SW,b,'Adafruit 3101',190+(i%3)*76.2,55+Math.floor(i/3)*40.64,{A:net,B:net,C:'GND',D:'GND'},'https://cdn-shop.adafruit.com/product-files/3101/C4817-001+datasheet.png','','200 ohm maximum closed contact resistance; custom footprint pending');});
passives(controls,[['R','4.7k','LOGIC_3V3','I2C_SDA'],['R','4.7k','LOGIC_3V3','I2C_SCL'],['R','10k','LOGIC_3V3','BUTTON_INT_N'],['R','10k','LOGIC_3V3','EXP_RESET_N'],['C','100n','EXP_RESET_N','GND'],['C','100n','LOGIC_3V3','GND'],['C','10u','LOGIC_3V3','GND'],...buttons.map(b=>['R','10k','LOGIC_3V3',b==='FN'?'BUTTON_FN_N':`BTN_${b}_N`])],40,170,5,76.2,29.21);
const display=page('display_sd','03 / Display, microSD and backlight',[
 'J2 display ASSUMED photo order: GND,VCC,SCL,SDA,RES,DC,CS,BLK; verify delivered board before footprint.',
 'J3 SD photo order: 3V3,CS,MOSI,CLK,MISO,GND. Both modules use 3.3 V logic. No 5 V SD reader.',
 'Separate pulled-up chip selects. Initialize SD in SPI mode with display deselected; serialize all bus transactions.',
 'Backlight is powered through Q3, never directly from GPIO. BL_SUPPLY-to-BLK 100R limiter is a conservative bring-up value.',
 'Check BLK topology/current before changing limiter. SD internal DAT pull-ups must be checked; unused pads not exposed.'
]);
part(display,'J2',H8,'XIITIA TFT header','PPTC081LFBN-RC',60,70,{1:'GND',2:'LOGIC_3V3',3:'SPI_SCK',4:'SPI_MOSI',5:'TFT_RST_N',6:'TFT_DC',7:'TFT_CS',8:'BLK'},'sullins-female-headers.pdf','','Display module B0DFWL25RB is a separate assembly item');
part(display,'J3',H6,'GODIYMODULES SD','PPTC061LFBN-RC',165,65,{1:'LOGIC_3V3',2:'SD_CS',3:'SPI_MOSI',4:'SPI_SCK',5:'SPI_MISO',6:'GND'},'sullins-female-headers.pdf','','SD module B0F82XWT4F is a separate assembly item');
part(display,'Q2',NPN,'KSP2222ABU','KSP2222ABU',270,65,{1:'GND',2:'BL_BASE',3:'BL_SINK'},'ksp2222a.pdf');
part(display,'Q3',PNP,'BC32725BU','BC32725BU',355,65,{1:'BL_SUPPLY',2:'BL_PNP_BASE',3:'LOGIC_3V3'},'bc327.pdf');
passives(display,[['R','10k','LOGIC_3V3','TFT_CS'],['R','10k','LOGIC_3V3','SD_CS'],['R','10k','LOGIC_3V3','TFT_RST_N'],['R','10k','LOGIC_3V3','SPI_MOSI'],['R','10k','LOGIC_3V3','SPI_MISO'],['C','100n','LOGIC_3V3','GND'],['C','10u','LOGIC_3V3','GND'],['C','100n','LOGIC_3V3','GND'],['C','100u','LOGIC_3V3','GND'],['R','4.7k','BL_PWM','BL_BASE'],['R','100k','BL_BASE','GND'],['R','220','BL_PNP_BASE','BL_SINK'],['R','100k','LOGIC_3V3','BL_PNP_BASE'],['R','100','BL_SUPPLY','BLK','Bring-up current limit; bright-screen qualification required']],40,125,5,76.2,34.29);
const irMotor=page('ir_motor','04 / IR transmit / receive and vibration',[
 'IR is a 38 kHz demodulated remote-control channel; not a sub-GHz radio or arbitrary optical waveform receiver.',
 'IR LED starts at modest current. R_LED is 100 ohms; range must be measured before increasing current.',
 'Motor TN0702N3-G: pin1=S, pin2=G, pin3=D. TO-92 is not a universal transistor pinout.',
 'Motor 3.2 V supply comes from power PCB. Flyback diode cathode at ACT_3V2. Keep loop short.',
 'MOTOR_EN is on/off through MCP23017, not hardware PWM. Verify starting/dropout margins at hot/cold conditions.'
]);
part(irMotor,'D1',LED,'TSAL6200','TSAL6200',50,65,{1:'IR_LED_K',2:'IR_LED_A'},'tsal6200.pdf','LED_THT:LED_D5.0mm');
part(irMotor,'Q1',NPN,'KSP2222ABU','KSP2222ABU',130,65,{1:'GND',2:'IR_BASE',3:'IR_LED_K'},'ksp2222a.pdf');
part(irMotor,'U2',IR,'TSOP38238','TSOP38238',235,65,{1:'IR_RX',2:'GND',3:'IR_RX_3V3'},'tsop382.pdf');
part(irMotor,'Q4',FET,'TN0702N3-G','TN0702N3-G',335,65,{1:'GND',2:'MOTOR_GATE',3:'MOTOR_RETURN'},'tn0702.pdf');
part(irMotor,'J4',H2,'LCM0827A3038F motor','S2B-PH-K-S(LF)(SN)',240,117,{1:'ACT_3V2',2:'MOTOR_RETURN'},'jst-ph.pdf');
part(irMotor,'D2',D,'1N5819','1N5819-E3/54',340,115,{1:'ACT_3V2',2:'MOTOR_RETURN'},'1n5819.pdf','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal');
passives(irMotor,[['R','100','LOGIC_3V3','IR_LED_A'],['R','1k','IR_TX','IR_BASE'],['R','100k','IR_BASE','GND'],['R','100','LOGIC_3V3','IR_RX_3V3'],['C','100n','IR_RX_3V3','GND'],['C','10u','IR_RX_3V3','GND'],['R','100','MOTOR_EN','MOTOR_GATE'],['R','100k','MOTOR_GATE','GND'],['C','100n','ACT_3V2','MOTOR_RETURN','Suppression physically close to motor leads'],['C','100u','ACT_3V2','GND']],40,175,5,76.2,38.1);
const audio=page('audio','05 / Filtered PWM, bridge amplifier and speaker',[
 'UTC TDA2822 DIP8 bridge application, datasheet page 4. Speaker is floating: neither output goes to GND.',
 'Two RC low-pass stages, AC coupling and input attenuation. Start with low digital volume / >=200 kHz PWM carrier.',
 'AMP_EN high powers amplifier via PNP switch; low/off at reset. Stop PWM before off; ramp volume after settling.',
 'FS1511P08-H3.0 wired 8-ohm speaker retained for prototype. Exact rating/acoustic qualification still outstanding.',
 'This is circuit capture and analytical review, NOT a full SPICE/firmware/acoustic simulation.'
]);
part(audio,'U3',AMP,'TDA2822L-D08-T','TDA2822L-D08-T',75,70,{1:'SPK_P',2:'AMP_VCC',3:'SPK_N',4:'GND',5:'AMP_NP2',6:'GND',7:'AMP_IN',8:'AMP_NP1'},'tda2822.pdf','Package_DIP:DIP-8_W7.62mm');
part(audio,'J5',H2,'8 ohm speaker','S2B-PH-K-S(LF)(SN)',175,65,{1:'SPK_P',2:'SPK_N'},'jst-ph.pdf');
part(audio,'Q5',NPN,'KSP2222ABU','KSP2222ABU',275,65,{1:'GND',2:'AMP_BASE',3:'AMP_SINK'},'ksp2222a.pdf');
part(audio,'Q6',PNP,'BC32725BU','BC32725BU',355,65,{1:'AMP_VCC',2:'AMP_PNP_BASE',3:'ACT_3V2'},'bc327.pdf');
passives(audio,[['R','1k','AUDIO_PWM','AUDIO_LP1'],['C','10n','AUDIO_LP1','GND'],['R','1k','AUDIO_LP1','AUDIO_LP2'],['C','10n','AUDIO_LP2','GND'],['C','1u','AUDIO_LP2','AUDIO_AC'],['R','100k','AUDIO_AC','AMP_IN'],['R','1k','AMP_IN','GND','Conservative fixed attenuation; prototype gain check'],['C','10u','AMP_NP1','AMP_NP2'],['C','10n','AMP_NP2','GND'],['C','100n','SPK_P','ZOBEL_P'],['R','4.7','ZOBEL_P','GND'],['C','100n','SPK_N','ZOBEL_N'],['R','4.7','ZOBEL_N','GND'],['C','100u','AMP_VCC','GND'],['C','100n','AMP_VCC','GND'],['R','4.7k','AMP_EN','AMP_BASE'],['R','100k','AMP_BASE','GND'],['R','100','AMP_PNP_BASE','AMP_SINK'],['R','100k','ACT_3V2','AMP_PNP_BASE']],40,125,5,76.2,34.29);
// Explicit source declarations for ERC only: J1 is an external powered interface, not rail generation.
const FLAG=box('ExternalPowerSource',[[1,'SUPPLIED','power_out']],10.16);
['MCU_5V','LOGIC_3V3','ACT_3V2','GND'].forEach((net,i)=>part(core,'#FLG0'+i,FLAG,'External source','',315,100+i*20.32,{1:net},'','','ERC declaration, not a fitted component'));
part(irMotor,'#FLG04',FLAG,'Via R27 filter','',75,117,{1:'IR_RX_3V3'},'','','Power derived from LOGIC_3V3 through receiver filter resistor; analytical drop checked');
part(audio,'#FLG05',FLAG,'Via Q6 switch','',80,265,{1:'AMP_VCC'},'','','Switched rail derived from ACT_3V2 via Q6; power flag does not assert always-on');
for(const p of pages){text(p,p.notes.join('\n'),12.7,12.7,1.05);
 let body=`(kicad_sch(version 20250114)(generator "eeschema")(generator_version "9.0")(uuid ${q(p===core?root:uuid(p.file+'file'))})(paper "A3")
 (title_block(title ${q(p.title)})(date "2026-09-10")(rev "C.0 DRAFT")(company "Keychain Kreatures")(comment 1 "Engineering prototype - no fabrication release"))
 (lib_symbols ${[...p.used].map(k=>dump(definitions.get(k))).join('\n')})\n${p.items.join('\n')}`;
 if(p===core){pages.slice(1).forEach((s,i)=>{const x=15+(i%2)*110.49,y=247.65+Math.floor(i/2)*20.32;body+=`(sheet(at ${x} ${y})(size 101.6 10.16)(stroke(width 0.1524)(type default))(fill(color 0 0 0 0))(uuid ${q(s.id)})
 (property "Sheetname" ${q(s.title)}(at ${x} ${y-1.27} 0)(effects(font(size 1 1))(justify left bottom)))
 (property "Sheetfile" ${q(s.file+'.kicad_sch')}(at ${x} ${y+11.43} 0)(effects(font(size 1 1))(justify left top)))
 (instances(project ${q(project)}(path ${q('/'+root)}(page ${q(String(i+2))})))))`;});body+='(sheet_instances(path "/"(page "1")))';}
 fs.writeFileSync(path.join(dir,p.file+'.kicad_sch'),body+')\n');
}
fs.writeFileSync(path.join(dir,'KK_Draft.kicad_sym'),`(kicad_symbol_lib(version 20250114)(generator "kicad_symbol_editor")\n${[...definitions.values()].map(a=>{const b=structuredClone(a);b[1]=q(val(b[1]).replace('KK_Draft:',''));return dump(b)}).join('\n')})\n`);
fs.writeFileSync(path.join(dir,'sym-lib-table'),'(sym_lib_table\n  (version 7)\n  (lib (name "KK_Draft") (type "KiCad") (uri "${KIPRJMOD}/KK_Draft.kicad_sym") (options "") (descr "Revision C self-contained engineering symbols"))\n)\n');
fs.writeFileSync(path.join(dir,'capture.json'),JSON.stringify({revision:'C.0 draft',pages:pages.map(p=>p.file),components},null,2)+'\n');
const csv=rows=>rows.map(r=>r.map(x=>q(String(x??''))).join(',')).join('\n')+'\n';
fs.writeFileSync(path.join(dir,'CAPTURE_BOM.csv'),csv([['Reference','Page','Value','MPN','Datasheet','Footprint','Review'],...components.filter(c=>!c.ref.startsWith('#')).map(c=>[c.ref,c.page,c.value,c.mpn,c.datasheet,c.footprint,c.note])]));
fs.writeFileSync(path.join(dir,'CAPTURE_CONNECTIONS.csv'),csv([['Reference','Pin','Net'],...components.flatMap(c=>Object.entries(c.nets).map(([pin,net])=>[c.ref,pin,net??'NC']))]));
console.log(`Captured ${components.filter(c=>!c.ref.startsWith('#')).length} fitted schematic symbols on ${pages.length} sheets. Engineering draft; fit and module qualification required.`);
