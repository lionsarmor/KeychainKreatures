# Power P.4 — troubleshooting and factory-return guide

For the compact **50 × 50 mm, four-layer** Keychain Kreatures power module, paired with C.6 main. Guide version 1, 2026-09-12. Work from the first failed stage, not from a guessed bad component.

**Students begin with identification and unpowered inspection. All powered power-module tests are instructor/qualified-technician work.** Students may observe and record results. This board contains fine-pitch surface-mount parts and lithium-battery charging/protection circuitry; it is not the student through-hole soldering exercise.

This is a proposed test procedure for engineering samples, not a record of completed testing or a battery-safety certification. If the required equipment or qualified supervision is missing, mark the test **BLOCKED** and ask the factory to perform it.

## 1. What should a factory-delivered board do?

| Delivered item | Correct expectation |
|---|---|
| Bare P.4 PCB | Cannot regulate or charge until its parts are assembled. Do not connect power. |
| Factory-assembled P.4 | Can be tested independently with the approved fixture. It does not need ESP32 firmware. |
| P.4 without a battery/thermistor | Not a complete rechargeable product. Missing charge indications do not by themselves prove failure. |
| P.4 attached to a blank main board | Does not create game software or prove the main is assembled correctly. |

There are 108 fitted electrical positions and 28 rear bare test pads. The four mounting holes do **not** align with main C.6. Use independent supports; do not force a common four-standoff stack. Some inherited BOM value text says `C.5 SYS_IN / XH`; J3's actual four-wire interface remains the one below. Identify the power revision from the PCB/title and current release files, not that inherited connector description.

Before rework, collect photographs, serial/lot numbers, factory inspection/X-ray reports, approved BOM substitutions and bare-board electrical-test results. Preserve one untouched failing unit when possible. “DRC passed” means the design files passed the reported CAD checks; it does not mean every fabricated joint and IC works.

## 2. Stop conditions and prohibited shortcuts

Stop for smoke, unusual smell, rapid temperature rise, reversed polarity, swelling/leaking cell, oscillating startup or unexplained current limiting. Turn off external supplies if safe and alert the instructor. Do not touch hot parts, move a damaged cell by hand or continue cycling power. Follow the lab's emergency procedure.

- Never short or jumper a fuse, protection FET, eFuse, rail gate, regulator enable or thermistor input to make the board start.
- Never replace F1 with a higher rating, bypass the USB current limiter, or substitute a “similar” charging IC without design review.
- Never connect an unspecified battery. The eventual pack is conventional **1S, 4.2 V maximum** Li-ion/LiPo; chemistry, current, temperature limits, connector polarity and protection coordination still need approval.
- Never place a multimeter in A/mA mode directly across a rail or cell. Never short a real cell for a protection test.
- Never connect external sources to J3 outputs. J3 is an **output**, not a battery or USB input.
- Never plug ESP32 USB in while the main receives this board's external rails.
- Never lift equipment protective earth to solve a grounding problem. Use the right isolated/floating fixture and rated measurement equipment.
- No student hot-air rework of QFN/WCSP packages. Preserve factory return evidence before any technician repair.

## 3. The two returns: the most important wiring rule

**J2 pin 2 / TP3 is BAT_NEG. J3 pin 2 / J4 pin 2 / TP4 is system GND. They are different nets.** The protection FETs control the connection between them. An external wire or test-equipment earth connection between them can bypass protection.

A small voltage difference or low resistance between BAT_NEG and GND does **not** automatically prove a solder bridge: the protection FETs may be conducting normally, and meter polarity can affect semiconductor readings. Never demand an open-circuit reading in every operating state. The technician must distinguish intended conduction through Q1–Q3 from an unintended copper/solder/fixture bypass, using the schematic and controlled emulator tests.

