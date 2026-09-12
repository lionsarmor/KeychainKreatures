# Keychain Kreatures — current C.6 / P.3 prototype projects

Both boards use a **96 × 105 × 1.6 mm** outline with R4 corners and matching M2 mounting holes. Main-board resistors, electrolytics and TO-92 bodies lie flat; sockets, buttons and optical parts retain their necessary height.

| Board | Open this KiCad project | Manufacturing package |
|---|---|---|
| Main C.6, two layers | [C6_flat_stack/KK_main_module.kicad_pro](KK_main_module/C6_flat_stack/KK_main_module.kicad_pro) | [Full five-prototype review ZIP](KK_main_module/manufacturing/KK_MAIN_C6_5_PROTOTYPE_REVIEW_2026-09-12.zip) · [Gerbers/drills ZIP](KK_main_module/manufacturing/KK_MAIN_C6_GERBERS.zip) |
| Power P.3, four layers | [P3_matching_stack/KK_power_module.kicad_pro](KK_power_module/P3_matching_stack/KK_power_module.kicad_pro) | [Full five-prototype review ZIP](KK_power_module/manufacturing/KK_POWER_P3_5_PROTOTYPE_REVIEW_2026-09-12.zip) · [Gerbers/drills ZIP](KK_power_module/manufacturing/KK_POWER_P3_GERBERS.zip) |

These are **engineering prototype review files, not a qualified finished toy**. Read each package's fabrication requirements before ordering. Power requires assembler approval of fine-pitch WCSP/QFN parts and filled/capped/planarized via-in-pad processing. Physical module/plug fit, final stack spacing, battery selection and powered validation remain open. No order has been placed.

## Assembly and verification

- [Main assembly/wiring guide](KK_main_module/C6_flat_stack/assembly/ASSEMBLY_GUIDE.md) · [Main reference BOM](KK_main_module/C6_flat_stack/assembly/C6_BOM_BY_REFERENCE.csv) · [Complete paired-kit extras](KK_main_module/C6_flat_stack/assembly/C6_COMPLETE_KIT_EXTRAS.csv)
- [Power assembly and current-limited first-power-up](KK_power_module/P3_matching_stack/assembly/P3_REVIEW_AND_TEST.md) · [Power reference BOM/placement](KK_power_module/P3_matching_stack/release_checks/BOM_AND_PLACEMENT.csv)
- [Printable stack review](docs/C6_P3_STACK_REVIEW.pdf) · [Main front actual-size fit](KK_main_module/C6_flat_stack/assembly/C6_front_FIT_100_PERCENT.pdf) · [Main back actual-size fit](KK_main_module/C6_flat_stack/assembly/C6_back_FIT_100_PERCENT.pdf)
- [Release index and ZIP hashes](docs/C6_P3_RELEASE_INDEX.json) · [Independent two-board static audit](docs/C6_P3_STATIC_AUDIT.json) · [Design changes and limits](docs/FLAT_STACK_REWORK.md)

Current native ERC/DRC, opens and schematic/PCB parity must all be zero, with hashes matching the supplied releases. Run `node tools/check_project.mjs` for a lightweight consistency check; it does not rerun native checks or prove electrical performance. Do not use a ZIP after editing its source CAD without a fresh release.

Power J3 → main J1 is pin-for-pin: **1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2**. Main cannot take raw battery power. Power TP3 BAT_NEG is not TP4 GND. Charger USB has no data path; do not connect the ESP32 USB and external main rails simultaneously until backfeed is qualified.

## Project organization

`C6_flat_stack/` and `P3_matching_stack/` are the only current CAD projects. Each contains local libraries, models, datasheets, assembly documents and fresh `release_checks/`. Manufacturing folders contain the current full review package and separate Gerber/drill ZIP. Complete-kit extras apply once per main+power pair.

The unversioned main CAD at `KK_main_module/KK_main_module.*`, its old `assembly/` files and `C5_relayout/`, and power `P2_compact/` remain **historical baseline evidence**, not current manufacturing sources. Old manufacturing outputs are archived under `revisions/2026-09-12_C6_P3_release/`. Close stale KiCad tabs before reopening the exact current paths above.

Do not rerun historical placement/routing scripts on the finished boards. Native CAD is authoritative; original Git staging/deletions were not reset or committed.
