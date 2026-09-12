# Documentation index — main C.6 / power P.3

Start with the [repository overview](../README.md) and [project/file map](../START_HERE.md). This index distinguishes current build instructions from preserved historical work.

## Current build and release documents

| Topic | Current document |
|---|---|
| Main assembly, orientation and wiring | [C.6 assembly guide](../KK_main_module/C6_flat_stack/assembly/ASSEMBLY_GUIDE.md) |
| Main electrical parts | [C.6 BOM by reference](../KK_main_module/C6_flat_stack/assembly/C6_BOM_BY_REFERENCE.csv) |
| Sockets, modules, mating plugs and hardware | [Complete main+power kit extras](../KK_main_module/C6_flat_stack/assembly/C6_COMPLETE_KIT_EXTRAS.csv) |
| Power BOM, positions and maps | [P.3 release checks](../KK_power_module/P3_matching_stack/release_checks/) |
| Power assembly and bench procedure | [P.3 review and first-power-up](../KK_power_module/P3_matching_stack/assembly/P3_REVIEW_AND_TEST.md) |
| Factory process requirements | [Main C.6](../KK_main_module/C6_flat_stack/FABRICATION_REQUIREMENTS.md) · [Power P.3](../KK_power_module/P3_matching_stack/FABRICATION_REQUIREMENTS.md) |
| Printable mechanical review | [Stack review PDF](C6_P3_STACK_REVIEW.pdf) |
| Actual-size main fitting | [Front PDF](../KK_main_module/C6_flat_stack/assembly/C6_front_FIT_100_PERCENT.pdf) · [Back PDF](../KK_main_module/C6_flat_stack/assembly/C6_back_FIT_100_PERCENT.pdf) |
| Design changes and unresolved limits | [Flat-stack review](FLAT_STACK_REWORK.md) |
| Source and release integrity | [Release index/hashes](C6_P3_RELEASE_INDEX.json) · [Static audit](C6_P3_STATIC_AUDIT.json) · [Drill alignment](C6_P3_DRILL_ALIGNMENT_AUDIT.json) |
| Prototype test record | [C.6 acceptance worksheet](../KK_main_module/C6_flat_stack/assembly/C6_BENCH_TEST_RECORD.csv) |
| Safe project tooling | [Tools](../tools/README.md) · [Contributing](../CONTRIBUTING.md) |

Current releases and ZIPs are immutable snapshots. Later documentation updates at the repository root do not change the hash-verified snapshot contents or imply another electrical review. After any CAD edit, repeat native checks and issue a new source-bound manufacturing revision.

## Historical documents

`POWER_PROTOTYPE_REVIEW.md`, `POWER_FINAL_SCAN_2026-09-12.md` and `POWER_FABRICATION_REQUIREMENTS.md` describe **P.2**, not the P.3 physical layout. `CLEANUP_REPORT.md` records earlier folder moves. Source notes in `source_material/` record user input and earlier design goals, not overrides of later decisions. Component investigations, older BOMs, route attempts and archived manufacturing files remain historical evidence.

Use [revisions/README.md](../revisions/README.md) and its move manifests for recovery. Do not rewrite an old signed report to make it appear to have checked a new design. Do not mix older upright-resistor instructions, 84 × 95 mm main or 50 × 50 mm power Gerbers into the current 96 × 105 mm stack.

Native CAD checks passed, but factory DFM/supply approval, physical fit, battery/case selection and powered testing remain open. These are engineering samples, not finished student toys.
