# Historical component investigations — not the current BOM

Use the current [C.6 reference BOM](../C6_flat_stack/assembly/C6_BOM_BY_REFERENCE.csv), [complete paired-kit extras](../C6_flat_stack/assembly/C6_COMPLETE_KIT_EXTRAS.csv), [assembly guide](../C6_flat_stack/assembly/ASSEMBLY_GUIDE.md) and [P.3 power status](../../KK_power_module/CURRENT_STATUS.md). The dated investigations below include superseded architectures and open-item lists. Their “CURRENT” labels refer to the time they were written, not today's release.

**CURRENT circuit work:** the [revision C editable schematic and validation](../schematic/README.md) supersede revision B's logical connection/GPIO tables. Use the [KiCad-exported draft BOM](../schematic/SCHEMATIC_BOM.csv) for captured circuit quantities. Assembly-only kit items and physical qualification still need completion before the final BOM is released. Older component-review statements below describe their original review date, not today's schematic status.

**Datasheet audit completed:** [part-by-part index](DATASHEET_AUDIT.md) / [download packet](MAIN_BOARD_DATASHEETS.zip). Standard-part documentation is distinct from circuit/fit work: 31 BOM rows have manufacturer documents/drawings, three modules have partial documentation, and the exact speaker sheet was not found. Other rows are unselected/custom parts or unfinished circuit groups. No part substitution or schematic qualification is implied.

**Print list:** [main-board HTML](MAIN_BOARD_PRINT.html) / [Markdown](MAIN_BOARD_PRINT.md). All added regulators, including the motor regulator, are deferred to the separate power board. The print view excludes power-board and enclosure parts but includes main-board open items; it is not a final bagging list. Incoming rail/connector requirements still need agreement before routing.

**Latest addition:** [separate microSD reader plan](SD_STORAGE.md). Retain XIITIA B0DFWL25RB; add B0F82XWT4F under the screen as a placement target. SD card, header/socket and support requirements are included in the updated master table. User's back-side photo confirms the 3V3 supply label and six-signal order; delivered-module electrical testing, footprint orientation and stack-up remain pending.

**CURRENT — revision B:** [architecture and browser/Wi-Fi plan](REVISION_B.md), [updated component table](MASTER_BOM.md), [CSV](MASTER_BOM.csv). Main MCU is again a socketed ESP32-S3 SuperMini; charging and system regulation move to a future separate power-board revision. Main-board interface is SYS_IN. Previous Waveshare physical pin mapping is withdrawn; the connection table now retains only logical MCU ports. Entries below describing integrated charging or Waveshare selection are historical and superseded.

## Historical revision A review

2026-09-10. **NOT A FINAL BOM.** The non-power selections have been consolidated, but a complete safe power circuit has not been selected. Do not buy this as a complete kit or fabricate a board from it.

**Current entry point:** [whole-kit component table](MASTER_BOM.md), [spreadsheet CSV](MASTER_BOM.csv), and [initial circuit design](CIRCUIT_START.md). These supersede earlier module proposals and quantity pools. The selected processor is now the full-size Waveshare ESP32-S3-DEV-KIT-N16R8-M, SKU 28836, sourced directly from Waveshare. Full-size is explicitly accepted; battery power remains unqualified.

- [41-row exact-parts register](parts.csv): component identities, packages, planned quantities, datasheets and individual holds.
- [Datasheet index](DATASHEETS.md): archived manufacturer documents and original URLs.
- [Power requirements](../INTEGRATED_THT_POWER_REVISION.md): current integrated-board scope.

This register supersedes power assumptions in older kit lists. There is no separate power module, regulator breakout or main-board USB connector. Only the ESP32 module's USB-C port is externally accessible. All main-board electronic parts must be THT; the preassembled ESP32 and screen are the permitted electronics exceptions. Wired actuators and the connectorized battery remain electromechanical assemblies. Board size is secondary to student assembly.

## What can be carried into the schematic

