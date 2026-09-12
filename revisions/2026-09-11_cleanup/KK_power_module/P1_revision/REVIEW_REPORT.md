# Keychain Kreatures power module P.1 — engineering review

2026-09-11. **NOT FOR FABRICATION. Not a tested or finished power module.**

## What is saved

The native [KiCad project](KK_power_module.kicad_pro), [schematic PDF](SCHEMATIC_DRAFT.pdf), [candidate BOM](BOM_DRAFT.csv), [native ERC report](erc.rpt), [native PCB DRC report](placement_drc.json), and [independent connectivity/calculation audit](VERIFICATION.json) are in this folder. Manufacturer datasheet links are in the BOM and [source index](datasheets/sources.json); this is not a complete set of locally downloaded PDFs.

The root legacy power project and the C.5 main PCB remain unchanged. The legacy manufacturing ZIP is **not compatible with C.5** and must not be ordered for this assembly.

## USB-A and USB-C decision implemented in the draft

| Source | Intended behavior | Important limitation |
|---|---|---|
| Powered computer USB-A, A-to-C cable | Approximately 50 mA nominal charger-input limit; slow charge with toy off | Playing may consume more than the port supplies; no host enumeration or suspend detection |
| USB-C advertising default current | Same conservative input mode | A USB-C connector alone does not authorize higher current |
| USB-C advertising 1.5 A or 3 A | Approximately 1 A nominal input limiter; about 297 mA nominal cell-charge setting | Available charging decreases with system demand and thermal/input regulation |
| Sleeping, switched-off or disabled computer port | Not guaranteed to charge | No promise that VBUS remains present or that this is universally host-compliant |

D+/D− and SBU are deliberately unconnected. No ESP32 data cable, USB-PD voltage request, or BC1.2 charger detection is implemented. This is not USB certification or universal compatibility approval.

U3 TUSB320LAI decodes the USB-C current advertisement. U13 **TPS22950YBHR** provides a separate low-current input limit; the TPS22950C/L variants are not interchangeable at this setting. Its 0.4 mm-pitch WCSP requires factory SMT assembly. U14 TLV75533PDBVR powers the CC circuitry at 3.3 V: raw USB must not feed a detector whose recommended VDD maximum is 5 V. CC pullups use that same rail. Q4/Q5 AO3400A have specified 2.5 V gate-drive operation.

The TPS22950 datasheet gives 34–66 mA at the exact 19.2 kΩ setting under its stated test conditions. The resistor-tolerance screening maximum is about 66.1 mA. A **10 mA overhead allocation** leaves a screening total of about 76.1 mA; that allocation is not a validated bound on CC, LED, TVS and LDO current. Plug-in inrush and current-mode transitions still require measurement.

## Output connection — unchanged main-board interface

Connect power-module J3 to main-board J1 by **pin number**, not wire color or a visual left-to-right guess.

| J3 pin | Main J1 pin | Net | Purpose |
|---|---|---|---|
| 1 | 1 | MCU_5V | Regulated nominal 5.0 V |
| 2 | 2 | GND | Protected common ground |
| 3 | 3 | LOGIC_3V3 | Regulated nominal 3.3 V |
| 4 | 4 | ACT_3V2 | Regulated nominal 3.2 V |

The output connector is JST-XH four-pin. J2 is a **different, higher-current JST-VH two-pin battery connector**; it does not reuse the old PH/XH battery harness. J4 is the two-pin PH thermistor connector. J5 carries service signals at USB/battery-related levels and is **not a direct ESP32 GPIO header**.

BAT_NEG is the cell-side negative connection, not protected GND. Do not bridge these with wiring, a scope ground or a thermistor return: that can bypass low-side cell protection. Use isolated/differential measurements where required. Do not power the ESP32 USB socket and the main supply together until reverse-feed behavior is qualified.

## Circuit changes represented

- BQ24074 charger/power path replaces the legacy part for the screened load envelope; temperature sensing is retained.
- SW1 now carries control current, not the whole toy's current. Charging is intended to remain available with the toy off.
- TPS259530 provides electronic switching, controlled turn-on, current limiting and normal undervoltage shutdown.
- Three TPS63060 buck-boost channels generate the required rails. Forced PWM is selected to avoid relying on a wider power-save voltage tolerance.
- TPS386000 independently monitors raw rail voltages and is powered before the eFuse, keeping normal MR switching within its supply range. Converter PG outputs are diagnostics, **not** substituted for voltage supervision.
- Three TPS22918 output gates provide controlled rises and resistor-limited output discharge. Their common enable does not prove that ESP32/peripheral I/O sequencing is safe.
- DW01A is restricted to the linked H&M Semiconductor part. Three parallel Fortune FS8205 pairs and a 4 A fuse are candidates; current sharing, trip thresholds and fuse coordination are not yet qualified.
- 25 labeled test pads expose rails, protected/cell grounds, controls and fault signals. USB-C now faces the top edge; the side switch actuator faces outward.

