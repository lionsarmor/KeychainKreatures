# P.2 power module — five-sample engineering review

This report covers the 50 × 50 mm, four-layer power board, not a new revision of the main board. **Final native results: zero DRC violations, zero unconnected items, zero schematic/PCB mismatches, and zero reported ERC violations.** The checked board has 3,515 track segments and 260 vias. It is an engineering prototype, not a proven consumer-product or battery-safety release. The accompanying verification files record the exact reports and CAD hashes. An assembler must approve the fabrication process and exact component supply before ordering populated samples.

## What this pass changed

- Completed and repaired the unfinished signal routing in an isolated working copy; retained the manually placed converter hot loops and wide output paths.
- Removed shorted/redundant signal routes, added local IC pin escapes and ground stitching, and refilled all planes.
- Added a locked **1.5 mm SYS_SW bridge on In1.Cu**, connecting the eFuse source via bank to the left converter input bank. This avoids depending on a thin signal trace across a split supply pour. In1 remains predominantly ground, but is not an uninterrupted ground-only plane.
- Added a 0.6 mm local supply connection to C8. An independent filled-plane check confirms the eFuse output, all converter input banks and C8 remain connected when long thin supply traces are excluded. Low-current monitor/test-point branches are intentionally excluded from that width screen; it is not a thermal simulation.
- Moved rear debug pads clear of component escapes: TP10 EF_FAULT_N to (44,40), TP19 NTC to (22,41), and TP18 ACT_3V2 to (29,47) mm. Coordinates are native KiCad board coordinates, viewed from the front.
- Preserved all 108 fitted components, 28 bare debug pads, four mounting holes, rounded outline, connector pin assignments, and the current main-board files.

No protection, supervision or USB-current control was removed simply to reduce the IC count. The three independently regulated rails and existing main-board interface remain. A materially simpler architecture would require another design revision and renewed electrical review.

## Electrical review and limits

| Function | Reviewed design | Qualification still needed |
|---|---|---|
| Battery charging | BQ24075**T**RGTR; about 0.303 A nominal charge current, screened 0.271–0.332 A | Selected cell's charge limit, thermal rise, charge termination, source/load interaction |
| Temperature interlock | Semitec 103AT-2, 10 kΩ, with R74/R75 bias network; nominal thresholds about 4.8°C and 40.0°C; open/short inhibits charging | Bonded thermistor thermal lag and actual pack limits; screened corners extend roughly 2.9–42.2°C |
| USB-C input | TUSB320LAI GPIO sink detects advertised current; dedicated 3.3 V CC supply; high-current mode only for adequate advertisement | Attach/unplug transients, weak chargers, cable behavior, total input current |
| USB-A/default input | TPS22950**YBHR**, base variant, nominal 50 mA limiter; datasheet range approximately 34–66 mA, plus upstream loads | Startup and host behavior. No USB enumeration, suspend detection or BC1.2; not a claim of universal USB compliance |
| USB-C charge-path limit | BQ24075T programmed around 1.23 A, screened maximum about 1.32 A | Full toy load plus charging may exceed input budget; the battery may supplement |
| Battery protection | DW01A, three parallel FS8205 dual-FET banks, 4 A fuse; separate protected return | Pack, fuse and protection-trip coordination; short-circuit recovery and FET heating |
| System cutoff | TPS259530, nominal approximately 3.27 A limit; SYS_RAW UVLO about 3.38 V rising / 3.10 V falling | Threshold tolerance, loaded battery sag, startup and hysteresis |
| Rails | TPS63060 converters: MCU_5V, LOGIC_3V3 and ACT_3V2; output gates and independent voltage supervision | Regulation, ripple, startup/stop sequencing, transients and thermal margin into the actual toy |

The calculation sheet is a screening exercise, not a simulation or measurement. Working load targets are 5 V at 0.6 A, 3.3 V at 0.4 A and 3.2 V at 0.5 A (5.92 W combined). These are **not validated output ratings**. At low battery voltage the combined load can require roughly 2.5 A; test the complete current path, not just each converter separately. Confirm effective ceramic capacitance under DC bias and the board house's actual copper stackup.

