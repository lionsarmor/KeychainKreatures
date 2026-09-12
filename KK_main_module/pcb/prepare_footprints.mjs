// Preserve the hand-readable schematic; assign footprints in place without redrawing it.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url)),root=path.dirname(dir);
const q=JSON.stringify;
function parse(s){const t=s.match(/"(?:\\.|[^"\\])*"|[()]|[^\s()]+/g);let i=0;function p(){const a=[];if(t[i++]!=='(')throw Error('syntax');while(t[i]!==')'){if(i>=t.length)throw Error('EOF');a.push(t[i]==='('?p():t[i++]);}i++;return a;}return p();}
const val=s=>s?.startsWith('"')?JSON.parse(s):s,children=(a,k)=>a.filter(x=>Array.isArray(x)&&x[0]===k),get=(a,k)=>children(a,k)[0];
const dump=a=>Array.isArray(a)?`(${a.map(dump).join(' ')})`:a;
const libdir=execFileSync('flatpak',['info','--show-location','org.kicad.KiCad.Library.Footprints'],{encoding:'utf8'}).trim()+'/files/footprints';
const pretty=path.join(root,'KK_Main.pretty');fs.mkdirSync(pretty,{recursive:true});
const all=new Map(),audit=[];
function standard(name,source,evidence,note=''){const s=fs.readFileSync(path.join(libdir,source.replace('/','.pretty/')+'.kicad_mod'),'utf8');const a=parse(s);a[1]=q(name);fs.writeFileSync(path.join(pretty,name+'.kicad_mod'),dump(a)+'\n');all.set(name,{evidence,note,source,status:'DATASHEET_DIMENSIONS_CHECKED'});return name;}
function custom(name,pads,body,description,status='DATASHEET_DIMENSIONS_CHECKED',extra=''){
const[x1,y1,x2,y2]=body;let s=`(footprint ${q(name)}(version 20240108)(generator "pcbnew")(layer "F.Cu")(descr ${q(description)})(attr through_hole)
 (property "Reference" "REF**"(at 0 ${y1-1.5} 0)(layer "F.SilkS")(effects(font(size 1 1)(thickness 0.15))))
 (property "Value" ${q(name)}(at 0 ${y2+1.5} 0)(layer "F.Fab")(effects(font(size 1 1)(thickness 0.15))))
 (fp_rect(start ${x1} ${y1})(end ${x2} ${y2})(stroke(width 0.1)(type default))(fill none)(layer "F.Fab"))
 (fp_rect(start ${x1-.5} ${y1-.5})(end ${x2+.5} ${y2+.5})(stroke(width 0.05)(type default))(fill none)(layer "F.CrtYd"))`;
for(const [num,x,y,drill=1,size=1.8]of pads)s+=`(pad ${q(String(num))} thru_hole ${String(num)==='1'||num==='A'?'rect':'circle'}(at ${x} ${y})(size ${size} ${size})(drill ${drill})(layers "*.Cu" "*.Mask"))`;
s+=extra+')\n';fs.writeFileSync(path.join(pretty,name+'.kicad_mod'),s);all.set(name,{evidence:description,note:'Project-local drawing. See footprint audit for prototype holds.',status,source:'custom'});return name;}
const resistor=standard('MFR25_10p16','Resistor_THT/R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal','Yageo MFR-25: body 6.3+/-0.5 x 2.4+/-0.2 mm; wire 0.55+/-0.05 mm','Form axial leads to 10.16 mm pitch; do not seat body under mechanical stress.');
const ceramic=custom('KEMET_C315_P2p54',[[1,0,0,.9,1.7],[2,2.54,0,.9,1.7]],[-.635,-1.27,3.175,1.27],'KEMET exact C315C104K5R5TA / C315C103J1G5TA / C315C105K5R5TA sheets: 3.81 x 2.54 mm max body, 2.54 mm pitch, wire <=0.61 mm');
const electrolytic=standard('Nichicon_UVR_D5_P2','Capacitor_THT/CP_Radial_D5.0mm_P2.00mm','Nichicon UVR1C100MDD / UVR1C101MDD: 5 mm diameter, 11 mm height, 2 mm lead pitch','Both values use the same diameter/pitch; keep the 11 mm body outside the under-screen volume.');
const dip28=standard('ED281DT_DIP28_Socket','Package_DIP/DIP-28_W7.62mm_Socket_LongPads','Microchip SPDIP28 plus On Shore ED281DT socket: 7.62 mm rows, 2.54 mm pitch','Narrow socket, not wide ED28DT.');
const dip8=standard('ED08DT_DIP8_Socket','Package_DIP/DIP-8_W7.62mm_Socket_LongPads','UTC DIP8 plus On Shore ED08DT socket: 7.62 mm rows, 2.54 mm pitch');
const to92=standard('TO92_LeadFormed_P2p54','Package_TO_SOT_THT/TO-92_Inline_Wide','onsemi KSP2222ABU / BC32725BU and Microchip TN0702N3-G / LP0701N3-G package drawings','WIDE footprint requires spreading native 1.27 mm leads to 2.54 mm using a jig; flat face follows F.Fab. Pins 1-2-3: KSP E-B-C; BC327 C-B-E; TN0702 and LP0701 S-G-D.');
const led=standard('TSAL6200_LED5','LED_THT/LED_D5.0mm','Vishay TSAL6200: 5 mm LED body, 2.54 mm pitch. Pin1 cathode, pin2 anode.');
const diode=standard('1N5819_DO41','Diode_THT/D_DO-41_SOD81_P10.16mm_Horizontal','Vishay 1N5819-E3/54 DO-41 axial body; 10.16 mm formed lead pitch. Pin1 cathode band.');
const ph=standard('JST_PH_S2B_2','Connector_JST/JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal','JST S2B-PH-K-S(LF)(SN) ePH drawing: right-angle two-pin, 2.00 mm pitch');
const xh=standard('JST_XH_B4B_4','Connector_JST/JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical','JST B4B-XH-A(LF)(SN) eXH drawing: vertical four-pin, 2.50 mm pitch');
const button=custom('Adafruit3101_ABCD', [['A',-4,-2.25,1,1.9],['B',4,-2.25,1,1.9],['C',-4,2.25,1,1.9],['D',4,2.25,1,1.9]],[-4.7,-3.9,4.7,3.9],'Adafruit linked C4817-001 drawing: 8 x 4.5 mm hole centers, 4 x 1 mm holes, A/B upper pair C/D lower pair, body 7.8 mm, lead envelope 9.4 mm','DATASHEET_DIMENSIONS_CHECKED','(fp_circle(center 0 0)(end 1.75 0)(stroke(width 0.15)(type default))(fill none)(layer "F.SilkS"))');
const rx=custom('TSOP38238_Vertical',[[1,0,0,1.1,1.9],[2,2.54,0,1.1,1.9],[3,5.08,0,1.1,1.9]],[-.6,-1.4,5.7,3.4],'Vishay TSOP382 package drawing: 2.54 mm lead spacing, OUT-GND-VS order when facing lens; body 5 x 4.8 mm. Lens faces +Y','DATASHEET_DIMENSIONS_CHECKED','(fp_text user "LENS"(at 2.54 4.3)(layer "F.Fab")(effects(font(size .8 .8)(thickness .12))))');
function socket(n){return custom(`Sullins_PPTC${String(n).padStart(2,'0')}1_LFB`,Array.from({length:n},(_,i)=>[i+1,0,i*2.54,1.05,1.85]),[-1.27,-1.27,1.27,(n-.5)*2.54],`Sullins PPTC${String(n).padStart(2,'0')}1LFBN-RC: one row 2.54 mm pitch; 8.5 mm housing height. Pin1 marked square. Module orientation still requires sample check.`);}
const h8=socket(8),h6=socket(6);
const mcu='ESP32-S3-SuperMini';
if(!fs.existsSync(path.join(pretty,mcu+'.kicad_mod')))throw Error('Import the user-supplied SuperMini footprint first.');
all.set(mcu,{evidence:'User supplied ESP32-S3-SuperMini.kicad_mod. Original geometry preserved: 15.24 mm rows, nominal 2.54 mm pitch, 1 mm drills, 1.508 mm pads.',note:'Schematic pins use supplied GPIO/power pad names. GPIO13 y=-2.50 mm retained (0.04 mm off nominal pitch). Physical fit/stack not certified.',source:'User-supplied footprint; see pcb/SUPERMINI_IMPORT.json',status:'USER_SUPPLIED_FOOTPRINT'});
const schemaPath=path.join(root,'KK_main_module.kicad_sch'),schema=parse(fs.readFileSync(schemaPath,'utf8'));
const rootUUID=val(get(schema,'uuid')[1]),rows=[];
for(const sym of children(schema,'symbol')){const props=Object.fromEntries(children(sym,'property').map(p=>[val(p[1]),val(p[2])]));const r=props.Reference;if(r.startsWith('#'))continue;let f;
if(r.startsWith('R'))f=resistor;else if(r.startsWith('C'))f=props.MPN.startsWith('UVR')?electrolytic:ceramic;else if(r.startsWith('SW'))f=button;else if(r.startsWith('Q'))f=to92;else f={MOD1:mcu,U1:dip28,U2:rx,U3:dip8,D1:led,D2:diode,J1:xh,J2:h8,J3:h6,J4:ph,J5:ph}[r];if(!f)throw Error('No footprint '+r);
const fp=children(sym,'property').find(p=>val(p[1])==='Footprint');fp[2]=q('KK_Main:'+f);
rows.push({ref:r,mpn:props.MPN,value:props.Value,footprint:'KK_Main:'+f,uuid:val(get(sym,'uuid')[1]),path:'/'+rootUUID+'/'+val(get(sym,'uuid')[1]),...all.get(f)});
}
if(rows.length!==91)throw Error('Component count changed: '+rows.length);
fs.writeFileSync(schemaPath,dump(schema)+'\n');
fs.writeFileSync(path.join(root,'fp-lib-table'),'(fp_lib_table\n (version 7)\n (lib (name "KK_Main") (type "KiCad") (uri "${KIPRJMOD}/KK_Main.pretty") (options "") (descr "Main-board checked THT footprints; SuperMini provisional"))\n)\n');
fs.writeFileSync(path.join(dir,'footprint_assignments.json'),JSON.stringify(rows,null,2)+'\n');
fs.writeFileSync(path.join(dir,'FOOTPRINT_AUDIT.csv'),[['Reference','MPN','Footprint','Status','Source','Evidence','Assembly note'],...rows.map(r=>[r.ref,r.mpn,r.footprint,r.status,r.source,r.evidence,r.note])].map(r=>r.map(x=>q(x||'')).join(',')).join('\n')+'\n');
console.log(`Assigned ${rows.length} THT footprints; ${all.size} project-local package patterns. User-supplied SuperMini footprint retained.`);
