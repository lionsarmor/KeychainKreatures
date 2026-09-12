# Keychain Kreatures — C.4 RGB engineering prototype

Current main board: **80 × 115 × 1.6 mm**, two layers, R4 corners, filled front/back ground pours, 25 bare debug holes and a separate through-hole RGB mood LED. D1 remains infrared. J1, J4 and J5 are top-entry connectors. Main-board assembly remains through-hole; MCU, screen and SD reader are preassembled plug-in modules.

All 98 electrical positions now have 3D models, including socketed chips, modules and soft buttons. Models are nominal, not certified assembly measurements. The seller-module geometry and RGB socket retention remain provisional. See the [3D accuracy notes](3dmodels/README.md).

## Current files

- [KiCad project](KK_main_module.kicad_pro) · [Routed PCB](KK_main_module.kicad_pcb) · [One-sheet schematic PDF](KK_main_module.pdf)
- [Completion report and remaining qualification](C4_PROTOTYPE_REPORT.md)
- [Print the full BOM](assembly/C4_BOM_PRINT.html) · [Assembly and wiring guide](assembly/ASSEMBLY_GUIDE.md)
- [Debug guide](assembly/C4_DEBUG_GUIDE.md) · [Bring-up record](assembly/C4_BENCH_TEST_RECORD.csv)
- [Prototype fabrication ZIP](manufacturing/KK_MAIN_C4_PROTOTYPE_FAB.zip) · [Fabrication notes](manufacturing/README.md)
- [Datasheet ZIP](assembly/C4_DATASHEETS.zip) · [Datasheet index](assembly/C4_DATASHEETS.md)
- [Front actual-size fit PDF](pcb/front-fit-check.pdf) · [Mirrored back PDF](pcb/back-fit-check.pdf)
- [Front 3D view](pcb/c4-front-3d.png) · [Back 3D view](pcb/c4-back-3d.png)
- [FreeRouting handoff](routing/README.md)

The current BOM accounts for 98 electrical positions, plus kit modules, sockets, mating plugs and wiring. Debug holes and four mounting holes are not fitted parts. The RGB driver is TLC5916IN in an ED16DT socket; D3 is Kingbright WP154A4SEJ3VBDZGW/CA, with leads formed to 2.54 mm pitch and fitted in a PPTC041LFBN-RC socket. The LED is now just below the ESP32 on the right. Do not substitute an arbitrary RGB pin order.

**This is an unpowered engineering prototype, not a factory-ready student product.** J1 requires three coordinated regulated rails; it is not a battery input. Do not connect raw battery, the old power board, or USB and SYS_IN together. Separate power-board development, exact module dry-fit, speaker rating, backlight measurements and powered qualification remain open. Firmware is not supplied by this hardware pass.

Close/reload any stale KiCad editor tabs before saving. The root board/schematic and C.4 BOM are authoritative. Earlier C.2 reports, shopping lists, placement scripts and routing candidates are history, not current build instructions. Backups are retained under `pcb/backups/`; C.2/C.3 fabrication files are archived under `archive/`. Do not import an old SES or rerun historical placement generators over the root board.
