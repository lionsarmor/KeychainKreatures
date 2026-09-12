# Revision C — schematic-first engineering prototype

**Current drawing: [one-sheet grouped schematic](../KK_main_module.pdf) / [main KiCad project](../KK_main_module.kicad_pro).** The five-sheet project in this folder is retained as the C.0 backup. C.1 is a layout-only redraw with the same 91 components and 267 pin connections. [Equivalence check](REDRAW_CHECK.json) · [current ERC](ONE_SHEET_ERC.json). All circuit limitations and prototype tests below still apply.

2026-09-10. **An actual editable five-sheet KiCad schematic now exists. This is not a fabrication or purchasing release.** This capture supersedes the old logical `STARTER_CONNECTIONS.csv` and unassigned GPIO table for ongoing circuit work. Revision B's small socketed modules, external power ownership and wireless software direction remain in force.

- [Open the schematic PDF](KK_main_module.pdf)
- [Open the KiCad project](KK_main_module.kicad_pro); root schematic: [KK_main_module.kicad_sch](KK_main_module.kicad_sch)
- [BOM exported by KiCad](SCHEMATIC_BOM.csv) — actual schematic quantities, **not the complete kit BOM**
- [Unambiguous per-reference component register](CAPTURE_BOM.csv) and [pin connections](CAPTURE_CONNECTIONS.csv)
- [Electrical-rule report](ERC.json) and [connection/calculation validation](VALIDATION.json)

Use KiCad 10.0.6, the installed version used to open/export/check this design. The custom symbol library is project-local and included. Standard resistor/capacitor/transistor graphics originate from the installed KiCad libraries; custom IC/module drawings expose individual electrical pins. Identical global labels connect the sheets. This is labelled-net schematic capture, not a breadboard assembly drawing or PCB layout.

## What is captured

| Sheet | Circuit |
|---|---|
| 1 | Socketed SuperMini, proposed external rail connector and local bulk/bypass capacitors |
| 2 | MCP23017, nine four-terminal soft buttons, external pull-ups, reset RC and interrupt |
| 3 | Separate display and SD chip selects on shared SPI; display reset; discrete backlight driver |
| 4 | Current-limited IR transmitter, filtered 38 kHz receiver, motor MOSFET, flyback and suppression |
| 5 | PWM reconstruction filter, fixed attenuation, TDA2822 bridge amplifier, output stability networks and power gating |

There are 91 fitted schematic symbols: 39 resistors, 26 capacitors, nine buttons, six transistors, five connectors, three ICs, two diodes and one MCU module. Six additional source-declaration symbols are ERC annotations, not purchased parts. Header-connected display/SD assemblies, the motor and speaker are represented by their carrier connectors and still need separate assembly BOM lines. Likewise MCU sockets, DIP sockets, male headers, card, mating harnesses, PCB, test pads and mechanical parts are not silently included in the schematic count.

## Decisions made during capture

1. **Use the small SuperMini.** Allocate fourteen of the assumed fifteen exposed GPIOs; leave GPIO3 unused because of strapping and possible internal USB sensing. No underside solder pads are required. Module symbol numbering is a logical carrier convention, not a released footprint numbering scheme.
2. **Correct the switch contact representation.** Adafruit's four-terminal drawing has A/B internally common and C/D internally common. All four terminals now appear; A/B connect to the input and C/D to ground. The old abstract A/B connection list must not be used as physical wiring instructions.
3. **Keep timing on the MCU.** SPI, audio PWM, backlight PWM and IR use direct GPIOs. Display reset, amplifier enable and motor on/off use the expander. No attempt to drive SPI or audio through I2C.
4. **Separate the regulator outputs.** Feed the MCU's assumed 5 V input; leave its 3V3 output unconnected to the peripheral supply. Added voltage generation remains entirely on the future power PCB. Local capacitors, transistor switches and protection of inductive loads remain on the main board.
5. **Select a documented THT motor switch.** Q4 is Microchip **TN0702N3-G**, TO-92, not an arbitrary MOSFET selected from threshold voltage alone. Its [datasheet](../component_review/datasheets/tn0702.pdf) specifies on-resistance at low gate voltages. The source/gate/drain numbering is explicitly remapped to 1/2/3.
6. **Complete audio topology.** UTC's DIP-8 bridge application is captured, including the 10 uF feedback-coupling capacitor, 10 nF feedback bypass, two 100 nF/4.7-ohm stability branches and supply bypass. A two-stage PWM filter and 100k/1k input attenuator precede it. A transistor power switch addresses the amplifier's idle current. The speaker is connected between the two outputs, never output-to-ground.
7. **Protect the backlight GPIO from unknown load current.** The MCU drives a transistor pair; it does not supply the BLK pin directly. The 100-ohm BLK series resistor is intentionally a low-current bring-up value. It may produce a dim display and must be revised from actual BLK topology/current measurements, not blindly bypassed.

