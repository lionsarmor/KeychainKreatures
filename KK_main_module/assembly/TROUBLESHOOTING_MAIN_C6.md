# Main C.6 — student troubleshooting guide

For the 96 × 105 mm, two-layer Keychain Kreatures main board, paired with compact P.4 power. Guide version 1, 2026-09-12. Read in order on the first attempt; use the symptom table later.

**A board that does not work is a clue, not a student's failure.** Change one thing, measure again, and write down what changed. This guide describes tests to perform; it does not claim these prototypes have passed physical or powered testing.

## 1. Start here: what did the factory actually supply?

| What arrived | What it can do before assembly/programming |
|---|---|
| Bare main PCB | Nothing by itself. It needs its parts, socketed modules, power and software. |
| Populated main without ESP32/display/SD | Some power and wiring tests only; no game screen is expected. |
| Complete main with an unprogrammed or wrong-version ESP32 | It may look completely dead even with correct hardware. |
| Complete main with a verified C.6 diagnostic program | The functional tests below can begin, after the electrical checks. |

The hardware release does **not** include a validated C.6 diagnostic program or completed game/upload firmware. The instructor must supply and identify the correct test program. Record its version/hash. If none exists, mark software-dependent steps **BLOCKED — test firmware unavailable**, not FAIL. Do not install an old C3/MAX98357A/PCF8574 sketch on this S3/MCP23017/TDA2822L design.

A known-good comparison board means one that has actually passed these tests, not merely another untested factory sample.

## 2. Safety and who does what

**Students, with supervision:** identify parts, inspect unpowered boards, check a disconnected cable, record measurements, and operate an instructor-approved test setup. **Instructor only:** prepare power, attach live-test clips, change meter current ranges, use an oscilloscope, repair solder joints, program/recover modules, and approve replacement parts.

Stop immediately for smoke, unusual smell, a reversed connector, a swelling/leaking battery, sudden temperature rise or a supply repeatedly entering current limit. Switch off the bench supply and disconnect external power if safe. Do not touch a hot component or handle a damaged battery; alert the instructor and follow the lab's emergency procedure. Do not keep cycling power to see whether it improves.

- Never connect a battery directly to main J1. It needs **three regulated rails**, not a single battery voltage.
- Never attach ESP32 USB while external power is connected to main. For USB programming, remove the ESP32 from the unpowered board and use it alone.
- Power off and disconnect all sources before inserting/removing a module, SD card, chip, plug or meter clip. Verify the rails have fallen near 0 V; never discharge a capacitor with a screwdriver.
- Speaker J5 has **two driven outputs**. Neither is ground. Motor J4 pin 2 is also not a ground terminal.
- Do not bridge a pad with wire, replace a resistor with a short, bypass R23/R24, or increase a current limit to conceal a fault.
- Use a nonconductive bench mat and board holder. No metal rulers, loose screws or battery pouches beneath solder tails. Do not probe a handheld board.
- Protect your eyes during supervised soldering/lead clipping; use ventilation and wash hands afterward. Repairs must be inspected before power returns.

## 3. Your tools and a few useful words

Bring the board, this guide, the matching assembly drawing, a magnifier, a multimeter, insulated fine probes, and the instructor's verified power fixture. Functional testing also needs the identified test firmware, a spare test-only SD card, a known-compatible 38 kHz IR remote and a verified data USB cable. Scope/logic-analyzer work is instructor-only and uses voltage-compatible inputs.

| Word on the sheet | Meaning |
|---|---|
| J / U / R / C / Q / D / TP | Connector / integrated circuit / resistor / capacitor / transistor / diode or LED / test point. |
| Rail | A distributed power supply, such as LOGIC_3V3. |
| GND | The system's voltage reference. It is not automatically every metal part. |
| Open | A connection that should conduct but does not. |
| Short | An unintended low-resistance connection. |
| High / low | A digital signal near its logic supply / near ground. Not every signal uses 5 V. |
| `_N` | Usually active-low: the function is asserted when the signal is low. |
| PWM | Fast on/off pulses. A voltmeter shows an average, not the waveform. |

### How to use the meter without creating a fault