Before power, draw the grounding of the **source, oscilloscope, electronic load, USB host, USB meter and computer-connected instruments**. If the source's negative terminal at BAT_NEG is tied to earth and a scope/load ties GND to earth, the protection is bypassed. Use a verified floating source/fixture or appropriately isolated measurements that do not create this return connection. A battery-powered meter can also become grounded through its USB logging cable. Do not assume “USB disconnected from main” eliminates every earth path.

System rail measurements below use **TP4 GND** unless explicitly stated otherwise. Cell-side voltage is measured across **J2 pin 1 and J2 pin 2**. Do not move a ground clip between those domains while powered.

## 4. Equipment and record keeping

Unpowered student station: printed current drawings, magnifier, nonconductive holder and supervised multimeter. Black lead in COM, red in V/Ω. Continuity/resistance only with all sources disconnected and capacitors discharged; verify the meter on shorted/separated probes first. A brief rail beep can be capacitor charging. Record settled resistance and probe direction rather than inventing one pass/fail resistance for all circuits.

Instructor powered station: current-limited, correctly isolated battery simulator; voltage/current readback; approved load fixture; fine insulated test clips; temperature measurement; scope/differential measurement; verified USB-C advertisement/source fixtures and cables. For **charging while a battery emulator is connected**, the emulator must be **sink-capable/bidirectional** and configured for the expected current. An ordinary bench supply generally cannot absorb charging current and is not acceptable in that state.

Keep the real cell and populated main disconnected until their prerequisite checks pass. Use the actual Semitec 103AT-2 in the bench fixture as appropriate; real-cell work requires a bonded, electrically insulated sensor on the selected cell. A loose sensor on the bench does not protect a real battery's temperature.

Record board serial, lot, setup photograph, equipment model, isolation arrangement, current limits, ambient temperature, load conditions, probe reference and actual readings. PASS means a performed test met its stated criterion. FAIL means an observed mismatch. BLOCKED means equipment/approved limits are missing. NOT RUN is not PASS.

## 5. P1 — unpowered incoming inspection

Check the 50 × 50 mm/R3 outline, four 2.2 mm mounting holes, intact board edges and P.4 revision. Inspect USB shell anchors, connector latches, switch and both copper faces. Look for missing components, wrong orientation, displaced tiny parts, solder beads, damaged pads or scratches. Use the [reference BOM/placement](../release_checks/BOM_AND_PLACEMENT.csv) and [schematic](SCHEMATIC.pdf), not an older revision's coordinates.

The assembler must confirm these particularly important parts, not just that a package fits:

| Position | Required part / reason to check |
|---|---|
| U1 | **BQ24075TRGTR** charger; the T variant matters. |
| U13 | **TPS22950YBHR**, base variant, 0.4 mm WCSP; C/L variants are not automatic substitutes. |
| U2 and Q1–Q3 | DW01A and three FS8205 banks; protection pinout/orientation matters. |
| U4 | TPS259530 eFuse and its programming resistors. |
| U5–U7 | TPS63060 regulators; L1–L3 and feedback/output capacitors must match the BOM. |
| U8–U10 / U11 / U12 | Output gates / buffer / independent voltage supervisor. Do not omit them to get output. |
| F1 | 4 A fast fuse, exact BOM part; do not bridge it. |
| J2/J3/J4 | Battery VH / four-wire XH / thermistor PH families; polarity is not guaranteed by wire color. |

Confirm the factory approved **filled, capped, planarized via-in-pad**, fine-pitch assembly and hidden-joint inspection. Ordinary tenting is not equivalent. The release lists 74 via centers inside SMD pads; partial overlaps also need review. Hidden WCSP/QFN joints cannot be cleared by looking only at the board's top. If assembly process or part substitution is undocumented, hold powered testing and obtain the factory response.

## 6. P2 — verify the connectors and fuse without power

