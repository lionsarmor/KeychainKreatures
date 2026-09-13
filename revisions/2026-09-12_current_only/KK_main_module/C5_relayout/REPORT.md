# C.5 compact landscape main-board pass

## Result

The revised **84 × 95 mm** board is routed and passes the stored electrical/clearance checks. It is **13.26% smaller in area** than the 80 × 115 mm C.4 board. This is an engineering prototype, not a powered or production-qualified toy. No power-module changes, firmware implementation, battery selection or manufacturing order were performed.

| Requested change | C.5 result |
|---|---|
| Screen-focused layout | Existing screen rotated to landscape, centered above controls. Logical 280 × 240 viewport; no resolution loss. |
| Controls below screen | Four D-pad switches left, four action switches right, one mode/function switch in the center. |
| Tighter through-hole placement | Supporting parts moved/repacked on the rear; 25 low-current resistors use upright 2.54 mm lead forms with unchanged values/MPNs. Audio/load resistors remain flat. |
| ESP32 centered on rear | Rear horizontal center, toward top. Antenna faces top edge; USB faces interior for service access. Both-layer antenna keep-outs checked. |
| IR transmitter and receiver | Rear D1 TSAL6200 given a nominal top-facing lead form. Existing U2 TSOP38238 receiver retained beside it, also facing top. Optical windows/baffle and sample lead forming still required. |
| RGB, sockets and connectors | RGB stays front upper-right. ESP32, display, SD, DIP chips and RGB removable; top-entry JSTs retained. SD has a side-access path. |
| Labels and logos | Pin-1/polarity/function labels updated; KiCad and standard open-gear silkscreen artwork added. No certification claim. |
| 3D and fit outputs | All 98 electrical positions modeled; front/rear/angled images, STEP and actual-size fit PDFs exported. Module dimensions and some mating stacks remain nominal. |
| Routing and checks | Fresh local FreeRouting export/run, five native-DRC open connections repaired, isolated thermal contacts corrected and two redundant one-layer vias removed. All final opens cleared. |
| Handoff | C.5 BOM, kit extras, debug map, assembly guide, circuit review and guarded prototype fabrication export. C.4 source backup preserved. |

## Final checks

| Check | Result |
|---|---:|
| Schematic ERC violations | 0 |
| PCB DRC violations under stored rules | 0 |
| Unconnected items | 0 |
| Schematic parity issues | 0 |
| Component pads independently checked | 297 |
| Pin/net/value changes | 0 |
| Electrical positions / modeled positions | 98 / 98 |
| Bare debug holes / mounting holes | 25 / 4 |
| Routed segments / vias | 1333 / 49 |
| Ground pours / antenna rule areas | 2 / 2 |
| Independent minimum-width violations | 0 |

Evidence: [ERC](ERC.json), [DRC/parity](DRC.json), [independent verification](VERIFICATION.json), [route audit](ROUTE_AUDIT.json), [fabrication manifest](manufacturing/MANIFEST.json). The native report's inherited ignored categories remain disclosed; no new category was disabled to force a pass. The existing bare-TP courtyard exception applies only to unpopulated debug holes, not normal component leads.

The copied project had reverted to a single 0.2 mm default class. C.5 restores the intended signal/audio/load/power widths and verifies their actual DSN export and routed copper. The local repair geometry was also corrected to use the full rounded-square capacitor pad outline; native DRC caught the early repair intersections, and final routes clear them. Earlier candidate reports are retained for traceability and are **not** release results.

## Electrical path checks

Measured trace-graph lengths, excluding via barrels and plane shortcuts:

| Path | Routed length |
|---|---:|
| U3 supply bypass C26 → supply pin | 4.43 mm |
| C26 return → U3 ground | 4.33 mm |
| U3 local bulk C25 → supply | 8.66 mm |
| Feedback C21 negative → U3 pin 5 | 8.75 mm |
| Feedback C22 → U3 pin 5 | 4.01 mm |
| Output stability capacitors → U3 outputs | 3.55 / 6.41 mm |
| Motor suppression C16 → J4 supply/return | 5.66 / 5.66 mm |
| Motor switch Q4 drain → J4 return | 4.04 mm |
| IR receiver ceramic / bulk → supply | 3.11 / 4.63 mm |
| MCP23017 ceramic C8 → VDD | 3.71 mm |
| Display ceramic / bulk → header supply | 3.38 / 8.69 mm |
| SD ceramic / bulk → header supply | 7.14 / 10.49 mm |
| RGB-driver ceramic → VDD | 3.08 mm |

The lower-edge speaker connector creates approximately 44.7/49.1 mm output traces; these are 0.50 mm load paths, not high-impedance input routes. Motor bulk C17 is about 19.2 mm of copper from J4, while the actual suppression capacitor and switch paths are short.

**Not every same-net capacitor is local.** C9's route to U1 is about 65 mm; count C8 as the local high-frequency bypass, not C9 as a close reservoir. C11 serves the SD side, not U1. The IR-filter test-point branch is long and must be checked for noise pickup on hardware. R37/R39 gate-bias paths are also longer than the amplifier's local feedback network; test reset, switching and simultaneous-load behavior. These are explicit prototype qualification items, not claims that a clean DRC proves analog performance.

At nominal 35 µm copper, the 113.7 mm, 0.8 mm-wide MCU feed is roughly 0.07 Ω at room temperature: about 42 mV drop at a hypothetical 0.6 A. This trace-only estimate excludes the source, connectors, socket, return and module regulator. Actual rail dips and current budget must be measured.

## Before ordering a kit batch

Read the [full circuit review](CIRCUIT_REVIEW.md). The significant holds are:

- **Power:** J1 needs regulated, coordinated 5 V / GND / 3.3 V / 3.2 V; the unfinished power module and a raw battery are not interchangeable with that interface. No simultaneous USB/SYS_IN power without qualified isolation.
- **Depth:** the nominal socketed front/rear assembly requires roughly **39 mm overall component depth before case walls/clearance**, despite the smaller PCB area. Review the STEP and real samples before shell design.
- **Mechanical:** actual module/header dimensions, RGB socket grip, upright and IR lead forms, screen support, card access and harness bends remain sample checks.
- **Function:** speaker continuous-power rating, audio stability/volume, display BLK load, motor startup, RF/IR range, safe firmware initialization and SD power-loss recovery need bench qualification.

## Open and print

[Native project](KK_main_module.kicad_pro) · [Front 3D](front-3d.png) · [Rear 3D](back-3d.png) · [Angled 3D](angled-3d.png) · [STEP](KK_main_module_C5_assembly.step)

[Front actual-size fit PDF](front-fit-check.pdf) · [Mirrored rear fit PDF](back-fit-check.pdf) · [Schematic PDF](KK_main_module.pdf)

[Printable BOM](assembly/C5_BOM_PRINT.html) · [Assembly guide](assembly/ASSEMBLY_GUIDE.md) · [Debug map](assembly/C5_TEST_POINT_MAP.csv) · [Prototype fabrication ZIP](manufacturing/KK_MAIN_C5_PROTOTYPE_FAB.zip)

Reload any stale KiCad editor tab from disk before saving. Do not mix C.4 Gerbers/fit sheets with this C.5 population.
