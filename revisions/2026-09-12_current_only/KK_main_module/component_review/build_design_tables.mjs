// Regenerate the derived tables: node KK_main_module/component_review/build_design_tables.mjs
// This script only rewrites its seven named output files in this directory.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const read = name => fs.readFileSync(path.join(dir, name), 'utf8');
const write = (name, body) => fs.writeFileSync(path.join(dir, name), body);
const parse = line => {
  assert(line.startsWith('"') && line.endsWith('"'));
  return line.slice(1, -1).split('","').map(s => s.replaceAll('""', '"'));
};
const rows = read('parts.csv').trim().split(/\r?\n/).map(parse);
assert(rows.every(r => r.length === 8));
const fields = rows.shift();
const parts = rows.map(r => Object.fromEntries(fields.map((k, i) => [k, r[i]])));
const get = block => { const p = parts.find(p => p.block === block); assert(p, block); return p; };
const partByCode = code => { const p = parts.find(p => p.exact_part === code); assert(p, code); return p; };
const components = [];
const add = (ref, part, pins) => { assert(!components.some(c => c.ref === ref)); components.push({ref, part: part.exact_part, pins}); };
const resistor = (ref, value, a, b) => add(ref, partByCode('MFR-25FBF52-' + value), {'1': a, '2': b});
const cap = (ref, code, a, b) => add(ref, partByCode(code), {'1': a, '2': b});
// Revision B: invalidate every Waveshare header/GPIO assignment. These are
// logical interface requirements, not 18 promised SuperMini header GPIOs.
// Slow outputs must migrate to the expander as part of the new pin budget.
const signals = ['I2C_SDA','I2C_SCL','BUTTON_INT_N','BUTTON_FN_N','EXP_RESET_N',
 'IR_TX','IR_RX','TFT_CS','TFT_MOSI','TFT_SCK','TFT_DC','TFT_RESET',
 'TFT_BACKLIGHT_CONTROL','AUDIO_PWM','MOTOR_CONTROL','BATTERY_ADC','POWER_STATUS','AUDIO_ENABLE',
 'SD_MISO','SD_CS'];
const connectedSignals = signals.slice(0,7);
const gpio = signals.map(s => ['TBD','TBD',s,'UNASSIGNED; SuperMini pin budget reopened']);
add('MOD1', get('CORE'), Object.fromEntries([
  ['LOGICAL_3V3','LOGIC_3V3'], ['LOGICAL_GND','GND'],
  ...connectedSignals.map(s => ['LOGICAL_' + s, s])
]));
const mcp = {'1':'BTN_A_N','2':'BTN_B_N','3':'BTN_X_N','4':'BTN_Y_N',
 '5':'NC','6':'NC','7':'NC','8':'NC','9':'LOGIC_3V3','10':'GND','11':'NC',
 '12':'I2C_SCL','13':'I2C_SDA','14':'NC','15':'GND','16':'GND','17':'GND',
 '18':'EXP_RESET_N','19':'NC','20':'BUTTON_INT_N','21':'BTN_UP_N',
 '22':'BTN_DOWN_N','23':'BTN_LEFT_N','24':'BTN_RIGHT_N','25':'NC','26':'NC','27':'NC','28':'NC'};
