# Charging-only power-module revision — pre-schematic assessment

2026-09-11. Status: proposed engineering direction, not a released circuit or purchasing BOM.

## Scope fixed by the user

- External USB-C is power/charging only. No USB data routing, internal USB cable, or USB communication circuitry is to be added.
- Keep the C.5 main PCB unchanged. Its four-pin JST-XH input is authoritative: 1 = MCU_5V, 2 = GND, 3 = LOGIC_3V3, 4 = ACT_3V2.
- Keep charging, cell protection and conversion on the separate power module. The existing power module is an SMT assembly; this does not add student-soldered SMT to the main board.
- Physical battery selection remains deferred, but electrical battery requirements must be established before releasing the power design.
- This document lists changes before altering the schematic/PCB. Neither has been altered in this assessment.

## Existing design and newly identified constraint

The existing MCP73871-2CCI/ML charger feeds a switched, unregulated two-pin SYS_OUT. It does not generate any of the three regulated rails. USB data pins are intentionally unconnected. SEL is low, PROG2 high, and PROG1 has 3.3 kohm: nominal USB input ceiling 500 mA and charge setting about 303 mA, subject to system demand and thermal regulation.

**A regulator addition alone is not sufficient qualification.** MCP73871 datasheet section 6.1.1.7 recommends system load no greater than the lesser of 1 A and the selected cell's discharge capability. Its internal battery-to-system diode is described as supporting up to 2 A, with thermal shutdown possible. That is not a blanket 2 A continuous design rating. The existing C&K JS102011SAQN series switch is rated 0.3 A at 6 VDC and must not remain the unqualified whole-system current path.

The charger need not automatically be replaced: retaining it depends on demonstrating a load envelope within its recommended operating/thermal limits. A higher-capacity power-path design is the alternative if that cannot be demonstrated. Do not bypass the charger power path by simply moving the load onto the cell; that changes charge termination and protection behavior.

## Preliminary converter sizing envelope

These are deliberately labeled **engineering screening allowances**, not measured consumption, final guaranteed rail ratings, or a statement that all loads draw this current continuously.

| Output | Screening allowance | Power | Loads |
|---|---:|---:|---|
| 5.0 V | 0.60 A | 3.00 W | SuperMini including its onboard regulator; RGB common anode |
| 3.3 V | 0.40 A | 1.32 W | Display, SD, expander, IR and RGB-driver logic |
| 3.2 V | 0.50 A | 1.60 W | Audio and motor, including transient allowance |
| Simultaneous screening total | — | 5.92 W | Not a measured operating point |

At a hypothetical 3.0 V converter input and 85% efficiency, this envelope requires 5.92/(3.0*0.85) = **2.32 A**, before other losses. It therefore cannot be claimed compatible with the old charger path. Even a 3 W actual load would require about 1.18 A under those assumptions. Build a realistic simultaneous load model before deciding how much of the screening allowance must be supported.

The selected motor document specifies 80 mA maximum rated current and 120 mA maximum starting current under its stated conditions. Display-module current, SD-card write peaks, delivered SuperMini behavior and usable audio volume remain sample-dependent. Converter current-limit numbers must not be substituted for guaranteed output-current capability.

## Proposed changes, in order

