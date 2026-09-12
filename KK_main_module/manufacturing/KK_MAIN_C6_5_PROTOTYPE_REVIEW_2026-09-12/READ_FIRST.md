# C6 — five engineering samples, not a production approval

Current project: KK_main_module/C6_flat_stack. Open cad/KK_main_module.kicad_pro in KiCad 10 with its standard footprint/3D libraries installed. Local custom symbols, footprints, models and source datasheets are included. Do not use older 84x95 main or 50x50 power outputs. Both revised boards are 96x105 mm; MAIN HAS TWO COPPER LAYERS, POWER HAS FOUR.

fabrication/: Gerbers, separate PTH/NPTH drills, drill maps/report, IPC-D-356. Read FABRICATION_REQUIREMENTS.md and obtain factory DFM approval before ordering. For POWER this includes filled/capped/planarized via-in-pad and 0.4mm WCSP assembly; ordinary tenting is not sufficient. Factory must verify partial land/via overlaps, stencil and hidden joints, rotations and all substitutions.

assembly/: BOM grouped for FIVE (no attrition), reference BOM/placement, test-point and connector maps, schematic PDF, current assembly/test guide, complete paired-kit extras and mounting review. Placement reference CSV uses native X-right/Y-down coordinates; POSITIONS_NATIVE.csv is KiCad's native Y-up export. Neither is approved machine programming; assembler must validate conventions, side, rotations and polarity. Main is a through-hole kit; power is a factory SMT subassembly. Complete-kit extras apply ONCE per main+power pair, not once per board.

drawings/: front/back assembly and body views plus 3D previews. Bottom views are mirrored. Model attachment coverage is not physical certification. Flat capacitors have actual maximum body envelopes, but sockets, buttons and optics still stand above the board. Physical module/plug fit, 20mm trial stack spacing, battery/case/RF clearance and solder-tail trimming need a real mock-up. No STEP model can approve an unselected battery.

verification/: fresh native ERC/DRC/parity, independent audits and hashes. Clean reported CAD checks do not prove charging safety, thermal margin, current capacity, USB compliance, firmware behavior or toy certification. Existing ignored-check settings are recorded verbatim, not claimed as tests performed.

Power J3 -> main J1: pin1 MCU_5V, pin2 GND, pin3 LOGIC_3V3, pin4 ACT_3V2. Never connect raw battery to main. Power TP3 BAT_NEG is NOT TP4 GND. Charger USB carries no data. Do not combine ESP32 USB power with external main rails until backfeed is qualified. USB-A/default charging is deliberately very slow; running load may still discharge the cell. Battery choice, speaker rating and integrated peak-load qualification remain open. Follow the current-limited first-power-up guide; no real-cell testing without a qualified cell/NTC setup.

Nothing has been uploaded, purchased or ordered. SHA256_MANIFEST.json inventories package files; RELEASE_VERIFICATION.json binds current CAD to checks/exports. No failed route candidates or historical Gerbers are included.