| Function | Exact baseline | Remaining condition |
|---|---|---|
| ESP32 module | Waveshare ESP32-S3-DEV-KIT-N16R8-M, SKU 28836 | User-selected; battery power path NOT qualified |
| Screen | XIITIA B0DFWL25RB | Retained; module-specific pinout/backlight circuit needs verification |
| GPIO expander | Microchip MCP23017-E/SP | Narrow DIP-28; GPA7/GPB7 output-only, never button inputs |
| Nine soft buttons | Adafruit 3101 | One ten-pack; sample dimensions before footprint/caps |
| Audio amplifier | UTC TDA2822L-D08-T | DIP-8; PWM filtering, attenuation, bridge wiring and supply gating needed |
| Speaker | FUET FS1511P08-H3.0 wired | HOLD: no controlled drawing recovered; listing conflicts on rated power |
| Motor | LEADER LCM0827A3038F | Wired; full 2025 specification now archived |
| Motor regulator | Microchip MCP1700-3002E/TO | Candidate 3.0 V rail, TO-92; startup/stall/thermal tests required |
| IR transmit / receive | Vishay TSAL6200 / TSOP38238 | 940 nm transmitter and 38 kHz demodulating receiver; drivers/filtering required |
| Drivers | onsemi KSP2222ABU / BC32725BU | TO-92; counts/base drive depend on schematic |
| Motor flyback | Vishay 1N5819-E3/54 | Axial; additional power-diode use not qualified |
| MCU sockets | 2 × Sullins PPTC221LFBN-RC | 22-way, THT; verify module fit and row spacing |
| DIP sockets | On Shore ED281DT / ED08DT | GPIO / amplifier respectively |
| Screen socket | Sullins PPTC081LFBN-RC | Eight-way THT; match actual screen orientation |

The CSV also includes exact JST connectors/contacts, the cell thermistor, nine resistor values and five capacitor values. Their counts are explicitly not a released bag list. No invented final quantities or total kit price.

## Blocking finding: battery power into the selected module

The USB charging input is only half of the circuit. Battery power must also reach the ESP32 without energizing the computer's USB power connection or reverse-driving its onboard regulator.

The [NOLOGO reference schematic](datasheets/nologo-reference-schematic.png) connects USB VBUS directly to the 5 V header and the ME6217 regulator input. It also shows a BAT-to-VBUS diode. It resembles this board but is NOT a controlled schematic for the exact Teyleten assembly. The user's screenshots confirm the ASIN and show the 5 V/GND/3V3 headers and separate underside battery pads; seller photos do not establish continuity or current ratings.

| Proposed battery connection | Unresolved problem |
|---|---|
| Module 5 V header | On the reference design, this also energizes the USB connector VBUS. A diode only in the external charger branch cannot break that internal connection. |
| Module 3V3 header | The onboard regulator is still connected. The ME6217 datasheet warns of reverse current when its output exceeds input by over 0.3 V. |
| Underside B+/B− pads | Not THT header connections; invoke the onboard charger and do not establish USB isolation. No hidden-pad student soldering is authorized. |

See [ME6217 manufacturer-authored datasheet, page 7](datasheets/me6217.pdf). This is conditional evidence from the reference circuit, not a claim that every Teyleten revision is identical. **No unmodified header-only solution has been qualified.** A larger main-board regulator does not fix internal module isolation.

The user has now approved investigating a documented alternative mini module. See the replacement review above. No factory rework or student SMD work is authorized, and no replacement circuit has been released.

## Battery may be selected later, against this interface

The user explicitly deferred the battery brand and physical size. This is no longer a requirement to retain the old MakerHawk pack. Define an electrical envelope before layout, then choose a compliant pack later:

- One conventional Li-ion/LiPo cell, 3.6/3.7 V nominal, 4.20 V charge endpoint. Not 2S, LiFePO4 or a 4.35 V high-voltage cell.
- Proposed connector: JST B3B-PH-K-S(LF)(SN), three pins: **1 BAT+, 2 NTC, 3 BAT−**. This is our proposed assignment, not a universal JST convention. The future pack/harness must match it. Three pins also distinguish it from the two-pin actuator ports.
- Vishay NTCLE100E3103JB0 tracks cell temperature through an insulated harness and suitable thermal attachment. It must not merely measure PCB ambient temperature.
- Initial engineering charge target: at most 100 mA, reduced or disabled when USB has insufficient remaining current for both the toy and charging. This is not a released charger setting. The selected cell must expressly permit the configured charge current and temperature range.
- Initial pack capability target: at least 1 A continuous and 1.5 A brief discharge, to be checked against the complete load budget. These are proposed pack requirements, not measured toy consumption or USB allowances.
- Prefer documented pack protection as independent backup; it does not replace correct charging and normal low-battery cutoff. If all protection must additionally be on the main PCB, that circuitry remains an unresolved design block.
- Capacity, supplier and shape can be chosen later; connector polarity, charge/protection architecture and current/temperature limits cannot be left arbitrary after fabrication.

