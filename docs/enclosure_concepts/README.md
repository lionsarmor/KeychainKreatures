# Keychain Kreatures enclosure concepts

Concept artwork, not dimensionally verified CAD, printable STLs, or a manufacturing release. No PCB, circuit, or Gerber changes were made for these concepts.

The user selected Pixel Pod. **Current direction:** [round 3: simplified front/back shell with rear battery hatch](pixel_pod_round3/README.md). [Round 2: separate skins and click-in carriers](pixel_pod_round2/README.md) is preserved as an earlier construction exploration, not the latest choice. The original artwork below remains the initial style reference.

## Three starting points

| Concept | Artwork | Direction and tradeoff |
| --- | --- | --- |
| 01 Pixel Pod | [Concept sheet](01_pixel_pod.png) | Clean retro capsule; the simplest starting point for a serviceable enclosure with few decorative pieces. |
| 02 Critter Buddy | [Concept sheet](02_critter_buddy.png) | Broad creature ears and shallow cheek details; strongest pet identity, with a larger silhouette. |
| 03 Trail Bot | [Concept sheet](03_trail_bot.png) | Faceted bumper and grip ribs; a playful field-companion appearance, with more accent parts. No impact rating is implied. |

Recommendation: start with Pixel Pod's basic construction, or use that construction beneath Critter Buddy's face and ear silhouette. Colors are suggestions for separately printed parts, not a requirement for a multicolor printer. Printed button caps do not by themselves make switches softer.

## Hardware the CAD must accommodate

- Main board C.6: 96 × 105 mm, 1.6 mm thick, rounded corners. The shell must be larger than this; these are chunky handheld concepts, not tiny keyfobs.
- Power board P.4: 50 × 50 mm, 1.6 mm thick, on its own supports behind the main board. Its mounting pattern is different from the main board's.
- Existing 280 × 240 landscape display at upper center; do not substitute a larger screen because of artistic proportions in the images.
- Nine controls below the screen: four direction switches left, four action switches right, one mode/function switch centered and slightly lower.
- One RGB LED near the upper right. The existing front RGB assembly envelope is about 22.1 mm from the PCB; verify the socket and physical part before sizing its protective pod.
- Rear ESP32/socket envelope is about 15.3 mm from the PCB. Final depth also needs solder-tail clearance, insulation, supports and wiring; a thin phone-like enclosure is not a valid assumption.
- One IR transmitter (D1, TSAL6200) and one receiver (U2, TSOP38238), looking out through top-edge openings. Preserve their actual locations and orientation, and do not assume ordinary printed filament transmits infrared adequately.
- Keep metal, battery and wiring out of the top-center ESP32 antenna clearance region. Do not place a decorative metal eyelet or screw there.
- One externally accessible charging USB-C port on the power module; it does not carry application data. Preserve internal service access to the ESP32 module.
- Keep JST connectors, SD-card access, speaker/motor wiring and debug pads serviceable. Confirm cable bends and connector unplugging space before closing the case design.
- Battery part, retention, exact position and enclosure depth are not finalized. The rear service-panel artwork is not a validated battery compartment.

## FDM construction brief

Use a flat-printable face assembly and a separate deep rear tray, with screw-removable access and captured button caps. Separate accent parts allow different filament colors without requiring automatic material changes. Prefer broad ears, ribs and attachment features over fragile protrusions.

Choose print orientation and part splits in CAD, not from the renders. Chamfer bed-facing transitions where a rounded underside would create difficult overhangs. Prototype button guides, fastener bosses and mating edges as small fit coupons before printing a complete enclosure. Printer calibration, material and orientation determine clearances; there is no universal press-fit allowance. These choices follow [Prusa's modeling-for-3D-printing guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135).

Support-free printing, screw strength, button travel, heat behavior and drop resistance have not been demonstrated. A printed shell is not battery safety certification. Keep students' access to replaceable parts in the final design rather than gluing the enclosure shut.

## Visual review and known artwork deviations

All three sheets communicate the nine-button arrangement, upper-right RGB feature, separate rear enclosure and distinct styling directions. They are intentionally not dimensioned drawings.

- The rendered screen/bezel proportions are approximate, and the pixel graphics do not imply changing the actual color display to monochrome.
- Some views place IR optics on the front face rather than the actual top-edge direction. Trail Bot's large perspective view also invents an extra pair of optics; ignore those duplicates. The hardware remains exactly one transmitter and one receiver.
- Rear USB, switch, speaker grille, service panel and screw locations are placeholders, not approved cutouts. The artwork does not establish acoustic alignment, SD access or mounting-hole alignment.
- Shown curved surfaces, labels and seams may require different part splits or embossed details in printable CAD.

## Next step after choosing a direction

1. Import both current board assemblies into mechanical CAD; measure actual sockets, display and LED against their models.
2. Select and measure the battery, speaker, wiring and fastening hardware; establish the power-board orientation and safe clearances.
3. Build an interference-checked internal layout, including antenna clearance, accessible connectors and button travel/stops.
4. Design the shell around those envelopes and test small mating/fastener/button coupons.
5. Print a fit prototype, assemble without forcing parts, and check service access before publishing STLs.

## Generation record

Generated using the built-in `image_gen` tool, one call per concept. The final prompt set is preserved in [prompts.json](prompts.json); each call used `common_prompt` followed by its variant's `prompt`, with [the current main-board front render](../../KK_main_module/reports/main_front.png) as a layout reference. The image-generation workflow kept aesthetic exploration separate from verified mechanical design.

All three delivered PNGs are saved alongside this README. Original generated files were preserved. These enclosure files are local concept assets; the troubleshooting documentation was pushed separately to GitHub's `development` branch at commit `d54a51a03c62d845d911ff6748cdaaaa08349c86`.
