# Keychain Kreatures — current C.6 / P.4 prototype projects

Main C.6 is **96 × 105 × 1.6 mm**, R4. Compact power P.4 is **50 × 50 × 1.6 mm**, R3. Each has four 2.2 mm M2 holes, but they require separate supports. Main-board resistors, electrolytics and TO-92 bodies lie flat; sockets, buttons and optical parts retain their necessary height.

| Board | Open this KiCad project | Manufacturing package |
|---|---|---|
| Main C.6, two layers | [KK_main_module.kicad_pro](KK_main_module/KK_main_module.kicad_pro) | [Full five-prototype review ZIP](KK_main_module/manufacturing/KK_MAIN_C6_P4_PAIRING_5_PROTOTYPE_REVIEW_2026-09-12.zip) · [Gerbers/drills ZIP](KK_main_module/manufacturing/KK_MAIN_C6_P4_PAIRING_GERBERS.zip) |
| Power P.4, four layers | [KK_power_module.kicad_pro](KK_power_module/KK_power_module.kicad_pro) | [Full five-prototype review ZIP](KK_power_module/manufacturing/KK_POWER_P4_5_PROTOTYPE_REVIEW_2026-09-12.zip) · [Gerbers/drills ZIP](KK_power_module/manufacturing/KK_POWER_P4_GERBERS.zip) |

These are **engineering prototype review files, not a qualified finished toy**. Read each package's fabrication requirements before ordering. Power requires assembler approval of fine-pitch WCSP/QFN parts and filled/capped/planarized via-in-pad processing. Physical module/plug fit, final stack spacing, battery selection and powered validation remain open. No order has been placed.

## Assembly and verification

- [Main assembly/wiring guide](KK_main_module/assembly/ASSEMBLY_GUIDE.md) · [Main reference BOM](KK_main_module/assembly/C6_BOM_BY_REFERENCE.csv) · [Complete paired-kit extras](KK_main_module/assembly/C6_COMPLETE_KIT_EXTRAS.csv)
- [Power assembly and current-limited first-power-up](KK_power_module/assembly/P4_REVIEW_AND_TEST.md) · [Power reference BOM/placement](KK_power_module/release_checks/BOM_AND_PLACEMENT.csv)
- [Printable stack review](docs/C6_P4_MECHANICAL_REVIEW.pdf) · [Main front actual-size fit](KK_main_module/assembly/C6_front_FIT_100_PERCENT.pdf) · [Main back actual-size fit](KK_main_module/assembly/C6_back_FIT_100_PERCENT.pdf)
- [Release index and ZIP hashes](docs/CURRENT_RELEASE_INDEX.json) · [Independent two-board static audit](docs/CURRENT_STATIC_AUDIT.json) · [Design changes and limits](docs/FLAT_STACK_REWORK.md)

Current native ERC/DRC, opens and schematic/PCB parity must all be zero, with hashes matching the supplied releases. Run `node tools/check_project.mjs` for a lightweight consistency check; it does not rerun native checks or prove electrical performance. Do not use a ZIP after editing its source CAD without a fresh release.

Power J3 → main J1 is pin-for-pin: **1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2**. Main cannot take raw battery power. Power TP3 BAT_NEG is not TP4 GND. Charger USB has no data path; do not connect the ESP32 USB and external main rails simultaneously until backfeed is qualified.

## Project organization

`KK_main_module/` contains only the current C.6 project and its supporting files; `KK_power_module/` contains P.4. No extra revision subfolder is needed to reach either current board. Each has local libraries/models, datasheets, assembly documents, final reports and `release_checks/`. The `manufacturing/` subfolders contain the new C6/P4 review packages and Gerber/drill ZIPs. Prior issued packages remain unchanged in the compact-revision archive. Complete-kit extras apply once per main+power pair.

All old root CAD, C5_relayout, P2_compact, failed route candidates, obsolete guides and one-off generators are packed in [revisions/2026-09-12_current_only](revisions/2026-09-12_current_only/). The move manifest verifies recovery paths and unchanged source/package hashes. Older manufacturing archives remain under `revisions/2026-09-12_C6_P3_release/`. Open the exact current paths above, not entries from KiCad's old recent-project history.

Do not rerun archived placement/routing scripts on finished boards. Native CAD is authoritative. The current P.4 promotion changes the power outline and its absolute placement coordinates, not the circuit. Main C.6 CAD stays unchanged. Both review packages are refreshed; see the current release index. Historical move manifests remain recovery evidence.
