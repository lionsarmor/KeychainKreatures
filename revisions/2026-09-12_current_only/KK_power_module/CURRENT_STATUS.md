# Power board — current P.3 matching stack

Open [P3_matching_stack/KK_power_module.kicad_pro](P3_matching_stack/KK_power_module.kicad_pro). P2_compact is historical baseline evidence.

P.3 is **96 × 105 × 1.6 mm, four layers, R4 corners**, matching C.6 mounting holes. The routed power core was rigidly moved without changing electrical pad/net or trace/via geometry. It has 14 ICs, 108 fitted positions, 28 bare rear debug pads, 3,515 segments and 260 vias. All fitted model links resolve; real connector/stack fit remains unqualified.

- [Full five-prototype review ZIP](manufacturing/KK_POWER_P3_5_PROTOTYPE_REVIEW_2026-09-12.zip) · [Gerbers/drills ZIP](manufacturing/KK_POWER_P3_GERBERS.zip)
- [Current assembly/electrical review and first-power-up](P3_matching_stack/assembly/P3_REVIEW_AND_TEST.md)
- [Required factory DFM response](P3_matching_stack/assembly/FABRICATION_REQUIREMENTS.md)
- [Fresh checks, BOM/placement, test pads and connector map](P3_matching_stack/release_checks/)
- [Both projects and release hashes](../START_HERE.md)

Before ordering, obtain assembler approval of the 0.4 mm WCSP, fine-pitch packages, filled/capped/planarized via-in-pad processing and exact part supply. Before use, qualify the cell/NTC, charging, capacity, thermal behavior, USB attach/backfeed and coordinated rails. Not a proven production design.

J3 → main J1: **1 MCU_5V, 2 GND, 3 LOGIC_3V3, 4 ACT_3V2**. J2 battery pin2 is BAT_NEG, not GND; do not bypass protection with test-equipment grounds. Charger USB is charge-only. USB-A/default input charges very slowly and may not cover a running toy's load. Do not combine ESP32 USB and external main rails until verified.

The 5 V/0.6 A, 3.3 V/0.4 A and 3.2 V/0.5 A values are screening targets, not measured ratings. Reconcile the older main-board 0.5 A logic reservation with actual combined-load tests. No order or external submission has been made. Use one CPU for checks; do not rerun old generators over routed CAD.
