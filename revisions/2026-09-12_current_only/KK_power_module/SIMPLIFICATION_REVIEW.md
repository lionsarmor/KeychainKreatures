# P.2 simplification review — 2026-09-11

**Historical architecture review.** P.3 is now routed and packaged with a 96 × 105 mm matching outline. Use [current status](CURRENT_STATUS.md) and [P.3 review/bench procedure](P3_matching_stack/assembly/P3_REVIEW_AND_TEST.md). The unfinished-routing/release checklist below records the earlier draft and is not today's status; no protection was removed to reduce the IC count.

## Decision for this cleanup

Keep the current C.5 main-board circuit and four-pin power interface unchanged. Preserve P.2 as an unfinished draft, not as a proven working supply. No parts, nets, footprints or copper were removed in this pass. Archiving incomplete router candidates prevents them being mistaken for the current board.

Fourteen ICs is a reason to review the architecture, **not evidence that particular safety or supply blocks are redundant**. The draft contains three converters, three output switches, a charger, battery protection controller, eFuse, USB-C controller and its LDO, USB input limiter, supervisor and buffer. Six extra converter capacitors and the bulky service header had already been removed in the saved P.2 draft; that is prior work, not a new change in this cleanup.

## What can and cannot be simplified safely

| Area | Disposition | Reason / next evidence needed |
|---|---|---|
| Main-board connector | Keep pins 1=5 V, 2=GND, 3=3.3 V, 4=3.2 V | The existing main board uses each rail. Changing this would also require a main-board redesign. |
| Three regulator channels | Retain pending a real load budget | A shared 5 V converter plus downstream converters is a possible redesign, not a wire change. It concentrates all load in the 5 V stage and needs new low-battery, efficiency, transient and sequencing analysis. |
| Replace lower rails with LDOs from 5 V | Do not adopt at current screening loads | At 0.4 A on 3.3 V and 0.5 A on 3.2 V, nominal regulator heat would be (5−3.3)×0.4 + (5−3.2)×0.5 = **1.58 W** before other losses. This is a calculated screening point, not measured toy consumption. |
| Merge actuator 3.2 V into logic 3.3 V | Do not adopt | The selected motor's reviewed maximum operating voltage is 3.3 V. A nominal 3.3 V rail leaves no tolerance/overshoot margin and puts motor noise on the logic supply. |
| Supervisor U12, buffer U11 and output gates U8–U10 | Keep until sequencing is demonstrated | They coordinate the independent supplies. The TPS63060 PG signal monitors its current-control condition; do not assume it replaces all independent voltage-threshold checks. A common enable alone does not prove safe startup/shutdown. |
| USB limiter U13 / source-current handling | Highest-priority assembly simplification candidate | The base TPS22950 supplies the draft's low-current setting but uses a small ball-grid package. C/L variants have a different current-limit range, so an easier package is not a drop-in electrical substitution. A replacement must retain acceptable default-source current and reverse-current behavior. |
| Battery protection and NTC | Keep their functions | Do not remove protection just because a future battery may be protected. A specified pack and documented fault/current coordination are required before changing this block. |
| Three parallel protection FET packages | Review against measured load and cell requirements | A suitably rated replacement may simplify placement; package count alone does not establish safe resistance, thermal behavior or overcurrent-trip coordination. No replacement has been selected here. |
| Vias in assembly pads | Review before routing is frozen | Prefer moving nonessential fanout vias outside solderable pads. Retain adequate thermal paths under exposed pads; confirm the resulting via finish with the assembler. Do not silently substitute open vias where solder wicking matters. |
| Board size | Hold 50 × 50 mm for now | Connector access, mounting, heat and routing need closure before further shrinking. |
| Debug access | Retain 28 bare pads | They cost no fitted BOM parts. Routing can prioritize essentials without removing student/prototype fault-finding access. |

These recommendations are engineering judgments from the saved circuit and manufacturer information, not circuit simulation. Relevant primary references: [TI TPS63060 datasheet, power-good and current-limit behavior](https://www.ti.com/lit/ds/symlink/tps63060.pdf), [TI TPS22950 family comparison and package information](https://www.ti.com/lit/ds/symlink/tps22950.pdf), and the [C.5 circuit review](../KK_main_module/C5_relayout/CIRCUIT_REVIEW.md). Manufacturer PDFs and earlier screening calculations remain in [P2_compact/datasheets](P2_compact/datasheets/) and [electrical_screening.json](P2_compact/electrical_screening.json).

## Electrical constraints still to close

- The 5 V/0.6 A, 3.3 V/0.4 A and 3.2 V/0.5 A figures are **screening targets**, totaling 5.92 W, not measured demand or guaranteed ratings. Verify display, SD write peaks, ESP32 Wi-Fi bursts, motor start and audio together.
- The saved charge setting is about 0.303 A nominal. A physical battery can be selected later only within the final electrical, temperature and current requirements; the existing provisional envelope is not approval of an unspecified cell.
- Default/USB-A charging in P.2 is intentionally slow (about 50 mA nominal limiter setting). It has no USB enumeration or suspend detection. Support for every computer-port behavior has not been established. Faster USB-C charging must follow source advertisement; full charging and full toy load are not simultaneously guaranteed.
- Check charger reverse blocking and every possible supply path with USB-only, battery-only and switchover conditions. The ESP32 module's own USB is a separate unresolved reverse-feed path; do not power it and SYS_IN together during initial testing.
- Verify effective ceramic capacitance after DC bias, output tolerance/ripple, startup, low-battery regulation, charger/converter/FET heating and protection coordination. Existing static netlist checks do not establish these.

## Release checklist

1. **Organization complete:** current projects identified; superseded files archived and hash-verified; no circuit edits in cleanup.
2. **Architecture review recorded:** retain the required functions; investigate easier USB input limiting and protection implementation before changing the schematic. No replacement parts approved yet.
3. **Electrical review incomplete:** close the load/source/battery and sequencing items above.
4. **DFM and placement incomplete:** assembly service, fine-pitch support, vias in pads, thermal paths and connector mating clearances still need sign-off.
5. **Routing incomplete:** saved native report has 138 opens and three dangling-via warnings. Archived SES/local plans are unqualified; export fresh from the final circuit/placement.
6. **Final native checks pending:** refill pours; run ERC, DRC and schematic parity; inspect high-current paths. Do not call the board clean based on general-clearance checks while opens remain.
7. **Power manufacturing package not issued:** final purchasing BOM, mating connector/wire list, assembly drawings, Gerbers/drills and bench procedure follow only after those checks pass.

Initial hardware qualification must use suitable current-limited bench equipment/battery simulation before a real cell, measure each rail and source mode, then increase load progressively. Do not treat five prototype boards as a certified or production-ready student toy.
