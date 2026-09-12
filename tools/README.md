# Current project tools — C.6 / P.3

Native CAD in C6_flat_stack and P3_matching_stack is authoritative. Do not rerun old generators over routed boards.

- `node tools/check_project.mjs`: lightweight read-only current CAD/package/report/archive hashes, local assets, saved netlists and four-wire interface. Does not perform fresh native checks or powered qualification.
- `node tools/github_preflight.mjs`: read-only staged-publication check for required release/archive paths, current documentation links, oversized files, accidentally staged editor state and common credential patterns. Run after staging; it does not prove the absence of every possible secret or alter Git/GitHub.
- `flat_stack_audit.py`: read-only native two-board outline/hole, pin/net, horizontal-part and independent trace-width audit. Also refreshes the power reference placement CSV. Run inside KiCad Flatpak Python.
- `stack_release_prepare.py`: produces C.6/P.3 assembly/BOM support docs from preserved electrical reviews, without editing CAD.
- `stack_release_native.py`: native read-only BOM/pin/net/model checks, debug/connector maps and assembly plots.
- `stack_release.py`: sequential fresh ERC/DRC/parity, Gerber/drill/IPC/placement export and complete five-prototype packages. Refuses to overwrite an issued release. Review/update explicit revision paths before a future revision.
- `stack_release_finish.py`: guarded one-time preflight documentation seal and superseded-output archival for this C.6/P.3 release.
- `flat_stack_report.py`, `flat_stack_fit.py`: printable mechanical review and actual-size fit drawings.
- `check_project_legacy.mjs`, older power_* and flat placement/routing scripts: historical/one-shot evidence. Some overwrite working copper or rely on archived scratch inputs. Not general rebuild commands.

Use `nice -n 15 taskset -c 0` for heavy work; run native checks sequentially, no competing routers. With KiCad Flatpak, use `flatpak run --command=python3 org.kicad.KiCad /absolute/path/to/script.py`. Global KiCad 10 library models are checked natively, not by the lightweight host checker.

Current full and fabrication-only ZIP paths and hashes are in docs/C6_P3_RELEASE_INDEX.json. Never describe a saved hash check as a new electrical/thermal test. No tool here orders boards.
