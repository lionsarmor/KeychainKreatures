# Prototype / low-run cost allowances

2026-09-10, USD. **Budgetary engineering allowances, not a quoted/orderable BOM.** Exact MCU assembly, amplifier supplier, connectors and enclosure are unresolved. No retail target is imposed. Ranges allow small-quantity distribution and DIY-friendly parts; do not extrapolate them to mass production.

Sizing amendment: the board-first plan now starts at a provisional 50 × 65 mm. The 42 × 52 mm bare-PCB allowances below describe the previous study, not a quote for the revised outline. Refresh fabrication/assembly pricing once geometry and process are fixed; do not scale total cost simply by board area.

## Electronics materials per device

**Student-kit amendment:** no SMT assembly directly on the main PCB is permitted. The SMT setup/placement figures below are historical comparisons, not the current main-board process. Re-cost using a complete preassembled legged ESP32 module, THT sockets and parts, and student assembly; keep RODDY assembly costs separate. A bare RF-module price is not a compliant MCU cost. Regulator implementation remains unresolved, so the totals are not a qualified budget for this revised kit.

| Main-board group | Allowance | Basis / uncertainty |
|---|---:|---|
| Compact S3/PSRAM core and support parts | $5–12 | Bare-module versus preassembled core unresolved; excludes custom carrier assembly labor |
| Local regulated supply, inductor/capacitors and load switches | $3–8 | Low-Iq buck-boost and off-state behavior matter; THT-carrier approach may exceed this |
| Nine switches and optional DIP button expander | $2–5 | Exact tact size/force and whether expander is needed remain open |
| DIP audio amp plus analog filter/bulk parts | $2–6 | HT82V739 sourcing not qualified; no obsolete NJM stock price assumed |
| IR emitter/receiver and driver | $1–3 | Protocol receiver and emitter current/range not selected |
| Haptic drive electronics | $1–3 | ERM allowance; sophisticated LRA drive may cost more |
| Connectors, service access and level/sense circuits | $4–8 | Low-profile mating pairs/cables can dominate |
| Other passives / protective parts | $1–3 | Assembly margins and exact counts unresolved |
| **Main electronics subtotal, excluding bare PCB/labor** | **$19–48** | Sum of allowances, not a shopping list |

As a current price anchor rather than a design choice, [Seeed lists the normal XIAO ESP32S3 at $7.49](https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html). Its GPIO/charging/antenna constraints still need review. A bare Espressif module's volume price must not be substituted for a complete assembled MCU core's low-run cost.

| Separate retained assemblies | Additional allowance | Exclusions |
|---|---:|---|
| Existing-class 1.69-inch TFT assembly | $6–15 | Exact purchased part unknown |
| 1000 mAh protected battery pack | $5–12 | Genuine cell specification, lead/polarity and shipping unknown |
| RODDY power board electronics + bare PCB | $8–18 | Not a refreshed line-item quote; assembly labor excluded |
| Small 8-ohm speaker | $1–3 | Actual size/power unknown |
| Small ERM motor | $1–3 | Different actuator may exceed allowance |
| **Separate assemblies subtotal** | **$21–51** | No housing or labor |

Illustrative complete electronics materials total **$40–99**, excluding the main bare PCB, labor, enclosure, hardware, packaging, shipping/taxes, spares and testing. Retained parts already owned do not need repurchasing; their allowances describe another build, not this project's incremental spending.

## Main PCB and assembly

| Item | Five-unit prototype allowance | 25-unit pilot allowance |
|---|---:|---:|
| 42 × 52 mm bare main PCB | $1–6 each | $0.50–3 each |
| SMT core/regulator setup and associated small-order fees | $40–120 per order ($8–24/unit) | $40–120 per order ($1.60–4.80/unit) |
| SMT placement/reflow beyond setup | $1–4 each | $1–4 each |
| Through-hole assembly | DIY labor unpriced; outsourced allowance $6–20/unit | Same preliminary allowance; request actual work-content quote |

These are planning ranges, not proof a given factory accepts the chosen DIP parts or module/carrier process. Bare-board range spans process/layer choices; no two- or four-layer main board is frozen. A separate custom carrier adds another PCB/process/setup, so it can exceed these allowances. Do not double-count core assembly if buying a finished development-board core. Freight, component minimums/attrition, inspection and firmware flashing/testing are additional.

For context, [JLCPCB's published fee schedule](https://jlcpcb.com/help/article/pcb-assembly-price) lists Economy assembly setup $8.18 and stencil $1.53, versus Standard single-side setup $25.56 and stencil $8.21. These base fees are **not** a finished assembly quote: process eligibility, feeders, extended parts, hand work, component purchase and other charges affect the invoice. The larger allowances above deliberately budget for an unresolved mixed-technology low run.

## Outliers and later savings

1. **Connectors, sockets and stacked carriers:** cost both dollars and depth. Use fewer carefully selected mating systems; preserve essential repair access. Do not remove sockets silently.
2. **Unqualified/obsolete DIP audio:** irregular supply can dominate price and reliability. Qualify a current THT source first; do not cost the design around surplus stock.
3. **Compact MCU storage:** a tiny 4 MB module may require extra storage/carrier parts. Benchmark actual apps before buying capacity or committing an undersized part.
4. **Low-run setup and manual test time:** amortize setup across a pilot batch; prepare a fixture and repeatable programming/audio/button/current tests before claiming reduced assembly cost.
5. **DIP expander:** omit it if exact core pin count and direct routing make that the smaller, simpler design. No loss of nine-button functionality.
6. **Future SMT option:** may improve volume/efficiency but is a distinct product/assembly decision, not the default cost reduction for this DIY revision.

Next costing gate: source-qualified manufacturer part numbers, quantities, matched footprints, exact core/antenna, connector pairs, power path and enclosure fit; then obtain an actual PCB/assembly quote. No procurement, order upload or manufacturing authorization is implied.
