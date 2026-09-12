// Layout-only redraw. The prior capture is the electrical baseline, not a new BOM.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url)), out=path.dirname(here);
const q=JSON.stringify, mm=u=>Math.round(u*2540)/1000;
const uid=s=>{const h=createHash('sha256').update('one-sheet:'+s).digest('hex');return `${h.slice(0,8)}-${h.slice(8,12)}-4${h.slice(13,16)}-a${h.slice(17,20)}-${h.slice(20,32)}`;};
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')'){if(i>=t.length)throw Error('EOF');a.push(t[i]==='('?p():t[i++]);}i++;return a;}const a=p();if(i!==t.length)throw Error('trailing tokens');return a;}
const dump=a=>Array.isArray(a)?`(${a.map(dump).join(' ')})`:a;
const value=s=>s?.startsWith('"')?JSON.parse(s):s;
const ch=(a,k)=>a.find(x=>Array.isArray(x)&&x[0]===k), kids=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k);
const baseline=JSON.parse(fs.readFileSync(path.join(here,'capture.json'),'utf8'));
// C.2 electrical ECO: retain the C.0 capture as historical baseline.
for(const c of baseline.components){
 if(c.ref==='Q5')Object.assign(c,{symbol:'TN0702N3_G',value:'TN0702N3-G',mpn:'TN0702N3-G',datasheet:'https://ww1.microchip.com/downloads/en/DeviceDoc/TN0702-N-Channel-Enhancement-Mode-Vertical-DMOS-FET-Data-Sheet-20005941A.pdf',note:'C.2: NMOS gate driver, S-G-D pins 1-2-3.'});
 if(c.ref==='Q6')Object.assign(c,{symbol:'LP0701N3_G',value:'LP0701N3-G',mpn:'LP0701N3-G',datasheet:'https://ww1.microchip.com/downloads/en/DeviceDoc/LP0701-P-Channel-Enhancement-Mode-Lateral-MOSFET-Data-Sheet-20005447A.pdf',nets:{'1':'ACT_3V2','2':'AMP_PNP_BASE','3':'AMP_VCC'},note:'C.2: PMOS S-G-D pins 1-2-3. Do not fit former BC327 here.'});
 if(['R36','R38'].includes(c.ref))Object.assign(c,{value:'1k',mpn:'MFR-25FBF52-1K',note:'C.2 gate series resistor; no bipolar base current.'});
}
const modulePinMap=JSON.parse(fs.readFileSync(path.join(out,'pcb','SUPERMINI_PIN_MAP.json'),'utf8'));
const baselineModule=baseline.components.find(c=>c.ref==='MOD1');
baselineModule.nets=Object.fromEntries(Object.entries(baselineModule.nets).map(([pin,net])=>[modulePinMap[pin],net]));
// Preserve the package audit when regenerating the readable drawing.
const footprintFile=path.join(out,'pcb','footprint_assignments.json');
if(fs.existsSync(footprintFile)){
 const footprints=new Map(JSON.parse(fs.readFileSync(footprintFile,'utf8')).map(r=>[r.ref,r.footprint]));
 for(const c of baseline.components)if(footprints.has(c.ref))c.footprint=footprints.get(c.ref);
}
const parts=new Map(baseline.components.map(c=>[c.ref,c]));
// C.3: separate RGB mood lamp, socketed constant-current driver, top-entry
// actuator connectors. Do not consume ESP32 boot-strapping pins.
for(const ref of ['J4','J5'])Object.assign(parts.get(ref),{mpn:'B2B-PH-K-S(LF)(SN)',footprint:'KK_Main:JST_PH_B2B_2',note:'C.3 top-entry connector: mating plug inserts perpendicular to rear PCB.'});
Object.assign(parts.get('U1').nets,{'25':'RGB_DATA','26':'RGB_CLK','27':'RGB_LATCH','28':'RGB_OE_N'});
const rgbDS='https://www.kingbrightusa.com/images/catalog/SPEC/WP154A4SEJ3VBDZGW-CA.pdf';
const driverDS='https://www.ti.com/lit/ds/symlink/tlc5916.pdf';
parts.set('D3',{ref:'D3',symbol:'RGB_CA',value:'RGB mood / common anode',mpn:'WP154A4SEJ3VBDZGW/CA',footprint:'KK_Main:RGB_CA_5mm_LeadFormed',datasheet:rgbDS,note:'C.3: form 1.27 mm leads to 2.54 mm fixture spacing before soldering. 1=R, 2=A+, 3=B, 4=G.',nets:{'1':'RGB_RED_K','2':'MCU_5V','3':'RGB_BLUE_K','4':'RGB_GREEN_K'}});
parts.set('U4',{ref:'U4',symbol:'TLC5916_Functional',value:'TLC5916IN',mpn:'TLC5916IN',footprint:'KK_Main:ED16DT_DIP16_Socket',datasheet:driverDS,note:'C.3: 3.3 V logic, 5 V common-anode LED. OE high until zero data is latched.',nets:{'1':'GND','2':'RGB_DATA','3':'RGB_CLK','4':'RGB_LATCH','5':'RGB_RED_K','6':'RGB_GREEN_K','7':'RGB_BLUE_K','8':null,'9':null,'10':null,'11':null,'12':null,'13':'RGB_OE_N','14':null,'15':'RGB_R_EXT','16':'LOGIC_3V3'}});
for(const [ref,value,mpn,nets]of [['R40','1.8k','MFR-25FBF52-1K8',{'1':'RGB_R_EXT','2':'GND'}],['R41','10k','MFR-25FBF52-10K',{'1':'LOGIC_3V3','2':'RGB_OE_N'}]])parts.set(ref,{...parts.get('R1'),ref,value,mpn,nets,note:'C.3 RGB driver: '+(ref==='R40'?'Approx. 10.4mA/channel default; program low-current mode for dimming.':'Output blanking pull-up.')});
parts.set('C27',{...parts.get('C4'),ref:'C27',nets:{'1':'LOGIC_3V3','2':'GND'},note:'C.3 local U4 bypass.'});
for(const [ref,net]of [['R42','RGB_DATA'],['R43','RGB_CLK']])parts.set(ref,{...parts.get('R1'),ref,value:'100k',mpn:'MFR-25FBF52-100K',nets:{'1':net,'2':'GND'},note:'C.3 hold RGB CMOS input low while expander is reset/high impedance.'});
const lib=parse(fs.readFileSync(path.join(here,'KK_Draft.kicad_sym'),'utf8'));
const defs=new Map(kids(lib,'symbol').map(a=>[value(a[1]),structuredClone(a)]));
const symbolRoot=execFileSync('flatpak',['info','--show-location','org.kicad.KiCad.Library.Symbols'],{encoding:'utf8'}).trim()+'/files/symbols';
const device=parse(fs.readFileSync(path.join(symbolRoot,'Device.kicad_sym'),'utf8'));
const pm=structuredClone(kids(device,'symbol').find(a=>value(a[1])==='Q_PMOS'));
pm[1]=q('LP0701N3_G');
for(const u of kids(pm,'symbol')){
 u[1]=q(value(u[1]).replace('Q_PMOS','LP0701N3_G'));
 for(const p of kids(u,'pin'))ch(p,'number')[1]=q({S:'1',G:'2',D:'3'}[value(ch(p,'name')[1])]);
}
kids(pm,'property').find(p=>value(p[1])==='Value')[2]=q('LP0701N3-G');
defs.set('LP0701N3_G',pm);
const placed=new Map(), items=[], wires=[], labels=[], claimed=new Map();
const root=uid('root');
function txt(s,x,y,size=1.3){items.push(`(text ${q(s)}(at ${mm(x)} ${mm(y)} 0)(effects(font(size ${size} ${size}))(justify left top))(uuid ${q(uid('txt'+s+x+y))}))`);}
function lineGraphic(pts,width=0.254){items.push(`(polyline(pts ${pts.map(([x,y])=>`(xy ${mm(x)} ${mm(y)})`).join(' ')})(stroke(width ${width})(type default))(fill(type none))(uuid ${q(uid('graphic'+items.length))}))`);}
function group(title,x,y,w,h,note=''){lineGraphic([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],0.3);txt(title,x+2,y+2,3);if(note)txt(note,x+2,y+6,1.5);}
const eff=`(effects(font(size 1.3 1.3)))`;
// Functional pin order: logical identifiers preserved; footprint numbering is not released.
function box(name,pins,w,h){let s=`(symbol ${q(name)}(pin_names(offset 0.8))(in_bom yes)(on_board yes)
 (property "Reference" "U"(at 0 ${mm(h/2+2)} 0) ${eff})
 (property "Value" ${q(name)}(at 0 ${mm(h/2+1)} 0) ${eff})
 (symbol ${q(name+'_0_1')}(rectangle(start ${mm(-w/2)} ${mm(h/2)})(end ${mm(w/2)} ${mm(-h/2)})(stroke(width 0.254)(type default))(fill(type background))))
 (symbol ${q(name+'_1_1')}`;
 for(const [num,label,type,x,y,a] of pins)s+=`(pin ${type} line(at ${mm(x)} ${mm(-y)} ${a})(length 5.08)(name ${q(label)} ${eff})(number ${q(name==='SuperMini_Header'?modulePinMap[String(num)]:String(num))} ${eff}))`;
 defs.set(name,parse(s+'))'));return name;}
