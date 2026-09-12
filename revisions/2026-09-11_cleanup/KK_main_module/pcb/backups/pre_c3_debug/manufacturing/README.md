# C.2 engineering-prototype fabrication package

Order **bare PCBs only**, initially a small engineering batch. This package does not certify a functioning or student-ready product. The power module/battery are excluded; prototype bring-up requires the specified coordinated three-rail source. Speaker rating, exact seller-module revisions, backlight, RF performance, audio startup and thermal behavior remain hardware qualification tasks.

## Fabrication specification

| Item | Specification |
|---|---|
| Board | 80 x 100 mm, four 4 mm-radius corners |
| Stack | Two copper layers, FR-4, 1.6 mm nominal thickness |
| Copper | 1 oz / nominal 35 micrometres per layer |
| Finish | Lead-free HASL for low-cost prototype; ENIG optional, no redesign implied |
| Mask / legend | Solder mask and silkscreen on both sides; no paste stencil needed |
| Rules | 0.20 mm copper clearance; minimum signal track 0.25 mm; larger net-specific widths |
| Vias | 0.30 / 0.40 / 0.50 mm drills as plotted; consult drill report |
| Mounting | Four 2.2 mm NON-plated holes; component holes and vias are plated |
| Origin | Absolute coordinates for both Gerbers and drills; do not mirror manufacturing layers |
| Outline | Use Edge.Cuts Gerber only; not a rectangular crop or drawing border |

The ZIP contains seven fabrication layers, Gerber job file if produced by KiCad, separate PTH/NPTH Excellon drills, drill maps, drill report and a source/file integrity manifest. Do not send placement SVGs, fit-check PDFs, DSN or SES files as fabrication layers. All non-module main-board components are through-hole; this is not an SMT assembly order.

The export script refuses to create a new ZIP if fresh ERC, DRC, unconnected-net or schematic-parity checks fail. Check **MANIFEST.json** against the current board before using any ZIP; a later schematic/PCB edit invalidates an earlier package. Review the manufacturer's Gerber preview: rounded outline, both copper/mask/legend faces, open plated holes, four separate NPTH mounting holes and empty antenna copper windows. Confirm final hole sizes and mask registration with the fabricator.

Use [the assembly packet](../assembly/README.md) and [release report](../C2_PROTOTYPE_REPORT.md) for population, limitations and bring-up. No PCB order or external upload is performed by this package generator.