| Connector | Exact numbered functions |
|---|---|
| J1 USB-C | Charging input only. D+/D− and SBU are intentionally not connected. |
| J2 battery, VH | 1 CELL_PLUS; 2 BAT_NEG. |
| J3 to main, XH | 1 MCU_5V; 2 GND; 3 LOGIC_3V3; 4 ACT_3V2. |
| J4 thermistor, PH | 1 NTC; 2 GND. |

Check the disconnected four-wire harness end-to-end: power J3 1→main J1 1, 2→2, 3→3, 4→4; no cross-connections. Inspect crimps and gently flex the disconnected harness during continuity testing. Verify battery-harness polarity independently before any future cell connection. Connector mirroring in rear drawings is a common source of mistakes.

Technician: check F1 end-to-end for continuity using its identified pads and compare the meter's lead resistance. An open fuse is a **symptom**; determine the reason before replacing it. Confirm J2 pin 1 reaches F1's CELL_PLUS side and the other side reaches VBAT/TP2. Check VBUS, SYS_RAW, SYS_SW and all six pre-/post-gate rails for unresolved short indications to system GND and one another. Compare only with a verified board in the same unpowered state. Do not bypass protection to make a continuity test simpler.

**Pass:** correct mapping, no physical damage or unexplained short, fuse intact, approved test fixture grounding. Otherwise stop at this stage.

## 7. Understand the stages before chasing an output

| Stage | Function and accessible checkpoints |
|---|---|
| Cell path | J2 → F1 → VBAT TP2 → charger power path → SYS_RAW TP5; low-side protection is U2/Q1–Q3. |
| USB path | J1 → VBUS TP1 → U13 current limiter → USB_CHG TP22 → U1 → SYS_RAW TP5. U14/U3/Q4/Q5 select the permitted input-current mode. |
| User switch / eFuse | SW1/RUN_CTL TP7 and U4 create SYS_SW TP6 from SYS_RAW. |
| Regulation | U5/U6/U7 produce REG_5V TP13, REG_3V3 TP14 and REG_3V2 TP15. |
| Supervision | U12 evaluates the rails; VOLTAGES_OK TP28 → U11 → RAILS_EN TP12. PG_ALL TP11 is a separate regulator-status node. |
| Gated outputs | U8/U9/U10 → MCU_5V TP16, LOGIC_3V3 TP17, ACT_3V2 TP18 → J3. |

When all outputs disappear together, first check shared upstream power and supervision. Do not assume three regulators independently failed. Never jump across a gate or pull its enable high to defeat a failed prerequisite.

## 8. P3 — battery-simulator startup, USB disconnected

Instructor only. Disconnect main J3, USB J1 and any real battery. Connect the reviewed floating current-limited simulator to **J2 positive pin 1, negative pin 2**. Confirm the voltage at the disconnected fixture plug before inserting it. Start at **3.7 V with SW1 OFF** and an initial current limit around **50 mA**, as in the existing review procedure. This is a cautious off-state inspection setting, **not** a claim that an enabled three-regulator board will start at 50 mA.

Measure and record off-state input current. There is no validated quiescent-current acceptance number yet; compare with approved calculations/verified samples and investigate unexpected current or heat. USB status LEDs may be dark during battery-only operation. Check cell-side voltage, then the protected system path with the correct reference. If protection is latched, follow the selected protection devices' documented recovery sequence using the qualified fixture; do not bypass them.

Switch off the fixture before moving clips. The instructor then selects a bounded startup current limit justified by expected no-load inrush and equipment limits, records it, and enables the board. Increase only after determining that current limiting—not a short—is preventing startup. Watch voltage and current together; repeatedly increasing the limit is not troubleshooting.

### Locate the first missing stage

