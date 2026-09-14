# Pixel Pod — round 2: separate skins and click-in carriers

Design exploration only. These images are not mechanical CAD, print-ready parts, proof of interference clearance, or an instruction to order different electronics. No PCB or manufacturing file was changed.

The selected starting point is [the original Pixel Pod](../01_pixel_pod.png). This round preserves its green/cream/yellow identity while exploring a smoother exterior, separate printable parts, and accessible internal carriers.

## The finish tradeoff

FDM cannot guarantee a completely layer-line-free, seamless exterior straight from the printer. A flat surface printed against a suitable smooth build surface can look much smoother than an upright wall, but edges, curved transitions, first-layer toolpaths and assembly joints can remain visible. A textured build plate transfers texture instead of a smooth finish.

Splitting a design lets each part use a better print orientation. Test mating features rather than assuming one universal clearance, and avoid difficult bed-facing fillets when a chamfer will work. See [Prusa's FDM design guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135). The specific panel architecture below is our proposed application of those principles, not a validated Prusa enclosure design.

| Option | Parts strategy | What the finish actually requires |
| --- | --- | --- |
| [A — Flat Panel Pixel Pod](04_pixel_pod_flat_panels.png) | Hidden load-bearing chassis; separate front, back, four edge skins and small planar corner facets. | Best route toward bed-contact finish on nearly every broad outside face. More parts and intentional joints; small edges still need assessment. |
| [B — Snap Skin Pixel Pod](05_pixel_pod_snap_skins.png) | Flat main skins with separate rounded corner caps over an internal frame. | Keeps the original rounded feel. Flat skins print exterior-down; curved caps may need sanding/finishing. |
| [C — Finished Pixel Pod](06_pixel_pod_finished_shell.png) | Fewer, larger rounded outer parts over the same carrier concept. | For a visually line-free rounded finish, budget sanding, primer and paint on empty shell pieces. More manual work; not a straight-from-printer result. |

Recommendation: A if avoiding finishing is the priority; B if preserving the original roundness matters more. A completely rounded, visually line-free result with few seams points toward C. Final print orientation must also preserve structural strength; it is not enough to optimize appearance alone.

## Switch and charging port: driven by the actual board

The current P.4 [placement table](../../../KK_power_module/assembly/P4_BOM_AND_PLACEMENT_REVIEW.csv) and [PCB](../../../KK_power_module/KK_power_module.kicad_pcb) identify:

| Item | Part | Board position, mm | Rotation |
| --- | --- | --- | --- |
| SW1 | JS102011SAQN slide switch | X 46.125, Y 11.0 | 90 degrees |
| J1 | HC-TYPE-C-16P-01A USB-C | X 12.0, Y 3.34 | 180 degrees |

These are footprint origins, not final shell cutout centers. The [component-side board render](../../../KK_power_module/reports/power_compact_front.png) shows USB-C at the upper edge and the switch actuator at the right edge: adjacent edges, not both on the back face.

For this concept only, rotate the entire power board 180 degrees in its own plane, with components facing the removable back. Locate its cradle in the lower-left region **when looking straight at the rear**. USB then faces the bottom, and the switch faces the left side near the bottom in that rear view. In a front view, that is the user's right side. We are rotating the board assembly, not relocating either component or adding a remote switch.

Exact cradle offset must align both connectors with the case. Check connector insertion depth, switch travel and finger access in CAD. A guided switch cap may extend the actuator if needed, but must have travel stops and cannot apply bending loads to the soldered switch. The power board location remains provisional until it clears the main board, wiring and battery.

## Three serviceable chambers

1. **Main board and screen carrier:** support the complete current C.6 main assembly. The display stays attached/socketed as intended; the shell must not squeeze the display glass or press on component bodies. Use mounting holes or confirmed clear support areas, not arbitrary clips over copper or sockets.
2. **Power-board cradle:** support the 50 × 50 mm P.4 board independently. Latches retain the carrier, not fragile components; connector insertion forces need structural support. Maintain access to charging USB-C, switch, JST leads and test points.
3. **Battery carrier:** a removable smooth pocket with retention and clearance determined by the selected cell's dimensions and manufacturer requirements. The carrier clicks into the chassis; clips must not compress, scrape or puncture a pouch cell. Battery size is still TBD. Keep it isolated from solder tails and heat-producing parts, with lead routing and strain relief.

Design release tabs that can be reached after removing the back. Do not require PCB flexing to release an assembly. Snap geometry, material, print orientation, repeated-use life and insertion force need test coupons. Small screws may secure the outer back while the internal carriers remain click-in; the concepts do not imply a validated tool-free children's battery door.

The 96 × 105 mm main board, tall front RGB assembly, rear socketed ESP32, wiring and insulation set the envelope. Battery and power board must stay out of the top-center antenna clearance region. Keep SD access, IR line of sight, button travel, speaker/motor retention and troubleshooting access in the design. A three-chamber illustration does not prove these items fit.

## Before committing to printable geometry

- Choose the visual direction and finish expectation.
- Measure the actual printer/build surface and test a cosmetic panel plus snap/rail coupons.
- Select the battery and confirm assembled board/component heights.
- Import the current CAD assemblies, establish independent supports and cable paths, and verify the switch/USB alignment together.
- Make an inexpensive fit prototype before completing cosmetics; check button travel, optical openings, antenna clearance, removal access and electrical insulation.

## Artwork review: do not copy these details into CAD

The artwork communicates panel splitting and separate carriers, but its generated electronics are not faithful models. In particular, the exploded illustrations shorten the main assembly to a screen-sized board and visually mix front and rear layers. The real main PCB remains a full 96 × 105 mm board extending behind the controls. The power board and battery must occupy a separate rear depth layer, not the same plane as that PCB. Power-component artwork and proportions are approximate; use the actual CAD, not pictured chips or socket positions.

Some hero views still illustrate front-facing IR lenses despite the specified top-edge openings. Preserve the real transmitter/receiver axis in CAD. Some border pieces also look curved despite face-down print labels: only truly planar exterior surfaces can contact a flat build plate across their full face. In option A, replace such depicted curves with planar facets; in B/C, account for finishing. Generated claims such as “built for real hardware” are design intent, not fit verification.

## Image-generation record

Generated with the built-in `image_gen` tool, one call per option. Exact final prompts are in [prompts.json](prompts.json): each call concatenates `common_prompt` and the selected variant's `prompt`. Reference images are the original Pixel Pod style sheet and the current P.4 power-board front render.

The image-generation workflow separates finish targets from verified engineering. Illustrated joints, clips and electronic envelopes must be replaced by measured mechanical CAD before publishing printable files. The images and prompt record are saved in this folder; earlier concept assets are preserved.