1. Black lead in **COM**; red lead in **V/Ω**, never the A/mA jack for these student checks.
2. For continuity or resistance: all power and USB disconnected; instructor confirms discharged rails. Touch probes together first and note the lead resistance/beep. Separate them and observe the open indication, often `OL`.
3. A brief beep across a supply capacitor may stop as it charges from the meter. Semiconductor paths can also conduct. Record settled readings and probe direction; a beep alone does not prove a short. Do not invent a universal resistance threshold.
4. For voltage: select DC volts and a suitable range above 5 V. The instructor attaches the black clip to **main TP4, TP6, TP8 or J1 pin 2** while power is off. Turn on, touch only the intended point with red, record the value, then switch off before moving clips.
5. Never place a meter in current mode across a power rail. Current measurement needs a correctly fused series connection prepared by the instructor; prefer the supply's current display initially.

## 4. M1 — photograph and inspect before power

Record main serial number, revision, supplier/lot, assembly date and the exact ESP32, screen and SD-reader markings. Photograph both sides before rework. Check that the PCB says C.6 and matches the current files. Save the supplier's assembly/BOM/substitution report.

Use the [assembly guide](ASSEMBLY_GUIDE.md) and [reference BOM](C6_BOM_BY_REFERENCE.csv). Inspect one component group at a time:

- All 43 resistors lie flat; verify their values from the BOM, not appearance alone. In-circuit resistance can be lower because other paths are connected; an instructor may isolate a lead if needed.
- Capacitor pad 1 is positive, pad 2 negative. The sleeve stripe marks negative. C21 is special: positive to U3 pin 8, negative to U3 pin 5, **not ground**. Look for crossed formed leads or stressed seals.
- Q1/Q2 KSP2222A are E-B-C; Q3 BC327 is C-B-E. Q4/Q5 TN0702 and Q6 LP0701 are S-G-D in numbered-pin order. These are not interchangeable simply because the plastic bodies fit.
- DIP chips face their socket notch/pin-1 mark. No folded-under pins, half-inserted chips or one-hole-offset modules. Inspect the back-side U4 orientation from the correct-side drawing.
- D2's banded pad 1 goes to ACT_3V2. D1 is the IR transmitter, **not** the mood LED. D3 is the four-lead RGB LED.
- Check cold-looking/incomplete joints, actual cracks, solder bridges, lifted pads and clipped wire fragments. A dull lead-free joint is not automatically bad; inspect wetting and continuity.
- Look below socketed modules for contact with opposite-side solder tails. Display support must not rely only on the header. Debug holes remain bare, not tall posts under another part.

**Pass:** correct parts and orientation, no visible damage or suspected bridge. **If uncertain:** stop and ask the instructor; do not apply power to settle the question.

## 5. M2 — prove the plugs and unpowered wiring

Disconnect the four-wire harness from both boards. Use pin numbers from the drawings, never left/right in a rear-view photo. Power J3 pin 1 must reach main J1 pin 1, and similarly 2→2, 3→3, 4→4. Check each wire end-to-end and check that it does **not** connect to any of the other three wires. Gently flex the disconnected harness while measuring. An intermittent connection is a failure even if the plug clicks.

| Main connector | Numbered pins |
|---|---|
| J1 SYS_IN | 1 MCU_5V; 2 GND; 3 LOGIC_3V3; 4 ACT_3V2. |
| J2 display | 1 GND; 2 LOGIC_3V3; 3 SCK; 4 MOSI; 5 RESET; 6 DC; 7 CS; 8 BLK. |
| J3 SD reader | 1 LOGIC_3V3; 2 CS; 3 MOSI; 4 SCK; 5 MISO; 6 GND. |
| J4 motor | 1 ACT_3V2; 2 switched motor return. |
| J5 speaker | 1 amplifier OUT1; 2 amplifier OUT2. Neither is GND. |

The two-pin motor and speaker plugs physically fit each other's sockets. Label them **MOTOR** and **SPEAKER** and check the wiring; matching plastic does not prove compatibility.

With the main still unpowered, the instructor checks all three rails to GND and rail-to-rail for suspected shorts. Compare to a verified board in the same module-population state when readings are ambiguous. The ESP32 module's `3V3` output is intentionally **not connected** to the board's LOGIC_3V3 rail. Do not “repair” that intentional separation with a jumper.

