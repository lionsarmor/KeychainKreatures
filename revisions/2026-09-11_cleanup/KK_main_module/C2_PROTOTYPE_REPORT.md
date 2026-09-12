# Main-board C.2 engineering pass

Completed 2026-09-10. **The main PCB is routed, electrically connected and exported for a small engineering-prototype batch. It is not a factory-ready or qualified student product.** No power-module changes, manufacturing order, physical assembly or powered test were performed.

## Deliverables

| Requested work | Result |
|---|---|
| Improve placement | Audio bypass, feedback and stability parts clustered around U3; motor suppression and reservoir moved near J4; receiver, screen, SD and input-rail bypass placement improved. UI positions and outline retained. |
| Review amplifier switching | Q5 changed to TN0702N3-G, Q6 to LP0701N3-G; R36/R38 changed to 1 kohm. Active-high enable and default-off behavior retained. |
| Set routing rules | Explicit 0.25–0.80 mm track classes, 0.20 mm clearance and minimum-width rules. Critical audio paths measured after routing. |
| FreeRouting export | Prepared DSN, routed locally with FreeRouting 2.3.0, imported SES, and exported the finished board back to DSN. No cloud upload. |
| Returned-board checks | Both pours refilled; all connections complete; redundant vias and isolated thermal contacts corrected; independent pad/net and schematic-parity checks passed. |
| BOM and assembly guide | 91 reference positions, 36 grouped PCB purchasing rows, plus 22 kit-material rows covering sockets, modules, mating plugs, wires, optional headers and supports. Frozen for this prototype population, with product-qualification holds identified. |
| Prototype manufacturing files | Seven Gerber layers, separate plated/non-plated drills and maps, drill report, manifest and ZIP generated after fresh clean checks. |

## Open / print / manufacture

- [Main KiCad project](KK_main_module.kicad_pro) · [routed PCB](KK_main_module.kicad_pcb) · [one-sheet schematic PDF](KK_main_module.pdf)
- [Printable complete BOM](assembly/C2_BOM_PRINT.html) · [by-reference BOM](assembly/C2_BOM_BY_REFERENCE.csv) · [additional kit parts](assembly/C2_KIT_EXTRAS.csv)
- [Assembly and bring-up guide](assembly/ASSEMBLY_GUIDE.md) · [datasheet index](assembly/C2_DATASHEETS.md) · [24-document packet plus SD photos](assembly/C2_DATASHEETS.zip)
- [Prototype fabrication ZIP](manufacturing/KK_MAIN_C2_PROTOTYPE_FAB.zip) · [fabrication instructions](manufacturing/README.md) · [source/file checksums](manufacturing/MANIFEST.json)
- [Front fit/assembly PDF](pcb/front-fit-check.pdf) · [mirrored back PDF](pcb/back-fit-check.pdf) · [FreeRouting handoff](routing/README.md)

If an editor tab was open before these external changes, reload the root-level project from disk before saving. The earlier design is preserved in [pre-C.2 backups](pcb/backups/pre_c2_pass/). Earlier shopping lists and the five-sheet project are historical, not current population instructions.

## Verified final state

| Check | Result |
|---|---:|
| Schematic ERC violations | 0 |
| PCB DRC errors/warnings under stored project rules | 0 |
| Unconnected items | 0 |
| Schematic-parity issues | 0 |
| Independent pad/net mismatches | 0 / 267 checked |
| Electrical footprints | 91, all main-board component pads through-hole |
| Routed track segments / vias | 840 / 24 |
| Ground zones | 2, filled; front and back |
| Antenna rule areas | 2, on both copper layers |
| Drill counts | 291 plated holes, including 24 vias; 4 non-plated mounting holes |

Evidence: [fresh ERC](manufacturing/ERC.json), [fresh DRC/parity](manufacturing/DRC.json), [independent checks](pcb/C2_FINAL_VERIFICATION.json), [route measurements](pcb/C2_ROUTE_AUDIT.json), [drill report](manufacturing/DRILL_REPORT.txt). The stored project's pre-existing ignored DRC categories are listed in the manifest; no new violation exclusions were added to hide routing defects. Coordinate roundtrip changes were at most one nanometre per axis, recorded in the independent check, not meaningful component relocation.