The independent voltage monitor is retained: a converter's power-good behavior is not a substitute for verifying all three output voltages. Equal output-gate timing capacitors do not prove safe sequencing between the ESP32 module's onboard regulator and the external logic rail. Scope startup/shutdown and measure GPIO back-powering before attaching a populated main board. Exact SuperMini module revisions may differ.

Manufacturer references: [BQ24075T](https://www.ti.com/lit/ds/symlink/bq24075t.pdf), [TUSB320LAI](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf), [TPS22950](https://www.ti.com/lit/ds/symlink/tps22950.pdf), [TPS63060](https://www.ti.com/lit/ds/symlink/tps63060.pdf). Other selected manufacturer datasheets are retained with the CAD project and linked in the BOM. Availability, permitted substitutions and assembler inventory are not yet approved.

## Connector and assembly instructions

| Connector | Pin assignments | Important restriction |
|---|---|---|
| J1 USB-C | Charging input only; data/SBU pins deliberately NC | Does not communicate with the ESP32 |
| J2 battery, JST VH 2-pin | 1 CELL_PLUS; 2 BAT_NEG | **BAT_NEG is not system GND. Never bypass the low-side protection by bonding them externally.** |
| J3 to main-board J1, JST XH 4-pin | 1 MCU_5V; 2 GND; 3 LOGIC_3V3; 4 ACT_3V2 | Wire pin-for-pin. Front view left-to-right is 3V2, 3V3, GND, 5V because the header is rotated |
| J4 thermistor, JST PH 2-pin | 1 NTC; 2 GND | Bond and electrically insulate the thermistor against the cell; do not substitute a fixed resistor for normal use |

Use the native assembly drawings, reference designators and pad-1 marks. The placement CSV explicitly uses board coordinates with Y increasing downward; it is a reference table, **not an unreviewed machine-ready centroid conversion**. Have the assembler verify rotation and polarity for every IC, FET, diode, connector and switch against its actual reel/part drawing. Bare TP pads and mounting holes are not fitted parts. All fitted electrical components are on the front; test pads are on the rear. The power board is factory SMT assembled, not a student through-hole soldering exercise.

`BOM_AND_PLACEMENT.csv` uses the down-positive CAD coordinates described above. `POSITIONS_NATIVE.csv` is KiCad's native mm placement export (Y values are negative for this board origin); do not mix these coordinate conventions. Both include all 108 fitted parts. THT/mixed connector and switch operations need separate assembler handling. Drawings separate silkscreen labels from component-body/fab references to avoid double-printed text; bottom assembly views are mirrored for viewing from the back. Copper-layer drawings are viewed from the front.

Suggested mating hardware for each power-to-main harness: two JST XHP-4 housings and eight SXH-001T-P0.6 contacts with 22 AWG wire. Battery mating housing VHR-2N with two SVH-21T-P1.1 contacts and 20 AWG wire, subject to the selected battery's connector/polarity and insulation diameter. Thermistor mating housing PHR-2 with two SPH-002T-P0.5S contacts and suitable 28 AWG insulated leads. Check the current JST terminal drawing, crimp tooling, wire and insulation ranges before assembly. Matching pitch alone is not sufficient; do not mate unrelated connector families.

Battery selection is still open: conventional **1S, 4.2 V maximum** Li-ion/LiPo, provisionally at least 4 A continuous discharge capability and at least 0.34 A permitted charging, with documented temperature limits. Capacity, physical fit and protection coordination must be finalized before testing a real cell. The board does not establish safe reverse-battery behavior; verify the harness polarity before connecting it. Shell, mounting screw lengths and standoffs require physical fit checks. A 3D rendering is not dimensional certification; some stock models remain unavailable.

## Fabrication/assembly acceptance gate

Request **five engineering samples**, four copper layers, 50 × 50 mm, 1.6 mm nominal thickness, R3 corners and four 2.2 mm M2 clearance holes. Confirm layer order F.Cu / In1.Cu / In2.Cu / B.Cu, finished copper weights, drill plating and soldermask registration with the manufacturer. The CAD rules permit 0.15 mm traces and 0.20 mm drilled vias; some package clearances are fine-pitch exceptions to wider routing clearances.

The TPS22950 YBH footprint is a 0.4 mm-pitch six-ball WCSP with approximately 0.2 mm pads. Other small packages include 0.4/0.5 mm-pitch QFNs. **Do not substitute TPS22950C/L or another package without reviewing both behavior and footprint.** The selected base device supports the low USB-A current-limit setting.

The board has vias in surface-mount pads, including small parts and thermal pads. The accompanying CAD audit lists them. Ask for **filled, capped, planarized via-in-pad construction**, appropriate fine-pitch finish/stencil processing and assembler approval of the WCSP. Simple via tenting is not equivalent. Confirm whether X-ray inspection is available for hidden joints. If these processes exceed the five-board budget, stop before ordering: relocating vias or changing the current-limiter package is a layout/circuit revision, not a fabrication checkbox.

Ask the assembler to approve the BOM, substitutions, stencil apertures, centroid conversion, polarity and THT secondary operations. Do not send an old FACTORY.zip or a two-layer stackup. The current package is a DFM/engineering review package, not authorization for unreviewed substitutions or mass production.

## Current-limited first-power-up

1. Inspect under magnification before power. Verify IC orientation, hidden-joint inspection results, polarity, solder bridges and connector pin numbering. Check rail-to-ground resistance and confirm BAT_NEG is not accidentally hard-bonded to GND. Investigate unexpected readings rather than assuming a universal resistance threshold.
2. Keep the real cell and main board disconnected. Use a current-limited battery simulator at J2, positive to pin 1 and negative to pin 2. Begin at 3.7 V with the toy switched off and a low current limit (about 50 mA); verify expected idle behavior before increasing the limit. Protection may need its documented recovery sequence; do not bypass it.
3. Switch on with an appropriate bounded current limit. Measure all three J3 outputs before attaching loads. Target nominal 5.0/3.3/3.2 V; investigate deviations beyond ±5%, and reject actuator transients above the attached components' maximum (3.3 V target ceiling for this design). Measure ripple and overshoot with short probe grounds. A current limit that is too low can itself cause startup cycling.
4. Increase dummy loads gradually, first separately and then together toward the screening targets. Record input current, rail voltage, ripple and converter/charger/FET/fuse temperatures at high and low battery voltage. Test UVLO and recovery using the simulator; never deliberately overdischarge a real cell.
5. For charging tests with USB attached, use a **sink-capable/bidirectional battery emulator** or a qualified cell with its bonded NTC. An ordinary bench supply usually cannot absorb charging current and must not be used as a battery substitute while the charger is active.
6. Check USB-A/default input limit, USB-C default/1.5 A/3 A advertisements, attach/unplug, weak-source behavior and absence of damaging reverse feed. Confirm the default path does not request high current. Measure upstream CC/LED current as well as the limiter current. This does not establish USB certification.
7. Verify charging current, termination, NTC open/short inhibition and measured temperature thresholds using controlled test equipment. Check low-battery cutoff, current-limit behavior and recovery with a current-limited simulator, not uncontrolled shorting of a cell.
8. Scope rail rise/fall ordering and GPIO leakage/back-power behavior using the actual ESP32 module and main-board load model before full connection. Then test Wi-Fi bursts, SD writes, motor starts, IR, RGB and audio together. Stop for overheating, oscillation, unexpected current or out-of-range voltages.
9. Do **not** connect the ESP32's USB power and external SYS_IN simultaneously until reverse-feed paths are qualified. Charging USB on the power board is separate and has no data path. Update firmware over Wi-Fi, or program the removable ESP32 with the main-board supply disconnected.

Record results for all five serial-numbered boards. Retain one as the comparison unit. Successful ERC/DRC and routing do not replace these measurements or toy/product safety and EMC review. Do not distribute the samples as finished student products.