**Pass:** harness maps exactly, no intermittent connection, no unresolved rail-short suspicion. **Fail:** photograph and locate the fault before replacing any electronics.

## 6. M3 — verify main-board power first

Instructor: qualify the P.4 power module independently using its own guide before connecting main, or use a reviewed, coordinated three-rail fixture with correct sequencing. A random single-output supply is not a substitute. Begin with socketed loads and motor/speaker unplugged; test each populated stage with approved current limits. There is no validated universal main-board startup-current limit yet. Record the chosen limits and actual current; do not guess them from a USB charger's label.

Use a common system-GND reference. These are **investigation windows**, not a production specification or absolute maximum ratings:

| Main measurement | Nominal | Stop and investigate outside |
|---|---|---|
| TP1 or J1 pin 1, MCU_5V | 5.0 V | 4.75–5.25 V. |
| TP2 or J1 pin 3, LOGIC_3V3 | 3.3 V | 3.135–3.465 V. |
| TP3 or J1 pin 4, ACT_3V2 | 3.2 V | 3.04–3.30 V; upper bound deliberately tighter than +5%. |

Measure first at power J3, then at main J1 and the main TP. Correct source voltage but wrong main voltage points to the harness, connector or PCB path. Wrong voltage already at power J3 means troubleshoot power, not the screen. A steady voltmeter reading does not rule out fast brownout/overshoot; the instructor scopes startup and load changes.

After each approved stage: switch off, verify discharge, fit the next load, recheck polarity, power on and record the current change. If a rail collapses after adding a part, remove that part **with power off** and repeat the earlier stage. Do not put a suspect part into the known-good board until shorts/pinout have been checked.

## 7. M4 — isolate the ESP32 and firmware

If the processor will not communicate, the instructor removes it from the unpowered main board. Test the module **alone** with its own USB connector and a verified data cable. This separates a module/software issue from a main-board issue.

Check the selected port, OS permissions, cable and other programs holding the port. Record chip identification and actual flash/PSRAM; do not assume all “SuperMini” listings are N16R8. If needed, use the module's documented BOOT/reset procedure: on boards with the corresponding buttons, hold BOOT during reset to enter download mode, then release. Do not short unidentified header pins. Back up recoverable firmware/data before erasing or reflashing. See [Espressif boot-mode guidance](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/advanced-topics/boot-mode-selection.html) and [connection troubleshooting](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/troubleshooting.html).

**Module works alone, fails in main:** inspect socket alignment, 5 V at the module, its local regulator/reset behavior and GPIO back-powering during rail transitions. **Module also fails alone:** resolve cable/host/firmware/module first; main-board rework is not justified yet.

The power module's USB-C connector is charging-only and will never appear as the ESP32's data port. GPIO43/TX and GPIO44/RX are used for display DC/CS on this design; do not attach a UART adapter to them in the assembled toy. Use instructor-approved logging without a second power path.

## 8. M5 — buttons and the MCP23017 expander

The instructor's test firmware must identify U1 at I²C address **0x20**, set safe output latches before output directions, and report raw button state. AMP_EN and MOTOR_EN start low; RGB_OE_N starts high (blanked). A bus scan alone is not a complete functional test.

Instructor measurement: U1 pin 9 is 3.3 V, pin 10 GND; TP33/U1 pin 18 should leave reset and be high. SDA TP9 and SCL TP10 normally idle near 3.3 V. Persistent low can mean a bridge, reset/unpowered device, wrong initialization or a device holding the bus. Power off before isolation; do not force a bus high with a wire. U1 address pins 15–17 are grounded.

| Button | Expander / processor input | Expected when pressed |
|---|---|---|
| SW1 Up; SW2 Down | U1 GPA0 pin 21; GPA1 pin 22 | Low; released high. |
| SW3 Left; SW4 Right | U1 GPA2 pin 23; GPA3 pin 24 | Low; released high. |
| SW5 A; SW6 B | U1 GPB0 pin 1; GPB1 pin 2 | Low; released high. |
| SW7 X; SW8 Y | U1 GPB2 pin 3; GPB3 pin 4 | Low; released high. |
| SW9 Function | ESP32 GPIO2; TP12 | Low; released high. |