Geometry remains 80 x 100 x 1.6 mm, two layers and four 4 mm corner radii. The supplied SuperMini footprint is retained, including its named GPIO/power pads and original 0.04 mm GPIO13 offset. Physical part fit is provisionally accepted from the user's check, not independently certified here. Rear placement and final stack height still warrant a dry fit.

## Placement and actual routing

“Before” is straight pad-to-pad distance on the old board, not an old routed length. “Now” is the measured current copper path; vertical via barrel length and plane shortcuts are excluded. Thus these columns distinguish placement from actual routing rather than implying identical measurements.

| Connection | Before: direct distance | Now: routed length |
|---|---:|---:|
| C25 reservoir to U3 supply | 28.90 mm | 8.66 mm |
| C26 ceramic to U3 supply | 6.19 mm | 4.43 mm |
| C26 ground to U3 ground | 6.69 mm | 4.33 mm |
| C21 negative to U3 feedback pin 5 | 33.32 mm | 5.85 mm |
| C22 to U3 feedback pin 5 | 37.78 mm | 5.12 mm |
| C23 to U3 output 1 | 29.25 mm | 3.05 mm |
| C24 to U3 output 3 | 35.69 mm | 6.41 mm |
| R34 to C23 | 23.36 mm | 2.65 mm |
| R35 to C24 | 16.22 mm | 3.63 mm |
| Motor suppression C16 to J4 supply | 42.11 mm | 5.05 mm |
| Motor reservoir C17 to J4 supply | 45.11 mm | 15.29 mm |
| Receiver reservoir C15 to U2 supply | 57.75 mm | 6.63 mm |

The speaker pair is approximately 10.73/13.26 mm from U3 to J5. The motor return J4-to-Q4 path is 15.58 mm at 0.80 mm width. The amplifier's low-level input and feedback stay in its local cluster; these layout checks do not prove immunity to motor, SPI or PWM coupling. Test those combinations on hardware.

One shared-rail nuance: C9 remains extra bulk capacitance on the wider logic rail, with a long copper path around the DIP. It is **not** counted as U1's effective local reservoir. Instead, the nearby C11 10-uF reservoir is connected directly to U1's VDD by a measured 6.02 mm branch and also serves the adjacent SD connector. C8 provides U1's local ceramic bypass, with about 10.96 mm of supply trace. This is recorded explicitly rather than calling every capacitor local merely because it shares a net name.

The original antenna band at the board edge did not clear copper underneath the antenna end of the module. A second, conservative window at x=59.5–72.5 mm, y=7–15.5 mm now forbids tracks, vias and pours on both layers; affected signals were rerouted. Keep batteries, screens' metalwork and harnesses away from the antenna region when developing the shell. Exact module revision and RF range still need testing.

## Amplifier switch decision

| Reference | Previous | C.2 |
|---|---|---|
| Q5 | KSP2222ABU NPN | TN0702N3-G N-MOSFET |
| Q6 | BC32725BU PNP | LP0701N3-G P-MOSFET |
| R36 | 4.7 kohm | 1 kohm |
| R38 | 100 ohm | 1 kohm |

Q5/Q6 now have source/gate/drain at pins 1/2/3. In particular, Q6 pin 1 is ACT_3V2 and pin 3 is the switched amplifier supply; the schematic and PCB were changed together. Do not install the former BC327 in that position.

The former illustrative switch-drive current was about 23 mA plus 0.55 mA into Q5's base. The revised enabled-state control current is approximately `3.3/101k + 3.2/101k = 64.4 microamps`. This is a calculated control-current reduction, not measured whole-toy battery life; U3 still consumes its own enabled quiescent/output current.

