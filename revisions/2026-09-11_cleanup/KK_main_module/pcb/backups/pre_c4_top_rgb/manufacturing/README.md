# C.3 RGB — engineering prototype fabrication only

Use `KK_MAIN_C3_PROTOTYPE_FAB.zip`. Two-layer PCB, 80 × 115 mm, nominal 1.6 mm FR-4, 1 oz outer copper, R4 corners. Gerbers include both copper, soldermask, silkscreen and Edge.Cuts; separate metric PTH/NPTH Excellon drills, drill maps and report are included. Edge.Cuts controls the finished outline; do not scale or infer it from silkscreen. Through-hole assembly requires no stencil. Obtain the fabricator's stackup/tolerance confirmation before ordering.

Specify **lead-free HASL** solderable surface finish for this prototype. The exported job metadata is set to that requirement by the fabrication script; the native board's unset finish is not a request for bare copper. KiCad's job bounding box includes the outline stroke (80.05 × 115.05 mm); the Edge.Cuts centerline defines the nominal 80 × 115 mm finished profile.

`MANIFEST.json` records source/output SHA-256 hashes and fresh ERC/DRC/parity results. Export is blocked unless checks are clean and the independent board audit matches the board hash. A courtyard-only rule intentionally treats unpopulated TP holes as having no component body; copper/drill/edge rules remain active. Debug pads are plated holes, not fitted headers. Four mounting holes are NPTH.

The manifest also records five inherited ignored DRC categories: missing courtyard, off-center track/via endpoint, tuning-profile geometry, footprint-filter mismatch and footprint-type mismatch. No new general category was disabled in this pass. The independent audit verifies fitted electrical pads are through-hole and footprint IDs match the schematic.

No order has been placed. This is not a tested consumer/student product or a compliance release. Limit any first order to engineering prototypes. Actual socket/module/formed RGB LED fit, JST cable clearance, audio and speaker power limit, backlight, rail transients, thermal behavior, RF performance and interrupted SD writes require physical qualification. D3 leads require forming from 1.27 mm to 2.54 mm pitch; dry-fit a sample before committing a batch.

Assembly uses the root project's C.3 BOM and guide. The separate power module is unchanged; J1 requires coordinated regulated 5 V, 3.3 V and 3.2 V rails. Never connect raw battery, the old power module, or USB and J1 simultaneously. Battery, enclosure, firmware and student-product release are not included in this fabrication package.

Earlier C.2 files are archived under `../archive/C2_manufacturing_superseded/`; do not combine revisions.
