# P4 — five engineering samples; not production approval

Current editable project: KK_power_module at the repository root. This package is the C6/P4 pairing release. Open cad/KK_power_module.kicad_pro with KiCad 10 and its standard libraries. Custom assets and selected datasheets are included.

Main C.6: 96 x 105 x 1.6 mm, R4, TWO copper layers. Power P.4: 50 x 50 x 1.6 mm, R3, FOUR copper layers. Four 2.2 mm mounting holes on each board, DIFFERENT patterns: use independent case supports. Main CAD/fabrication geometry is unchanged; its documentation is refreshed. Do not use the old common-hole/20 mm shared-spacer instructions. Separate 1:1 templates are included; physical placement, antenna clearance, battery location and spacing are not approved.

fabrication/: Gerbers, separate PTH/NPTH drills, maps/report and IPC-D-356 netlist. Obtain factory DFM approval BEFORE ordering. Power requires filled/capped/planarized via-in-pad and 0.4 mm WCSP assembly approval; ordinary tenting is insufficient. No unreviewed substitutions.

assembly/: BOMs, placement, test-point and connector maps, schematic PDF, assembly/bench guides and paired-kit extras. Extras apply ONCE per pair. References to repository-relative datasheets in kit CSVs refer to the full repository; the selected board's datasheets are under cad/datasheets. Reference positions use CAD X-right/Y-down; POSITIONS_NATIVE.csv uses native KiCad Y-up. Assembler must validate rotations, origins, side, polarity and THT secondary operations before machine programming. Main is a student THT kit; power is factory SMT.

drawings/: assembly/body drawings and model previews; bottom views are mirrored. Model coverage is not delivered-part fit certification. verification/: fresh native checks, static audit and source hashes; ignored-check settings are recorded, not hidden.

Power J3 to main J1: 1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2, keyed pin-for-pin. Never connect raw battery to main. Power TP3 BAT_NEG is NOT TP4 GND. Charger USB has no data. Do not combine ESP32 USB power and main external rails until exact-module backfeed is qualified. Firmware and Wi-Fi game uploads are not implemented by this hardware release.

Read P4_REVIEW_AND_TEST.md before powering. Use current-limited equipment; charging tests need a sink-capable battery emulator or a qualified cell/NTC. Actual simultaneous loads, thermal behavior, rail sequencing, USB behavior, protection, speaker rating and physical/RF fit remain untested. The 3.3 V screening target is 0.4 A versus the older main 0.5 A reservation; measure demand and margin. No real cell is selected. No toy-safety or EMC certification is claimed.

RELEASE_VERIFICATION.json binds source CAD, fresh reports and fabrication outputs. SHA256_MANIFEST.json inventories all package files except itself. This package is for review, not an order; no factory submission or purchase has been made.
