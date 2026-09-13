# Historical revisions — do not manufacture from here

The [2026-09-11 cleanup archive](2026-09-11_cleanup/) preserves the original relative project paths. No archived design is the current project.

- `KK_power_module/`: legacy two-wire power board, P.1, previous backups, old fabrication outputs and original engineering scripts.
- `KK_power_module/P2_compact/`: abandoned P.2 routing candidates and intermediate board snapshots. These routes were not imported or qualified.
- `KK_main_module/`: superseded reports, BOMs, routing candidates, older schematic capture, backups and former archives.

The current projects remain outside this directory; open them through [START_HERE.md](../START_HERE.md).

## Current-only folder cleanup

[2026-09-12_current_only](2026-09-12_current_only/) holds the former C.5 main root, C5_relayout, P2_compact, old main assembly/component investigations, intermediate C.6 routes, historical documents and one-off generators. [MOVE_MANIFEST.json](2026-09-12_current_only/MOVE_MANIFEST.json) records each move and protected current CAD/ZIP hashes. Active C.6/P.3 now sit directly in their module folders.

Archived relative compatibility symlinks preserve their original text and may not resolve from their new archive location. Recover a historical project into a separate scratch tree using the manifest; do not copy it over current CAD. No material content was deleted.

## C.6 / P.3 release archive

[2026-09-12_C6_P3_release](2026-09-12_C6_P3_release/) preserves the superseded C.5/P.2 manufacturing directories, ZIPs and reports, plus the previous Desktop print sheet and the C.6/P.3 preflight ZIPs before final documentation cleanup. None of those ZIPs is the current release. [MOVE_MANIFEST.json](2026-09-12_C6_P3_release/MOVE_MANIFEST.json) distinguishes moves from preserved copies and records exact hashes. No baseline CAD was deleted or overwritten.

## Recovery

[MOVE_MANIFEST.json](2026-09-11_cleanup/MOVE_MANIFEST.json) records each original path, new path and per-file SHA-256 hash. Every move was verified. Active CAD/library/model hashes were checked separately to establish that cleanup did not modify them. Nothing was deleted.

For recovery, copy the desired archived files to a **separate scratch project**, preserving their recorded original relative paths. Include corresponding libraries/models and any generator inputs. Do not overwrite the current projects. Archived generation scripts retain original paths and are historical source, not working commands in their relocated tree. Never run them over current CAD.

The former compatibility symlinks at `KK_main_module/archive`, `KK_main_module/pcb/backups` and `KK_main_module/schematic` are now archived too. Historical reports may contain obsolete links; the move manifests, not the old links, are the recovery map.

The archive may contain packages named `FACTORY` or `release`. Those names are historical and do not approve them for the present main board, battery or product.
