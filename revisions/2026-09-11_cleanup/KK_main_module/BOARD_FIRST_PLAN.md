# Board-first sizing amendment

2026-09-10. The user has relaxed the original shell-first dimensions: make a comfortable, appropriately small handheld-toy board; the user will model its shell afterward. This supersedes the earlier enclosure-CAD-first gate, not the electrical, THT or feature requirements.

## Working proposal

Start component placement in a **50 W × 65 H × 1.6 mm PCB**, approximately R4 corners. This is an engineering trial size, not a fitted layout or finalized outline. Its 3250 mm² raw rectangular area is about **49% greater** than the previous 42 × 52 mm envelope. Use that space for controls, hand-solder access, sensible connectors and real component clearances.

A shell around this board might be roughly **55 × 72 mm in face dimensions**, depending on walls, mounting and connector protrusions. This is a packaging allowance, not a promised enclosure size. Thickness remains stack-dependent; the previous 19–20 mm ceiling is no longer treated as binding. Making the board wider/taller does not itself eliminate overlapping battery, power-board or socket heights.

Keep the 1.69-inch screen, nine gameplay inputs, compact S3/PSRAM, separate RODDY power PCB and battery, IR, speaker and haptics. Latest clarification: **all main-board mounting is through-hole for students; ESP32 uses a preassembled module with legs**. No factory-populated SMD parts directly on the main PCB. Recheck the trial footprint with real module/socket heights and hand-solder access. See [student-kit requirements](STUDENT_KIT_REQUIREMENTS.md). No separate sub-GHz hardware or automatic return to a large processor module.

## Placement priorities

1. Screen registration/window and nine-control geometry first. Test a real-size paper/button mock-up; a larger board is not evidence of comfortable controls by itself.
2. Reserve component and antenna keepouts, four practical mounting locations, power actuator/USB access, cable bends and soldering/tool access. Do not place mounting holes merely to make a symmetric drawing.
3. Arrange battery and power PCB against actual component height maps, keeping sharp leads and screw paths clear of the cell. Preserve RODDY's electrical architecture.
4. Compare direct GPIO against a THT button expander after selecting the exact compact S3 variant. Fit the full audio/IR/haptic circuits, not just their IC bodies.
5. Adjust the trial outline only where actual placement requires it. Report final dimensions and the reasons for meaningful growth before release. Do not add unused area by default.

## Shell handoff after board finalization

Provide the board outline and thickness, mounting-hole coordinates/diameters, control centers and actuation heights, display position and mounting envelope, connector mating/service clearances, IR window positions, RF/metal keepouts, speaker/motor pockets, battery/power-board placement and complete assembly depth limits. Export board 3D data and dimensioned drawings when geometry exists; none is claimed created by this amendment.

The exact display assembly, battery envelope and speaker/motor specifications remain necessary for a trustworthy final board. They do **not** require the user to model a shell first. Schematic/part qualification and trial placement can progress before enclosure modeling; do not fabricate unknown connector pinouts or component heights.

## Historical artifacts

The existing `mechanical/fit-study.svg` and `.pdf` show the **old 46 × 62 mm shell study**. Keep them for comparison only; they are not the new board outline. The earlier review's dimensional calculations remain valid for that old study, while its shell-first sequencing and dimensional limits are superseded here. Costs must be refreshed for final board dimensions/process.