| Probe, relative to TP4 | Expected qualitative state with a valid 3.7 V source and SW1 ON | If not present |
|---|---|---|
| TP2 VBAT | Battery-derived voltage when the protected return conducts; compare with cell-side measurement. | Check simulator, F1 and protection/return path; do not assume GND=BAT_NEG. |
| TP5 SYS_RAW | Battery-derived system supply, allowing power-path drop. | U1 power path, source/protection and assembly. |
| TP7 RUN_CTL | Close to SYS_RAW when ON; near GND when OFF. | SW1 mapping/joints and control path. |
| TP6 SYS_SW | Close to SYS_RAW after valid enable/UVLO and ramp. | U4, UVLO/divider, load fault or source sag. |
| TP13 / TP14 / TP15 | Approximately 5.0 / 3.3 / 3.2 V after startup. | Corresponding U5/U6/U7, shared REG_ENABLE, inductor, feedback/output path. |
| TP28 VOLTAGES_OK | High near REG_3V3 after required rails are valid and supervisor delay. | Find the rail below threshold, sensing network, U12 supply/reset or fault. |
| TP12 RAILS_EN | Follows a valid high through U11. | Check U11 supply and signal path; do not force it. |
| TP16 / TP17 / TP18 | Approximately 5.0 / 3.3 / 3.2 V at the gated outputs. | Compare pre-gate rail and enable, then U8/U9/U10 or downstream short. |

TP11 PG_ALL is pulled toward REG_3V3 when the tied regulator status outputs release it. A low value while a regulator is starting is not surprising; a high does **not** substitute for measuring all rails or the independent supervisor. State timing and scope capture matter.

These are steady-state diagnostic expectations, not permission to force power onto an unpowered control pin. Probe small IC pins only if a dedicated pad is insufficient and the technician has a safe method. Do not probe regulator switch-node/inductor pads casually; a slip there can destroy the converter.

## 9. P4 — qualify the outputs with no main attached

Measure each pre-gate rail, post-gate rail and J3 pin under the same settled condition. A correct test pad but bad connector pin points toward an open pad/trace/joint. Correct pre-gate voltage and missing post-gate voltage points toward gating, enable or a downstream load, not automatically the regulator.

| Rail | Nominal | Initial investigation window |
|---|---|---|
| REG_5V / MCU_5V | 5.0 V | 4.75–5.25 V. |
| REG_3V3 / LOGIC_3V3 | 3.3 V | 3.135–3.465 V. |
| REG_3V2 / ACT_3V2 | 3.2 V | 3.04–3.30 V. |

These windows are conservative prototype checks, **not qualified production limits**. ACT_3V2's upper bound is deliberately below +5%; reject unexplained excursions above the design's 3.3 V target ceiling before connecting main loads. Scope startup, shutdown and load transitions: a meter can miss dangerous spikes or short dropouts. Do not approve ripple or temperatures without defining limits for the actual attached components.

The calculated supervisor low thresholds are approximately 4.64 / 3.06 / 3.00 V. Therefore, “VOLTAGES_OK high” does **not** mean the rails meet the tighter investigation windows. A supervisor fault may correctly turn off all outputs when only one rail is low.

Switch OFF and check outputs decay without remaining powered by the load fixture. Record decay time and any residual voltage; an unloaded high-impedance meter can show leakage/charge. Do not use a wire to pull it down. Confirm the no-backfeed fixture state before declaring a gate stuck on.

## 10. P5 — controlled loads and low-voltage behavior

Instructor only, with correctly referenced rated loads and temperature measurement. Keep main and the real cell disconnected. Begin at no load, increase **one rail at a time** in reviewed steps, then test combined loads only after individual results are acceptable. Do not connect an earth-referenced electronic load in a way that bypasses BAT_NEG protection. Resistor loads can become burn hazards; calculate power rating and provide safe mounting if used.

The design's unvalidated screening targets are **5 V at 0.6 A, 3.3 V at 0.4 A and 3.2 V at 0.5 A**. They are not guaranteed delivered ratings. Record actual load/current, cell-side input power, rail minima/maxima, ambient and component temperatures at each step. Stop on unexpected heat, oscillation, current limit or rail excursions. Establish acceptable temperatures from component ratings and the intended enclosure/ambient before a prolonged run; “comfortable to touch” is not a thermal qualification.

