# C.6 main / P.3 power — flat-stack prototype release

Current C.6/P.3 Gerbers, drills, BOMs, assembly/fit drawings, source CAD and verification are listed in [the release index](C6_P3_RELEASE_INDEX.json). The prototype review packages have been issued. Factory DFM/parts approval, mechanical mock-up and bench testing remain required; issuing files is not a claim of qualified physical fit or electrical performance.

The current guides flag the integrated load budget: older main-board reservations included 0.5 A on 3.3 V, while power screening used 0.4 A. Measure actual combined peaks and margin before approving the toy; neither estimate is a validated rating.

User decisions: both boards stack behind one another; select low-profile through-hole capacitors; all main-board resistors lie flat; prioritize student assembly/access over aggressive packing. Preserve the front landscape display and below-screen controls.

The flat-body placement did not fit the old 84 × 95 mm outline with conservative component/body clearances. The issued prototypes use a shared **96 × 105 mm**, R4 rounded outline and matching M2 mounting-hole pattern: centers (4,4), (92,4), (4,101), (92,101) mm. The released files are frozen review snapshots, not a production approval. Power remains a preassembled surface-mount subassembly; students assemble the through-hole main board. Removable boards/modules provide access to solder joints, sockets and test pads during assembly and servicing.

Main revision replaces upright resistor footprints, changes capacitor parts/footprints/models together, provides horizontal body/lead envelopes, and preserves socketed ICs/modules and connectors. The BOM parts changed with the models; tall parts were not merely drawn smaller. Optical lenses still aim through the case; button caps and sockets necessarily have some height.

Power revision matches the outline and holes and reserves a metal-free region behind the main antenna. The routed circuit remains together with USB/switch access near case edges. Physical checks of overlapping bodies, solder tails, plugged connectors, wiring and cell envelope remain required. Battery placement remains unselected.

Do not order C.5/P.2 Gerbers for this stack. Those outputs are preserved in revisions. C.6 is rerouted and both boards pass native ERC/DRC with no opens or schematic mismatches. BOMs/models and replacement manufacturing files are updated. Physical stack spacing, connector/harness access, factory process/supply and powered testing remain qualification gates.

## Current working files

- Main: `KK_main_module/C6_flat_stack/KK_main_module.kicad_pro`
- Power: `KK_power_module/P3_matching_stack/KK_power_module.kicad_pro`
- Printable review: [C6_P3_STACK_REVIEW.pdf](C6_P3_STACK_REVIEW.pdf)
- Main current BOM: `KK_main_module/C6_flat_stack/assembly/C6_BOM_BY_REFERENCE.csv`
- Main changes: `KK_main_module/C6_flat_stack/component_changes.json`

All 43 resistors now use the existing horizontal 10.16 mm-pitch footprint. Ten electrolytics use new horizontal footprints and maximum-envelope STEP/VRML models; six TO-92 devices use a flat-body footprint with the same numbered electrical pins. Optical parts and socketed assemblies retain necessary height. No resistors were made smaller merely by changing a model.

Selected capacitors: Panasonic **ECEA1CKA101** (100 µF, 16 V, nominal D6.3 × L7 mm) and **ECEA1CKA100** (10 µF, 16 V, nominal D4 × L7 mm). [Manufacturer KA-A datasheet, 1 September 2025](https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1050.pdf), archived in the candidate's `datasheets` directory. Tolerances are included in the footprints/models: maximum diameter +0.5 mm and length +1 mm. With a 0.5 mm insulating support, flat heights are 7.3 mm and 5.0 mm. Their 85°C/1000h endurance and ripple limits must be assessed in the prototype; equal capacitance is not a claim of identical transient performance.

Power core is rigidly rotated 180° and translated (`x=51-old_x`, `y=104-old_y`), preserving every component pad/net and track/via size/layer/relative coordinate. Existing power planes remain limited to the original circuit area; they were not expanded behind the antenna. A 60 × 38 mm all-copper keepout reserves the upper antenna area. Main and power holes match; power front faces the rear cover, so its front-view X coordinates are mirrored in the assembled stack.

Use **20 mm insulating M2 standoffs for the first removable fit mock-up**, not as an approved enclosure dimension. The main ESP32 socket envelope is about 15.3 mm, and power solder tails can extend 2.5 mm toward it. Plugged JST connectors, wire bends and tolerances still need physical checking. Front RGB height remains about 22.1 mm; flattening passives does not make the entire toy 7 mm thick. Battery size/location, case depth, final spacer/fastener part numbers and connector/harness access are not frozen.

## Completed checks

- [Static audit and source hashes](C6_P3_STATIC_AUDIT.json): both outlines and all four holes agree; the prior C.5/P.2 source files remain unchanged.
- Main C.6: 1,052 trace segments and 35 vias; native ERC/DRC = 0 violations, opens = 0, schematic parity issues = 0.
- Power P.3: 3,515 trace segments and 260 vias; native ERC/DRC = 0 violations, opens = 0, schematic parity issues = 0. All routed component pad/net and trace/via geometry was preserved by the rigid transform, apart from the intentionally relocated mounting holes and refilled planes.
- Every main component pin/net mapping is unchanged. All 98 fitted electrical components retain through-hole assembly pads and model attachments. Seller-module models are still provisional, not qualified mechanical drawings.
- Missing power-board 3D links were repaired for 14 components, including the USB/battery connectors, switch, inductors and several ICs. All 108 fitted power parts now have resolving model files. New models distinguish manufacturer maximum dimensions, nominal connector envelopes and conservative package approximations; they are not vendor-certified mating assemblies. See `KK_power_module/P3_matching_stack/3dmodels/P3_MODEL_REPAIR_MANIFEST.json` and `reports/model_link_repair.json`.
- The saved main project had lost its explicit power/audio classes. These are restored in C.6: 0.8 mm power/motor, 0.6 mm ground, 0.5 mm speaker/auxiliary load, 0.3 mm audio, 0.25 mm default. A separate trace-by-trace audit checks minimum width without trusting the KiCad class settings alone.
- Two leftover IR/backlight routes were completed locally. Five component ground pads retain explicit ground tracks but omit ineffective local pour joins. Bare ground test pads use solid ground connections. No DRC category was disabled to hide those thermal issues.
- Silkscreen labels were relocated against actual pad/graphic geometry; the final native report has no silkscreen overlaps. Functional optical orientation and pin-1 markings remain present.

Power **J3 connects to main J1**, pin-to-pin: 1 = MCU_5V, 2 = GND, 3 = LOGIC_3V3, 4 = ACT_3V2. Do not infer wire order from an X-mirrored rear view. Do not power the main board from raw battery voltage, and do not combine ESP32 USB power with the external rails until the exact module's backfeed behavior is qualified.

Next: print the review sheet and C.6 front/back fit PDFs at actual size, place the real parts and plugged harnesses on the drawings, and mock up the removable stack. Verify antenna clearance with the actual battery and case. New fabrication files are exported from the exact revised CAD with fresh checks and source/output hashes. Approve physical fit and the factory DFM response before ordering; old Gerbers were not merely relabeled as current.

Actual-size main-board fit PDFs: [front](../KK_main_module/C6_flat_stack/assembly/C6_front_FIT_100_PERCENT.pdf), [back](../KK_main_module/C6_flat_stack/assembly/C6_back_FIT_100_PERCENT.pdf). Updated power assembly-coordinate table: [P.3 BOM/placement review](../KK_power_module/P3_matching_stack/assembly/P3_BOM_AND_PLACEMENT_REVIEW.csv). The ordinary main-board assembly CSV contains quantities/parts, not factory-ready SMT pick-and-place data.