const MCU=box('SuperMini_Header',[
 [1,'5V','power_in',-13,-18,0],[2,'GND','power_in',-13,-14,0],[3,'3V3 OUT','power_out',-13,-10,0],[6,'GPIO3 / STRAP','bidirectional',-13,-6,0],
 ...[[4,'GPIO1 / BUTTON INT','input'],[5,'GPIO2 / FUNCTION','input'],[7,'GPIO4 / SDA','bidirectional'],[8,'GPIO5 / SCL','output'],[9,'GPIO6 / IR RX','input'],[10,'GPIO7 / IR TX','output'],[11,'GPIO8 / AUDIO','output'],[12,'GPIO9 / BACKLIGHT','output'],[13,'GPIO10 / SD CS','output'],[14,'GPIO11 / MOSI','output'],[15,'GPIO12 / MISO','input'],[16,'GPIO13 / SCK','output'],[17,'GPIO43 / TFT DC','output'],[18,'GPIO44 / TFT CS','output']].map(([n,l,t],i)=>[n,l,t,13,-19.5+i*3,180])
 ],22,44);
const EXP=box('MCP23017_Functional',[
 [9,'VDD','power_in',0,-29,270],[10,'VSS','power_in',0,29,90],
 [12,'SCL','input',-12,-22,0],[13,'SDA','bidirectional',-12,-17,0],[20,'INTA','open_collector',-12,-12,0],[18,'RESET_N','input',-12,-7,0],
 [5,'GPB4 / AMP EN','bidirectional',-12,0,0],[6,'GPB5 / MOTOR EN','bidirectional',-12,5,0],[7,'GPB6 / TFT RESET','bidirectional',-12,10,0],
 [15,'A0','input',-12,16,0],[16,'A1','input',-12,19,0],[17,'A2','input',-12,22,0],
 ...[[21,'GPA0 / UP'],[22,'GPA1 / DOWN'],[23,'GPA2 / LEFT'],[24,'GPA3 / RIGHT'],[1,'GPB0 / A'],[2,'GPB1 / B'],[3,'GPB2 / X'],[4,'GPB3 / Y']].map(([n,l],i)=>[n,l,'bidirectional',12,-24.5+i*7,180]),
 ...[[8,'GPB7'],[11,'NC'],[14,'NC'],[19,'INTB'],[25,'GPA4'],[26,'GPA5'],[27,'GPA6'],[28,'GPA7']].map(([n,l],i)=>[n,l,[11,14].includes(n)?'no_connect':[8,28].includes(n)?'output':n===19?'open_collector':'bidirectional',-9+i*2.5,29,90])
 ],20,54);
