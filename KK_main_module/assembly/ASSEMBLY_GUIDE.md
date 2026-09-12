# HISTORICAL C.5 — do not use for current assembly

Superseded by [C.6 flat-part assembly/wiring](../C6_flat_stack/assembly/ASSEMBLY_GUIDE.md). The upright-resistor instructions and old outline below apply ONLY to the preserved C.5 baseline.

The following C.5 instructions supersede old C.4 positions, fit sheets and front/back assignments. Use only the C.5 board and BOM together.

- Board is **84 × 95 × 1.6 mm**, rounded corners. Screen is landscape on the front; D-pad left, four actions right and one mode button in the center, all below the screen.
- **Rear:** ESP32 socket, SD socket, IR emitter/receiver, DIP sockets, power/motor/speaker JSTs and supporting circuitry. **Front:** screen socket, nine soft buttons and socketed RGB. Passives and small transistors are soldered.
- ESP32 antenna points to the top; its USB faces the board interior. Service it with the rear cover removed or the module unplugged. Keep metal and wiring away from the marked antenna area on both sides.
- IR D1 is the same TSAL6200, but its leads are formed so the lens points toward the top edge, alongside U2. Proposed optical-axis height is 5 mm off the rear surface. Do not bend immediately at the epoxy or reverse the cathode/anode; use the pin-1 mark and meter check. Physical qualification is pending.
- Upright resistors use **2.54 mm hole pitch**, not the old 10.16 mm flat footprint. Form them with a jig, insulate the return lead if necessary, and inspect for shorts before power. No resistor value or MPN changed. Upright references: **R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R20, R22, R26, R29, R41, R42, R43**.
- Trim rear-component leads before fitting the screen. Check clearance under both screen and socketed modules. Support the display's free edge with shell features/spacers; the single socket must not take button or drop loads.
- SD insertion is toward the right edge as viewed from the front (left when looking at the rear). Keep the card/eject path clear. Use the socket, not soldered permanent module pins.
- RGB socket grip on the actual LED leads remains unqualified. Do not tin pins to force a fit. Its proposed front height is 22.1 mm; combined front/back components can require about **39 mm depth before shell clearance**.
- J1 requires coordinated **5 V / GND / 3.3 V / 3.2 V**, not raw battery power. Never assume the unfinished power module or simultaneous module USB is safe.
- Pin-1 squares, polarity marks and front/back fit sheets govern orientation. Some legends are beneath installed parts and are meant to be read during assembly. Bare test holes must not be populated with posts beneath opposite-side assemblies.
- Physical fit, powered bring-up, audio limits, firmware, optical windows, enclosure and battery are not qualified by the PCB checks. See [circuit review](../C5_relayout/CIRCUIT_REVIEW.md) and fill in the bench record with real measurements.

---

## Soldering order

1. Sort all 43 resistors with a meter. Populate flat resistors and D2 first, then ceramics and empty DIP sockets.
2. Populate the marked upright resistors and small transistors using their correct lead forms; do not confuse the two resistor pitches.
3. Fit rear electrolytics, JSTs and module sockets, followed by rear IR parts and front screen/RGB sockets and buttons. Check alignment after soldering one pin.
4. Trim and inspect both faces. Perform the unpowered continuity/polarity checks before inserting ICs, modules or the RGB LED.
5. Attach separately checked harnesses and mechanical supports, then proceed through the current-limited bring-up gates.

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

These are the prior main-board source reservations, not measured requirements. The added RGB circuit requires up to approximately 31 mA on 5 V at nominal default full-white current, plus driver logic current on 3.3 V. Reserve an additional 50 mA on 5 V and 20 mA on 3.3 V provisionally when designing the future power module; verify the combined peak and transient budget on hardware.

1. For initial flashing, remove the socketed MCU and use its USB port separately. Load a board-specific bring-up program; firmware is not included in this hardware pass.
2. With MCU, display, SD card, speaker and motor disconnected, have an experienced adult check the rails using a current-limited, common-ground, coordinated three-rail bench fixture. Start at low current limits to catch shorts. Avoid leaving connected logic with one rail powered and another off: GPIO back-powering can occur. Disconnect before changing the assembly.
3. Measure the actual rail voltages and confirm amplifier supply stays off with AMP_EN low. Check no reverse voltage appears on an inactive source. Stop for unexplained current, heating or an incorrect rail.
4. Power off, install MCU and modules, then apply the coordinated rails. Increase limits only as needed for measured startup current, within the interface capacities. Monitor dips during Wi-Fi/SD activity. These capacities are provisional requirements for the future power board, not built-in current limiting.
5. Test buttons, display and SD read/write first. Keep R23=100 ohm until the exact screen backlight circuitry/current is measured; do not bridge it for more brightness.
6. Test motor separately with short pulses. Measure ACT_3V2 and Q4 gate voltage, motor terminal voltage and startup current, including simultaneous Wi-Fi/SD activity. Do not sustain a stalled motor. Then test low-volume audio with the motor off.

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

The 3D render now includes D3, its socket and formed leads, all DIP chips/sockets, the modules and every fitted electrical position. These are nominal models: they do not prove module/wire clearance. Print the fit sheets and check the actual LED, socket, display underside and JST plugs before soldering. Record all physical tests in [C5_BENCH_TEST_RECORD.csv](C5_BENCH_TEST_RECORD.csv).

## C.5 removable RGB and 3D fit checks

Fit the PPTC041LFBN-RC socket at D3 before inserting the LED. Socket pin 1 is the square PCB pad (lower end of the vertical four-pin row); LED pin order remains 1 red cathode, 2 common anode, 3 blue cathode, 4 green cathode. Form the LED to 2.54 mm lead pitch with an adult-prepared fixture, preserving a straight section next to the body. Do not force it into the socket, tin the mating portions, or rely on friction without a sample test. The selected socket's housing/PCB footprint is checked, but its contact retention with the exact LED lead tolerance is not yet qualified. Reject loose or oversized combinations; resolve before releasing kits.

The nominal RGB model uses an 8.5 mm socket plus a 5 mm formed-lead standoff and 8.6 mm lens: approximately 22.1 mm above the front PCB surface. This is an assembly proposal, not a measured stack. The MCU/screen/SD models include socket and male-header heights; their module dimensions/header offsets remain provisional. Check the actual stack and lead trimming before modeling a close-fitting shell. The LED socket courtyard represents its board-level housing; the elevated lens/formed-lead envelope is shown in 3D/F.Fab and must also be checked.