assert.equal(Object.keys(mcp).length, 28);
assert.equal(mcp['8'], 'NC'); assert.equal(mcp['28'], 'NC');
add('U1', get('GPIO'), mcp);
resistor('R1','4K7','LOGIC_3V3','I2C_SDA');
resistor('R2','4K7','LOGIC_3V3','I2C_SCL');
resistor('R3','10K','LOGIC_3V3','EXP_RESET_N');
resistor('R4','10K','LOGIC_3V3','BUTTON_INT_N');
const buttonNets = ['BTN_UP_N','BTN_DOWN_N','BTN_LEFT_N','BTN_RIGHT_N','BTN_A_N','BTN_B_N','BTN_X_N','BTN_Y_N','BUTTON_FN_N'];
buttonNets.forEach((net, i) => {
  // A/B are logical contacts. Physical four-leg mapping must be sample-verified.
  add('SW' + (i + 1), get('CONTROLS'), {A: net, B: 'GND'});
  resistor('R' + (i + 5),'10K','LOGIC_3V3',net);
});
cap('C1','C315C104K5R5TA','LOGIC_3V3','GND');
cap('C2','UVR1C100MDD','LOGIC_3V3','GND');
resistor('R14','100R','LOGIC_3V3','IR_LED_A');
add('D1',get('IR_TX'), {A:'IR_LED_A',K:'IR_LED_K'});
add('Q1',get('NPN_DRIVER'), {'1':'GND','2':'IR_BASE','3':'IR_LED_K'});
resistor('R15','220R','IR_TX','IR_BASE');
resistor('R16','100K','IR_BASE','GND');
resistor('R17','100R','LOGIC_3V3','IR_RX_3V3');
add('U2',get('IR_RX'), {'1':'IR_RX','2':'GND','3':'IR_RX_3V3'});
cap('C3','C315C104K5R5TA','IR_RX_3V3','GND');
cap('C4','UVR1C100MDD','IR_RX_3V3','GND');
cap('C5','C315C104K5R5TA','LOGIC_3V3','GND');
assert.equal(components.filter(c => /^R\d/.test(c.ref)).length,17);
assert.equal(components.filter(c => /^C\d/.test(c.ref)).length,5);
const counts = new Map();
for (const c of components) counts.set(c.part, (counts.get(c.part) || 0) + 1);
assert.equal(counts.get('MFR-25FBF52-10K'), 11);
assert.equal(counts.get('MFR-25FBF52-100R'), 2);
const endpoints = new Map();
for (const c of components) for (const [pin, net] of Object.entries(c.pins)) {
  assert(net !== 'VBUS' && net !== 'BAT+' && net !== 'VCC_5V');
  const key = c.ref + '.' + pin;
  assert(!endpoints.has(key)); endpoints.set(key, net);
}
for (const net of new Set(endpoints.values())) {
  if (net !== 'NC') assert([...endpoints.values()].filter(n => n === net).length >= 2, net);
}
const extra = (block, qty, name, status, notes, pack = 'TBD') => ({block, planned_quantity: qty, manufacturer:'TBD', exact_part:name, package:pack, selection_status:status, local_datasheet:'', notes});
parts.push(
 extra('POWER_PATH','TBD','USB/battery source isolation and charger enable','HOLD — architecture','Must prevent battery boost powering its own charger; independently detect real USB power without modifying MCU module.'),
 extra('BATTERY_REGULATION','TBD','Battery-to-system converter and magnetics','HOLD — architecture','1S range and MCU onboard regulator require a qualified supply route; no external 3.3 V injection assumed safe.'),
 extra('CHARGE_SUPERVISION','TBD','Precharge / termination / restart / safety timer circuitry','HOLD — safety','CC/CV converter alone is insufficient. Independent hardware behavior required even with crashed firmware.'),
 extra('CHARGE_TEMPERATURE','TBD','NTC threshold and charge-inhibit network','HOLD — calculations','Select thresholds against cell datasheet; fail safe for disconnected/shorted thermistor.'),
 extra('BATTERY_PROTECTION','TBD','Overcharge / undervoltage / overcurrent protection','HOLD — safety','Protected pack backup plus appropriate main-board protections; exact architecture not chosen.'),
 extra('INPUT_PROTECTION','TBD','Fuse/PTC and reverse-polarity protection','HOLD — calculations','Set against source, wiring, cell and inrush limits. Do not treat a random PTC as lithium protection.'),
 extra('POWER_SWITCH','1 proposed','Through-hole power switch','HOLD — topology','Must support charging while toy is off; contact current and mechanical size depend on circuit.'),
 extra('BATTERY_MEASUREMENT','TBD','Switched ADC divider / input protection','HOLD — calculations','GPIO1 reservation only; battery must never connect directly to GPIO.'),
 extra('POWER_INDICATORS','TBD','Charge / fault indication parts','HOLD — user interface','Choose independent charge indication vs screen after charger architecture; avoid duplicate unnecessary LEDs.'),
 extra('POWER_PASSIVES','TBD','Power-specific resistors / capacitors / diodes / inductors','HOLD — topology','Not covered by ordinary resistor pool. Each value, rating and exact MPN must become its own row.'),
 extra('BACKLIGHT_DRIVER','TBD','Backlight control and default-off network','HOLD — display sample','Verify whether BLK is a logic input or LED-current terminal; do not drive an unknown LED load from GPIO.'),
 extra('AUDIO_NETWORK','TBD','PWM filter / attenuation / coupling / bridge stability','HOLD — calculations','Account for amplifier gain and speaker rating. Count from actual audio schematic, not guessed bag quantities.'),
 extra('AUDIO_GATE','TBD','Amplifier supply gating network','HOLD — calculations','Audio quiescent current matters; prevent PWM phantom-power when amp is off.'),
 extra('MOTOR_NETWORK','TBD','Motor drive / suppression','HOLD — startup and stall','Driver and flyback stay on main board; voltage regulation and regulator capacitors belong to the power-board revision.'),
 extra('SPEAKER_CONTACT','2','Speaker harness crimp contacts','HOLD — wire gauge','Choose JST contact for actual conductor and insulation diameter; motor contacts cannot be assumed interchangeable.','Crimp'),
 extra('HARNESS_WIRE','TBD length','Battery/NTC and actuator wire','HOLD — mechanical','26 AWG battery harness proposed; routing, strain relief, insulation and exact wire required.'),
 extra('BATTERY','1','1S 3.6/3.7 V nominal, 4.2 V maximum pack','Deferred by user','Capacity/shape chosen later; discharge capability, permitted charge current, connector polarity and temperature limits must be qualified before powering.','Wired pack'),
 extra('HARNESS_INSULATION','TBD length','Heatshrink / NTC insulation / strain relief','HOLD — mechanical','Prevent shorts; NTC must contact cell thermally while remaining electrically insulated.'),
 extra('MAIN_PCB','1','KK main-board custom PCB','Design pending','THT student assembly; final dimensions after placement, antenna keepout and safety separation.','Custom PCB'),
 extra('TEST_ACCESS','TBD pads','PCB test pads and optional service header','Design pending','Pads are PCB features, not separate bag parts. Any populated header gets its own exact row.'),
 extra('ENCLOSURE','1 set','Custom front and rear shell','Deferred to board outline','User models shell; include USB opening, IR window, antenna clearance and battery retention.','Custom printed/molded'),
 extra('BUTTON_CAPS','1 set','D-pad plus A/B/X/Y and Function caps','Mechanical design pending','Nine electrical switches; a single D-pad cap can operate four switches. Check travel, anti-jam guides and preload.'),
 extra('SCREEN_WINDOW','1 proposed','Display lens / protective window','Mechanical design pending','Define material, thickness, optical quality and retention before release.'),
 extra('SCREEN_RETENTION','1 set','Display retention hardware / spacers','Mechanical design pending','No pressure on flex tail or LCD glass; socket alone may not secure screen.'),
 extra('PCB_HARDWARE','TBD','PCB spacers and fasteners','Mechanical design pending','Exact thread/length after stack-up; no loose metal near battery.'),
 extra('SHELL_FASTENERS','TBD','Shell screws / inserts','Mechanical design pending','Keep small parts captive as appropriate; select against intended age and service requirements.'),
 extra('ACTUATOR_MOUNT','1 set','Speaker gasket and motor retention','Mechanical design pending','Speaker seal/acoustic cavity affect perceived quality; secure motor without damping all vibration.'),
 extra('BATTERY_RETENTION','1 set','Cell restraint and cushioning','Mechanical design pending','No sharp edges, crushing, piercing screws or forced bending.'),
 extra('KEYCHAIN_HARDWARE','1 set proposed','Split ring / tether and reinforced anchor','Mechanical design pending','Confirm age-appropriate attachment, retention and small-parts requirements.'),
 extra('USB_CABLE','1 proposed','USB data-capable host-to-USB-C cable','Exact SKU pending','Not charge-only. Host end and length to suit classroom; may be shared classroom supply.'),
 extra('PRINTED_MATERIAL','1 set','Assembly guide / polarity labels / safety notes','Content pending','Include firmware loading, battery use, sample inspection and test sequence.'),
 extra('PACKAGING','1 set','ESD bag and compartmented kit packaging','Exact SKU pending','Keep battery transport and packing requirements separate from ordinary parts packaging.'),
 extra('CLASSROOM_TOOLS','Shared; not per kit','Iron / solder / cutters / ESD mat / multimeter','Assembly plan pending','Crimped harnesses supplied preassembled; no student crimping of tiny contacts assumed.'),
 extra('MICROSD','1','microSD card; exact brand/capacity pending','Storage now included; card selection pending','Separate B0F82XWT4F reader; retain current screen. Persistent game packages/assets/saves, not PSRAM or automatic executable storage. Card not assumed included with reader.'),
 extra('EXTERNAL_USB','0 on main PCB','No additional main-board USB socket','Revised scope','Routine updates are wireless. Future power board may have charging USB and optional data; retain module USB for service.'),
 extra('SYS_IN_CONNECTOR','1','Keyed THT regulated-power input connector','Interface selection pending','Power board supplies required regulated rails. Single 5 V-only proposal is reopened because main-board voltage regulation is excluded. Pin count, rails, current and polarity must be frozen before routing.'),
 extra('SYS_IN_HARNESS','1 set','Power-board to main-board harness and mating contacts','Interface selection pending','Exact gauge, length, terminals and strain relief after current budget and connector selection.'),
 extra('MAIN_RAIL_INTERFACE','TBD','Main-board rail distribution / local bypass capacitors','Main-board engineering pending','No discrete voltage regulators on main PCB. Power board owns regulation and source protection; main board retains local decoupling and driver suppression. Do not assume safe external injection into MCU regulator output. Service USB isolation must be qualified jointly.'),
 extra('SD_SUPPORT','TBD','SD supply bypass / bus pull-ups / optional series resistors','Circuit inspection pending','Inspect populated module before assigning external values; card write transients must enter rail budget. Do not assume onboard 5 V regulation or level conversion.'),
 extra('SD_RETENTION','1 set if needed','Reader support and display clearance / insulation','Mechanical design pending','Under-screen target only; leave insertion/ejection space and safe separation from LCD metalwork. Exact spacers/fasteners depend on stack-up.')
);
const powerDeferred = new Set(['BAT_CONNECTOR','BAT_HOUSING','BAT_CONTACT','BAT_NTC','MAIN_REG','HAPTIC_REG','CHARGER',
 'POWER_PATH','BATTERY_REGULATION','CHARGE_SUPERVISION','CHARGE_TEMPERATURE','BATTERY_PROTECTION',
 'INPUT_PROTECTION','POWER_SWITCH','BATTERY_MEASUREMENT','POWER_INDICATORS','POWER_PASSIVES']);