function header(name,pinNames){return box(name,pinNames.map(([n,label],i)=>[n,label,'passive',-4,(i-(pinNames.length-1)/2)*3,0]),4,pinNames.length*3+1);}
const HPOWER=header('Power_Header',[[1,'5V MCU'],[2,'GND'],[3,'3V3'],[4,'3V2']]);
const HTFT=header('TFT_Header',[[1,'GND'],[2,'VCC'],[3,'SCL'],[4,'SDA'],[5,'RES'],[6,'DC'],[7,'CS'],[8,'BLK']]);
const HSD=header('SD_Header',[[1,'3V3'],[2,'CS'],[3,'MOSI'],[4,'CLK'],[5,'MISO'],[6,'GND']]);
const HMOTOR=header('Motor_Header',[[1,'+'],[2,'-']]);
const HSPK=header('Speaker_Header',[[1,'+'],[2,'-']]);
const RX=box('IR_Receiver',[[1,'OUT','output',6,0,180],[2,'GND','power_in',0,6,90],[3,'VS','power_in',0,-6,270]],8,8);
const AMP=box('TDA2822_Bridge',[[7,'IN1','input',-9,-5,0],[6,'IN2','input',-9,7,0],[2,'VCC','power_in',0,-12,270],[4,'GND','power_in',0,12,90],[1,'OUT1','output',9,-5,180],[3,'OUT2','output',9,7,180],[8,'NP1','input',-5,12,90],[5,'NP2','input',5,12,90]],14,20);
const RGB=box('RGB_CA',[[2,'A+ COMMON','passive',0,-7,270],[1,'RED K','passive',-6,7,90],[4,'GREEN K','passive',0,7,90],[3,'BLUE K','passive',6,7,90]],16,10);
const RGBDRIVER=box('TLC5916_Functional',[[16,'VDD 3V3','power_in',0,-13,270],[1,'GND','power_in',0,13,90],[2,'SDI','input',-12,-8,0],[3,'CLK','input',-12,-3,0],[4,'LATCH','input',-12,2,0],[13,'OE_N','input',-12,7,0],[15,'R-EXT','passive',6,13,90],[5,'OUT0 RED','open_collector',12,-8,180],[6,'OUT1 GREEN','open_collector',12,-3,180],[7,'OUT2 BLUE','open_collector',12,2,180],...[8,9,10,11,12,14].map((n,i)=>[n,n===14?'SDO':'UNUSED','output',12,7+i*.5,180])],20,22);
// Four physical contacts, drawn as a switch (not an IC-shaped box).
const oldSW=defs.get('SoftSwitch3101');
const SW=box('SoftSwitch', [['A','', 'passive',-3,-1,0],['B','','passive',-3,1,0],['C','','passive',3,-1,180],['D','','passive',3,1,180]],2,4);
const sw=defs.get(SW);const g=kids(sw,'symbol')[0];g.splice(2);for(const points of [[[-1,-1],[-1,1]],[[1,-1],[1,1]],[[-1,0],[0.6,0.8]]])g.push(parse(`(polyline(pts ${points.map(([x,y])=>`(xy ${mm(x)} ${mm(y)})`).join(' ')})(stroke(width 0.254)(type default))(fill(type none)))`));
function pins(name){return kids(defs.get(name),'symbol').flatMap(u=>kids(u,'pin')).map(p=>{const a=ch(p,'at');return{num:value(ch(p,'number')[1]),x:Number(a[1])/2.54,y:-Number(a[2])/2.54,angle:Number(a[3])};});}
function place(ref,x,y,angle=0,override=null){if(placed.has(ref))throw Error('duplicate '+ref);const c=parts.get(ref);if(!c)throw Error(ref);const name=override||c.symbol;const a=angle*Math.PI/180;const ps=pins(name).map(p=>({...p,x:Number((x+p.x*Math.cos(a)+p.y*Math.sin(a)).toFixed(4)),y:Number((y-p.x*Math.sin(a)+p.y*Math.cos(a)).toFixed(4)),angle:(p.angle+angle)%360}));
 const id=uid(ref),obj={...c,name,x,y,angle,pins:ps};placed.set(ref,obj);
 const compact=['R','C','C_Polarized'].includes(name)||name.startsWith('KSP')||name.startsWith('BC327')||name.startsWith('TN0702')||name.startsWith('LP0701');
 const pnp=name==='BC32725BU'||name==='LP0701N3_G';
 const py=['R19','R36'].includes(ref)?y+2.5:pnp?y-4:compact?(angle%180===90?y-4:y-2):y-Math.max(...ps.map(p=>y-p.y))-(name==='SoftSwitch'?3.5:5.5),px=pnp?x-3:compact&&angle===0?x+2:x;
 const anchor=pnp?'right':compact&&angle===0?'left':'center';
 const prop=(key,v,xx,yy,hidden=false)=>`(property ${q(key)} ${q(v)}(at ${mm(xx)} ${mm(yy)} ${angle%180})${hidden||ref.startsWith('#')?'(hide yes)':''}(effects(font(size 1.5 1.5))${anchor!=='center'&&!hidden?`(justify ${anchor})`:''}))`;
 let s=`(symbol(lib_id ${q('KK_Main:'+name)})(at ${mm(x)} ${mm(y)} ${angle})(unit 1)(in_bom ${ref.startsWith('#')?'no':'yes'})(on_board ${ref.startsWith('#')?'no':'yes'})(dnp no)(uuid ${q(id)})`;
 s+=prop('Reference',ref,px,py)+prop('Value',c.value,px,py+1.4)+prop('Footprint',c.footprint,x,y,true)+prop('Datasheet',c.datasheet,x,y,true)+prop('MPN',c.mpn,x,y,true)+prop('Review',c.note,x,y,true);
 for(const p of ps){s+=`(pin ${q(p.num)}(uuid ${q(uid(ref+':'+p.num))}))`;if(c.nets[p.num]===null)items.push(`(no_connect(at ${mm(p.x)} ${mm(p.y)})(uuid ${q(uid('nc'+ref+p.num))}))`);}
 items.push(s+`(instances(project "KK_main_module"(path ${q('/'+root)}(reference ${q(ref)})(unit 1)))))`);return obj;}
