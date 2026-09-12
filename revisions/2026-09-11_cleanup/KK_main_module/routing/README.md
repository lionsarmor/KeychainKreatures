# C.5 routing handoff

The root native board is now the routed **84 × 95 mm C.5** revision. Its current handoff is [C5_final_routed.dsn](../C5_relayout/C5_final_routed.dsn). [C.5 report](../C5_relayout/REPORT.md) and [route audit](../C5_relayout/ROUTE_AUDIT.json) describe the new routing and checks. The old C.4 files below are historical and must not be imported into C.5.

## Historical C.4 routing

[KK_main_module_C4_final.dsn](KK_main_module_C4_final.dsn) is the historical export for the old 80 × 115 mm outline.

`C4_LED_ROUTES.json` records three clearance detours plus four LED branches. `C4_GROUND_REPAIRS.json` records three explicit ground paths. `KK_main_module_C4_routed.kicad_pcb` is the promoted candidate. Only D3 is relocated; unrelated routes and all other placements are retained. No online routing service or design upload was used.

Do not use older 80 × 100 mm RGB proposals, unrouted candidates, or C.2 DSN/SES files as the current board. They are retained only for traceability. For subsequent routing: back up the root project, export a fresh DSN, route, import SES into a candidate copy, refill pours, run DRC including schematic parity, inspect power/audio/RF paths, then regenerate the manufacturing package. Autorouter completion alone is not qualification.