for (const p of parts) if (powerDeferred.has(p.block)) {
  p.planned_quantity = '0 on main PCB; TBD power revision';
  p.selection_status = 'Deferred to separate power-board revision; old candidate not selected';
  p.notes = 'Historical integrated-power candidate/requirement; do not purchase for main board. Future power board requires its own reviewed BOM. ' + p.notes;
}
const csv = lines => lines.map(r => r.map(x => '"' + String(x).replaceAll('"','""') + '"').join(',')).join('\n') + '\n';
const esc = s => String(s).replaceAll('|','/').replaceAll('\n',' ');
const bomRows = parts.map((p, i) => {
  if (p.local_datasheet) assert(fs.existsSync(path.join(dir, p.local_datasheet)), p.local_datasheet);
  const refs = components.filter(c => c.part === p.exact_part).map(c => c.ref);
  const starter = counts.get(p.exact_part) || 0;
  const qty = (p.block === 'RESISTOR' || p.block === 'CAPACITOR' || p.block === 'NPN_DRIVER') && starter ? `TBD total; ${starter} in starter circuit` : p.planned_quantity;
  let notes = p.notes;
  if (p.exact_part === 'MFR-25FBF52-39R') notes = 'Unpopulated candidate only. Starter IR circuit uses 100 ohm; no 39 ohm resistor is approved for assembly.';
  if (p.exact_part === 'MFR-25FBF52-100R') notes = 'Starter: R14 IR LED limit and R17 receiver rail filter. Other uses TBD.';
  if (p.exact_part === 'MFR-25FBF52-220R') notes = 'Starter: R15 IR transistor base. Other uses TBD.';
  return [`B${String(i+1).padStart(3,'0')}`,p.block,qty,starter,refs.join(' '),p.manufacturer,p.exact_part,p.package,p.selection_status,p.local_datasheet,notes];
});
write('MASTER_BOM.csv', csv([['id','function','whole_kit_quantity','starter_quantity','starter_references','manufacturer','exact_part_or_open_requirement','package','status','local_datasheet','notes'],...bomRows]));
let md = '# Whole-kit component table — revision B\n\n2026-09-10. **Main-board scope revision, NOT a finalized purchasing BOM.** A separate revised power board is now authorized and deferred. Integrated charging parts are zero on the main PCB; retained rows track deferred requirements rather than approved power-board parts.\n\n';
md += 'Selected family: **ESP32-S3 SuperMini**, assuming the original Teyleten Robot Amazon B0D47HBFDY unless the user chooses another seller revision. Photographed FH4R2 indicates 4 MB flash / 2 MB PSRAM; verify delivered hardware. Two nine-way sockets replace the Waveshare 22-way sockets. The previous Waveshare GPIO map is withdrawn, not reusable on this module.\n\n';
md += 'Main-board student assembly remains THT. The user now permits the preassembled MCU, original XIITIA display AND separate B0F82XWT4F SD reader, attached through headers. See [SD storage amendment](SD_STORAGE.md). Main PCB gets SYS_IN from a future regulated power-board output; the existing unmodified SYS_OUT is not approved as that source. Routine game/app uploads, firmware updates and trading will be wireless. Firmware is not implemented by these tables.\n\n';
md += '[Print-friendly main-board list](MAIN_BOARD_PRINT.html) · [current architecture](REVISION_B.md) · [CSV spreadsheet](MASTER_BOM.csv) · [logical peripheral connections](STARTER_CONNECTIONS.csv) · [part-by-part datasheets](DATASHEET_AUDIT.md) · [validation](VALIDATION.md)\n\n';
md += 'Quantity means per assembled kit unless stated. Starter counts describe retained logical peripheral circuits, not a wireable SuperMini circuit; they may change during pin allocation. Headers supplied with the MCU must not be purchased twice. Nine switches require one ten-pack when purchasing Adafruit 3101. Exact-MPN rows may still have validation holds. Open requirements must be expanded into individual parts after circuit/mechanical design.\n\n';
md += '| ID / function | Whole-kit quantity | Manufacturer / exact part or open requirement | Package | Status / condition | Datasheet |\n|---|---|---|---|---|---|\n';
for (const r of bomRows) md += `| ${r[0]} ${esc(r[1])} | ${esc(r[2])} | ${esc(r[5])}: ${esc(r[6])} | ${esc(r[7])} | ${esc(r[8])}. ${esc(r[10])} | ${r[9] ? '[local PDF/drawing]('+r[9]+')' : 'See notes / unavailable'} |\n`;
md += '\n## Exact quantities established for the initial circuit only\n\n| Reference(s) | Exact part | Count |\n|---|---|---|\n';
for (const r of bomRows.filter(r => r[3] > 0)) md += `| ${r[4]} | ${r[6]} | ${r[3]} |\n`;
md += '\nThis logical peripheral circuit excludes audio, motor, display wiring and supply entry. MOD1 uses logical signal names ONLY; no physical SuperMini pin assignments are released. Two MCU sockets and the expander DIP socket are separate assembly items. KiCad capture, GPIO allocation, footprints, ERC, power-interface qualification and prototype testing remain.\n';
write('MASTER_BOM.md',md);
// Main-board-only print view: omit power-board, enclosure and shared-tool rows.
// Keep open support requirements visible: they are not finalized line items.
const mainBlocks = new Set(['CORE','DISPLAY','GPIO','CONTROLS','AUDIO','SPEAKER','HAPTIC',
 'IR_TX','IR_RX','NPN_DRIVER','PNP_SWITCH','FLYBACK','MCU_SOCKET','MCU_HEADER','GPIO_SOCKET',
 'AUDIO_SOCKET','DISPLAY_SOCKET','ACTUATOR_CONNECTOR','ACTUATOR_HOUSING','MOTOR_CONTACT',
 'RESISTOR','CAPACITOR','SD_MODULE','SD_SOCKET','SD_HEADER','MICROSD','SPEAKER_CONTACT',
 'MAIN_PCB','SYS_IN_CONNECTOR','SYS_IN_HARNESS','MAIN_RAIL_INTERFACE','BACKLIGHT_DRIVER',
 'AUDIO_NETWORK','AUDIO_GATE','MOTOR_NETWORK','SD_SUPPORT','SD_RETENTION','SCREEN_RETENTION',
 'ACTUATOR_MOUNT','PCB_HARDWARE','TEST_ACCESS']);