const point=e=>{if(Array.isArray(e))return e;if(typeof e!=='string')throw Error('bad point');const [r,p]=e.split(':');const part=placed.get(r),pin=part?.pins.find(k=>k.num===p);if(!pin)throw Error('missing '+e);return[pin.x,pin.y];};
function wire(net,...points){const a=points.map(point);for(const s of points.filter(x=>typeof x==='string')){const[r,p]=s.split(':');if(parts.get(r).nets[p]!==net)throw Error(`wrong net ${s}: ${net}`);claimed.set(s,net);}for(let i=1;i<a.length;i++){const p=a[i-1],b=a[i];if(p[0]!==b[0]&&p[1]!==b[1])throw Error(`diagonal ${net} ${p}->${b}`);if(p[0]!==b[0]||p[1]!==b[1])wires.push({net,a:p,b});}}
function label(net,p,side='right'){p=point(p);labels.push({net,p});items.push(`(label ${q(net)}(at ${mm(p[0])} ${mm(p[1])} 0)(effects(font(size 1.5 1.5))(justify ${side} bottom))(uuid ${q(uid('lab'+net+p))}))`);}
function port(ref,pin,len=4,side=null){const part=placed.get(ref),p=part.pins.find(k=>k.num===String(pin));const net=part.nets[String(pin)];const rad=p.angle*Math.PI/180;const end=[Number((p.x-len*Math.cos(rad)).toFixed(4)),Number((p.y+len*Math.sin(rad)).toFixed(4))];wire(net,`${ref}:${pin}`,end);label(net,end,side||(p.angle===0?'right':'left'));return end;}
function supply(net,p,stem=2){const original=p;p=point(p);wire(net,original,[p[0],p[1]-stem]);label(net,[p[0],p[1]-stem],'left');}
function ground(p){const original=p;p=point(p);wire('GND',original,[p[0],p[1]+1]);label('GND',[p[0],p[1]+1],'left');lineGraphic([[p[0]-1,p[1]+1],[p[0]+1,p[1]+1]],0.25);lineGraphic([[p[0]-.65,p[1]+1.5],[p[0]+.65,p[1]+1.5]],0.25);lineGraphic([[p[0]-.3,p[1]+2],[p[0]+.3,p[1]+2]],0.25);}
function railCaps(refs,net,xs,yTop,yBottom){refs.forEach((ref,i)=>{place(ref,xs[i],(yTop+yBottom)/2);wire(net,[xs[i],yTop],ref+':1');wire('GND',ref+':2',[xs[i],yBottom]);});wire(net,[xs[0],yTop],[xs.at(-1),yTop]);wire('GND',[xs[0],yBottom],[xs.at(-1),yBottom]);supply(net,[xs[0],yTop]);ground([xs[0],yBottom]);}
txt('KEYCHAIN KREATURES  /  MAIN BOARD',6,6,4);
txt('ONE-SHEET CIRCUIT VIEW   |   C.3: RGB mood lamp + top-entry connectors   |   Engineering prototype',6,11,1.6);
group('POWER INPUT + LOCAL BYPASS',5,15,85,69,'Regulation / charging stay on the separate power board.');
place('J1',20,38,0,HPOWER);for(let i=1;i<=4;i++)port('J1',i,5);
railCaps(['C1','C2'],'MCU_5V',[45,57],31,47);
railCaps(['C3','C4'],'LOGIC_3V3',[17,29],59,75);
railCaps(['C5','C6'],'ACT_3V2',[55,67],59,75);
txt('J1: 5.0V / GND / 3.3V / 3.2V\nNOT raw battery. Old power output is not compatible.',36,50,1.15);
group('ESP32-S3 SUPERMINI / SOCKET',95,15,95,69,'Header signals shown by GPIO; pad names match supplied footprint.');
place('MOD1',137,51,0,MCU);for(const p of placed.get('MOD1').pins)if(parts.get('MOD1').nets[p.num]!==null)port('MOD1',p.num,p.x>137?8:4);
txt('USB service: remove socketed MCU first.\n3V3 OUT is intentionally not tied to the external 3V3 rail.',98,75,1.1);
group('SCREEN + microSD + BACKLIGHT',195,15,130,88,'Shared SPI clock / MOSI. Separate CS lines. Both modules use 3.3V logic.');
place('J2',310,40,0,HTFT);place('J3',310,78,0,HSD);
// Shared SPI trunks on the left; branches physically wired to each connector.
const sy={SPI_MOSI:39.5,SPI_SCK:36.5,SPI_MISO:82.5,TFT_CS:47.5,TFT_DC:44.5,TFT_RST_N:41.5,SD_CS:73.5};
const trunk={SPI_MOSI:219,SPI_SCK:212,SPI_MISO:226};
for(const [net,x]of Object.entries(trunk)){const ys=net==='SPI_MOSI'?[38.5,76.5]:net==='SPI_SCK'?[35.5,79.5]:[82.5];wire(net,[x,26],[x,Math.max(...ys)]);label(net,[x,26],'left');}
wire('SPI_SCK','J2:3',[212,35.5]);wire('SPI_MOSI','J2:4',[219,38.5]);wire('SPI_MOSI','J3:3',[219,76.5]);wire('SPI_SCK','J3:4',[212,79.5]);wire('SPI_MISO','J3:5',[226,82.5]);
for(const[ref,pin,x]of [['J2',5,286],['J2',6,277],['J2',7,263],['J3',2,269]]){const p=point(ref+':'+pin);wire(parts.get(ref).nets[pin],ref+':'+pin,[x,p[1]]);label(parts.get(ref).nets[pin],[x,p[1]],'right');}
wire('GND','J2:1',[300,29.5]);ground([300,29.5]);
wire('LOGIC_3V3','J2:2',[290,32.5],[290,25]);supply('LOGIC_3V3',[290,25]);
wire('LOGIC_3V3','J3:1',[292,70.5],[292,65]);supply('LOGIC_3V3',[292,65]);wire('GND','J3:6',[300,85.5],[300,89]);ground([300,89]);
// Pull-ups attach to the bus or the select/reset lines, not isolated labelled resistor stubs.
for(const [r,net,x,yend]of [['R17','SPI_MOSI',236,38.5],['R18','SPI_MISO',233,82.5],['R14','TFT_CS',266,47.5],['R16','TFT_RST_N',289,41.5],['R15','SD_CS',273,73.5]]){const yc=yend-5;place(r,x,yc);wire(net,r+':2',[x,yend]);supply('LOGIC_3V3',r+':1');if(net==='SPI_MISO')wire(net,[x,yend],[226,yend]);}
railCaps(['C10','C11'],'LOGIC_3V3',[245,253],27,40);
railCaps(['C12','C13'],'LOGIC_3V3',[242,252],78,91);
// Conventional high-side PNP / NPN driver, with pull-up and base resistors in circuit.
function highSide(prefix,refs,netIn,netOut,x,y){const [npn,pnp,rin,rdown,rseries,rup]=refs;
 place(pnp,x,y,180);place(npn,x+18,y+8);place(rin,x+9,y+8,90);place(rdown,x+14,y+14);place(rseries,x+11,y+1,90);place(rup,x+6,y-4);
 const source=prefix==='AMP'?'1':'3',drain=prefix==='AMP'?'3':'1';
 const e=point(pnp+':'+source),co=point(pnp+':'+drain),b=point(pnp+':2'),nb=point(npn+':2'),nc=point(npn+':3');
 wire(netIn,pnp+':'+source,[e[0],y-9],[x+6,y-9],rup+':1');supply(netIn,[e[0],y-9]);
 wire(prefix+'_PNP_BASE',pnp+':2',[x+6,y],rup+':2');wire(prefix+'_PNP_BASE',[x+6,y],[x+6,y+1],rseries+':1');
 wire(prefix+'_SINK',rseries+':2',[nc[0],y+1],npn+':3');
 wire(prefix+'_BASE',rin+':2',[x+14,y+8],npn+':2');wire(prefix+'_BASE',[x+14,y+8],rdown+':1');
 wire('GND',rdown+':2',[x+14,y+19],[x+19,y+19],npn+':1');ground([x+19,y+19]);
 port(rin,1,4);return {out:co,in:[e[0],y-9]};}