Using the simulator, check startup/shutdown and a controlled voltage ramp around the system cutoff. Calculated SYS_RAW eFuse UVLO is about **3.38 V rising / 3.10 V falling**, with tolerances and source sag. It is not a fixed guaranteed trip at the cell connector. Record the observed SYS_RAW thresholds, recovery and hysteresis. Do not deliberately overdischarge a real cell to perform this test.

Hard shorts, fuse opening and protection-trip validation require a separately approved technician test fixture/procedure and emulator. They are **not student exercises** and not accomplished by touching output pins together. Do not intentionally blow F1 as a routine incoming test. If fault-injection equipment or safe test limits are unavailable, record BLOCKED and obtain factory/design-lab testing.

Main's historical 3.3 V reservation was 0.5 A; this power screening used 0.4 A. Resolve actual combined peak demand and margin before approving integration. A failure at an unqualified combined load may expose a design limit, not a manufacturing defect.

## 11. P6 — USB input and current selection

Instructor only. First remove the non-sinking ordinary supply, if one was used for battery-only checks. Any emulator remaining at J2 during charging must absorb the charge current safely. Keep main disconnected. Use verified sources/cables and measure total USB input current with a reviewed fixture; an inline USB meter that changes CC behavior can invalidate the test.

Check TP1 VBUS for nominal 5 V when a compatible source is attached. Check TP25 CC_3V3 near 3.3 V, then TP22 USB_CHG. Voltage absent at TP1 suggests cable/source/connector; present at TP1 but absent at TP22 suggests U13, current-limit/fault conditions or a short downstream. A valid USB input does not guarantee the three toy outputs are on.

| Verified source advertisement | TP20 CC_DEFAULT_N | TP21 USB_HIGH_CURRENT | Interpretation |
|---|---|---|---|
| USB-A/default or USB-C default | High near CC_3V3 | Low | Default low-current path intended. |
| USB-C advertising 1.5 A or 3 A | Low | High near CC_3V3 | Higher-current path permitted by this design. |
| No USB source | CC supply may be absent | Not a meaningful normal logic test | Do not demand powered logic levels. |

This follows TUSB320 GPIO OUT1 and the Q4 inverter in the current netlist. The design does not distinguish 1.5 A from 3 A for its mode selection. A source's advertisement is an available limit, not the current the board must draw. See [TI's TUSB320 GPIO truth table](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf).

The default limiter is calculated near **50 mA**, with a datasheet screening range of roughly **34–66 mA**, plus upstream consumption and resistor tolerance. A USB-A connection may charge very slowly or fail to sustain a running toy; that behavior is not automatically a broken charger. This design has no USB enumeration, suspend detection or BC1.2 negotiation; do not claim universal computer-port compliance. Initial fault investigation should use controlled test sources, not risk a student's laptop port.

On a suitable USB-C source, U1's programmed input limit is approximately 1.23 A, screened up to about 1.32 A. This is not the battery charge current. A 3 A charger does not command 3 A charging. Check default, 1.5 A and 3 A advertised modes, both cable orientations, attach/unplug, weak-source behavior and switchover, recording overshoot/current. Do not force the higher-current mode when a source advertises only default current.

## 12. P7 — charging and the temperature sensor

Use a correctly configured sink-capable battery emulator and known sensor/test fixture, or a **previously approved** cell with its bonded/insulated sensor. No battery has been finalized by this hardware release. Charge tests with an unselected cell are BLOCKED.

At an appropriate simulated battery voltage and normal sensor temperature, check TP22 USB_CHG, TP19 NTC, input status and actual battery current. Record current direction: emulator sinking current indicates charge; the same connection may source current into the toy under other conditions. An LED alone does not prove charge current reaches the battery.

