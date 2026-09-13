# Main C.6 — prototype assembly and wiring

Use ONLY C.6 CAD/BOM/Gerbers with P.3 power. Both boards are 96 x 105 x 1.6 mm, R4 corners, four 2.2 mm mounting holes. Main is two-layer through-hole student assembly; power is a separately factory-assembled four-layer SMT board. These five samples are for adult-supervised engineering qualification, not finished toys.

## Flat parts and assembly order

1. Dry-fit the actual socketed ESP32, landscape screen, SD module, RGB, switches and plugged JSTs on the actual-size drawings. Print at 100% and measure the calibration line. Seller module revisions and socket retention remain unqualified.
2. Fit ALL R1-R43 horizontally, 10.16 mm pitch. No upright resistors. Fit flat axial D2, ceramic capacitors and empty DIP sockets; verify values before soldering.
3. Form Q1-Q6 to the flat-body outlines, marked flat face up, preserving numbered leads; support leads near the body. Do not swap Q6 LP0701N3-G for BC327.
4. Mount C1/C3/C5/C13/C17/C25 (ECEA1CKA101, 100uF/16V) and C9/C11/C15/C21 (ECEA1CKA100, 10uF/16V) horizontally on 0.5 mm insulating support. Maximum heights including support are 7.3 and 5.0 mm respectively. Full maximum can length is 8 mm. Pad1 positive, striped negative lead pad2. The 10uF part's native 1.5 mm leads must be formed to 2.54 mm; 100uF uses 2.5 mm. Support at the seal; do not cross, twist or pull leads or block the pressure vent.
5. Fit rear JSTs/module sockets, IR emitter D1 and receiver U2 facing the top case window, then front screen/RGB sockets and nine soft switches. Tack one pin and check alignment before completing. IR optics, buttons, connectors and sockets retain functional height; do not flatten them.
6. Trim solder tails to <=2.5 mm and inspect both sides before inserting modules/chips. Debug holes are bare probe points, not tall headers beneath opposite-side parts. Support the display's free edge mechanically.
7. For the first removable stack mock-up, use four 20 mm M2 insulating standoffs between PCB faces. Main display/buttons face front; power component side faces rear cover. Power front-view X is mirrored relative to main front in the assembled stack. Verify plugged connector/wire bends; 20 mm is NOT approved final spacing. Main ESP32 rear envelope is about 15.3 mm; front RGB remains about 22.1 mm. Battery and complete case depth are not frozen.

Keep the marked antenna region free of metal, battery, hardware and loose wiring. Unscrew/unplug the power board for access to main-board solder joints and sockets. Use insulating barriers and strain relief; do not press a cell against solder tails.

## Parts whose orientation matters

| Part | Required orientation / pin function |
|---|---|
| Q1, Q2 — KSP2222ABU | Pins 1 E, 2 B, 3 C. Match the TO-92 flat face in the assembly drawing. |
| Q3 — BC32725BU | Pins 1 C, 2 B, 3 E. Not interchangeable with Q1/Q2. |
| Q4, Q5 — TN0702N3-G | Pins 1 S, 2 G, 3 D. ESD-sensitive. |
| Q6 — LP0701N3-G | Pins 1 S, 2 G, 3 D. **Pin 1 is ACT_3V2; pin 3 is switched amplifier supply. Do not fit the former BC327.** |
| U1 — MCP23017-E/SP | Pin 1/notch matches the narrow ED281DT socket drawing. |
| U3 — TDA2822L-D08-T | Pin 1/notch matches the ED08DT socket. Neither speaker output is ground. |
| U4 — TLC5916IN | Back-side ED16DT socket; match notch/pin-1 dot, not an unmirrored front view. Pin 1 GND; pin 16 3.3 V. |
| D3 — WP154A4SEJ3VBDZGW/CA | Front, in PPTC041LFBN-RC socket: 1 red cathode, 2 common anode (+5 V), 3 blue cathode, 4 green cathode. Form native 1.27 mm leads to the footprint's 2.54 mm pitch using a fixture; support leads near the body. Dry-fit a sample without forcing it. |
| Polarized capacitors | Pad 1 positive, pad 2 negative. C21 positive goes to U3 pin 8; its negative goes to pin 5, not ground. |
| D2 — 1N5819 | Banded cathode at pad 1 / ACT_3V2; anode at pad 2 / motor return. |
| D1 — TSAL6200 | Pad 1 cathode; pad 2 anode. Confirm lead/flat markings against the drawing. |
| U2 — TSOP38238 | Pins 1 OUT, 2 GND, 3 VS; lens faces the direction in the assembly drawing. |
| Buttons | A/B are one internally connected pair; C/D are the other. Confirm a sample with a continuity meter. |