const bl=highSide('BL',['Q2','Q3','R19','R20','R21','R22'],'LOGIC_3V3','BL_SUPPLY',274,54);
place('R23',298,53,90);wire('BL_SUPPLY','Q3:1',[273,58],[294,58],[294,53],'R23:1');wire('BLK','R23:2',[303,53],[303,50.5],'J2:8');
txt('R23 = conservative bring-up current limit.\nConfirm BLK circuitry before raising brightness.',198,95,1.1);
group('BUTTONS + GPIO EXPANDER',5,89,185,84,'Each switch is wired to its pull-up and input. A/B are one contact; C/D are the other.');
place('U1',56,132,0,EXP);
for(const pin of [12,13,20,5,6,7])port('U1',pin,5);
for(const [pin,len]of [[25,2],[26,4],[27,6],[28,8]])port('U1',pin,len);
wire('LOGIC_3V3','U1:9',[56,101]);supply('LOGIC_3V3',[56,101]);
for(const pin of [15,16,17])wire('GND','U1:'+pin,[39,point('U1:'+pin)[1]]);wire('GND',[39,148],[39,157]);ground([39,157]);ground('U1:10');
// Reset RC and I2C/interrupt pull-ups sit beside the IC.
for(const [r,pin,x]of [['R2',12,25],['R1',13,29],['R3',20,33]]){const yp=point('U1:'+pin)[1];place(r,x,yp-4);wire(parts.get(r).nets[2],r+':2',[x,yp],[39,yp]);supply('LOGIC_3V3',r+':1');}
place('R4',19,117);place('C7',19,133);wire('EXP_RESET_N','R4:2',[19,125],'C7:1');wire('EXP_RESET_N',[19,125],'U1:18');supply('LOGIC_3V3','R4:1');ground('C7:2');
railCaps(['C8','C9'],'LOGIC_3V3',[15,25],145,157);
const btnpins=[21,22,23,24,1,2,3,4];
for(let i=0;i<8;i++){const y=107.5+i*7;place('SW'+(i+1),139,y,0,SW);place('R'+(i+5),111,y-3.5);const net=parts.get('SW'+(i+1)).nets.A;
 wire(net,'U1:'+btnpins[i],[105,y],[134,y],[134,y-1],'SW'+(i+1)+':A');
}
// Connections in a second loop keep the switch bank visually regular.
for(let i=0;i<8;i++){const y=107.5+i*7,sw='SW'+(i+1),r='R'+(i+5),net=parts.get(sw).nets.A;
 wire(net,[134,y],[134,y+1],sw+':B');wire(net,r+':2',[111,y]);supply('LOGIC_3V3',r+':1',1);
 wire('GND',sw+':C',[144,y-1],[144,y+1],sw+':D');ground([144,y+1]);}
