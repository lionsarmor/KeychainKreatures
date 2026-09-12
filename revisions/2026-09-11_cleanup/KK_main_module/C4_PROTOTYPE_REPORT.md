# C.4 — relocated, socketed RGB and populated 3D viewer

**Historical revision, superseded by [C.5](C5_relayout/REPORT.md).** C.4 native sources are preserved under `pcb/backups/pre_c5_relayout/` and its fabrication outputs under `archive/C4_manufacturing_superseded/manufacturing/`. Root project and manufacturing paths now refer to C.5.

The RGB LED D3 is on the right, just below the ESP32, as approved. Center: **69, 37.75 mm** from the board's top-left coordinate origin; its four-pin row is vertical, pin 1 at the lower end. Board size remains 80 × 115 mm. The ESP32 antenna keep-outs, all other component locations, mounting holes and top-entry JST connectors are unchanged. D1 remains infrared.

## Changes

- D3 gets a PPTC041LFBN-RC removable four-pin socket, 1.05 mm PCB drills and clear pin-order markings. The 2.54 mm formed LED pitch remains. Actual LED-to-socket contact fit and retention must be tested; this is not a qualified production interface yet.
- All 98 electrical positions now have visible 3D models. New models include the RGB/socket, soft buttons, ceramic capacitors, IR receiver, plug-in modules and their socket/header stacks. DIP chips now appear seated in their sockets. Electrolytic models use the selected 11 mm body height.
- Four LED branches rerouted. Five interfering segments on the motor supply/return and backlight-control nets were replaced by three local detours. Unrelated routed copper is retained. Three incomplete ground thermals at SW7:C, SW9:D and C4:2 were replaced by explicit 0.6 mm ground connections; their direct pour connection is disabled locally, not their electrical ground connection.
- Two GND pours refilled. Circuit pin/net mapping is unchanged. Main-board assembly remains through-hole; replaceable MCU, display, SD reader, DIP chips and RGB are socketed. Passives/small transistors stay soldered; speaker/motor unplug at JST connectors.
- Schematic footprint assignment, C.4 BOM with the added socket, assembly guide, fit sheets, 3D previews and STEP assembly updated. Older C.3 fabrication ZIP is archived; use only the C.4 prototype package for this board.

## Checks and limits

Fresh ERC, DRC, unconnected-item and schematic-parity reports are in `pcb/c4_final_*.json` and the fabrication package. [Independent verification](pcb/C4_FINAL_VERIFICATION.json) checks unchanged pin/net mapping, retained unrelated routes/placements, footprint IDs, through-hole pads and visible/resolvable models for every electrical position. The [manufacturing manifest](manufacturing/MANIFEST.json) records the source snapshot and export hashes.

The existing bare-TP courtyard rule and five inherited ignored DRC categories are unchanged and disclosed in the manifest. D3 introduces no new clearance-rule waiver: its courtyard is the board-level socket housing; the elevated LED envelope is reviewed separately in 3D.

The 3D assemblies are dimensioned nominal models, not proof of physical fit. [Model provenance and limitations](3dmodels/README.md) distinguishes manufacturer package dimensions from provisional seller-module envelopes. RGB height is approximately 22.1 mm above the PCB in the proposed stack. Actual LED socket retention, all module/header heights, wire bends, lens orientation and mechanical support need a physical sample check before shell design or a kit-production batch. Speaker/motor/cable/battery locations are not invented in the model.

Power-module development, firmware, speaker rating and all powered/thermal/RF testing remain pending. No power-board file was changed and no order was placed. This remains an engineering prototype, not a factory-qualified student product. J1 still requires coordinated regulated 5 V, 3.3 V and 3.2 V rails; never connect raw battery or USB and SYS_IN together.

Open the root KiCad project after closing/reloading stale editor tabs. [Front 3D](pcb/c4-front-3d.png) · [Rear 3D](pcb/c4-back-3d.png) · [Angled view](pcb/c4-iso-3d.png) · [STEP assembly](pcb/KK_main_module_C4_assembly.step) · [Printable BOM](assembly/C4_BOM_PRINT.html).