Press each ten times, hold for two seconds, release, then try intended two-button combinations. Raw changes should follow the correct switch; user-visible events should be one per deliberate press after debouncing. Contact bounce in raw readings is normal; stuck states are not. If the raw bit changes but the game ignores it, investigate firmware mapping/debounce rather than replacing the button.

Unpowered switch check: A/B are internally common and C/D internally common. Check **across the two groups**, not A-to-B; pressing joins the groups. In-circuit readings can include the pull-up network.

TP11/BUTTON_INT_N only behaves as a button interrupt **after firmware configures interrupts**. A constant high before setup is not evidence of a broken trace. GPA4–7 control RGB; GPB4/5 control audio/motor; GPB6 resets the screen. Do not configure those as more button inputs. GPB7 is unused.

## 9. M6 — display and backlight are separate tests

First check that J2 pin 2 receives 3.3 V and pin 1 reaches GND, with the header on the correct side and no one-pin offset. The supplied screen configuration is ST7789V2, **280 × 240 in landscape**. The instructor must use the exact panel's initialization, offsets and color order, not merely a similarly sized screen example.

| Symptom | Next check and what it means |
|---|---|
| Completely dark | TP20/BL_PWM command, Q2/Q3 path, R23 and TP21/J2 BLK. A faint image under external light can suggest backlight trouble, but is not definitive. |
| Backlight on, white/blank screen | Check reset TP19, CS TP17, DC TP18 and SPI clock/data TP13/TP14 with test firmware. Light alone does not prove data works. |
| Picture shifted, cropped or wrong colors | Check landscape dimensions, ST7789 initialization, offsets and RGB/BGR setting before reworking traces. |
| Works until SD is used | Check shared SPI transaction settings and that the non-selected device's CS is high. Test each module separately with power-off changes. |

R23 remains **100 Ω** until actual backlight current is measured. Do not bypass it to make the screen brighter. PWM measurements need a scope; a meter's average voltage is not an on-state limit. Instructor may calculate current from measured drop across R23 using I=V/R under a defined steady test, with insulated differential probing.

Pass the display test with red/green/blue/black/white fills, a border on all four edges, text and moving graphics. Record brightness setting, current and any resets. A black test pattern is not the same as a failed backlight.

## 10. M7 — microSD storage

Use a backed-up **test card**, not a student's only save data. Confirm the 3.3 V six-pin reader's pin order at J3. The selected 32 GB microSDHC card is intended for FAT32. Formatting erases data and is instructor-approved only.

Test in stages: detect card; write a uniquely named test file; close it; read it back and compare a checksum; reboot and read again. Repeat while the display updates, then during approved Wi-Fi activity. Record file size, checksum and SPI clock. Start with conservative bus speed; a speed reduction that helps suggests timing/signal-integrity or firmware transaction problems, not an automatic permanent fix.

TP16 is SD_CS. SPI clock is TP13, MOSI TP14. **There is no TP15 in this revision:** probe MISO at J3 pin 5 only with an instructor-prepared clip. Socket contamination, contact pressure, a wrong-voltage reader and incompatible software can all resemble a bad card.

Controlled interrupted-write recovery is an instructor test using disposable test data and the normal power-control fixture. Never pull the card live or repeatedly cut a real battery connection. An unimplemented recovery feature is BLOCKED, not a passed storage test. SD adds storage, not processor RAM or automatic support for downloadable applications.

## 11. M8 — RGB mood LED

Confirm D3's socket pin order: **1 red cathode, 2 common anode at 5 V, 3 blue cathode, 4 green cathode**. Do not force or twist the formed leads. U4 pin 16 uses 3.3 V; pin 1 GND. The LED must not be driven directly from the expander.

With test firmware: reset should keep the LED blank; command OFF, red, green, blue, then mixed colors briefly. Red is U4 OUT0/pin 5, green OUT1/pin 6, blue OUT2/pin 7. Data comes from U1 GPA4, clock GPA5, latch GPA6 and active-low blanking GPA7. There are no dedicated RGB test pads; the instructor checks DIP/socket pads with power-off clip placement.

If all colors are off, check both supply rails and OE_N first. If colors are swapped, compare socket lead order and software bits before bending leads. If one color fails, power off and check that lead/contact/path. R40 is **1.8 kΩ**, giving a calculated default near 10.4 mA/channel; measure rather than treating it as calibrated brightness. Always-on light at reset is a failure to investigate, not a harmless startup effect. Do not remove R40 or connect a cathode directly to ground.