// Function button bypasses expander and is kept adjacent to the other controls.
place('SW9',168,148,0,SW);place('R13',161,139);wire('BUTTON_FN_N','R13:2',[161,147],'SW9:A');wire('BUTTON_FN_N',[161,147],[161,149],'SW9:B');label('BUTTON_FN_N',[161,147],'right');supply('LOGIC_3V3','R13:1');wire('GND','SW9:C',[174,147],[174,149],'SW9:D');ground([174,149]);
txt('MCP address: 0x20\nGPB4: amplifier enable\nGPB5: motor enable\nGPB6: screen reset\nGPA7 / GPB7: not inputs',155,107,1.15);
group('IR TRANSMIT + RECEIVE',195,108,65,65,'38kHz remote-control IR, not sub-GHz RF.');
place('Q1',222,148);place('R25',213,148,90);place('R26',217,156);place('D1',223,135,90);place('R24',223,125);
port('R25',1,5);wire('IR_BASE','R25:2','Q1:2');wire('IR_BASE',[217,148],'R26:1');wire('IR_LED_K','D1:1','Q1:3');wire('IR_LED_A','R24:2','D1:2');supply('LOGIC_3V3','R24:1');wire('GND','Q1:1',[223,162],[217,162],'R26:2');ground([223,162]);
place('U2',247,143,0,RX);place('R27',240,125,90);place('C14',239,153);place('C15',250,153);port('R27',1,5);wire('IR_RX_3V3','R27:2',[247,125],'U2:3');wire('IR_RX_3V3',[247,131],[234,131],[234,148],[239,148],'C14:1');wire('IR_RX_3V3',[239,148],[250,148],'C15:1');
wire('GND','C14:2',[239,160],[250,160],'C15:2');wire('GND','U2:2',[247,160]);ground([247,160]);port('U2',1,2);
group('VIBRATION MOTOR',265,108,60,65,'Flyback diode + low-side MOSFET.');
place('Q4',289,148);place('R28',278,148,90);place('R29',284,156);place('J4',316,130,0,HMOTOR);place('D2',299,134,270);place('C16',306,137);place('C17',273,137);
port('R28',1,4);wire('MOTOR_GATE','R28:2','Q4:2');wire('MOTOR_GATE',[284,148],'R29:1');wire('GND','Q4:1',[290,164],[284,164],'R29:2');ground([290,164]);
wire('ACT_3V2','J4:1',[309,128.5],[309,124],[273,124],'C17:1');wire('ACT_3V2','D2:1',[299,124]);wire('ACT_3V2','C16:1',[306,124]);supply('ACT_3V2',[290,124]);
wire('MOTOR_RETURN','J4:2',[309,131.5],[309,144],[290,144],'Q4:3');wire('MOTOR_RETURN','D2:2',[299,144]);wire('MOTOR_RETURN','C16:2',[306,144]);ground('C17:2');
group('AUDIO  /  PWM FILTER -> BRIDGE AMPLIFIER -> SPEAKER',5,179,233,49,'Speaker floats between OUT1 and OUT2. Never ground either speaker lead.');
// Signal chain reads left-to-right, with shunt capacitors visibly going to ground.
place('R30',17,198,90);place('C18',24,205);place('R31',33,198,90);place('C19',41,205);place('C20',51,198,90);place('R32',64,198,90);place('R33',73,205);place('U3',98,203,0,AMP);place('J5',155,204,0,HSPK);
port('R30',1,5);wire('AUDIO_LP1','R30:2',[24,198],'R31:1');wire('AUDIO_LP1',[24,198],'C18:1');wire('AUDIO_LP2','R31:2',[41,198],'C20:1');wire('AUDIO_LP2',[41,198],'C19:1');wire('AUDIO_AC','C20:2','R32:1');wire('AMP_IN','R32:2',[73,198],'U3:7');wire('AMP_IN',[73,198],'R33:1');
for(const r of ['C18','C19','R33'])ground(r+':2');ground('U3:6');ground('U3:4');
place('C21',93,219,90);place('C22',106,221);wire('AMP_NP1','U3:8',[87,215],[87,219],'C21:1');wire('AMP_NP2','C21:2',[106,219],'C22:1');wire('AMP_NP2','U3:5',[103,219],[106,219]);ground('C22:2');
place('C23',126,205);place('R34',126,217);place('C24',140,216);place('R35',140,222);
wire('SPK_P','U3:1',[126,198],[148,198],[148,202.5],'J5:1');wire('SPK_P',[126,198],'C23:1');wire('ZOBEL_P','C23:2','R34:1');ground('R34:2');
wire('SPK_N','U3:3',[140,210],[150,210],[150,205.5],'J5:2');wire('SPK_N',[140,210],'C24:1');wire('ZOBEL_N','C24:2','R35:1');ground('R35:2');
const ap=highSide('AMP',['Q5','Q6','R36','R37','R38','R39'],'ACT_3V2','AMP_VCC',184,198);
place('C25',219,207);place('C26',230,207);wire('AMP_VCC','Q6:3',[183,203],[213,203],[213,199],[230,199],'C26:1');wire('AMP_VCC',[219,199],'C25:1');
wire('GND','C25:2',[219,219],[230,219],'C26:2');ground([219,219]);
wire('AMP_VCC',[183,203],[174,203],[174,190],[98,190],'U3:2');
group('RGB MOOD LED / CONSTANT CURRENT',243,179,82,49,'D1 remains IR. U4 drives visible D3; no ESP32 strap pin used.');
place('U4',268,206,0,RGBDRIVER);place('D3',306,196,0,RGB);
for(const pin of [2,3,4,13])port('U4',pin,3);
supply('LOGIC_3V3','U4:16');ground('U4:1');supply('MCU_5V','D3:2');
for(const [up,dp,x]of [[5,1,288],[6,4,292],[7,3,296]]){const a=point('U4:'+up),z=point('D3:'+dp);wire(parts.get('U4').nets[up],'U4:'+up,[x,a[1]],[x,z[1]+(up-4)*2],[z[0],z[1]+(up-4)*2],'D3:'+dp);}
place('R40',280,221,90);wire('RGB_R_EXT','U4:15',[274,221],'R40:1');ground('R40:2');
place('C27',249,194);supply('LOGIC_3V3','C27:1');ground('C27:2');
place('R41',310,219);supply('LOGIC_3V3','R41:1');port('R41',2,2);
place('R42',250,220);port('R42',1,2);ground('R42:2');
place('R43',260,224);port('R43',1,2);ground('R43:2');
txt('GPA4=DATA; GPA5=CLK; GPA6=LATCH; GPA7=OE_N\nDefault blanked; latch 0 before enabling. Approx. 10.4mA/channel.',245,229,1.05);
// ERC source markers live on existing rail wires, not in the purchased BOM.
for(const [ref,x,y,net]of [['#FLG00',47,31,'MCU_5V'],['#FLG01',19,59,'LOGIC_3V3'],['#FLG02',57,59,'ACT_3V2'],['#FLG03',47,47,'GND'],['#FLG04',244,125,'IR_RX_3V3'],['#FLG05',225,199,'AMP_VCC']]){
 const F='SupplyFlag';if(!defs.has(F))defs.set(F,parse(`(symbol "SupplyFlag"(pin_numbers(hide yes))(pin_names(hide yes))(in_bom no)(on_board no)
 (property "Reference" "#FLG"(at 0 0 0)(hide yes) ${eff})(property "Value" "PWR_FLAG"(at 0 0 0)(hide yes) ${eff})
 (symbol "SupplyFlag_0_1"(polyline(pts(xy 0 0)(xy -1.27 2.54)(xy 1.27 2.54)(xy 0 0))(stroke(width 0.2)(type default))(fill(type none))))
 (symbol "SupplyFlag_1_1"(pin power_out line(at 0 0 90)(length 0)(name "" ${eff})(number "1" ${eff}))))`));place(ref,x,y,0,F);wire(net,ref+':1',[x+.5,y]);}
