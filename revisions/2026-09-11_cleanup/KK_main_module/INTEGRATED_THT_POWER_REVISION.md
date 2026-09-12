# Integrated through-hole power revision

**HISTORICAL — superseded by [revision B](component_review/REVISION_B.md):** user now wants the socketed ESP32-S3 SuperMini and a separate revised power board with regulation. Integrated charging is no longer a main-board requirement. No power-board edits have been made by this scope revision.

2026-09-10 — latest user direction; feasibility brief, NOT a verified circuit or fabrication release.

**Processor amendment:** replacement with another mini ESP32 is now authorized. See [replacement review](component_review/MINI_MODULE_REPLACEMENT.md) for the Nano-M candidate, separate VUSB/VIN nodes and the additional step-up requirement. No power circuit is released and no SMD rework is authorized.

**Follow-up component review:** [exact-parts register and unresolved power gates](component_review/README.md). The user permits choosing the battery after board design, subject to a defined electrical interface. Its old brand/model is no longer a fixed requirement. Twenty-three datasheets/drawings are archived, but the exact module power circuit and integrated charge/protection implementation still prevent a final component freeze.

## Requirements replacing the separate-power architecture

- Leave the existing `KK_power_module` project unchanged and exclude it from this toy's proposed architecture for now.
- Integrate battery charging, system power routing, protection and voltage regulation on the main PCB using actual through-hole parts. No separate regulator/charger breakout and no factory-populated SMD island on the main PCB.
- The permitted preassembled electronics are the screen and legged ESP32 module; the battery remains a separate, connectorized assembly. No student soldering to cell tabs. Speaker/motor remain electromechanical parts, not driver breakout boards.
- Retain ONE externally accessible USB-C connection for computer data and charging: the existing connector on the ESP32 module. Latest user clarification excludes an additional main-board USB receptacle. Take USB input power through a qualified module header connection to the main-board charger; do not connect USB 5 V directly to the battery. The battery-powered return path and isolation are not yet selected.
- Prioritize student solderability over the previous provisional 50 × 65 mm outline. No replacement dimensions are established yet; retain a comfortable handheld form where feasible.
- Keep existing non-power component candidates provisionally, but requalify rail voltage/current and mechanical fit. Prior kit CSV/report power rows and totals are superseded, not a purchasing release.

## Feasibility evidence, not selected purchase parts

**Lithium charging is possible with a true through-hole IC.** Analog Devices lists **LT1512CN8#PBF** and **LT1512IN8#PBF** in 8-lead PDIP. The LT1512 implements a switching constant-current/constant-voltage charger with a 2.7 V maximum specified minimum operating input, making nominal 5 V USB input a plausible starting point. This is not a complete USB charger, cell-protection system or charging safety controller by itself.

Sources: [manufacturer ordering table](https://www.analog.com/en/products/lt1512.html), [LT1512 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/1512fc.pdf).

The IC requires magnetics, a diode, capacitors, sensing/feedback and a carefully laid out switching loop. Additional circuitry must address charge termination/restart, deeply discharged or absent cells, permitted charging temperature, fault timeout, input-current limits, reverse current and system load sharing. Do not adopt an old example circuit as a complete modern toy battery-safety design. Source pricing and a full THT magnetics/capacitor implementation remain open; this approach is not established as cheaper than an SMD module.

**Regulation remains a separate design task.** The previously discussed MCP1826S-3302E/AB is a THT linear-regulator candidate, not a buck-boost replacement: heat and low-battery headroom still apply. Integrating charging does not automatically supply regulated 3.3 V. A THT switching alternative must be sized for the actual load and sleep-current target.

## One-port USB gate

With the module's existing port, USB data stays entirely on the module; the main PCB does NOT need header access to GPIO19/D− or GPIO20/D+. The main-board charger instead needs USB power and ground through the module header. Source for native USB: [Espressif schematic checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html).

The [NOLOGO reference schematic](https://wiki.nologo.tech/assets/img/esp32/esp32s3supermini/1.png) shows USB VBUS tied to H2 pin 1 and an onboard TP4054 charger, plus a BAT-to-VBUS diode. This establishes a plausible header-powered charging architecture, not exact compatibility: the delivered Teyleten board has not been matched to this schematic. The illustrated battery diode also means isolation must not be assumed. Check the real board's continuity, module current/thermal limits and reverse-current behavior before wiring. Leave its battery pads unused when using the separate main-board charger; do not parallel chargers.

Do not assume that taking 5 V from a SuperMini header is isolated or safe on battery, or that its onboard charger can operate in parallel with the proposed charger. Resolve the exact module schematic, reverse-current paths, VBUS sensing, reset/boot recovery and powered-off states before selecting the USB topology. No soldering to hidden SMD pads is permitted. A module replacement needs an explicit selection decision, not a silent swap.

No additional USB-C receptacle is planned. Review the existing module's USB-C CC termination and ESD implementation, plus negotiated/advertised input-current limits for the combined toy and charger. A fixed 500 mA charging setting is not a universal entitlement to draw that much from every computer port, especially before enumeration.

## Battery and release gates

- Qualify the exact cell/pack datasheet, charge voltage/current, temperature limits, connector polarity and protection. A protected pack is a candidate within the separate-battery allowance, not evidence that the current pack is protected. Pack protection does not replace correct charging.
- Complete independent battery fault protection and a fail-safe charging shutdown strategy; do not depend solely on downloadable game code or normal ESP32 execution for battery safety.
- Establish whole-system operating/peak current, USB load priority, thermal behavior and low-battery shutdown. The old power board's switch rating no longer constrains the new design, but every replacement path component must be rated.
- Bench-test charging alone and with system load, battery/USB insertion and removal, low/absent battery, temperature faults, output shorts, charge termination and firmware failure. Use current-limited equipment and qualified battery review before student trials.
- Audit every exact BOM package, footprint and assembly operation for THT compliance. Size the board only after these blocks are credible.

Current result: the requirement is technically plausible and a real DIP charger exists. No complete all-THT power circuit, final BOM, main-board schematic, routed PCB or safety qualification has been completed.
