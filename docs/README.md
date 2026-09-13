# Documentation index — main C.6 / power P.4

Start with the [repository overview](../README.md) and [project/file map](../START_HERE.md). This index distinguishes current build instructions from preserved historical work.

## Current build and release documents

| Topic | Current document |
|---|---|
| Main assembly, orientation and wiring | [C.6 assembly guide](../KK_main_module/assembly/ASSEMBLY_GUIDE.md) |
| Main electrical parts | [C.6 BOM by reference](../KK_main_module/assembly/C6_BOM_BY_REFERENCE.csv) |
| Sockets, modules, mating plugs and hardware | [Complete main+power kit extras](../KK_main_module/assembly/C6_COMPLETE_KIT_EXTRAS.csv) |
| Power BOM, positions and maps | [P.4 release checks](../KK_power_module/release_checks/) |
| Power assembly and bench procedure | [P.4 review and first-power-up](../KK_power_module/assembly/P4_REVIEW_AND_TEST.md) |
| Factory process requirements | [Main C.6](../KK_main_module/FABRICATION_REQUIREMENTS.md) · [Power P.4](../KK_power_module/FABRICATION_REQUIREMENTS.md) |
| Printable mechanical review | [Stack review PDF](C6_P4_MECHANICAL_REVIEW.pdf) |
| Actual-size main fitting | [Front PDF](../KK_main_module/assembly/C6_front_FIT_100_PERCENT.pdf) · [Back PDF](../KK_main_module/assembly/C6_back_FIT_100_PERCENT.pdf) |
| Design changes and unresolved limits | [Flat-stack review](FLAT_STACK_REWORK.md) |
| Source and release integrity | [Release index/hashes](CURRENT_RELEASE_INDEX.json) · [Static audit](CURRENT_STATIC_AUDIT.json) |
| Prototype test record | [C.6 acceptance worksheet](../KK_main_module/assembly/C6_BENCH_TEST_RECORD.csv) |
| Safe project tooling | [Tools](../tools/README.md) · [Contributing](../CONTRIBUTING.md) |

Current releases and ZIPs are immutable snapshots. Later documentation updates at the repository root do not change the hash-verified snapshot contents or imply another electrical review. After any CAD edit, repeat native checks and issue a new source-bound manufacturing revision.

## Historical documents

The P.2 reviews, earlier cleanup report and original source notes now live in [the cleanup archive's docs folder](../revisions/2026-09-12_current_only/docs/). They are historical evidence, not current P.4 instructions or overrides of later decisions. Older component investigations/BOMs, failed routes and generation scripts are archived with their original relative paths in the same cleanup archive.

Use [revisions/README.md](../revisions/README.md) and its move manifests for recovery. Do not rewrite an old signed report to make it appear to have checked a new design. Use only current C.6 main and P.4 power packages. P.4 is 50 × 50 mm, but old P.2 files of the same size are not the current release. Main remains 96 × 105 mm; use separate mounting supports.

Native CAD checks passed, but factory DFM/supply approval, physical fit, battery/case selection and powered testing remain open. These are engineering samples, not finished student toys.

The previous oversized P.3 board, C6/P3 packages and shared-hole reports are preserved in [the compact-revision archive](../revisions/2026-09-12_power_compact/P3_previous/). Main C.6 CAD and fabrication geometry are unchanged; its new review package replaces obsolete shared-stack documentation.
