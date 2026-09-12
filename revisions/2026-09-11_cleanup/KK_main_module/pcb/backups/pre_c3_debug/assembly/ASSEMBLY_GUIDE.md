# Keychain Kreatures C.2 — prototype assembly and bring-up

This guide is for an adult-supervised engineering prototype, not a released student product. Use only the C.2 BOM and root-level one-sheet schematic. The preassembled MCU, display and SD reader are the only surface-mount assemblies students handle; all main-board solder joints are through-hole. No battery, charger or regulator is fitted to this main PCB.

## Before assembly

1. Compare PCB revision, BOM and schematic: **C.2**. Do not mix earlier Q5/Q6 or resistor selections into this board.
2. Print the front and mirrored rear fit/assembly drawings at actual size. Confirm 80 x 100 mm outline with a ruler. A viewer at 67% is not a dimensional check. The user's earlier component fit check is accepted provisionally; check the revised rear placement and assembled height before soldering.
3. Dry-fit sockets and headers. MOD1 uses the supplied 2x9 footprint with 15.24 mm row separation; GPIO13 retains the supplied 0.04 mm pitch offset. Do not force a module or socket into place. Match GPIO names, not an unrelated SuperMini pin-number diagram.
4. Keep the antenna area free of copper additions, battery, wire bundles and metal hardware. The conservative PCB keepouts do not establish the delivered module's RF performance.
5. Check module undersides clear trimmed rear-component leads. Use nonconductive display supports; the header must not take button-press or drop loads. Keep SD insertion/removal accessible. Rear electrolytics are about 11 mm high; the 15 mm bench standoffs are not a finished enclosure design.

## Soldering order

1. Sort the 39 resistors by value with a meter, then populate the back using the by-reference BOM. Form axial leads to 10.16 mm without pulling on the body.
2. Fit D2, small ceramic capacitors, transistor packages and DIP sockets. Keep ICs out of sockets. Solder one pin, check alignment, then finish. Spread TO-92 leads gently from their native pitch to the 2.54 mm footprint using a jig, supporting the lead near the body.
3. Fit rear electrolytics and JST connectors. Check polarity before soldering. Install the front IR components, nine soft buttons and module sockets. The mirrored back drawing is the view while working on that side; do not mirror pin numbering a second time.
4. Trim protruding leads so they cannot touch the display, SD board, MCU or neighboring parts. Inspect both faces for bridges and loose cut leads. Use appropriate ventilation and eye protection.
5. Prepare and electrically check harnesses separately. Fit the mounting hardware, then the ICs and plug-in modules only after the unpowered checks below.

## Parts whose orientation matters

| Part | Required orientation / pin function |
|---|---|
| Q1, Q2 — KSP2222ABU | Pins 1 E, 2 B, 3 C. Match the TO-92 flat face in the assembly drawing. |
| Q3 — BC32725BU | Pins 1 C, 2 B, 3 E. Not interchangeable with Q1/Q2. |
| Q4, Q5 — TN0702N3-G | Pins 1 S, 2 G, 3 D. ESD-sensitive. |
| Q6 — LP0701N3-G | Pins 1 S, 2 G, 3 D. **Pin 1 is ACT_3V2; pin 3 is switched amplifier supply. Do not fit the former BC327.** |
| U1 — MCP23017-E/SP | Pin 1/notch matches the narrow ED281DT socket drawing. |
| U3 — TDA2822L-D08-T | Pin 1/notch matches the ED08DT socket. Neither speaker output is ground. |
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

Label both ends of J4's harness MOTOR and both ends of J5's SPK. Their keyed connectors are physically interchangeable, which is an assembly hazard. Neither the motor return nor either speaker terminal should be assumed to be ground. The 150 mm cut lengths are a bench allowance; final enclosure lengths and the power-board end of J1 are deferred.

## Unpowered inspection

- Confirm resistance checks show no persistent short between GND and any of the three supply rails; capacitor charging can cause a brief meter indication. Check no cross-rail short, especially the isolated MCU-module 3V3 output.
- Check J1 pin numbering against the actual plug. Check Q6 source and drain by continuity to ACT_3V2 and U3 pin 2 respectively.
- Verify all module header pins align, no row is offset by one position, and the MCU 3V3 pin is intentionally not tied to the external 3.3 V rail.
- Check J5 only connects to U3 outputs 1 and 3. Do not attach a grounded oscilloscope probe clip to either speaker pin; use differential measurement or two grounded channels with mathematical subtraction.

