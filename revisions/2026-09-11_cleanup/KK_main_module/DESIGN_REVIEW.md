# Compact main-module feasibility report

2026-09-10. Engineering review, not a fabrication release. Requirements: [DESIGN_BRIEF.md](DESIGN_BRIEF.md). Costs: [COST_ESTIMATE.md](COST_ESTIMATE.md).

**Later user amendment:** comfortable compact board first; user models the shell afterward. [BOARD_FIRST_PLAN.md](BOARD_FIRST_PLAN.md) supersedes this report's original 46 × 62 × 19 mm / 42 × 52 mm limits and enclosure-first sequencing. Start with a provisional 50 × 65 mm PCB. The dimensional sections below are the earlier constrained-envelope study, retained as historical analysis; electrical findings remain open/current.

## Verdict

**Student-kit amendment:** [STUDENT_KIT_REQUIREMENTS.md](STUDENT_KIT_REQUIREMENTS.md) also supersedes all direct-mounted SMT core/regulator/audio recommendations below. The ESP32 must be a preassembled module with through-hole legs. Bare-module dimensions in this historical comparison do not include a compliant carrier/header/socket; no exact processor or regulator is approved. Reassess footprint and sourcing accordingly.

Keep the 46 × 62 mm face, existing display, nine controls and separate RODDY board as the design target. **19–20 mm assembled depth is not yet demonstrated.** The battery/board/component stack is the highest-risk constraint, ahead of processor body size. No evidence yet proves that 42 × 52 mm cannot accommodate the circuitry; there is also no placed-board evidence that it can. Do not enlarge or route it on either assumption.

The previous large WROOM default, eight-button map and sub-GHz reservations have been withdrawn. No main schematic/layout or production enclosure has been generated. No power-board circuitry was changed.

## 1. Mechanical arithmetic and collision risks

Dimensions below distinguish user targets, source-file evidence and provisional assumptions. See [printable worksheet](mechanical/fit-study.svg); its front controls are an ergonomic study, not manufactured-part geometry.

| Check | Calculation / evidence | Consequence |
|---|---|---|
| Width | 46 mm shell minus 42 mm PCB = 2 mm per side | That 2 mm includes wall thickness; it cannot also be a 2 mm air gap |
| Trial wall | With 1.6 mm side walls: internal width 42.8 mm | Only 0.4 mm clearance per PCB side; printer tolerance, board tolerance and bosses still matter |
| Literal 2 mm internal gap | 42 + 2 × (1.6 + 2) = 49.2 mm | Would exceed width target; use local notches/clearance review before proposing growth |
| Depth lower bound | 10 mm cell + 1.6 mm main + assumed 1.6 mm power PCB + 2 × trial 1.2 mm face skins = **15.6 mm** | Only **3.4 mm at 19 mm**, or **4.4 mm at 20 mm**, remains for display, all overlapping parts, solder tails, insulation and gaps |
| Nominal display active area | 1.69 × 25.4 mm diagonal, square pixels, 240:280 aspect → about **27.94 × 32.59 mm** | This is NOT the glass, flex, breakout or bezel envelope; cannot assign mounting geometry from diagonal |
| Power-board outline | Existing Edge.Cuts spans approximately X198.70–228.70 and Y42.35–82.35 mm | Approximately 30 × 40 mm confirmed from PCB; protruding/mated connectors not included |
| Flat battery/power placement | Battery footprint 20 × 50 mm; power PCB 30 × 40 mm | In an axis-aligned layout, narrowest side-by-side width is 50 mm; end-to-end height at least 80 mm. They cannot simply occupy one nonoverlapping plane inside this shell |

The depth bound applies where all four assemblies overlap; it is not a final stack prediction. Actual battery protection, tabs, wrap and permitted clearance may add depth/length. Neither housing force nor clipped leads may press into the pouch. Provide an insulating barrier and a mechanically retained cell pocket with no screw path into the cell; verify clearance against the actual pack maker's guidance.

The power-board BOM already specifies right-angle JST-PH connectors on both board faces and vertical 2.54 mm headers. **The mated headers/cables and underside battery connector are real volume consumers**, not just PCB thickness. Account for USB plug insertion and the power actuator too. Short wiring to a reviewed low-profile connector may help; unsocketed leads are thinner but reduce repairability. No substitution is approved by this report.

### Through-hole placement budget — provisional courtyards, not a fitted layout

| Consumer | Trial XY allowance | Area | Main concern |
|---|---:|---:|---|
| Nine 6 mm-class tact switches | 9 × (8 × 8 mm) | 576 mm² | Solder feet, cap travel, D-pad pivot and simultaneous presses; actual switch drawing required |
| PCF8574N DIP-16 plus assembly margin | 22 × 11 mm | 242 mm² | Socket/body height and solder tails |
| DIP-8 amp with filter/coupling/bulk parts | 18 × 20 mm | 360 mm² | Capacitor heights and socket accessibility |
| S3-MINI bare module body | 15.4 × 20.5 mm | 316 mm² | Excludes antenna keepout, carrier, support parts and solder courtyard |
| Four trial boss exclusion disks | Diameter 5 mm each | 79 mm² | Not mounting-hole coordinates or validated boss strength |
| Subtotal / raw 42 × 52 rectangle | 1573 / 2184 mm² | ~72% | Still omits regulator, connectors, IR, haptic driver, sensing, routing and corner loss |