1. **Close the load budget and source path first.** Check simultaneous operation, startup/inrush, low-battery current, charger loss and battery supplementation. Determine whether the existing charger can be retained or needs a higher-capacity replacement. Do not assume charging continues at full rate during gameplay.
2. **Add regulated outputs.** Use converters that regulate across both battery-powered SYS and USB-powered SYS. A plain boost cannot regulate downward; a plain LDO/buck cannot maintain a rail when SYS falls below the necessary headroom. Compare direct per-rail buck-boost against a shared intermediate rail for cost, efficiency, fault behavior and noise.
3. **Replace the load-current role of SW1.** Prefer retaining its physical control function while switching converter enables or a properly rated electronic disconnect. Off must stop the toy while leaving charging available. Account for quiescent drain and unintended power through signal/status paths.
4. **Add the four-pin regulated output and defined harness.** Match the main-board JST-XH pin numbering; include mating housings, contacts, wire gauge, labels and a continuity test. Keep any reusable raw SYS output distinctly labeled and mechanically incompatible where practical. No USB data pins are needed.
5. **Coordinate startup, brownout and shutdown.** Common enable alone does not prove safe sequencing. The MCU's internal 3.3 V regulator and external logic supply can rise/fall differently. Verify I/O injection limits, discharge paths, rail faults and reset behavior without assuming an unavailable MCU reset connection on this four-wire interface.
6. **Review cell protection and temperature sensing.** Check DW01A/FS8205 current/thermal behavior, connector limits and pack polarity. Preserve BAT_NEG versus protected GND separation. Set normal low-battery shutdown above emergency protection cutoff, with hysteresis to avoid restart cycling. Final thresholds/charge current must agree with the approved cell.
7. **Keep USB power rules explicit.** Leaving data disconnected does not authorize drawing arbitrary current from a computer or USB-C supply. Retain conservative operation or add appropriate source-current detection/control if more input power is required. No USB-PD voltage negotiation is assumed.
8. **Add filtering and accessible test points.** Include VBUS, battery positive, protected ground, raw SYS, all regulated rails, enable/power-good and temperature-sense points. Clearly distinguish raw battery-negative probes. Size bulk capacitance and soft start together; do not rely on capacitors to sustain an undersized source indefinitely.
9. **Rework layout only after the above circuit choices.** Keep switcher loops short, provide charger/converter thermal copper, keep feedback away from switching nodes and protect connector access. The old approximately 30 x 40 mm board size is not yet guaranteed for the revised assembly.
10. **Verify and qualify.** Repeat ERC/DRC/parity, then test with a current-limited source and battery simulator before a cell. Cover no battery, depleted battery, source removal, charging plus gameplay, motor startup, audio noise, SD writes, shutdown, reverse feeding and temperature.

## Regulator shortlist — not yet a selected BOM

- **TI TPS63070**, adjustable buck-boost: candidate for 5 V, with broad input range. Its advertised 2 A boost output is conditional on 4 V input/5 V output; verify low-input current and layout/thermal performance for this design.
- **TI TPS63802**, adjustable buck-boost: candidate for separate 3.3 V and 3.2 V outputs. Its 5.5 V maximum recommended input needs review against the complete SYS and transient envelope. Evaluate PWM/PFM behavior, ripple and possible reverse-current operation. Datasheet protections do not make external-source backfeeding safe by assumption.

A 3.2 V output must have a defined total tolerance/ripple/overshoot budget: the motor document specifies a 3.3 V maximum operating voltage. Shared nominal enables and nominal resistor values do not close these issues. No exact inductors, compensation/support passives or final footprints are selected yet.

## Unchanged-design evidence

At assessment time, native KiCad checks reported zero ERC violations, zero DRC violations, zero open connections and zero schematic/PCB parity issues under the existing project settings. These checks do not validate the new power requirements.

SHA-256 of unchanged source files:

- Power schematic: `8a544722583fc994f665f53255b7053021f6a8add73af85a513a50f3e8a08506`
- Power PCB: `36233b1973132dd5006cd06d59c546c395f8d20f4acbd6d0e8d46eba6b151277`
- C.5 main PCB: `b840262c37afad89ec5307568ace5b6acb4406f89c44c91f1579771642a89003`

## References

- [Microchip MCP73871 datasheet, particularly section 6.1.1.7](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP73871-Data-Sheet-DS20002090F.pdf)
- [C&K JS switch datasheet](https://www.ckswitches.com/media/1422/js.pdf)
- [TI TPS63070 datasheet](https://www.ti.com/lit/ds/symlink/tps63070.pdf)
- [TI TPS63802 datasheet](https://www.ti.com/lit/ds/symlink/tps63802.pdf)
- [Selected motor manufacturer specification](../KK_main_module/component_review/datasheets/motor.pdf)
- [Current main-board circuit review](../KK_main_module/C5_relayout/CIRCUIT_REVIEW.md)

No revised manufacturing files, new circuit performance claims, hardware tests or battery approval are issued by this assessment.