R37 pulls Q5's gate low at reset and R39 holds Q6 off. With AMP_EN high, Q5 pulls Q6's gate down through R38. The [TN0702 data](https://www.microchip.com/content/dam/mchp/documents/APID/ProductDocuments/DataSheets/TN0702-N-Channel-Enhancement-Mode-Vertical-DMOS-FET-Data-Sheet-20005941A.pdf) include low-voltage gate-drive conditions; here Q5 only sinks approximately 32 microamps. Even a conservative 2.5 V logic-high estimate leaves about 2.48 V at Q5's gate through the resistor divider.

The [LP0701 data](https://ww1.microchip.com/downloads/en/DeviceDoc/LP0701-P-Channel-Enhancement-Mode-Lateral-MOSFET-Data-Sheet-20005447A.pdf) specify a 2-ohm maximum at VGS=-3 V, ID=-150 mA and 25°C. At that test point the drop/loss are 0.30 V / 45 mW. The nominal gate divider provides approximately -3.17 V; source tolerance and trace drop retain a little margin above 3 V in magnitude under the stated prototype load assumptions. These are conditional checks, not hot/cold or inrush guarantees. C25's charging transient, turn-on/off pops, U3 supply headroom and temperature require measurements. There is no dedicated inrush controller in this revision.

The [UTC TDA2822 bridge application](https://www.unisonic.com.tw/uploadfiles/836/part_no_pdf/TDA2822.pdf) remains the topology basis: U3 outputs 1 and 3 drive the speaker differentially; C21/C22 are feedback components and C23/R34 plus C24/R35 are output stability branches. Neither speaker terminal goes to ground. Start with reduced firmware amplitude and test carrier rejection, clipping, noise, differential DC and speaker heating before releasing a volume limit.

## Routing and power review

| Class | Track width | Purpose |
|---|---:|---|
| Default | 0.25 mm | Digital/control and SPI |
| Audio | 0.30 mm | Filter/input/feedback/stability branches |
| AuxLoad | 0.50 mm | IR LED and switched backlight paths |
| Speaker | 0.50 mm | Both bridged speaker outputs |
| Ground | 0.60 mm | Explicit ground tracks, supplemented by both pours |
| Power / Motor | 0.80 mm | Incoming rails, amplifier supply and motor return |

Minimum copper clearance is 0.20 mm. Net-specific minimum track widths are enforced by project custom rules and independently checked on the final copper. Actual drill sizes, including 0.30/0.40/0.50 mm vias, are listed in the drill report. Nominal copper is 35 micrometres on each side.

As a trace-only sanity check using copper resistivity about 1.72e-8 ohm-metres at room temperature: the 35.92 mm / 0.80 mm MCU supply path is about 0.022 ohm, or 13 mV at 0.6 A; the longest measured 132.46 mm logic supply path is about 0.081 ohm, or 41 mV if the entire reserved 0.5 A flowed through it. These estimates omit connector/contact, return-path and source drops and are not temperature-rise qualification. The motor's supply and switched return copper together contribute only a few millivolts at a 120 mA starting-current example; Q4 and the source dominate its voltage margin. Measure at the actual loads during simultaneous activity.

Most ground pads retain thermal connections for hand soldering. SW1 pad D and U3 pin 4 use their explicit ground tracks instead of useless isolated thermal contacts; their full electrical connectivity was checked after refill. No DRC severity was relaxed for this. Two unnecessary one-layer-only vias were removed, then connectivity and clearances rechecked. Copper/placement views were visually inspected after final routing; plated/non-plated drill counts and the rounded outline were checked against the fabrication outputs.

## Remaining qualification — before a student/product release

1. **Power source:** develop and qualify the separate module against J1's 5 V / GND / 3.3 V / 3.2 V interface, current capacity, coordinated sequencing, protection and USB backfeed behavior. The old power output and a raw battery are not compatible substitutes. Do not attach USB and SYS_IN together.
2. **Speaker and audio:** obtain the exact FS1511P08-H3.0 continuous-power rating or select a documented substitute. Verify MOSFET inrush, audio headroom, noise, pops, differential DC, clipping and hot/cold behavior with the actual speaker.
3. **Actual modules and firmware:** verify delivered SuperMini memory/pinout, display BLK circuitry, SD SPI operation and card write/power-loss recovery. The selected card is Transcend TS32GUSD300S, 32 GB; game loading, uploads and recovery firmware are not implemented by this PCB pass.
4. **Motor and IR:** test startup/current, suppression and interference during Wi-Fi/SD/audio activity; validate the IR carrier/protocol and range.
5. **Mechanical/product checks:** dry-fit the revised rear placement and stack; support the screen, retain the modules and actuators, label the interchangeable motor/speaker plugs, and validate shell/battery placement, RF performance, drop/handling and applicable product compliance.

The immediate next step is an adult-supervised engineering prototype and the documented bring-up checklist—not distribution of untested kits. The manufacturing ZIP is a bare-board prototype deliverable, not certification that the assembled toy will work when plugged into an arbitrary supply.