| Indicator/checkpoint | What it tells you—and what it does not |
|---|---|
| LED1 POWER GOOD / TP26 PGOOD_N | Charger recognizes a valid input when status is asserted low. Does not certify J3 output rails. |
| LED2 CHARGING / TP27 CHARGE_N | Low generally indicates charging. Off may mean complete, disabled, invalid source, temperature inhibit or another condition; flashing can indicate a timer fault. Measure and consult U1's status definitions. |
| TP19 NTC | Analog temperature-sense voltage, not a digital on/off flag. Depends on USB_CHG, R74/R75 and sensor resistance. |

PGOOD_N and CHARGE_N are open-drain indicators connected through their LED/resistor paths to VBUS, not guaranteed 3.3 V logic outputs. Use an appropriately rated meter/probe. Do not connect them directly to an ESP32 or a 3.3 V-only logic analyzer.

The nominal full charge-current setting is about **0.303 A**, screened **0.271–0.332 A** under the reviewed conditions. Precharge, near-full taper, thermal regulation, input limits or system load can legitimately lower it. Do not demand 0.303 A at every battery voltage. Verify termination and recharge behavior against [BQ24075T's datasheet](../datasheets/BQ24075TRGTR.pdf), recording source, battery voltage, temperature and load conditions.

Sensor check with **all power off and sensor unplugged**: measure the actual 103AT-2 resistance at a recorded temperature; nominal is 10 kΩ at 25°C, not at every room temperature. Inspect J4 and its lead continuity. An instructor may gently change the detached sensor's ambient temperature in a controlled setup; do not heat/chill a real cell to provoke faults.

Temperature-threshold screening gave roughly 4.8°C cold and 40.0°C hot nominal, with screened corners about 2.9–42.2°C. These are calculations, not certified pack limits. Instructor-only open/short/temperature simulations use a purpose-built fixture and emulator, changing connections with power off. Confirm charging inhibits as specified and recovers properly; never leave a short or fixed resistor installed as a replacement for a real pack sensor. Do not bypass a temperature inhibit to finish a test.

## 13. P8 — reverse feed, sequencing and final integration

Before attaching main, the technician checks rail rise/fall ordering, load-gate behavior and absence of damaging GPIO/module back-powering using the exact SuperMini revision. Equal timing capacitors do not prove safe sequencing. Do not power one output separately as an improvised test; use a reviewed fixture for controlled backfeed analysis.

Measure USB reverse feed with an approved breakout/isolation test arrangement, not by shorting VBUS or returning power to a laptop. Record current as well as voltage: residual voltage on a high-impedance meter can be stored charge or leakage, not necessarily damaging backfeed. Validate source transitions with the actual planned load. If the fixture or acceptance limits are missing, record BLOCKED.

Only after P1–P7 and sequencing/backfeed checks pass, connect the verified pin-for-pin harness to an unpowered main at its minimal approved population. No ESP32 USB cable. Recheck rails at both ends before adding loads in the main guide's order. Stop when the first added function causes a fault; power off, remove that load and compare with the last passing stage. Do not use a known-good main as a sacrificial dummy load for an unqualified power board.

For each sample, record repeated cold-start behavior and a supervised representative-load run after temperature/current limits are approved. Keep battery and power PCB clear of the main antenna and solder tails; separate support height, plug access and final case fit remain unqualified. Passing a bench test in open air is not proof of enclosed thermal safety.

## 14. Quick symptom route

| Symptom | First investigation |
|---|---|
| Board appears dead from the factory | Confirm assembled vs bare; P1/P2; source polarity and protected return; P3 first missing stage. No firmware is needed by power itself. |
| Input immediately current-limits | Stop; source/fixture setting, polarity, bridges and the first shorted stage. Never just increase the limit. |
| Battery-only works; USB does not | P6 VBUS → CC_3V3 → USB_CHG, cable orientation/source mode; then charger status. |
| USB works; battery-only does not | P2 fuse/harness; P3 protection and U1 battery power path; emulator recovery state. |
| SYS_RAW present, SYS_SW absent | SW1/RUN_CTL, UVLO and U4/fault/load condition. |
| All three outputs absent | Measure pre-gate rails, TP28 and TP12; one low rail may correctly gate all outputs off. |
| One regulator output wrong | That U5/U6/U7 channel's input/enable, inductor, feedback values, capacitor/joint and load. |
| Regulator output correct, J3 rail missing | Enable plus U8/U9/U10 gate path and connector continuity. |
| LEDs lit, main dead | LED1/2 describe charger status, not main rails. Measure J3 and the harness. |
| Charges on USB-C but slowly on USB-A | May be intended default-current behavior; verify P6 mode and measured current before calling it a defect. |
| Charging never starts | Source, emulator/cell state, actual current direction, NTC/sensor, status; P7. |
| Repeated on/off or ticking | Source sag/current limiting, UVLO, load transients, unstable regulator or supervisor cycling; scope first failed stage. |
| Works on bench, fails in case | Support shorts, wire stress, connector access, cooling and antenna/cell placement; do not keep operating closed. |

## 15. Complete test-point reference

All 28 test points are on **B.Cu, the rear copper face**. Coordinate values below are native front-view CAD coordinates, X right/Y down; rear drawings are mirrored. Use the reference label and [assembly drawings](../release_checks/drawings/) to locate the actual pad. Attach clips with power off, support the board and do not bridge adjacent pads.

**TP numbers are board-specific.** Power TP3 is BAT_NEG; main TP3 is ACT_3V2. Never carry a remembered TP number from one board to the other.

<!-- GENERATED_TEST_POINT_TABLE -->

| TP | Signal | What to expect / use | CAD X, Y mm |
|---|---|---|---|
| TP1 | `VBUS` | Raw USB VBUS; nominal 5 V when attached. | 5.0, 29.0 |
| TP2 | `VBAT` | Fused battery positive; interpret with protection state/reference. | 8.5, 29.0 |
| TP3 | `BAT_NEG` | BAT_NEG, cell-side return. Never use as a spare system GND. | 12.0, 29.0 |
| TP4 | `GND` | System GND; usual rail-measurement reference. | 15.8, 28.5 |
| TP5 | `SYS_RAW` | Charger/system power path output; varies with source and operating state. | 20.0, 29.0 |
| TP6 | `SYS_SW` | After eFuse; near SYS_RAW when enabled and healthy. | 23.0, 29.0 |
| TP7 | `RUN_CTL` | User run command; OFF near GND, ON near SYS_RAW. | 26.5, 29.0 |
| TP8 | `EF_UVLO` | eFuse analog undervoltage divider; do not drive externally. | 30.0, 29.0 |
| TP9 | `EF_ILIM` | eFuse current-programming node; no universal digital level. | 34.0, 29.0 |
| TP10 | `EF_FAULT_N` | Active-low eFuse fault; pull-up is to SYS_RAW, not fixed 3.3 V. | 44.0, 40.0 |
| TP11 | `PG_ALL` | Regulator status, pulled toward REG_3V3; not independent supervisor output. | 41.0, 29.0 |
| TP12 | `RAILS_EN` | Common output-gate enable; high after valid supervision. | 44.5, 29.0 |
| TP13 | `REG_5V` | Pre-gate 5 V regulator output. | 5.0, 32.5 |
| TP14 | `REG_3V3` | Pre-gate 3.3 V regulator output. | 8.5, 32.5 |
| TP15 | `REG_3V2` | Pre-gate 3.2 V regulator output. | 12.0, 32.5 |
| TP16 | `MCU_5V` | Gated MCU_5V to J3 pin 1. | 16.0, 32.5 |
| TP17 | `LOGIC_3V3` | Gated LOGIC_3V3 to J3 pin 3. | 19.5, 32.5 |
| TP18 | `ACT_3V2` | Gated ACT_3V2 to J3 pin 4. | 29.0, 47.0 |
| TP19 | `NTC` | Analog thermistor node; depends on source and sensor. No forced logic levels. | 22.0, 41.0 |
| TP20 | `CC_DEFAULT_N` | CC-mode OUT1: high for default, low for 1.5/3 A attached advertisement. | 30.0, 32.5 |
| TP21 | `USB_HIGH_CURRENT` | Inverted mode control: low default, high for 1.5/3 A advertisement. | 34.0, 32.5 |
| TP22 | `USB_CHG` | USB supply after U13 current limiter, before charger. | 37.5, 32.5 |
| TP23 | `USB_PORT_ILIM` | USB current-limit programming node; do not drive externally. | 41.0, 32.5 |
| TP24 | `USB_LIMIT_FAULT_N` | Active-low U13 fault; pull-up to VBUS. Use voltage-rated probe. | 44.5, 32.5 |
| TP25 | `CC_3V3` | Dedicated CC supply, nominal 3.3 V with USB input. | 5.0, 39.0 |
| TP26 | `PGOOD_N` | Charger input-good status, active-low via VBUS LED path; not 3.3 V logic. | 8.0, 39.0 |
| TP27 | `CHARGE_N` | Charge status, active-low via VBUS LED path; read with charge conditions. | 14.0, 39.0 |
| TP28 | `VOLTAGES_OK` | Independent supervisor result; high after valid rails and delay. | 17.0, 39.0 |

<!-- END_GENERATED_TEST_POINT_TABLE -->

TP8 EF_UVLO, TP9 EF_ILIM, TP19 NTC and TP23 USB_PORT_ILIM are analog programming/sense nodes, not places to inject a logic level. TP10 EF_FAULT_N and TP24 USB_LIMIT_FAULT_N have pull-ups to their associated power domains; TP26/27 use VBUS indicator paths. “High” is not always 3.3 V. Only use voltage-rated probes, and evaluate status when that circuit is actually powered.

## 16. When to send it back instead of repairing it

Contact the factory/designer for a wrong/undocumented IC substitution, open internal trace/via, damaged pad, suspected hidden-joint defect, incorrect via-in-pad process, persistent rail error or multiple boards failing identically. Fine-pitch rework and protection changes belong to a qualified technician; repeated failures can be a design/fixture problem, not five bad ICs.

Send the exact C6/P4 release identification, serial/lot, both-side photographs, unmodified as-received evidence, setup/isolation diagram, source and load settings, ambient temperature, first failed step and a table of measurements with references. Attach scope traces with scales/trigger/probe setup, the factory's X-ray/electrical-test records and approved substitutions. State whether a real cell was connected and whether any rework occurred. Do not send a damaged battery through ordinary return shipping; coordinate the appropriate process with the responsible lab/supplier.

After an approved repair, repeat incoming inspection, unpowered checks, every power stage and the relevant charging/protection/integration tests. Keep all five board records separate. A completed worksheet reports only the conditions actually tested; battery, product/EMC and student-use approval are separate responsibilities.

Sources: [P.4 electrical review](P4_REVIEW_AND_TEST.md), [test-point map](../release_checks/TEST_POINTS.csv), [connector map](../release_checks/CONNECTOR_PIN_MAP.csv), [calculated screening](../electrical_screening.json), [DW01A](../datasheets/DW01A.pdf), [FS8205](../datasheets/FS8205_rev1_7.pdf), [TPS259530](../datasheets/TPS259530DSGR.pdf), [TPS63060](../datasheets/TPS63060DSCR.pdf), [TPS386000](../datasheets/TPS386000RGPR.pdf), [TPS22950](../datasheets/TPS22950YBHR.pdf), [103AT-2](../datasheets/103AT-2.pdf). This supplement does not alter CAD or previously issued manufacturing ZIPs.
