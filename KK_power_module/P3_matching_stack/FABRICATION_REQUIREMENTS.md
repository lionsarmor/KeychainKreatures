# Required DFM response — 5 × P.3 power modules

**Engineering review/quotation only. Do not fabricate or substitute parts until the customer approves your DFM response.**

| Item | Requested specification / required confirmation |
|---|---|
| Quantity | Five assembled engineering samples; quote assembly attrition separately |
| Board | 96 × 105 mm, 1.6 mm nominal, R4 corners, four 2.2 mm M2 clearance holes |
| Layer order | F.Cu / In1.Cu / In2.Cu / B.Cu; use all four supplied copper files |
| Copper / stackup | CAD nominal 35 µm copper layers; confirm actual finished stackup and plating before build |
| Routing / drills | CAD minimum track 0.15 mm; smallest via drill 0.20 mm, smallest via diameter 0.50 mm; check all fine-pitch land patterns |
| Via-in-pad | **Filled, capped, planarized** component-pad vias; coordinate exact process with assembler. Bare tenting is NOT sufficient |
| Via identification | `VIA_IN_PAD_REVIEW.csv` lists via centers inside front SMD lands; evaluate all land/via overlaps from CAD/Gerbers, including partial overlaps |
| Surface finish | Confirm a finish and flatness suitable for 0.4 mm-pitch WCSP; propose ENIG if supported |
| Soldermask / stencil | Confirm fine-pitch mask registration, paste apertures, thermal-pad windowing and stencil thickness |
| Critical package | U13 **TPS22950YBHR**, base variant, six-ball 0.4 mm-pitch WCSP. Do not substitute C/L variants or another package without circuit review |
| Other packages | QFN/WSON and 0.4/0.5 mm-pitch devices; confirm placement/reflow capability and inspection of hidden joints |
| Assembly | 108 fitted electrical parts per board; front-side assembly with THT/mixed connector/switch operations |
| Do not fit | 28 rear bare test pads, four mounting holes, and two silkscreen logo footprints |
| Placement | `POSITIONS_NATIVE.csv`: native KiCad mm/Y-up export. `BOM_AND_PLACEMENT.csv`: reference CAD mm/Y-down coordinates. Validate rotations, polarity and origin before machine programming |
| Net testing | Use supplied IPC-D-356 netlist and bare-board electrical test; retain test results |
| Substitutions | Written approval required, including capacitors' effective DC-bias capacitance, FET package/pinout, charger T variant, regulators, NTC and connector families |
| Testing scope | Do not attach an unspecified battery. Follow the included current-limited bench procedure after inspection |

The silkscreen OSHW mark is not a certification ID. This request does not claim USB, battery, toy-safety or EMC certification. Report any process or supply limitation before proceeding.
