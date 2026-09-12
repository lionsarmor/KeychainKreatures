# C.4 populated 3D assemblies — accuracy and socket notes

**C.5 update:** the current PCB rotates the screen to landscape and moves MCU/SD/IR to the rear. It additionally uses the project-owned `TSAL6200_C5_edge_formed` model and KiCad's upright DIN0207 resistor models for 25 low-current resistors. See [C.5 mechanical limits](../C5_relayout/CIRCUIT_REVIEW.md) and [IR model dimensions/provenance](../C5_relayout/IR_MODEL.json). The package assumptions below still apply, but old C.4 component locations do not. The complete front/rear stack is roughly 39 mm before case walls/clearance.

Every one of the 98 electrical positions on the main board has a visible 3D model. Bare test holes and mounting holes have no fitted component model. Speaker, motor, battery, cables, mating JST plugs and enclosure are not shown at invented locations: their final positions and wire bends remain a mechanical-design task. Board-mounted JST receptacles are modeled.

## What the models represent

| Parts | Model basis | Remaining limitation |
|---|---|---|
| D3 RGB lens | Kingbright 5 mm lens, 5.9 mm flange, 8.6 mm body drawing | Proposed formed leads and seating height, not a manufactured lead-form drawing |
| D3 socket | Sullins PPTC041LFBN-RC / LFB housing dimensions | Actual retention/contact fit with the LED lead tolerance is unqualified; never force or tin mating portions |
| C315 ceramics | Exact KEMET maximum 3.81 × 2.54 × 3.14 mm body | Proposed 1 mm seating gap, simplified corners/leads |
| UVR electrolytics | Nichicon 5 mm diameter × 11 mm body | Nominal 0.5 mm seating gap, simplified top/stripe |
| Soft buttons | Linked Adafruit 3101/C4817 drawing, 7.8 mm body, 5.5 mm height | Seller height conflicts; verify actual sample |
| U1/U3/U4 | On Shore narrow sockets with DIP chips seated above them | Generic DIP-family body detail; 9 mm illustrative seated height, not a certified mating-stack drawing |
| TSOP38238, TSAL6200 | Vishay package dimensions and lens orientation | Proposed lead trimming/seating height |
| ESP32 SuperMini | User footprint outline, seller photo, two 8.5 mm sockets and male headers | Provisional 18 × 23.5 mm module, 1 mm PCB; exact seller revision and underside details unavailable |
| Display | Seller 31 × 48 mm board plus socket/header stack | Provisional header-to-edge offset, panel thickness and active aperture; not controlled supplier CAD |
| microSD reader | Seller 17.9 mm square board plus socket/header stack | Provisional header offset, socket height, PCB thickness and card position |
| Resistors, TO-92, axial diode, JST receptacles | Installed KiCad package models matching assigned package families | Nominal package geometry; exact molding/lead tolerances still require checking |

Project-owned models have colored VRML files for the viewer and same-name STEP twins for mechanical export. Geometry, evidence and SHA-256 hashes are recorded in [MODEL_MANIFEST.json](MODEL_MANIFEST.json). Regeneration source: `../pcb/c4_build_models.py`. KiCad stock model assets retain their upstream attribution/license and remain referenced through KICAD10_3DMODEL_DIR.

All models use millimeters internally; VRML coordinates are converted to KiCad's 0.1-inch model units. The visual LED is white diffused and unpowered, not a claim that firmware is running. Decorative SMD details on seller-module envelopes are not an electrical BOM.

## Height and clearance checks before making a shell

- RGB proposal: 8.5 mm socket + 5 mm lead-form standoff + 8.6 mm lens = **22.1 mm above the front PCB**. Measure an assembled sample before committing the shell or cutting LED leads.
- The model includes the 8.5 mm female socket and 2.54 mm male-header insulator under each plug-in module. Confirm actual mating engagement; headers must not be forced or suspended short of proper contact.
- The D3 PCB courtyard represents the board-level socket housing. Its elevated lens/formed-lead envelope is larger; review the 3D model and physical sample too. No extra courtyard-clearance waiver was introduced for D3.
- Limit trimmed lead protrusion and inspect both faces. The model's trimmed tails do not physically trim a student's leads. Do not populate TP holes with posts beneath opposite-face parts.
- Check all actual components, JST mating plugs, wire bends, screen support, SD extraction, battery location and antenna clearance. A nominal 3D render and clean DRC do not establish fit or RF performance.

RGB socket contact qualification is specifically still pending: a housing drawing is not proof of retention for a bare LED's lead dimensions. If the sample is loose or oversized, resolve the socket/lead interface before releasing kits; do not repair a poor mating fit by adding solder to the contact area.
