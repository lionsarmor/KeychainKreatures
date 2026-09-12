# Component decisions — 2026-09-10

**Latest decision — revision B:** return to ESP32-S3 SuperMini, nine-way sockets, separate revised power PCB, and SYS_IN on the THT main board. Routine software delivery by browser over Wi-Fi and wireless pet trading. See [current scope and limitations](component_review/REVISION_B.md); all contrary processor/power decisions below are history.

Planning record, not a released purchasing BOM or verified circuit. Later user messages override earlier specifications.

**Latest module permission:** the user now accepts a full-size development module and proposes Amazon B08D5ZD528. This supersedes the mini-only restriction. The linked ESP-WROOM-32 board is not an S3/PSRAM replacement; the listing photo shows micro-USB and no matching board-level power schematic has been qualified. Treat it as a user-proposed candidate, not a frozen BOM selection. See the [updated replacement review](component_review/MINI_MODULE_REPLACEMENT.md). No SMD rework is authorized.

**Latest sourcing review:** [single-board component register](component_review/README.md) and [datasheet archive](component_review/DATASHEETS.md). Battery brand/size is deferred by the user; define its electrical envelope now. The previous Teyleten selection is reopened because its header-only battery integration is not qualified. This review also corrects motor crimp selection and records a switch-height drawing conflict.

**Latest architecture amendment:** [integrated THT power](INTEGRATED_THT_POWER_REVISION.md) replaces the separate-power and regulator-breakout permissions below. Main-board charging/protection/regulation must use through-hole parts; screen, ESP32 module and battery remain separate. One external USB-C port must handle charging and data. Size is relaxed, not fixed. No exact integrated power circuit is selected yet.

Latest user amendment: **no XIAO; inexpensive off-brand parts preferred.** Exact processor listing supplied by user: Teyleten Robot ESP32S3SuperMini, Amazon B0D47HBFDY. The photographed ESP32-S3FH4R2 implies 4 MB flash / 2 MB PSRAM; incoming verification and memory-budget qualification remain required. See [entire-kit report](ENTIRE_KIT_PARTS.md), which supersedes the 16/8 recommendation and historical speaker/motor shortlists below. MCP23017-E/SP is the proposed THT expander; Adafruit 3101 is the soft-switch selection. Converter selection reopened with the processor change.

Latest purchasing direction: [budget parts list](BUDGET_PARTS_LIST.md). Retain the Amazon screen; suppliers are no longer restricted to Mouser. Replace the Same Sky speaker preference below with a sampled wired 1511 micro-speaker and seek a generic wired coin motor. Earlier supplier shortlists below are historical references, not active purchase selections.

## Confirmed by the user

- A preassembled regulator module with through-hole pins is permitted on the main board. Students must still assemble a through-hole kit; no main-board SMD soldering or hidden-pad connections. This exception does not authorize unrelated breakout substitutions.
- Charging/protection remains on the separate reusable power module. Its unregulated SYS_OUT feeds regulation on the main board; do not redesign the power module for convenience.
- The user chose to retain the Amazon XIITIA B0DFWL25RB 1.69-inch 240 × 280 display at their approximately $7.50-per-display benchmark. DFRobot and Adafruit alternatives are no longer preferred. Mouser-only sourcing is withdrawn; direct suppliers and wholesalers are permitted.
- No existing speaker or vibration assembly must be retained. Select affordable compact replacements and their necessary driver circuitry.

## Engineering recommendations, not user-approved exact parts

### Memory

Preferred target: **16 MB flash and 8 MB PSRAM on the preassembled compact ESP32-S3 module**. Flash holds firmware, update/recovery space, games/assets and saves; advertised capacity is not all downloadable storage. PSRAM is working memory, not persistent storage. Do not promise a game count before representative packages and firmware are built.

Use 8 MB flash as a cost/size fallback only after showing the tradeoff; do not silently substitute the earlier 4 MB-flash S3 MINI. A 2 MB-PSRAM implementation may be adequate for simple games, but must be benchmarked against the proposed app runtime. Prefer optional microSD expansion when the selected screen already provides a socket; the pet and bundled games should work without a card.

These capacities exist in small S3 boards, but do not establish a compatible kit module. For example, the [Seeed S3 Plus](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/) has 16 MB flash/8 MB PSRAM, but its additional GPIO access needs checking against the no-SMD/underside-pad requirement. Do not select it on dimensions and memory alone. Exact Mouser-sourced core, accessible GPIO count, supply isolation, sleep draw and footprint remain open.

### Speaker shortlist

**Same Sky CLS0201MA-L152**, Mouser **490-CLS0201MA-L152**: 8 ohm, 0.5 W nominal, 20 mm diameter × 3.8 mm deep, attached wires. [Manufacturer datasheet](https://www.sameskydevices.com/product/resource/cls0201ma-l152.pdf).

The [Mouser US page](https://www.mouser.com/ProductDetail/Same-Sky/CLS0201MA-L152?qs=WyjlAZoYn52yoRnHQzEFHQ%3D%3D) retrieved during this review lists $2.81 at quantity one, but cached prices vary; confirm at checkout. Shipping, tax and any listed surcharge are additional. No comparison with the unknown salvaged speaker has been measured.

Connect the wired speaker through a THT connector and provide mechanical retention/strain relief. Qualify the THT amplifier, filtering, clipping limit, quiet shutdown and enclosure baffle/gasket before claiming crisp audio. Speaker power rating is not a promise of amplifier output. Never drive it directly from GPIO. Earlier NJM2073D/HT82V739 proposals are not released parts; lifecycle and sourcing must be checked before adoption.

### Haptic shortlist

**SparkFun ROB-08449**, Mouser **474-ROB-08449**, wired coin ERM motor. [Mouser](https://www.mouser.com/en/ProductDetail/SparkFun/ROB-08449?qs=WyAARYrbSnZj6jJCAHtRrQ%3D%3D) lists $2.95 base price; shipping, tax and possible surcharge extra.

Its linked [manufacturer specification](https://cdn.sparkfun.com/datasheets/Robotics/B1034.FL45-00-015.pdf) identifies B1034.FL45-00-015, 10 mm diameter × 3.4 mm housing, 3.0 V nominal, 2.3–3.6 V operating range and 60 mA maximum rated running current. Running current is not startup/stall current; confirm delivered revision and actual peaks before driver release.

Prefer this simple motor plus THT transistor, flyback diode, bias/drive resistors, suppression and connector on the main board, rather than an extra haptic breakout. Use short rumble patterns; do not promise LRA-style sharp clicks. Feed from a reviewed regulated rail, not raw SYS_OUT or GPIO; default off during reset/sleep. Verify mounting, noise coupling, startup and total supply load.

## Remaining release gates

Exact core and regulator, amplifier, driver values, connector/cable parts, final display and total current budget remain unresolved. The existing power-path switch rating is still a gate: regulator-module permission does not increase upstream capacity. No schematic, PCB, power-board change, physical audio/haptic test or purchase was performed by this update.