## 12. M9 — IR receive first, then transmit

U2 is the **TSOP38238 receiver**. D1 is the **TSAL6200 transmitter**; D3 is RGB. Check U2 pin order 1 OUT, 2 GND, 3 supply and lens direction. TP32 is its filtered supply after R27; it should be close to the 3.3 V logic rail under normal light. A substantial drop suggests incorrect assembly, excess current or a supply-path problem.

Test receive with a known-compatible 38 kHz remote at a modest distance, away from strong sunlight. TP31/IR_RX normally rests high and produces low-going **demodulated bursts**, not a continuous 38 kHz waveform. Use a scope/logic analyzer and the decoder's raw-event display. A decoder saying “unknown protocol” while pulses arrive means the optical/electrical path may work but the software does not understand that remote. See the [Vishay receiver datasheet](https://www.vishay.com/docs/82491/tsop382.pdf).

Then transmit short, protocol-valid carrier bursts using GPIO7/TP30. Check Q1, R25, R26 and the **100 Ω R24** LED current-limiting path. The transmitter is supplied from LOGIC_3V3, not 5 V. Never hold the output on continuously as a brightness test or bypass R24. Verify with a second known-good receiver at a controlled distance; self-reception alone is insufficient. A phone camera may show some IR, but many filter it out: a dark camera image does not prove failure. Do not aim the LED into anyone's eyes.

## 13. M10 — vibration motor

Check the motor is at J4, not J5. Start with motor command OFF. Instructor verifies U1 GPB5/pin 6 remains low until requested, then commands a short pulse (for example 100 ms) with a current limit approved for the actual motor. Secure the motor; do not stall or hold its shaft/rotor.

During ON, Q4 pulls J4 pin 2 / TP29 toward GND; voltage **across J4 pins 1 and 2** drives the motor. An unloaded OFF return may float; do not demand a universal TP29 off-voltage. Check the ACT_3V2 rail dip, R28 gate path, R29 pull-down, and D2/C16 suppression if there is a reset or large transient. D2 band faces ACT_3V2. A motor that stays on when commanded off needs investigation before reconnecting it for further use.

No movement with correct voltage across the connected motor points toward its harness/motor or mechanical retention. Voltage disappearing under load points toward a short, excessive load or supply path. Do not test it by connecting it straight to an unspecified battery.

## 14. M11 — audio: protect the speaker and the meter

Instructor first leaves the speaker disconnected. Verify U3 and C21 orientation, Q6 LP0701 pin order, and the bridge wiring: U3 pin 1→J5 pin 1, U3 pin 3→J5 pin 2, U3 pin 4→GND. Q6 pin 1 is ACT_3V2; Q6 pin 3/C25 positive/U3 pin 2 is switched amplifier supply.

With AMP_EN (U1 GPB4/pin 5) low, the amplifier supply should decay toward zero after settling. With AMP_EN high, it should rise toward ACT_3V2; record Q6's drop and current. Unexpected enable behavior suggests Q5/Q6 orientation, R36–R39 or firmware, not necessarily a bad amplifier. There are no separate amplifier-enable/supply test pads: use identified component pads, not guessed TP numbers.

Signal path: GPIO8/TP22 → R30/C18 → R31/C19/TP23 → C20 → R32/R33 → U3 pin 7. Scope input PWM, filtered signal and the two outputs under a defined silence/tone program. The design review assumed a 200 kHz PWM carrier; an arbitrary example may hiss, click or use the wrong output pin. Use midscale PWM silence, settle, then enable/fade in; fade out before disabling.

**Never clip a grounded scope lead to either J5 pin.** Use an appropriately rated differential probe, or two compatible channels with both ground clips at system GND and channel subtraction. Scope grounds are usually connected together. Do not connect a grounded external audio input to the bridged speaker pair.

At commanded silence, measure differential DC **across J5**; individual outputs can have a normal DC bias. The exact speaker's continuous power rating is unresolved, so no validated allowable DC offset or production volume limit exists. If there is sustained unexplained differential DC, clipping, strong popping or heating, leave the speaker disconnected and escalate. After instructor approval, attach the speaker with power off and start the test tone at the lowest practical volume, increasing only while measuring. Do not infer speaker safety from a firmware percentage.