## Important corrections from the recovered drawings

- Motor drawing: AWG32 leads, 27 mm nominal lead length, 8 mm body diameter, 2.7 mm body thickness plus adhesive/foam. Its operating range is 2.7–3.3 V. A nominal 3.3 V supply with positive tolerance can exceed that limit; a dedicated 3.0 V rail is proposed, subject to dropout/stall/thermal checks.
- JST SPH-004T-P0.5S is the conductor-size candidate for those motor leads (AWG32–28). The older SPH-002 selection does not cover AWG32. Verify the actual insulation diameter fits 0.5–0.9 mm before crimping. Use factory-prepared harnesses.
- Adafruit's listing says 4.9 mm button height; its supplied drawing says 5.5 mm with an 8 × 4.5 mm hole pattern. Sample before fixing the footprint and cap travel. The listing does not guarantee force; do not advertise the drawing's force as a controlled delivered specification.
- The UTC amplifier's high gain requires attenuation and filtering of a logic-level PWM signal. In bridge operation, neither speaker terminal is ground. Include stability networks, anti-pop behavior and powered-off input protection.
- The TSOP38238 is a demodulating receiver with carrier/burst/gap constraints, not a raw arbitrary-frequency IR receiver. Design pet-trading timing accordingly.
- Passives in the CSV are a value pool. Charge-voltage accuracy, current sensing, compensation, timing, switching-converter ripple and magnetics need their own calculated exact parts.

## Power parts still missing from a final list

| Block | Status |
|---|---|
| USB/battery isolation and MCU return supply | Blocked on the exact module circuit and permitted integration method |
| Charger | LT1512CN8#PBF is a real PDIP CC/CV candidate, NOT a complete autonomous charger/protection system |
| Independent charge supervision | Exact termination, precharge, restart, timeout and temperature-fault circuit not selected; do not rely solely on game/ESP32 software |
| Charger magnetics and sensing | Inductors, switch/diode, precision feedback/current-sense resistors and compensation depend on charger topology |
| Main voltage regulation | MCP1826S-3302E/AB is only a linear alternative; battery dropout and USB heat remain. No full-current THT buck-boost circuit selected |
| Battery protection | Exact independent overvoltage, undervoltage, overcurrent and short-circuit implementation unresolved |
| Input current / load sharing | Whole-toy and charger current, USB enumeration/suspend and source limits must be handled together |
| Disconnect / reverse polarity / fuse | No exact system-rated switch/FET/fuse selected. A PTC alone is not lithium protection; do not reuse the old 0.3 A switch as the whole-system load switch |
| Indicators / ADC sensing / service | Level conditioning, default-off sensing, test points and charge/fault LEDs require defined power states and quantities |
| Power support parts | Supervisor sockets, precise passives and bulk capacitors are not covered by the current non-power register |

[LT1512 manufacturer documentation](https://www.analog.com/en/products/lt1512.html) confirms the package, but does not make the missing circuit complete. BQ2054PN was also investigated: TI describes a DIP-capable family with more charging supervision, while DigiKey labels the exact PN obsolete. That lifecycle discrepancy must be resolved before any selection; it is not adopted here. [TI](https://www.ti.com/product/BQ2054), [exact-PN distributor listing](https://www.digikey.com/en/products/detail/texas-instruments/BQ2054PN/380003).

## Source gaps and next schematic step

The [Teyleten listing](https://www.amazon.com/dp/B0D47HBFDY) is a module identity, not a controlled board datasheet. The [XIITIA listing](https://www.amazon.com/dp/B0DFWL25RB) does not replace its module/backlight schematic. The [FUET seller listing](https://korean.alibaba.com/product-detail/15-11MM-8-Ohm-0-5W-1600442871788.html) still needs a drawing and unambiguous nominal power. None of those missing documents has been fabricated or silently replaced with a chip-only datasheet.

The user's screenshot shows $16.99 for three ESP32 modules, about $5.66 each before tax/shipping; that is user-provided evidence, not a fresh checkout quote. No total cost is claimed while the power BOM is unresolved.

Non-power schematic blocks can start from the exact baselines, with the listed interface holds. The complete board cannot be called component-frozen until the module power connection and full THT charger/protection circuit are resolved. Then calculate all passive values, verify package pinouts, export actual quantities and audit student assembly.

No purchases, supplier messages, battery tests, schematic capture, hardware modifications or changes to the reusable power-board project were made in this review.