## Connectors and harnesses

Read pin numbers on the PCB/assembly drawing, not left/right from a cable photograph. Verify each finished harness with a continuity meter; wire color is only a secondary aid.

| Connector | Pinout | Mating parts |
|---|---|---|
| J1 — SYS_IN | 1 MCU_5V; 2 GND; 3 LOGIC_3V3; 4 ACT_3V2 | XHP-4 housing + 4 SXH-001T-P0.6 contacts |
| J2 — screen | 1 GND; 2 3.3V; 3 SCK; 4 MOSI; 5 RESET; 6 DC; 7 CS; 8 BLK | Already-counted PPTC081LFBN-RC female socket; module's male strip |
| J3 — SD | 1 3.3V; 2 CS; 3 MOSI; 4 SCK; 5 MISO; 6 GND | Already-counted PPTC061LFBN-RC female socket; module's male strip |
| J4 — MOTOR | 1 ACT_3V2; 2 switched motor return | PHR-2 + 2 SPH-002T-P0.5S contacts on added 24-AWG pigtails |
| J5 — SPK | 1 amplifier OUT1; 2 amplifier OUT2 | PHR-2 + 2 SPH-002T-P0.5S contacts on added 24-AWG pigtails |

Use Alpha 3050 stranded 24-AWG cut stock for the added pigtails and J1 lead. Its nominal insulation OD is 1.42 mm, within the selected PH and XH contact ranges. Have a qualified assembler make the crimps and pull-test them. **The motor's fine AWG32 wires must not be crimped into those larger pigtail terminals.** The prototype harness instead uses short, individually insulated splices between the supplied actuator leads and the pigtails. Verify sleeve coverage over each joint and insulation at both ends; provide separate strain relief so no pull reaches motor/speaker terminals. Never tin wire before crimping or use solder as a substitute for a sound crimp.

Label both ends of J4's harness MOTOR and both ends of J5's SPK. Their keyed connectors are physically interchangeable, which is an assembly hazard. Neither the motor return nor either speaker terminal should be assumed to be ground. The 150 mm cut lengths are a bench allowance; both power J3 and main J1 now use XHP-4 housings. Use eight XH contacts for the complete pin-for-pin harness; final lengths depend on the shell.

## Unpowered inspection

- Confirm resistance checks show no persistent short between GND and any of the three supply rails; capacitor charging can cause a brief meter indication. Check no cross-rail short, especially the isolated MCU-module 3V3 output.
- Check J1 pin numbering against the actual plug. Check Q6 source and drain by continuity to ACT_3V2 and U3 pin 2 respectively.
- Verify all module header pins align, no row is offset by one position, and the MCU 3V3 pin is intentionally not tied to the external 3.3 V rail.
- Check J5 only connects to U3 outputs 1 and 3. Do not attach a grounded oscilloscope probe clip to either speaker pin; use differential measurement or two grounded channels with mathematical subtraction.

## First power and integrated testing

Read the accompanying P3_REVIEW_AND_TEST.md before connecting anything. First qualify the power board alone with current-limited equipment and dummy loads; battery selection remains open. Main J1 is NOT a raw battery input. Do not combine ESP32 USB power and external SYS_IN until exact-module backfeed behavior is proven. Program the removable MCU separately for recovery; Wi-Fi app/game loading requires firmware not provided here.

Power J3 -> main J1: 1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2, pin-for-pin. The charger USB-C carries no data to main. Do not assume the two physically compatible speaker/motor plugs are interchangeable electrically.

P.3 screening load targets are 5 V/0.6 A, 3.3 V/0.4 A and 3.2 V/0.5 A; none is a measured rating. Older main-board reservations included 0.5 A on 3.3 V and additional RGB allowance. Those reservations were estimates, not measurements: the integrated peak budget remains an explicit bench qualification item. Do not silently treat a 0.4 A screening result as proof of a 0.5 A logic requirement. Test combined Wi-Fi, SD, RGB, IR, audio and motor peaks and adjust the design if capacity is insufficient.

