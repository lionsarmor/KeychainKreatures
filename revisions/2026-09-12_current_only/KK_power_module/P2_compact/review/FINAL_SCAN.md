# Power module P.2 — final artwork and manufacturer review

## Result

Fresh KiCad checks after adding the logos: **0 DRC violations, 0 unconnected items, 0 schematic/PCB mismatches, 0 reported ERC violations.** The native audit confirms 108 fitted parts, 28 rear test pads, 3,515 track segments and 260 vias. The main board was not modified.

Pad numbers, nets, component values, footprint identities, the four-pin main-board power interface and battery-return isolation were checked. An exact comparison of pad/track/via geometry and filled copper before and after the artwork change confirms that the electrical layout is unchanged. This preserves the earlier supply-path review; it does not replace measured testing.

The KiCad and standard open-source-hardware logos are now on the **rear silkscreen**, in the open area above the test pads. They are board-only artwork, excluded from the BOM and placement file. They are not certification marks. The stock OSHW artwork needed the same no-courtyard metadata used by the KiCad logo because it is not a physical component; no electrical/clearance rule was disabled and no DRC finding was excluded.

## Test pads are present

There are **28 labeled, 1.5 mm rear copper test pads**, exposed through soldermask. The package includes their signal names and coordinates in `TEST_POINTS.csv`, a test-pad guide, and a rear assembly drawing. They are bare probe pads, not fitted pins. Ground reference is **TP4 (GND)**. **TP3 (BAT_NEG) is the unprotected cell return, not an interchangeable scope ground.** Use suitable isolated/differential measurements where needed; ordinary grounded equipment can accidentally bypass the protection return.

The pads cover battery/USB input, both sides of the protection/power path, all regulated and switched output rails, charger and thermistor signals, USB-current selection, regulator enables, power-good and fault signals. Do not short adjacent pads with a probe; never conduct fault testing by shorting a real battery.

## What to send

Use the new dated review ZIP, not the previous unmarked-artwork ZIP. It includes four-layer Gerbers, mask/silkscreen/paste/outline layers, separate plated/non-plated drills and maps, IPC-D-356 electrical-test netlist, grouped five-board BOM, native placement CSV, schematic PDF, assembly/copper drawings, test-pad documentation, source CAD/local libraries, datasheets, native checks and file hashes.

This is a **five-unit engineering/DFM review request**. Ask the manufacturer to confirm the mandatory items below before accepting a fabrication/assembly quote. No order has been placed.

## Still open — do not mistake CAD checks for qualification

- Fine-pitch assembly acceptance, including the 0.4 mm-pitch TPS22950 YBH WCSP, and exact BOM availability/substitution approval.
- **Filled, capped and planarized via-in-pad processing.** The CAD has tenting defaults; tenting alone is not an acceptable substitute for the required component-pad via process. The written fabrication requirements must be acknowledged, not inferred from a default upload form.
- Confirmation of the fabricator's four-layer stackup, copper weights, drill plating and stencil/hidden-joint inspection process.
- Actual battery choice, charge/discharge ratings, thermistor attachment, harness crimping/polarity and physical fit.
- Current-limited first-power-up, charging/thermal/fault testing, rail rise/fall sequencing and GPIO back-power checks with the actual main board. Output load targets are not measured ratings.
- Universal USB-host behavior is not established: default USB-A charging is deliberately slow, with no USB enumeration/suspend or BC1.2 implementation. ESP32 USB and external main-board power must not be used simultaneously until qualified.

The detailed electrical review and first-power-up procedure are included as `READ_FIRST_REVIEW_AND_TEST.md`. These are test samples, not finished consumer or student-distribution units.
