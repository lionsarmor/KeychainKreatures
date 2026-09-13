# Main board — C.6, all resistors flat

Open [KK_main_module.kicad_pro](KK_main_module.kicad_pro) or [KK_main_module.kicad_pcb](KK_main_module.kicad_pcb) directly from this folder. **This is now the current C.6 board, not the old C.5 root.**

96 × 105 × 1.6 mm, two copper layers, R4 rounded corners and its own mounting pattern. Compact power P.4 is 50 × 50 mm and needs separate supports. All 43 resistors are horizontal; ten electrolytics and six TO-92 bodies lie flat. There are 98 fitted through-hole electrical positions and 25 bare debug holes. Sockets, optical parts and buttons retain their functional height.

- [Assembly/wiring](assembly/ASSEMBLY_GUIDE.md) · [Reference BOM](assembly/C6_BOM_BY_REFERENCE.csv) · [Complete paired-kit extras](assembly/C6_COMPLETE_KIT_EXTRAS.csv)
- [Front actual-size fit](assembly/C6_front_FIT_100_PERCENT.pdf) · [Rear actual-size fit](assembly/C6_back_FIT_100_PERCENT.pdf)
- [Manufacturing packages](manufacturing/README.md) · [Verification and maps](release_checks/)
- [Both current projects](../START_HERE.md) · [Archived old designs](../revisions/2026-09-12_current_only/)

Local libraries, models and datasheets sit alongside the project. Install KiCad 10 standard libraries too. Use the current schematic and pin labels for orientation. The prior C5_relayout and old assembly/component-review files are archived, not mixed into this directory.

Prototype only: physical part/plug fit, battery/case selection, peak-load/thermal behavior, firmware and powered safety qualification remain pending. Do not connect raw battery to main J1 or combine ESP32 USB and external rails until backfeed is qualified.
