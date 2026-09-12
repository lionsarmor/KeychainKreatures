# C.3 RGB main-board completion report

Date: 2026-09-11. Status: **CAD-complete engineering prototype; not powered or factory-qualified.** No PCB order was placed. The separate power-module files were not changed by this main-board pass.

## Completed

- Approved outline applied: 80 × 115 × 1.6 mm, two layers, 4 mm corner radii. Bottom mounting holes moved 15 mm down; existing controls and electrical component locations retained.
- Separate front RGB LED D3 added. D1 remains the IR transmitter. TLC5916IN socketed through-hole driver uses four spare MCP23017 outputs; no additional ESP32 pin or strapping-pin use. Exact ED16DT socket and Kingbright WP154A4SEJ3VBDZGW/CA selected with datasheets. Four resistors and bypass capacitor complete the seven-component addition.
- RGB OE pull-up keeps outputs blanked at reset; SDI/CLK pull-downs define startup inputs. R_EXT=1.8 kΩ gives approximately 10.4 mA nominal default channel current. RGB lead order and required lead forming are marked/documented. Driver supply capacitor connection is approximately 4.15 mm.
- 25 bare plated debug holes, orientation/connector markings, top-entry J1/J4/J5, prior amplifier switching improvements and motor suppression placement retained. J4/J5 use B2B-PH-K-S(LF)(SN); mating PHR-2 housings unchanged.
- Original routed copper retained exactly; 15 local RGB branches added with 0.8 mm power and 0.25 mm control/LED traces. Both GND pours refilled, both antenna keepouts retained. Final board has 1,356 track segments and 40 vias, 362 plated drill hits including vias and 4 NPTH mounting holes.
- Single grouped schematic, actual-size front/back fit sheets, 3D previews, 98-reference BOM, sockets/harness extras, 26-document datasheet packet, debug instructions, RGB initialization and bench-test record updated.
- Fresh FreeRouting DSN and locally generated prototype Gerber/drill ZIP prepared. No external autorouting upload was used.

## Verification evidence

| Check | Result |
|---|---|
| Schematic ERC | 0 violations |
| PCB DRC | 0 violations |
| Unconnected items | 0 |
| Schematic/PCB parity | 0 issues |
| Independent population, values, MPNs, footprint IDs and pad/net comparison | Pass: all 98 electrical positions |
| Student-soldered PCB pads | All electrical component pads through-hole |
| Prior copper and electrical placement preservation | Pass; only bottom mounting holes moved |
| Ground pours / antenna rule areas | 2 filled pours / 2 retained keepouts |

The [independent verification JSON](pcb/C3_FINAL_VERIFICATION.json) and [manufacturing manifest](manufacturing/MANIFEST.json) identify the exact board hash. Export reruns ERC/DRC/parity and refuses mismatched audit hashes. A documented, scoped courtyard exception treats **bare TP holes** as having no fitted component body. It does not waive copper, drill or edge clearances; all other relevant placement checks remain active.

The zero-violation result is under the recorded project settings, not a claim that every optional KiCad check is enabled. Five inherited categories remain ignored: missing courtyard, track endpoint not centered on via, tuning-profile geometry, symbol footprint-filter mismatch and footprint-type mismatch. They are listed in the DRC JSON/manifest. This pass did not newly disable those categories; the independent audit separately verifies the electrical pad type and exact assigned footprint IDs. Physical fit is still a bench requirement.

## Physical and electrical limits — still pending

CAD courtyard checks and visual review do not establish real assembly fit. The actual SuperMini, display and SD modules, formed RGB leads, rear socket/electrolytic heights, JST plugs and wire bends need dry-fit. D3's native 1.27 mm leads must be formed to 2.54 mm without stressing its body. There is no qualified D3 formed-lead 3D model. The prior user fit check is provisional, not a new measured assembly test. Top-entry PH plugs need about 8 mm mated height plus wire bending/insertion room; 15 mm bench standoffs are not a final enclosure guarantee.

The board needs coordinated **5 V, 3.3 V and 3.2 V** regulated inputs at J1. It is not safe to connect raw battery or assume the existing power module matches. Do not apply module USB and SYS_IN simultaneously. Reserve additional RGB current in the future power-module budget and verify rail sequencing, transients, backfeed and fault protection. No upstream charger/regulator change was made.

Speaker FS1511P08-H3.0 continuous-power rating remains undocumented. Audio switch/inrush, speaker clipping/DC/pops, backlight current, motor startup, simultaneous Wi-Fi/SD/RGB loading, thermal behavior and RF performance must be measured. Clean DRC is not circuit simulation or proof of operation. Exact module revisions and delivered memory also require verification.

No full application, browser upload, trading, game loader or bench firmware was implemented by this hardware pass. RGB safe-state and control requirements are in the assembly guide. Firmware and physical prototype tests remain separate work; every entry in the [bench record](assembly/C3_BENCH_TEST_RECORD.csv) is honestly marked pending.

## Handoff

Use the root KiCad project, [C.3 BOM](assembly/C3_BOM_PRINT.html), [assembly guide](assembly/ASSEMBLY_GUIDE.md) and [C.3 fabrication ZIP](manufacturing/KK_MAIN_C3_PROTOTYPE_FAB.zip). Reload stale KiCad tabs before saving. Old checkpoint reports and routing candidates are history. Next: dry-fit the exact new parts, assemble a supervised engineering prototype, test with the specified bench supply interface, then develop/qualify the separate power module and firmware before any student-product release.