## Power and first startup

**Do not connect a raw battery or the old power module to J1. Do not power USB and J1 simultaneously.** The future power module must meet this interface and qualify backfeed, rail sequencing, discharge, off-state behavior and fault protection. None of those upstream functions was implemented in this pass.

| Rail | Nominal / tolerance | Reserved source capacity, not measured consumption |
|---|---|---|
| MCU_5V | 5.0 V +/-5% | 0.6 A |
| LOGIC_3V3 | 3.3 V +/-3% | 0.5 A |
| ACT_3V2 | 3.2 V +/-1% | 0.4 A |

1. For initial flashing, remove the socketed MCU and use its USB port separately. Load a board-specific bring-up program; firmware is not included in this hardware pass.
2. With MCU, display, SD card, speaker and motor disconnected, have an experienced adult check the rails using a current-limited, common-ground, coordinated three-rail bench fixture. Start at low current limits to catch shorts. Avoid leaving connected logic with one rail powered and another off: GPIO back-powering can occur. Disconnect before changing the assembly.
3. Measure the actual rail voltages and confirm amplifier supply stays off with AMP_EN low. Check no reverse voltage appears on an inactive source. Stop for unexplained current, heating or an incorrect rail.
4. Power off, install MCU and modules, then apply the coordinated rails. Increase limits only as needed for measured startup current, within the interface capacities. Monitor dips during Wi-Fi/SD activity. These capacities are provisional requirements for the future power board, not built-in current limiting.
5. Test buttons, display and SD read/write first. Keep R23=100 ohm until the exact screen backlight circuitry/current is measured; do not bridge it for more brightness.
6. Test motor separately with short pulses. Measure ACT_3V2 and Q4 gate voltage, motor terminal voltage and startup current, including simultaneous Wi-Fi/SD activity. Do not sustain a stalled motor. Then test low-volume audio with the motor off.

## Firmware requirements and audio qualification

- MCP23017 address is 0x20. Set output latches to safe states **before** enabling their output directions: GPB4 AMP_EN low, GPB5 MOTOR_EN low, GPB6 display reset as required. Do not configure GPA7/GPB7 as button inputs.
- Audio enable remains active-high. Q5/Q6 now use MOSFET gate drive, reducing calculated steady switch-control current to about 65 microamps. It does not eliminate amplifier quiescent current while enabled.
- Initialize PWM to its midscale silence duty, allow settling, then enable the amplifier and fade in. Fade out before disabling. Test startup/shutdown pops and residual differential DC with the actual speaker. Do not assume a pin at static zero gives pop-free playback through the AC-coupled filter.
- The passive-filter calculation used a 200 kHz PWM carrier, not an arbitrary lower carrier. Confirm achievable PWM resolution, carrier rejection and audible noise on hardware. Start at no more than 50% waveform amplitude; a firmware percentage is not a certified speaker power limit.
- Check U3 supply at audio peaks, Q6 voltage drop/temperature, and C25 charging inrush. LP0701's 2-ohm maximum cited at VGS=-3 V and 150 mA is a 25°C datasheet test point, not a guarantee at every temperature or arbitrary current. The present switch has no dedicated inrush controller.
- The exact FS1511P08-H3.0 continuous-power rating is not documented. Obtain the supplier rating or qualify a documented replacement before setting a production volume limit. Do not infer it from a similar model's datasheet.
- SD: format the selected 32 GB card FAT32; start with conservative SPI clocks and qualify higher speeds while the display is active. Commit saves safely, close files, and test interrupted writes/recovery. SD storage is not executable RAM and does not implement app loading by itself.
- Validate Wi-Fi uploads/trading and RF range with the final shell, display and battery placement. Keep a recovery programming path through the removable MCU.

## Prototype acceptance record

Record serial number, module markings, rail currents/voltages, button results, display/backlight current, SD write/read checksum, Wi-Fi transfer/range, IR transmit/receive, motor startup, audio noise/clipping/DC/pops, and temperatures. Test cold starts and repeated power cycles before unattended operation. Bench qualification, safe power-module integration, enclosure retention/drop testing and applicable toy/EMC compliance are prerequisites for any student/product release; a clean PCB DRC does not perform those tests.
