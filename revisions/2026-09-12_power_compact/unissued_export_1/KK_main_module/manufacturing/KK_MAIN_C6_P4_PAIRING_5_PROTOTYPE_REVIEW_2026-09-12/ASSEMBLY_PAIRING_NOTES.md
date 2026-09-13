# Current C.6 main / compact P.4 power

The [release index](CURRENT_RELEASE_INDEX.json) identifies the current source-bound manufacturing packages. These are five-sample engineering review files, not a qualified product or authorization to fabricate without a DFM response.

## Mechanical change

| Board | Outline and layers | M2 hole centers, native top-left origin |
|---|---|---|
| Main C.6 — unchanged | 96 × 105 × 1.6 mm, R4, two copper layers | (4,4), (92,4), (4,101), (92,101) mm |
| Power P.4 — compact | 50 × 50 × 1.6 mm, R3, four copper layers | (3,3), (47,3), (3,47), (47,47) mm |

All mounting holes are 2.2 mm NPTH. **The patterns do not match.** The smaller power PCB can sit behind main using separate removable case supports. Final position, support heights and battery location are not frozen. The previous common-hole four-standoff / 20 mm arrangement is superseded. Keep the complete power PCB, cell, wires and metal hardware out of the main antenna's clearance region; a small PCB does not automatically guarantee RF clearance.

In the power PCB's native front view, USB is at the top edge and the switch at the right; harness connectors are toward the bottom. Case-facing orientation must be chosen with actual cables, plugged JSTs and wire bends. Do not infer connector pin order from a mirrored rear view. Preserve access to the main board's student solder joints and replaceable modules.

The [actual-size mechanical PDF](C6_P4_MECHANICAL_REVIEW.pdf) contains **separate** mounting templates, not an approved combined placement. Print at 100%, measure the calibration line, and fit the actual boards/components. Main [front](../KK_main_module/assembly/C6_front_FIT_100_PERCENT.pdf) and [back](../KK_main_module/assembly/C6_back_FIT_100_PERCENT.pdf) fit sheets remain valid because main CAD is unchanged.

## What was preserved

P.4 restores the original compact routed core, using the inverse rigid transform from oversized P.3: `x=51-P3_x`, `y=104-P3_y`, rotation 180°, layers unchanged. Electrical pad/net/trace/via geometry matches the compact reference; outline, mounting holes, large-board keepout and revision label are intentionally changed. Copper is refilled. P.3 repaired 3D models remain attached. Historical transformation evidence is in [COMPACT_CHANGE_AUDIT.json](../KK_power_module/reports/COMPACT_CHANGE_AUDIT.json); its candidate-stage wording predates the fresh release checks.

Main's 43 horizontal resistors, ten horizontal Panasonic electrolytics and six flat TO-92 bodies remain unchanged. All 98 fitted main positions are through-hole. All 108 fitted power positions retain resolving model links, but power is a **factory SMT subassembly**, not a student SMT exercise. Sockets, buttons and optics retain functional height. Main rear ESP32 envelope is about 15.3 mm and front RGB about 22.1 mm; actual module dimensions and retention need sample checks.

Main capacitor selections remain ECEA1CKA101 / ECEA1CKA100, with maximum-envelope flat heights of 7.3 / 5.0 mm including 0.5 mm insulating supports. Follow the current BOM and lead-forming instructions; do not cross polarity or stress seals. Main routing remains 1,052 segments / 35 vias; power remains 3,515 segments / 260 vias.

## Verification and release limits

Fresh native ERC, DRC, opens and schematic parity must be zero. The [static audit](CURRENT_STATIC_AUDIT.json) separately checks each outline/hole pattern, unchanged main pin mapping, main trace widths, models and four-wire interface. Release manifests bind these checks and fabrication exports to the exact sources. Main fabrication geometry is independently compared with the archived C.6 package; refreshed main documents do not imply a new main electrical revision.

Power J3 → main J1: **1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2**, wired pin-for-pin. Never connect raw battery to main. Power TP3 BAT_NEG is not TP4 GND. Charger USB carries no data; do not combine ESP32 USB power and external main rails until exact-module backfeed behavior is qualified.

Before ordering, obtain factory approval for fine-pitch WCSP/QFN assembly and filled/capped/planarized via-in-pad processing. The via-center audit does not replace review of partial pad overlaps. Do not silently substitute the TPS22950 base variant. See [power fabrication requirements](../KK_power_module/FABRICATION_REQUIREMENTS.md).

Still unqualified: actual supports/plug/case/RF fit, battery and bonded NTC, speaker rating, simultaneous load capacity, ripple/thermal behavior, USB input behavior, rail sequencing and back-powering. Main's older 3.3 V reservation was 0.5 A while power screening used 0.4 A; measure integrated demand and margin. Screening targets are not tested ratings. Follow the [current-limited bench procedure](../KK_power_module/assembly/P4_REVIEW_AND_TEST.md); clean CAD is not proof of battery safety or a finished student product.

Previous P.3 sources, issued packages and shared-hole instructions are [archived intact](../revisions/2026-09-12_power_compact/). Do not use historical P.2 files merely because their dimensions also happen to be 50 × 50 mm.