## 15. M12 — integration, intermittents and repeatability

Only after each earlier stage passes, add normal Wi-Fi traffic, display updates, SD writes, one RGB state, short IR/motor bursts and low-level audio in controlled combinations. Use approved loads and temperature limits. Record the rail minima/maxima and reset logs; a handheld meter can miss the event that causes a brownout.

For a first prototype run, propose ten supervised cold starts and a ten-minute representative activity run **after** the instructor approves power and temperature limits. These are repeatability screens, not lifetime, toy-safety or battery certifications. Never leave an unqualified assembly charging unattended. Stop for resets, rail excursions, current-limit cycling or abnormal temperature rise.

Keep the power PCB, battery and wires outside the main antenna region. Compare radio behavior with and without the final enclosure only under the same test conditions. Don't call weak Wi-Fi a solder fault before checking firmware, network configuration and the metal/battery placement.

The old main reservation of 0.5 A on 3.3 V exceeds the power screening target of 0.4 A. The instructor must measure the actual simultaneous demand and approve margin; neither figure is a measured capacity. A failure under combined load can require design revision, not more solder or a larger battery.

## 16. Quick symptom route

| Symptom | First route |
|---|---|
| Absolutely nothing happens | Section 1 (assembly/firmware state), M2 harness, then M3 rails. |
| Supply current limit / part heating | Stop; M1/M2 unpowered inspection, instructor isolates the last-added load. |
| ESP32 repeatedly resets | M3 transient power, M4 boot/firmware, then isolate the triggering peripheral. |
| Buttons and motor/audio controls all fail | M5 expander supply/reset/I²C, not nine independent switch replacements. |
| One button stuck | M5 raw bit, pin grouping, pull-up and joint. |
| Screen lit but blank | M6 initialization/reset/SPI; then firmware prerequisites. |
| SD works alone but not with screen | M7 and M6 shared-bus chip selects/settings. |
| RGB never lights / wrong colors | M8 rails, blanking and lead/bit order. |
| IR does not decode | M9 raw pulses and known-compatible source before decoder changes. |
| Motor causes reset | M10 current/suppression and M3 transient rail measurement. |
| Audio hums/pops or gets hot | M11 bridge wiring, DC, supply, PWM/filter and switch timing. |
| Works only when pressed/bent | Power off; inspect socket, crimp, joint and solder-tail contact. Do not keep flexing live. |

## 17. Record the failure; repair only with evidence

Use the accompanying worksheet. Record setup, connected modules, source/limits, firmware version, exact probe points, measured values, and the first failed step. Photograph before/after each repair. Write PASS, FAIL, BLOCKED or NOT RUN—never leave an unperformed test marked PASS. For all five boards, record serials separately and keep one genuinely verified unit as the comparison reference.

An instructor may reflow a confirmed through-hole joint, correct an identified assembly error or replace a verified wrong part. First preserve the factory evidence and check return/warranty instructions. Missing internal copper, repeated identical failures, damaged pads or an unresolved design/load issue go to the designer/factory; do not hide them with undocumented jumper wires.

After a repair, repeat M1/M2, M3 power, the failed function, and M12 integration. Keep the repaired part/lot information. Passing this guide establishes only the tests actually recorded, not a finished product certification.

## 18. Instructor pin and probe reference

All main test points are on **B.Cu, the rear copper face**. Their numbers have intentional gaps. Native CAD coordinates use the board's front-view origin, X right/Y down; a rear viewing drawing is mirrored. Find the reference in the assembly drawing before measuring. Do not add pins beneath parts just to make probing easier.

| ESP32 GPIO / header label | Assigned main signal |
|---|---|
| GPIO1 / 1; GPIO2 / 2 | Button interrupt; function button. |
| GPIO4 / 4; GPIO5 / 5 | I²C SDA; I²C SCL. |
| GPIO6 / 6; GPIO7 / 7 | IR receive; IR transmit. |
| GPIO8 / 8; GPIO9 / 9 | Audio PWM; backlight PWM. |
| GPIO10 / 10 | SD chip select. |
| GPIO11 / 11; GPIO12 / 12; GPIO13 / 13 | SPI MOSI; MISO; clock. |
| GPIO43 / TX; GPIO44 / RX | Display DC; display chip select—not a free debug UART. |
| GPIO3 / 3; module 3V3 output | Intentionally unconnected to main functions / external logic rail. |