## Checks completed — and their limits

| Check | Current result |
|---|---|
| Native schematic ERC | 0 errors, 0 warnings under project settings |
| ERC checks not evaluated | Single-use global labels, four-way joins, SPICE models, footprint filters; see ERC report |
| Native netlist vs design manifest | PASS |
| Independent four-wire mapping to C.5 | PASS |
| Symbol pin sets vs footprint pad numbers | PASS; not a dimensional or solderability approval |
| Native schematic/PCB parity | 0 issues |
| Placement DRC | 0 errors, 0 warnings |
| Independent USB copper-to-NPTH check | 8 pad/hole pairs below the current 0.25 mm rule; manual hold |
| Unconnected PCB items | 301 — expected because the PCB is unrouted, not waived |
| Hardware measurements / switching simulation | Not performed |

The placement study is **70 × 65 mm, four layers**, with 138 electrical footprints including 25 bare test pads, plus four mounting holes. This is a provisional engineering arrangement, not the final enclosure size or a cost-optimized production BOM. Its increased complexity and assembly cost need review before layout freeze. No tracks or ground pours have been presented as a completed power layout. Existing 3D models are incomplete.

### Outstanding placement DRC items


Native placement DRC currently reports no general violations. However, an independent, rotation-invariant footprint check finds approximately **0.185 mm** copper-to-NPTH spacing, below the current **0.25 mm** project rule. KiCad previously reported this gap before the USB connector was rotated; rotation did not change the physical spacing. Treat this as a manual manufacturing hold despite the native result.

Do not shrink USB mechanical holes, move contact pads away from the manufacturer pattern, or globally relax clearances merely to remove a message. Resolve the connector drawing against the chosen fabricator's copper-to-NPTH capability first.

## Required next work, in order

1. Close the realistic simultaneous load budget and compare the present three-converter architecture's size/cost with a shared intermediate supply. Screening allowances are not guaranteed output ratings.
2. Confirm every critical land pattern and the assembler's WCSP/thermal-pad process. Resolve USB drill clearance and complete connector/cable/3D envelope checks. Finish purchasing and mating-harness BOM review.
3. Deliberately place and route charger/converter high-current loops and feedback returns, with thermal copper and a controlled ground return. Ordinary autorouting is not a substitute for this power layout.
4. Fill zones and repeat native ERC, full DRC, open-net and schematic-parity checks. Review layer stack, copper thickness, narrow pin escapes, fuse path and current-carrying vias with the fabricator.
5. Conduct staged prototype qualification below. Only then issue an explicitly versioned prototype/release package; do not reuse the legacy ZIP.

## Staged bring-up and battery qualification

These are future tests, not results. Use a current-limited bench supply, electronic loads and a suitable battery simulator before attaching a real lithium cell or the main board.

- First inspect polarities, exposed-pad joints, resistance between each rail and GND, BAT_NEG isolation, and end-to-end harness pin numbering.
- With toy off, verify legacy input current, thermistor open/short behavior, no-battery behavior and the USB-C detector supply. Scope high-current request from cold plug-in through attachment; it must not authorize high current prematurely.
- Sweep USB source capability and removal/reconnection. Verify total port current, inrush, source-advertisement downgrades, charger input-DPM interaction and automatic recovery. Test USB-A with actual target computers while awake; document sleep behavior rather than assuming it.
- With a battery simulator, sweep the useful cell voltage range and apply individual/simultaneous rail loads. Measure regulation, ripple, overshoot, undervoltage cycling, shutdown discharge, current sharing and temperatures at intended ambient extremes.
- Before a real cell: approve 1S **4.2 V** chemistry, at least **4 A continuous** discharge capability for this draft envelope, charge-current limits, protection/fuse coordination, cable/contact ratings and polarity. The physical battery may be selected later, but these electrical checks cannot be deferred until after connecting it.
- The isolated, cell-bonded thermistor must match the approved battery temperature window. A nominal 103AT-2 with the bare BQ24074 TS thresholds is approximately a 0–50 °C scheme before tolerances, not automatic approval for a cell limited to 0–45 °C. Adjust and qualify the network as needed; never fit a dummy bypass resistor.
- Finally connect C.5 and exercise Wi-Fi, SD writes, full backlight, audio and motor startup together. Measure rail sequencing/backfeed and resets. Confirm the motor supply stays within its actual permitted range including ripple/overshoot.