These are planning allocations, not additive proof of routing density: parts may occupy opposite faces, but through-hole tails and overlapping height envelopes limit that freedom. The active PCF8574N option is documented by [TI](https://www.ti.com/lit/ds/symlink/pcf8574.pdf). Keep an all-direct nine-button GPIO option open on a sufficiently exposed S3 module: eliminating an unnecessary expander is a valid space optimization, not an SMT conversion. It needs more routing and exact-module pin verification.

### Smallest-change sequence

1. Obtain actual component envelopes; keep 46 × 62 × 19 mm and 42 × 52 mm as the trial boundaries.
2. Nest component heights into unoccupied front/control regions and power-board voids; offset the battery and route wires along channels. Keep copper/battery/display away from the RF keepout. Validate local cross-sections, not only overall volume.
3. Prefer low-profile THT parts and selective sockets; try direct button GPIO before paying for a DIP expander in both area and height. Socket choices require an explicit repairability tradeoff.
4. Evaluate only necessary connector-orientation changes on RODDY. Preserve its electrical architecture.
5. If measured depth is the remaining conflict, show a 20 mm option first. Any further change must state exactly how many millimeters are missing and which part causes them. A thinner cell, different display assembly or SMT audio is a separate user decision, not an assumed optimization.

### FDM concept

Use a flat cosmetic front plate, a separately printed midframe carrying the loads, and a flat-backed rear cover. Put screw access on the rear; trial captive M2 nuts or tested printed pilot holes where boss width permits. Avoid fitting four oversized heat-set-insert bosses by default. Captive button caps and a pivoted D-pad need positive travel stops so squeezing the shell does not preload the switches. A replaceable keyring lug should transmit force into the midframe, not the display bezel. Print-fit coupons must establish actual clearances before defining production offsets. No STL is issued from this unmeasured study.

## 2. Compact processor options

| Candidate | Documented size / memory | Assessment |
|---|---|---|
| ESP32-S3-MINI-1-N4R2 | 15.4 × 20.5 × 2.4 mm; 4 MB flash, 2 MB PSRAM | Strong integrated-board size candidate, but app/update storage is tight; underside lands require a preassembled SMT core, not novice THT soldering |
| ESP32-S3-MINI-1U-N4R2 | 15.4 × 15.4 × 2.4 mm; same memory | Smaller body, but needs external antenna, connector/cable and antenna placement volume |
| Seeed XIAO ESP32S3, normal version | 21 × 17.8 mm; 8 MB flash, 8 MB PSRAM; 11 ordinary GPIO | Useful tiny prototype reference; insufficient exposed GPIO for the independent interfaces budgeted here without compromises/additional pads. Includes extra USB/charging circuitry and external antenna |

Source specifications: [Espressif MINI datasheet](https://documentation.espressif.com/esp32-s3-mini-1_mini-1u_datasheet_en.html), [Seeed board documentation](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/). “Super Mini” alone does not establish memory, pin access, regulator quality or sleep consumption. The MINI **N8 has no PSRAM**; do not accidentally substitute it for N4R2. MINI-N4R2 GPIO26 is consumed by PSRAM. Do not carry over WROOM-octal pin restrictions without checking the selected variant.

Recommendation: fit-test the MINI-1 footprint and a small preassembled core strategy, while comparing storage and assembly cost before selecting it. Prefer **8–16 MB flash and 2 MB or more PSRAM as design targets**, not a claim that the listed MINI part has those flash sizes. A 4 MB design must demonstrate room for firmware/recovery, filesystem and pet data; extra storage carries its own footprint and I/O cost. XIAO Plus/other cores require exact schematic and underside-pad review before being treated as solutions. No carrier or module is frozen.

## 3. Audio decision

NJM2073D's 1.8–15 V operating range includes 3.3 V; voltage alone does not disqualify it. Its quoted 6 mA typical idle current is specified at 6 V, not a measured 3.3 V result. It lacks a dedicated shutdown pin and would need supply gating. Its high-voltage/high-distortion watt ratings must not be promised into this product's 8-ohm speaker at 3.3 V. See the [manufacturer-authored NJM2073 datasheet, distributor-hosted](https://akizukidenshi.com/goodsaffix/njm2073d.pdf). [DigiKey lists the exact DIP part as obsolete](https://www.digikey.at/en/products/detail/nisshinbo-micro-devices-inc/NJM2073D/673707); treat existing genuine stock as an experiment, not a secure production supply.

A promising **THT candidate to qualify is Holtek HT82V739 in DIP-8**: the manufacturer-authored excerpt specifies 2.2–5.5 V, enable/shutdown, and 300 mW typical into 8 ohms at 3 V and 1% THD+N. Source: [Holtek datasheet excerpt hosted with the distributor kit](https://akizukidenshi.com/goodsaffix/AE-82V739_20220725.pdf). Verify current DIP availability, complete package/reference circuit and real audio behavior before substitution; it is NOT pin-compatible with NJM2073D. Pull CE high for disabled reset behavior, and follow reference-bias/startup sequencing.

Do not replace either with a standard LM386 on a 3.3 V rail: [TI specifies minimum 4 V or 5 V by variant](https://www.ti.com/lit/ds/symlink/lm386.pdf). An I2S class-D solution such as [MAX98357A](https://www.analog.com/media/en/technical-documentation/data-sheets/max98357a-max98357b.pdf) is a useful efficiency/quality fallback, but its SMT implementation is an explicit alternative, not the adopted THT design.

S3 audio needs an external conversion path for an analog amplifier. Prototype filtered high-rate PWM with attenuation/bias/coupling appropriate to the amplifier; sampled audio is possible but fidelity, hiss and CPU/DMA load need testing. If inadequate, compare an external DAC plus DIP amp against the explicit I2S alternative. Neither bridge speaker output is ground. Use the actual 8-ohm speaker's power rating and sealed-shell loudness tests to set volume limits.

## 4. Electrical fixes retained from the breadboard review

- IR receiver directly to MCU pulse-capture/RMT input, never through the button expander. Select a protocol/carrier receiver; a demodulating receiver is not universal raw IR capture. [Espressif RMT](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/rmt.html).
- Nine independent button inputs. Candidate PCF8574 mapping uses all eight bits for directions and A/B/X/Y, with Function directly on a wake-capable pin. Keep boot straps free from gameplay inputs. See [ARCHITECTURE.md](ARCHITECTURE.md).
- Add actual IR LED current limiting/driver, actuator-appropriate motor driver/protection, backlight control and default-off outputs. The old three-pin breakout modules may have provided circuits absent from a bare component.
- RODDY J3 SYS_OUT is not regulated 3.3 V; local regulation remains necessary. J5 status nets and VBAT need safe voltage-domain and powered-off handling. Do not bridge protected BAT_NEG to main GND. Full evidence in [POWER_INTERFACE.md](POWER_INTERFACE.md).
- Existing C&K JS102011SAQN switch is a rated-path concern: [manufacturer guide](https://www.ckswitches.com/media/2222/shortform.pdf) gives 0.3 A at 6 V DC. Example 3.3 V × 0.5 A / (3.0 V × 90%) = 0.611 A upstream, already above that rating. This is an illustrative load, not measured failure. Resolve real peaks before release; do not bypass protection/switching to make the prototype run.
- RODDY USB currently provides power, not routed MCU data. Preserve an accessible programming/recovery path without joining independently driven USB supplies or parallel chargers.

## 5. Runtime budget — battery-side, illustrative

1000 mAh / 168 h = **5.95 mA** average for one nominal week. Reserving an illustrative 20% for unusable capacity/tolerance yields **4.76 mA**. Neither number establishes the actual pack capacity or regulator efficiency.

| Defined test profile | Assumed battery current | Calculated runtime with 800 mAh usable |
|---|---|---|
| Continuous screen-on gameplay | 200 mA | 4.0 h |
| Continuous heavier gameplay | 300 mA | 2.67 h |
| 20 min/day play, remaining time asleep | 200 mA active, 0.10 mA whole-product sleep | 11.6 days |
| Same usage, higher active demand | 300 mA active, 0.10 mA whole-product sleep | 7.8 days |

These estimates include no separately added current because the assumed currents must be measured at the battery and encompass the whole device. An always-on load of 6 mA alone consumes 1008 mAh/week; that is a generic illustration, NOT NJM2073's measured idle draw at our voltage. Set an initial whole-product sleep target of ≤100 µA, then test whether the existing power path and selected MCU assembly can meet it. Do not advertise the target until measured. Screen-on hours, sound level, IR use and trade frequency must accompany any battery-life claim.

## 6. Verification and immediate next inputs

Completed in this revision: full brief and root DOCX intake; current power PCB outline/BOM cross-check; processor and audio source review; arithmetic fit/current/runtime checks; obsolete proposal isolation; functional I/O and cost estimates; a printable front/stack worksheet ([PDF](mechanical/fit-study.pdf)). The DOCX's MCP23008 and exact discrete-component candidates remain for qualification; see [change log](CHANGELOG.md). This is document/design analysis, not ERC, DRC, thermal, RF or prototype testing.

Needed for physical closure: product link or dimensional drawing and front/back photos of the exact TFT; caliper measurements of the protected battery including tabs/lead exit; speaker diameter/thickness/power rating; motor type/dimensions/rating. The screen assembly is the first bottleneck. Populate component height models and connector mating envelopes, then validate 1:1 controls and CAD cross-sections. Only afterward freeze the enclosure, outline, schematic and routing.

Prototype acceptance must include: every button/chord and wake/reset behavior; display/update load; sampled audio and pops; IR under simultaneous gameplay; motor stall/transients; minimum-battery and USB transitions; status isolation with MCU off; whole-product sleep/active current; charger/cell temperature; antenna performance in the assembled shell; power loss during saves/app updates/trades; fastener access and repeated keyring/button loading. Clean ERC/DRC is necessary but not evidence that these tests passed.
