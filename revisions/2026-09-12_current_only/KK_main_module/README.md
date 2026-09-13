# Main board — current C.6

Open [C6_flat_stack/KK_main_module.kicad_pro](C6_flat_stack/KK_main_module.kicad_pro). **Unversioned CAD files in this folder are preserved C.5 baselines, not the current project.**

C.6 is 96 × 105 × 1.6 mm, two layers, R4 corners, matching P.3 mounting holes. All 43 resistors are horizontal, ten electrolytics and six TO-92 bodies lie flat. There are 98 fitted through-hole electrical positions and 25 bare debugging holes. All fitted positions have resolving 3D model links; actual module/socket/plug fit remains unqualified.

- [Current assembly/wiring](C6_flat_stack/assembly/ASSEMBLY_GUIDE.md)
- [Reference BOM](C6_flat_stack/assembly/C6_BOM_BY_REFERENCE.csv) · [Complete paired-kit extras](C6_flat_stack/assembly/C6_COMPLETE_KIT_EXTRAS.csv)
- [Full review ZIP](manufacturing/KK_MAIN_C6_5_PROTOTYPE_REVIEW_2026-09-12.zip) · [Gerbers/drills](manufacturing/KK_MAIN_C6_GERBERS.zip)
- [Fresh checks, BOM/placement and debugging maps](C6_flat_stack/release_checks/)
- [Both projects](../START_HERE.md) · [Printable fit review](../docs/C6_P3_STACK_REVIEW.pdf)

Prototype only. Use with P.3 regulated power, never raw battery. Do not combine ESP32 USB and external rails until exact-module backfeed is checked. Physical fit, cell/case selection, speaker rating, firmware and integrated electrical/thermal qualification remain open. Historical C.5 assembly/fit documents do not apply to this flat-part revision.
