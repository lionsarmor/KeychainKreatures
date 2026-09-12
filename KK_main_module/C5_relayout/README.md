# C.5 compact landscape revision

**Completed CAD prototype pass; physical qualification remains pending.** The checked C.5 board is now also the root project. C.4 sources and manufacturing outputs are preserved under `../pcb/backups/pre_c5_relayout/` and `../archive/C4_manufacturing_superseded/`.

84 × 95 mm rounded board; landscape screen above a left D-pad, right action buttons and center mode button. Rear ESP32, SD and top-facing IR transmitter/receiver; front RGB. All main-board component soldering remains through-hole, with the selected replaceable parts socketed. Two standard KiCad-library silkscreen logos are included.

The [completion report](REPORT.md) records zero final ERC, DRC, open-connection and schematic-parity issues. The [circuit review](CIRCUIT_REVIEW.md) documents the actual power requirements, electrical assumptions and physical-test holds. Use the [assembly guide](assembly/ASSEMBLY_GUIDE.md), [BOM](assembly/C5_BOM_PRINT.html), [front preview](front-3d.png), [rear preview](back-3d.png) and [prototype fabrication package](manufacturing/KK_MAIN_C5_PROTOTYPE_FAB.zip) together. Do not treat earlier intermediate DRC files as the final result.

Do not run the historical placement scripts on routed files. C.5 generators and their protected snapshots are engineering tools, not an automatic instruction to discard later user edits.