Sources: [Microchip TN0702](https://ww1.microchip.com/downloads/en/DeviceDoc/TN0702-N-Channel-Enhancement-Mode-Vertical-DMOS-FET-Data-Sheet-20005941A.pdf), [MCP23017](../component_review/datasheets/mcp23017.pdf), [UTC amplifier](../component_review/datasheets/tda2822.pdf), [button drawing](../component_review/datasheets/soft-buttons.png). Module assumptions remain tied to [the available seller evidence](../component_review/MODULE_SOURCE_NOTES.md), not claimed manufacturer schematics.

## Working GPIO allocation

| SuperMini signal label | Main-board function |
|---|---|
| GPIO1 | Expander interrupt; potential RTC wake input |
| GPIO2 | Function button; potential RTC wake input |
| GPIO3 | Unconnected externally |
| GPIO4 / GPIO5 | I2C SDA / SCL |
| GPIO6 / GPIO7 | IR receive / transmit |
| GPIO8 | Audio PWM |
| GPIO9 | Backlight PWM |
| GPIO10 | SD CS |
| GPIO11 / GPIO12 / GPIO13 | Shared MOSI / MISO / SCK |
| TX / GPIO43 | TFT data/command; boot UART transitions harmless only while TFT CS stays high |
| RX / GPIO44 | TFT CS, external pull-up |

MCP23017 address is 0x20. GPA0–3 handle directions; GPB0–3 handle A/B/X/Y. GPB4/5/6 are amplifier enable, motor enable and display reset. GPA7/GPB7 are not used as inputs. Configure mirrored open-drain interrupts, initialize control latches before setting output directions, debounce buttons, and configure unused GPIOs to known states. MCU native USB remains on its own connector; GPIO43/44 are no longer available as an external UART console in normal firmware.

## Proposed power-module contract — main board only

| J1 pin | Rail | Design target at connector | Reserved source capacity |
|---|---|---|---|
| 1 | MCU_5V | 5.0 V ±5% | 0.6 A |
| 2 | GND | Common return | Sum of rail currents |
| 3 | LOGIC_3V3 | 3.3 V ±3% | 0.5 A |
| 4 | ACT_3V2 | 3.2 V ±1% | 0.4 A |

These are proposed regulator/interface requirements, not measured loads or assertions about the existing power PCB. Motor and amplifier share the actuator rail. Three rails require three regulated supply outputs (possibly derived from fewer converter stages), not just a renamed two-wire SYS_IN. The future power design may simplify this after module measurements; changing the contract requires revisiting this schematic.

J1 is **JST B4B-XH-A(LF)(SN)**, with proposed XHP-4 mating housing and SXH-001T-P0.6 contacts on 24 AWG wire. [JST XH drawing/specification](../component_review/datasheets/jst-xh.pdf). It is deliberately distinct from the two-pin PH actuator connectors. Pin assignments must be reproduced on the future power board and harness. No live mating, no raw battery input, no connection to the old SYS_OUT. The power PCB must own rail sequencing, current limiting/protection and shutdown.

**Programming safety:** until tested, remove MOD1 from the socket and program it separately. Merely unplugging the external power board while leaving a USB-powered MCU connected can backfeed unpowered peripherals through signal pins. Never connect USB and SYS_IN simultaneously on the assembled draft. Initial bring-up requires qualified, current-limited rails and module supply-path inspection.

## Checks actually performed

- KiCad 10.0.6 opened the complete five-sheet hierarchy, exported its PDF/netlist/BOM, and reported **zero ERC errors or warnings** without rule exclusions. Source flags identify the external rails and the two derived filtered/switched supply nets; they do not simulate those sources.
- An independent parser compared **267 pin records** against KiCad's exported netlist. It additionally asserts switch-pair mapping, separate SPI selects, shared data/clock, floating bridge output, motor switch and flyback polarity, and isolation of the module's regulator output.
- Analytical corner checks: 200-ohm button contact with a 1%-tolerance 10k pull-up stays below 0.068 V; I2C pull-up sink demand is about 0.73 mA; a shorted IR LED cannot make its 100-ohm resistor exceed 0.117 W at the specified logic-rail maximum. These checks do not replace GPIO timing, component-temperature or optical tests.
- Complex nodal AC analysis of the actual audio passive ladder, including a 100k amplifier input load: approximately -40.46 dB at 1 kHz and -84.33 dB at 200 kHz. Relative carrier rejection is about 43.9 dB. This is **passive linear frequency analysis**, not amplifier distortion, PWM timing, speaker response, pop-noise or whole-device simulation. Start digital volume low; the amplifier's typical gain is not a guaranteed output limiter.
- At 25°C, assuming at least 3.0 V at Q4's gate and 120 mA startup current, its specified 2.5-ohm resistance gives approximately 2.868 V at the motor with a minimum 3.168 V source. A deliberately illustrative 4-ohm hot scenario gives 2.688 V during startup, so temperature/startup qualification is still required; 4 ohms is not a manufacturer-specified hot limit. At 80 mA running current the same assumed resistance gives 2.848 V. Do not claim motor margin across temperature from a threshold-voltage figure.

No board has been assembled or powered here. No ESP32/SD/display behavioral simulation, full SPICE simulation, firmware bring-up, thermal test, EMC test, PCB DRC or manufacturing review was performed.

## Remaining work before freezing the BOM

| Specific issue | How to close it |
|---|---|
| Exact SuperMini revision/power route | Verify header labels/continuity, 5 V input path, independent 3V3 rail compatibility, 4 MB flash / 2 MB PSRAM and recovery behavior on the delivered module |
| Display BLK circuit/current | Inspect/measure the retained display; choose final limiter/drive values; test full brightness and PWM noise |
| SD module pull-ups and shared bus | Check existing resistor connections, DAT1/DAT2 pull-ups, MISO release, write-current peaks and operation alongside TFT; choose/test the actual card |
| Motor startup over temperature | Measure gate voltage, motor terminal voltage/current and repeated starts; revise switch or rail target if margins fail |
| Speaker and amplifier performance | Obtain exact speaker rating or qualify a documented replacement; measure DC differential, startup pops, stability, usable volume and dissipation |
| Complete physical kit | Assign/verify every THT footprint and module socket spacing, add assembly-only BOM lines and test pads, then derive final fitted quantities |
| Power-interface validation | Confirm future supply implementation meets the three-rail target and controls sequencing/backfeed; existing power board remains untouched |

These are concrete prototype acceptance tasks, not another open-ended supplier shortlist. Continue editing this schematic and record changes here; issue the final BOM only after the circuit and selected assemblies pass those checks. No PCB routing or power-board redesign was started in this revision.

## Reproducibility and editing

The generator is a reproducible starting capture, not a replacement for KiCad editing. **Do not rerun `build_schematic.mjs` after manual schematic edits unless those edits have been merged into the generator or safely preserved.** It regenerates the five sheets/library/registers. Subsequent KiCad edits should be treated as authoritative; the connectivity checker intentionally fails when the capture intent and exported netlist diverge.

Commands from the project root:

```sh
node KK_main_module/schematic/build_schematic.mjs
flatpak run --command=kicad-cli org.kicad.KiCad sch export netlist --output KK_main_module/schematic/KK_main_module.net KK_main_module/schematic/KK_main_module.kicad_sch
flatpak run --command=kicad-cli org.kicad.KiCad sch erc --format json --output KK_main_module/schematic/ERC.json KK_main_module/schematic/KK_main_module.kicad_sch
node KK_main_module/schematic/validate_capture.mjs
flatpak run --command=kicad-cli org.kicad.KiCad sch export pdf --output KK_main_module/schematic/KK_main_module.pdf KK_main_module/schematic/KK_main_module.kicad_sch
```
