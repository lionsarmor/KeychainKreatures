# KK Power Module — Low-Run Release Report

Release: `0.2-LR1`  
Prepared: 2026-09-09  
Intended use: controlled first-article and low-volume pilot manufacture

## Executive decision

The design package is suitable for quotation and a five-unit controlled pilot build. It is not approved for unrestricted sale or volume production until the numerical product requirements are completed and the first-article tests pass.

## Changes in this release

- Corrected R1 display value from `R5.1 kΩ` to `5.1 kΩ` in schematic and PCB.
- Selected ENIG as the controlled surface finish.
- Locked critical functional and mechanical components in a vendor-neutral production BOM.
- Added controlled passive specifications and example approved MPNs.
- Defined a hybrid low-run process: factory SMT reflow plus hand-installed through-hole connectors and USB shield tabs.
- Added fabrication notes, assembly notes, and a first-article test procedure.
- Generated Gerber X2, separate PTH/NPTH drill data, position data, and BOM outputs.

## Automated verification

The release was checked with KiCad 10.0.6.

| Check | Result |
|---|---|
| Schematic ERC | PASS — 0 violations |
| PCB DRC | PASS — 0 violations |
| Unconnected PCB items | PASS — 0 |
| Schematic/PCB parity | PASS — 0 issues |
| Gerber export with zone check | PASS |
| Separate PTH/NPTH drill export | PASS |
| Placement export | PASS |
| BOM export | PASS |

The board is two-layer FR-4, nominally 1.60 mm thick with 35 µm copper. The routed outline is closed and fabrication outputs generate without tool errors.

## Controlled production assumptions

- Single-cell 4.2 V Li-ion/Li-polymer chemistry only.
- 5 V USB-C input without USB Power Delivery voltage negotiation.
- U1 is the Microchip `MCP73871-2CCI/ML` option.
- Production uses the exact J1, U1, U2, Q1, D1, SW1, and JST connector parts in `production_bom.csv` unless engineering approves a substitute.
- J2 cable polarity is controlled by the product wiring documentation.

## Required first-article closure

The following are deliberately not claimed by CAD checks and must be closed on real hardware:

1. Maximum intended SYS load and acceptable SYS voltage range.
2. Programmed charge-current measurement and agreement with the intended cell.
3. U1 junction/case-temperature margin at maximum load, low battery voltage, and maximum ambient temperature.
4. Charger termination, safety-timer, NTC/NO_NTC, LBO, and protection thresholds.
5. J1/J2/J3 mechanical fit and cable polarity.
6. LED colors, brightness, and status interpretation.
7. Product enclosure clearance and strain relief.
8. Approved battery model and its maximum charge rate.

## Risk register

| Risk | Control |
|---|---|
| Incorrect substituted protection IC/MOSFET pinout | No substitution without engineering approval |
| QFN exposed-pad solder voiding or poor thermal path | Controlled stencil/reflow; first-article inspection and thermal test |
| USB-C or JST mechanical mismatch | Exact MPN lock and first-article fit check |
| Reversed battery harness | Polarity-controlled drawing and 100% continuity test |
| Excess charger heating | Current-limited bring-up and worst-case thermal soak |
| Incorrect pick-and-place rotation | Review assembler placement preview and first article |
| Lithium-cell transport/documentation gap | Use a reputable cell and retain its UN 38.3 test summary |

## Release recommendation

Release only five pilot units initially. Hold the balance until one first article completes the test procedure and all five pass inspection plus one full charge/discharge cycle. After recording numerical limits in the product specification, a 20–50 unit low run is reasonable without another PCB revision if no circuit, footprint, or mechanical changes are needed.

## External references

- Microchip MCP73871 product page and datasheet: https://www.microchip.com/en-us/product/MCP73871
- JLCPCB BOM requirements: https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly
- JLCPCB KiCad BOM/CPL guidance: https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad
- JLCPCB surface-finish comparison: https://jlcpcb.com/help/article/jlcpcb-surface-finish
- PHMSA lithium-battery transport guidance: https://www.phmsa.dot.gov/lithiumbatteries
