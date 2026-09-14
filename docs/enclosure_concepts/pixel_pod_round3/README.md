# Pixel Pod — simplified front/back shell

Current concept direction: **two main shell halves plus a small battery-access hatch**. This replaces the many cosmetic skins and corner caps explored in round 2. Button caps and an internal insulating battery support are still functional parts.

## Artwork

- [Exterior and battery access](07_pixel_pod_simple_exterior.png)
- [Illustrative internal assembly](08_pixel_pod_simple_assembly.png)

Concept art only: not dimensionally verified CAD, printable STLs, or proof that the assembly fits. No circuit, PCB or manufacturing files were changed.

## Arrangement to develop in CAD

The **front shell** supports the complete current 96 × 105 mm main board, including its screen, nine switches, RGB LED and rear-mounted electronics. The main PCB extends behind the controls; it is not just a small board behind the screen. A recessed opening on the **top edge**, aligned to the existing IR transmitter and receiver, gives both an outward view. An open aperture avoids assuming ordinary printed plastic transmits IR; any later protective optical insert needs suitable material and testing.

The **rear shell** holds the 50 × 50 mm power board and battery stacked in depth, not side by side. Proposed order from front toward the battery hatch:

`Main assembly → clearance → power board → clearance/insulated battery pocket → battery → hatch`

Independent supports must keep the battery away from components and solder tails. The insulating pocket is not proof of thermal safety: charging/regulator heat, enclosure temperature and the chosen battery's requirements need evaluation. Keep the stack low enough to preserve the top-center ESP32 antenna clearance. Battery size, exact stack position and final shell depth remain open until measured.

The **battery hatch** opens without separating the main shell halves or removing the power PCB. Proposed retention is a small captive screw, a locating lip and a battery pull tab. The battery's connector should be reachable; retention must not squeeze or puncture a pouch cell. Opening the hatch should expose the battery pocket, not bare power electronics. Hatch geometry, fastener retention and suitability for the students' age group still need review.

The switch stays on the actual power board. The proposed 180-degree power-board orientation puts USB-C on the bottom and the switch on an adjacent side: right when viewed from the front, left when viewed from the rear. The physical footprint positions in [the current power-board placement table](../../../KK_power_module/assembly/P4_BOM_AND_PLACEMENT_REVIEW.csv) govern cutouts, not the artwork. No remote switch or extra USB is added.

## FDM priorities

- Broad flat external front/back faces and short chamfered transitions; avoid unnecessary curved undercuts and decorative pieces.
- Explore exterior-face-down printing for the main halves, with internal bosses rising upward. The final LED collar, shell depth and top-edge opening may change the best orientation; check a sliced model before promising support-free printing.
- Use accessible shell screws, supported board mounting points, reachable retention tabs and replaceable button caps. Test button travel, snap fits and fasteners with small coupons.
- Keep room for the existing socket heights, speaker, vibration motor, JST cable bends, SD access, solder tails and debug access. Do not resize or omit these to make a rendering look thinner.
- Simpler two-half construction means some visible sidewall layer lines can remain. Smooth renderings are finish targets, not guaranteed as-printed surfaces.

This follows the general part-orientation and test-fit principles in [Prusa's FDM modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135); our specific enclosure has not been tested.

## What is still needed for actual fit

Choose/measure the battery; check actual populated-board/socket heights; import both current assemblies into mechanical CAD; establish supports and wiring routes; verify stack clearance, thermal behavior and antenna clearance; then print an unpowered fit prototype before final cosmetic work. Exact screw locations, wall thicknesses, clearances and cutout dimensions are deliberately not frozen by concept art.

## Generation record

Created with the built-in `image_gen` tool: one exterior sheet and one companion assembly sheet, each followed by a targeted review edit. Initial prompts are in [prompts.json](prompts.json); each initial call combines `common_prompt` with its variant `prompt`. Final correction prompts and their source images are recorded in [review_edits.json](review_edits.json). References are the original Pixel Pod style sheet plus actual main-board and power-board front renders. Original assets remain preserved.

The image-generation workflow is used for visual exploration only; any illustrated electronics and internal supports must be replaced with the real assemblies in CAD before making fit claims. Review edits added the missing exterior switch/port detail and removed exposed circuitry from the battery-access view. Remaining artistic approximations include screen scale, internal board offsets, fastener count/locations, cosmetic accents and shell depth. The top-window labels and drawn optical shapes are not a component-identification or drilling template. Use the exterior sheet for the simpler appearance and the internal sheet only for the proposed assembly order; it does not model every rear-mounted main-board component or cable.