// All baseline components must appear once; no accidental circuit deletions in a visual task.
for(const ref of parts.keys())if(!placed.has(ref))throw Error('unplaced '+ref);
for(const [ref,c]of placed)for(const p of c.pins)if(c.nets[p.num]!==null&&!claimed.has(ref+':'+p.num))throw Error('unwired pin '+ref+':'+p.num);
// Split wires at all same-net endpoints/pins; explicit junctions distinguish joined branches.
const on=(p,s)=>s.a[0]===s.b[0]?p[0]===s.a[0]&&p[1]>=Math.min(s.a[1],s.b[1])&&p[1]<=Math.max(s.a[1],s.b[1]):p[1]===s.a[1]&&p[0]>=Math.min(s.a[0],s.b[0])&&p[0]<=Math.max(s.a[0],s.b[0]);
const terminals=[...placed.values()].flatMap(c=>c.pins.filter(p=>c.nets[p.num]!==null).map(p=>({p:[p.x,p.y],net:c.nets[p.num]})));
const endpoints=[...wires.flatMap(w=>[{p:w.a,net:w.net},{p:w.b,net:w.net}]),...labels,...terminals];
const collisions=new Set();for(const e of endpoints)for(const w of wires)if(e.net!==w.net&&on(e.p,w))collisions.add(`${e.net}/${w.net} at ${e.p}`);if(collisions.size)throw Error('Unintended joins:\n'+[...collisions].join('\n'));
const segments=new Map();for(const w of wires){const pts=endpoints.filter(e=>e.net===w.net&&on(e.p,w)).map(e=>e.p);const uniq=[...new Map(pts.map(p=>[p.join(','),p])).values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);for(let i=1;i<uniq.length;i++){const a=uniq[i-1],b=uniq[i];segments.set(w.net+':'+a+':'+b,{net:w.net,a,b});}}
const counts=new Map();for(const s of segments.values()){items.push(`(wire(pts(xy ${mm(s.a[0])} ${mm(s.a[1])})(xy ${mm(s.b[0])} ${mm(s.b[1])}))(stroke(width 0)(type default))(uuid ${q(uid('wire'+s.net+s.a+s.b))}))`);for(const p of [s.a,s.b]){const k=s.net+':'+p;counts.set(k,{p,n:(counts.get(k)?.n||0)+1});}}
for(const [key,c]of counts)if(c.n>=3)items.push(`(junction(at ${mm(c.p[0])} ${mm(c.p[1])})(diameter 0.9)(color 0 0 0 0)(uuid ${q(uid('dot'+key))}))`);
const used=new Set([...placed.values()].map(c=>c.name));
const cached=[...used].map(name=>{const d=structuredClone(defs.get(name));d[1]=q('KK_Main:'+name);return dump(d)});
fs.writeFileSync(path.join(out,'KK_main_module.kicad_sch'),`(kicad_sch(version 20250114)(generator "eeschema")(generator_version "9.0")(uuid ${q(root)})(paper "User" 841 640)
 (title_block(title "Main board - grouped wired schematic")(date "2026-09-10")(rev "C.3 / RGB, debug pads, assembly access")(company "Keychain Kreatures")(comment 1 "Engineering prototype; bench qualification required"))
 (lib_symbols ${cached.join('\n')})\n${items.join('\n')}(sheet_instances(path "/"(page "1"))))\n`);
fs.writeFileSync(path.join(out,'KK_Main.kicad_sym'),`(kicad_symbol_lib(version 20250114)(generator "kicad_symbol_editor")\n${[...used].map(k=>dump(defs.get(k))).join('\n')})\n`);
fs.writeFileSync(path.join(out,'sym-lib-table'),'(sym_lib_table\n  (version 7)\n  (lib (name "KK_Main") (type "KiCad") (uri "${KIPRJMOD}/KK_Main.kicad_sym") (options "") (descr "One-sheet main board symbols"))\n)\n');
console.log(`Redrawn ${placed.size} symbols / ${segments.size} wired segments on one A1 sheet.`);