const printable = bomRows.filter(r => mainBlocks.has(r[1]));
assert(printable.every(r => !powerDeferred.has(r[1])));
const intro = '2026-09-10 — main-board review checklist, not a final purchasing/bagging list. Charging, battery protection and ALL added voltage regulation, including the motor regulator, belong to the separate power board. MCU, display and SD reader are permitted preassembled modules with THT student connections. Local bypass capacitors and actuator drivers remain on the main PCB. No hardware has been ordered or fabricated.';
let printMd = '# Keychain Kreatures — printable main-board list\n\n' + intro + '\n\nQuantity is per toy. “TBD total” means the schematic must determine the count; starter counts are subtotals, not extra parts. Zero-use candidate values are not instructions to buy a resistor bag. Module-bundled headers must not be purchased twice.\n\n| Item | Exact part / candidate | Quantity | Status |\n|---|---|---|---|\n';
for (const r of printable) printMd += `| ${esc(r[1])} | ${esc(r[6])} | ${esc(r[2])} | ${esc(r[8])} |\n`;
const closeout = 'Before final release: (1) verify SuperMini pinout and fit, display/backlight interface and SD socket stack; (2) select a documented speaker, exact microSD card and remaining harness/mating parts; (3) finish GPIO allocation and audio/motor/SD circuits, then count every resistor/capacitor/driver; (4) agree incoming regulated rails and connector pinout with the power board. Only its interface is needed now, not the completed charger design. Enclosure/battery/packaging are outside this main-board print view and remain in the master kit register. No ERC or prototype qualification has been completed.';
printMd += '\n## Remaining work\n\n' + closeout + '\n\n[Full register and datasheets](MASTER_BOM.md) · [Printable HTML](MAIN_BOARD_PRINT.html)\n';
write('MAIN_BOARD_PRINT.md',printMd);
const html = s => String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
write('MAIN_BOARD_PRINT.html','<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Keychain Kreatures — main-board list</title><style>body{font:12px Arial,sans-serif;max-width:1100px;margin:24px auto;color:#111}h1{font-size:22px}p{line-height:1.4}table{border-collapse:collapse;width:100%}th,td{border:1px solid #aaa;padding:5px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#eee}thead{display:table-header-group}tr{break-inside:avoid}h2{font-size:16px} @media print{@page{size:A4 landscape;margin:12mm}body{margin:0;font-size:10px}h1{font-size:18px}.screen{display:none}a{color:#111;text-decoration:none}}</style></head><body><h1>Keychain Kreatures — main-board review checklist</h1><p>'+html(intro)+'</p><p class="screen">Use your browser Print command (Ctrl+P); layout is set for landscape A4. This is a review list, not a fabrication release.</p><p>Per-toy quantities. Starter counts are subtotals; TBD counts and candidate values are not a final purchase list. Do not double-count bundled headers.</p><table><thead><tr><th>Item</th><th>Exact part / candidate</th><th>Quantity</th><th>Status</th></tr></thead><tbody>'+printable.map(r=>'<tr>'+[r[1],r[6],r[2],r[8]].map(v=>'<td>'+html(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table><h2>Remaining work</h2><p>'+html(closeout)+'</p><p>Full notes and datasheets: <a href="MASTER_BOM.md">MASTER_BOM.md</a>.</p></body></html>\n');
write('STARTER_CONNECTIONS.csv',csv([['reference','exact_part','pin_or_logical_contact','net'],...components.flatMap(c => Object.entries(c.pins).map(([pin,net]) => [c.ref,c.part,pin,net]))]));
write('GPIO_ALLOCATION.csv',csv([['gpio','manufacturer_header_pin','signal','connection_status'],...gpio]));
assert(components.find(c => c.ref === 'MOD1') && Object.keys(components.find(c => c.ref === 'MOD1').pins).every(p => p.startsWith('LOGICAL_')));
assert(gpio.every(g => g[0] === 'TBD' && g[1] === 'TBD'));
assert.equal(parts.filter(p => p.block === 'SD_MODULE').length, 1);
assert.equal(parts.find(p => p.block === 'MICROSD').planned_quantity, '1');
assert.equal(parts.find(p => p.block === 'DISPLAY').exact_part, 'B0DFWL25RB');
assert.equal(signals.filter(s => s === 'SD_CS' || s === 'SD_MISO').length, 2);
assert(parts.filter(p => powerDeferred.has(p.block)).every(p => p.planned_quantity.startsWith('0 on main PCB')));
write('VALIDATION.md',`# Design-table validation — revision B\n\nGenerated by \`node KK_main_module/component_review/build_design_tables.mjs\`.\n\nPASS: ${parts.length} BOM rows; ${components.length} unique logical-circuit references; ${endpoints.size} pin/contact records; 17 resistors, 5 capacitors. Referenced local datasheet paths exist. All physical MCU GPIO/header assignments are explicitly withdrawn; MOD1 has logical ports only. MCP23017 has all 28 pins accounted for with GPA7/GPB7 unused. Every connected net has at least two endpoints. Battery, external VBUS and external 5 V nets are absent from the logical circuit. Deferred integrated-power rows have zero main-board quantity.\n\nNOT CHECKED: SuperMini GPIO feasibility, physical module pin mapping, SYS_IN circuit, ERC, SPICE or hardware behavior. This is not a wireable main-board schematic. The previous Waveshare pin-map validation no longer applies. No KiCad schematic or PCB was generated.\n`);
console.log(`Validated and generated ${parts.length} BOM rows, ${components.length} circuit references and ${endpoints.size} pin records.`);