## Detailed unresolved conditions

- This is an unrouted placement study, not a finished power board. No manufacturing release.
- Full simultaneous 5.92 W screening load needs about 2.74 A at 2.7 V and 80% efficiency. The revised eFuse screening minimum is about 2.99 A; actual load/efficiency/drop/thermal envelope must still be closed before layout freeze.
- H&M DW01A is selected, but parallel-FET current sharing, protection trip thresholds versus temperature, fuse coordination and cell discharge/pulse ratings remain unqualified.
- Battery must be 1S 4.2 V Li-ion/LiPo rated at least 4 A continuous with an isolated cell-bonded 10k NTC; capacity, charge limits, connector polarity and temperature curve must be approved before fitting a cell. VH connector replaces the old PH/XH battery connector.
- Legacy/default USB input is now limited separately, nominally 50mA. The 10mA upstream overhead allocation must be verified including TVS leakage, CC controller, LDO and LEDs; the screening total is not a guaranteed maximum. Verify plug-in inrush, attach/detach and current-advertisement transitions on the bench.
- D+/D- remain unconnected: no enumeration, BC1.2 detection or USB suspend detection. Charging from an active powered USB-A port is targeted, not guaranteed from sleeping/disabled ports. No universal USB-host compatibility or USB certification claim.
- The added CC LDO and pullup arrangement correct the raw-VBUS supply-range issue. Probe the high-current request during cold start: it must remain default-limited until a valid higher-current advertisement is decoded.
- BQ24074 with a bare 103AT-2 NTC has a nominal charge-temperature window around 0 to 50C, with threshold/NTC tolerance. That is not approval for a cell requiring a narrower window: qualify or adjust before battery charging.
- Three soft-start outputs do not prove safe ESP32/peripheral rail sequencing. Actual SuperMini regulator, GPIO backfeed, restart and brownout behavior need measurements. Never power the socketed ESP32 USB and main supply simultaneously before reverse-feed qualification.
- Motor rail static tolerance, ripple and startup overshoot must remain within the actual motor rating; the nominal 3.2 V calculation alone does not guarantee this.
- Manufacturer land-pattern dimensions, bulk-capacitance bias derating, component MPNs, USB ESD and thermal layout remain purchasing/layout review items.
- 3D models are incomplete; current rendering is not a complete assembly or enclosure-fit approval.
- The 0.4mm-pitch TPS22950 WCSP, thermal-pad soldering and USB footprint drill clearances need explicit assembler/fabricator approval; this power board is factory SMT, not a student hand-soldering kit.
- Independent USB footprint geometry check finds approximately 0.185mm copper-to-NPTH spacing, below the present 0.25mm project minimum. Native DRC no longer reports this after connector rotation; the physical gap did not change. This remains a manual manufacturing hold, not a waived or fixed clearance.

## Primary design references

- [BQ24074RGTR](https://www.ti.com/lit/ds/symlink/bq24074.pdf)
- [TUSB320LAIRWBR](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf)
- [TPS259530DSGR](https://www.ti.com/lit/ds/symlink/tps2595.pdf)
- [TPS63060DSCR](https://www.ti.com/lit/ds/symlink/tps63060.pdf)
- [TPS22918DBVR](https://www.ti.com/lit/ds/symlink/tps22918.pdf)
- [SN74AUP1G17DBVR](https://www.ti.com/lit/ds/symlink/sn74aup1g17.pdf)
- [TPS386000RGPR](https://www.ti.com/lit/ds/symlink/tps386000.pdf)
- [TPS22950YBHR](https://www.ti.com/lit/ds/symlink/tps22950.pdf)
- [TLV75533PDBVR](https://www.ti.com/lit/ds/symlink/tlv755p.pdf)
- [AO3400A](https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf)
- [DW01A](https://hmsemi.com/downfile/DW01A.PDF)
- [FS8205](https://www.ic-fortune.com/upload/Download/FS8205-DS-19_EN.pdf)
- [XFL4020-102MEC](https://www.coilcraft.com/getmedia/50632d43-da1b-4cdb-8ab4-3029cab51df3/xfl4020.pdf)
- [JS102011SAQN](https://www.ckswitches.com/media/1422/js.pdf)
- [HC-TYPE-C-16P-01A](https://datasheet.lcsc.com/lcsc/2211161000_HCTL-HC-TYPE-C-16P-01A_C2894897.pdf)
