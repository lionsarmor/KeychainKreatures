# Upload power BOM

Upload **UPLOAD_POWER_P4_BOM.csv**. It is a byte-identical copy of the issued grouped BOM, with MPNs, references, footprints, assembly type, quantity per board and total for five boards **without attrition**.

Confirm order quantity 5; do not treat the five-board column as a per-board quantity. PCBWay must quote purchasing minimums, setup losses and spare parts separately. Expect 108 fitted positions per board (540 fitted placements across five boards).

Confirm manufacturer and exact orderable part for every line, especially generic part identifiers such as SMAJ5.0A, DW01A and FS8205. Missing distributor codes/manufacturer fields must be resolved with sourcing; they are not permission to substitute. Use the supplied datasheets in the full package. U13 must remain TPS22950YBHR base variant.

The source J3 description retains the legacy text “C.5 SYS_IN / XH”; it is the same current keyed connector for C.6 pairing, not a request to order C.5 hardware. Do not change its MPN/pinout.

KIT EXTRAS, battery, cell thermistor, wiring and the student main-board parts are not part of these 108 power-board positions and are not automatically ordered here. No battery is selected.
