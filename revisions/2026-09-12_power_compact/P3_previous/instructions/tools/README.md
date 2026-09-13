# Current-project tools

Current native CAD is directly in KK_main_module and KK_power_module. These folders are C.6/P.3; all older designs and one-off generators are in [the cleanup archive](../revisions/2026-09-12_current_only/).

- `node tools/check_project.mjs`: read-only source/package hashes, saved netlist/interface checks, local assets, protected cleanup files and archive recovery integrity. Not a new powered or native CAD test.
- `node tools/github_preflight.mjs`: staged-publication checks for release/archive paths, documentation links, large files and common accidental credential/editor-state inclusions. Run after staging the intended changes, not during an unstaged move.
- `flat_stack_audit.py`: native static outline/mounting, flat-part/model, pad/net and independent track-width checks. Refreshes the current audit and power placement table, never routed CAD.
- `flat_stack_fit.py`: actual-size main front/back fitting PDFs generated from a temporary board copy.
- `flat_stack_report.py`: printable four-page stack review.
- `stack_release_native.py main|power`: native BOM/pad/net/model checks and assembly/connector/debug maps; it rewrites generated review tables/plots, not CAD.
- `current_only_cleanup.mjs`: completed one-time move script, retained as recovery evidence. It refuses to run again once its archive exists.

Run heavy tools sequentially with `nice -n 15 taskset -c 0`. Native Python tools use `flatpak run --command=python3 org.kicad.KiCad /absolute/path/to/tool.py`. Fit/report documents are generated artifacts; do not confuse updating a print sheet with issuing new manufacturing files.

Historical placement, route-import, power generation and release scripts have been packed away. They retain their original source assumptions and are not supported commands from their relocated paths. Restore a complete historical scratch workspace using the move map if needed; never run them over current CAD.

Issued review/Gerber ZIPs are unchanged snapshots. Their recorded original source paths remain historical metadata; docs/C6_P3_RELEASE_INDEX.json points to current source locations and verifies the same bytes. Any future circuit edit needs a new checked release, not merely updated hashes. No tool here orders boards.