Start with socketed loads and actuators disconnected. Check short circuits, pin polarity, rail nominal values, disabled amplifier/motor and unexpected current. Power OFF before changing connections. Scope rail rise/fall and GPIO back-powering before attaching all logic. Increase current limits only as justified by measured startup; stop for heat, oscillation or incorrect rails. R23 stays 100 ohm until the exact display backlight current is measured. Test motor short pulses without stalling, then audio at low volume; neither speaker output is ground. Record results for each sample.

## Firmware requirements and audio qualification

- MCP23017 address is 0x20. Set output latches to safe states **before** enabling their output directions: GPB4 AMP_EN low, GPB5 MOTOR_EN low, GPB6 display reset as required; GPA7 RGB_OE_N high. Do not configure GPA7/GPB7 as button inputs.
- Audio enable remains active-high. Q5/Q6 now use MOSFET gate drive, reducing calculated steady switch-control current to about 65 microamps. It does not eliminate amplifier quiescent current while enabled.
- Initialize PWM to its midscale silence duty, allow settling, then enable the amplifier and fade in. Fade out before disabling. Test startup/shutdown pops and residual differential DC with the actual speaker. Do not assume a pin at static zero gives pop-free playback through the AC-coupled filter.
- The passive-filter calculation used a 200 kHz PWM carrier, not an arbitrary lower carrier. Confirm achievable PWM resolution, carrier rejection and audible noise on hardware. Start at no more than 50% waveform amplitude; a firmware percentage is not a certified speaker power limit.
- Check U3 supply at audio peaks, Q6 voltage drop/temperature, and C25 charging inrush. LP0701's 2-ohm maximum cited at VGS=-3 V and 150 mA is a 25°C datasheet test point, not a guarantee at every temperature or arbitrary current. The present switch has no dedicated inrush controller.
- The exact FS1511P08-H3.0 continuous-power rating is not documented. Obtain the supplier rating or qualify a documented replacement before setting a production volume limit. Do not infer it from a similar model's datasheet.
- SD: format the selected 32 GB card FAT32; start with conservative SPI clocks and qualify higher speeds while the display is active. Commit saves safely, close files, and test interrupted writes/recovery. SD storage is not executable RAM and does not implement app loading by itself.
- Validate Wi-Fi uploads/trading and RF range with the final shell, display and battery placement. Keep a recovery programming path through the removable MCU.

## Prototype acceptance record

Record serial number, module markings, rail currents/voltages, button results, display/backlight current, SD write/read checksum, Wi-Fi transfer/range, IR transmit/receive, motor startup, audio noise/clipping/DC/pops, and temperatures. Test cold starts and repeated power cycles before unattended operation. Bench qualification, safe power-module integration, enclosure retention/drop testing and applicable toy/EMC compliance are prerequisites for any student/product release; a clean PCB DRC does not perform those tests.

## RGB wiring and safe firmware initialization

U1 GPA4 → U4 SDI (pin 2), GPA5 → CLK (3), GPA6 → LE (4), GPA7 → OE_N (13). U4 OUT0 (5) drives D3 red, OUT1 (6) green, OUT2 (7) blue; OUT3–7 and SDO are unused. The common anode is 5 V; logic is 3.3 V. Do not drive the LED directly from MCP23017 pins.

1. Preserve button states/directions and all unrelated expander bits. Write GPA7 high and GPA4–6 low to the output latch before making GPA4–7 outputs. R41 blanks OE_N at boot; R42/R43 define SDI/CLK, and LE has the driver's internal pull-down.
2. In normal mode, keep LE low, shift eight zero bits into SDI on CLK rising edges, then pulse LE high and return it low with CLK stationary. Keep OE_N high throughout initialization, then lower it to display the latched value. Do not unintentionally clock the special-mode OE/LE entry sequence.
3. For normal eight-bit writes, shift bit 7 first; bit 0 controls OUT0/red, bit 1 OUT1/green, bit 2 OUT2/blue. Latch after each complete byte. Always keep bits 3–7 zero. Verify red/green/blue individually at first startup before displaying mixed colors.
4. R40=1.8 kΩ sets nominal default channel current around 10.4 mA (about 31 mA total for white). Confirm actual current and LED/driver temperature. The TLC5916 supports global current-gain adjustment and a low-current range; this is not independent hardware PWM for each color. Basic seven-color states are available; smooth per-color fades need additional firmware timing design. Color balance is not calibrated.
5. Verify cold start, processor reset and expander reset produce no unintended light; verify commanded OFF and sleep current. Probe U4 pin 16 (3.3 V), D3 pin 2 (5 V), R40 and U4 control pins with insulated fine probes and power off before attaching clips. Never short adjacent DIP pins.