Verify the actual seller module matches these header assignments before using firmware. The following complete TP table is generated directly from the current release map.

<!-- GENERATED_TEST_POINT_TABLE -->

| TP | Signal | What to expect / use | CAD X, Y mm |
|---|---|---|---|
| TP1 | `MCU_5V` | Main 5 V input; nominal 5.0 V. | 54.0, 33.0 |
| TP2 | `LOGIC_3V3` | Logic supply; nominal 3.3 V. | 29.5, 73.5 |
| TP3 | `ACT_3V2` | Actuator supply; nominal 3.2 V. NOT power-board BAT_NEG. | 28.5, 53.5 |
| TP4 | `GND` | System ground reference. | 55.5, 76.5 |
| TP6 | `GND` | Alternate system ground. | 59.5, 76.5 |
| TP8 | `GND` | Alternate system ground. | 55.5, 80.5 |
| TP9 | `I2C_SDA` | I2C SDA; normally idle high with valid logic power. | 9.5, 4.5 |
| TP10 | `I2C_SCL` | I2C SCL; normally idle high with valid logic power. | 22.5, 73.5 |
| TP11 | `BUTTON_INT_N` | Active-low expander interrupt; requires firmware interrupt configuration. | 35.0, 39.5 |
| TP12 | `BUTTON_FN_N` | Function button; released high, pressed low. | 44.5, 75.0 |
| TP13 | `SPI_SCK` | Shared SPI clock; activity only during transfers. | 35.5, 43.5 |
| TP14 | `SPI_MOSI` | Shared SPI MOSI; activity during transfers. | 66.5, 52.0 |
| TP16 | `SD_CS` | SD chip select; normally high when deselected. | 61.5, 43.0 |
| TP17 | `TFT_CS` | Display chip select; normally high when deselected. | 44.5, 39.5 |
| TP18 | `TFT_DC` | Display command/data selection; state depends on transfer. | 48.5, 39.5 |
| TP19 | `TFT_RST_N` | Display reset, active-low; controlled by U1 GPB6. | 22.5, 69.5 |
| TP20 | `BL_PWM` | Backlight PWM before driver; meter shows only an average. | 26.5, 69.5 |
| TP21 | `Net-(J2-BLK)` | Display BLK after switching/current-limiting path; load/PWM dependent. | 72.0, 66.5 |
| TP22 | `AUDIO_PWM` | Audio PWM before filter; inspect with scope and known test program. | 56.0, 37.0 |
| TP23 | `Net-(C19-Pad1)` | Second low-pass filter node, C19 pad 1/C20 input; waveform and DC bias depend on PWM. C19 is nonpolarized. | 48.5, 72.5 |
| TP29 | `Net-(D2-A)` | Switched motor return; near GND during ON, may float unloaded when OFF. | 19.5, 90.5 |
| TP30 | `IR_TX` | IR transmit logic; valid carrier bursts, not continuous DC test. | 17.5, 16.5 |
| TP31 | `IR_RX` | IR receive output; normally high, low-going demodulated bursts. | 22.5, 13.5 |
| TP32 | `Net-(U2-VS)` | IR receiver filtered supply; normally close to LOGIC_3V3. | 13.5, 4.5 |
| TP33 | `Net-(U1-RESET_N)` | Expander reset; should rise high after startup. | 73.5, 73.5 |

<!-- END_GENERATED_TEST_POINT_TABLE -->

Sources: [current schematic](SCHEMATIC.pdf), [connector coordinates](../release_checks/CONNECTOR_PIN_MAP.csv), [test-pad coordinates](../release_checks/TEST_POINTS.csv), [MCP23017 datasheet](../datasheets/mcp23017.pdf), [TDA2822L datasheet](../datasheets/tda2822.pdf), [TLC5916 datasheet](../datasheets/tlc5916.pdf). Existing release manifests identify the exact CAD; this troubleshooting supplement does not change the boards or previously issued ZIPs.
