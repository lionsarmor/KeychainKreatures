# Budget parts list — 2026-09-10

Latest user direction: retain the Amazon screens, remove the Mouser-only sourcing preference, replace the expensive speaker with a smaller cheaper compromise, and prioritize premium assembled feel at low cost. This list supersedes earlier supplier/part preferences. It is a purchasing brief and engineering budget, not a released exact BOM.

## Assembly and sourcing

All student PCB soldering remains through-hole. ESP32 and regulator are preassembled pin-header modules; display, speaker and motor arrive ready to connect. Require factory-attached speaker/motor wires, not student soldering to miniature pads. Purchase semiconductors from traceable sources where possible; generic mechanical parts must come from a consistent sampled supplier. No purchases or supplier contacts made.

## Per-device component budget

USD targets for approximately 10–25 kits using multipacks/direct sourcing, **not verified quotes** unless explicitly identified. Shipping, tax, tariffs, minimum-order surplus, spares, assembly, packaging, tooling, battery, separate power module and shell are excluded. Lower bounds are procurement goals, not confirmed availability.

| Qty | Block / purchase specification | Budget per device |
|---|---|---:|
| 1 | Existing XIITIA Amazon B0DFWL25RB display, 1.69-inch ST7789V2 240 × 280, pin-header breakout | $7.50, user's two-for-$15 price |
| 1 | Compact ESP32-S3 module with THT pins; preferred 16 MB flash / 8 MB PSRAM, exact module still open | $7–10 |
| 1 | Fixed 3.3 V buck-boost regulator module with THT pins, suitable input range and low idle current | $5–10 |
| 1 | Wired 1511-format speaker, approximately 15 × 11 mm, 8 ohm, 0.5 W nominal | $0.50–1.00 |
| 1 set | UTC TDA2822L-D08-T DIP-8 audio candidate, socket, filtering/bias/coupling and switched-power support | $0.60–1.20 |
| 1 | Wired 3 V coin ERM motor, approximately 8–10 mm diameter; no breakout | $0.40–0.80 |
| 9 | Consistent low-force 6 × 6 mm THT tactile switches; D-pad + A/B/X/Y + Function | $0.90–1.80 total |
| 1 | PDIP GPIO expander and socket; MCP23008-E/P candidate, omit only if exact GPIO plan permits | $0.50–1.50 |
| 1 each | TSAL6200 IR emitter and TSOP38238 38 kHz receiver, genuine THT parts preferred | $0.80–1.60 total |
| 1 set | Remaining THT drivers, flyback/supply diodes, resistors, capacitors, battery/status conditioning and USB isolation allowance | $1–2 |
| 1 set | MCU sockets, keyed THT peripheral connectors, mating leads and service header | $1.20–2.50 |
| 1 | Small two-layer main PCB, allocated across batch; final board/vendor quote pending | $1–2 |
| 1 set | Speaker gasket, motor retention, spacers and screws; shell/caps excluded | $0.50–1.00 |
| | **Main assembly, screen and peripherals subtotal** | **$26.90–42.90** |
| | **Same subtotal excluding screen** | **$19.40–35.40** |

Rounded working budget: $27–43 before the exclusions above. Target the low end through consistent batch sourcing, not removal of necessary power/interface circuitry. Support-part allowances may rise after circuit design. No second radio, extra charging board, microSD hardware or decorative LED array is added. The retained Amazon display does not provide the DFRobot candidate's microSD slot.

## Smaller speaker recommendation

Sample a **wired 1511, 8-ohm, 0.5 W micro-speaker**. One supplier example is YUENENG YN-1511, listed as 15 × 11 × 3.2 mm with lead wires. Its [wholesale listing](https://germany.alibaba.com/product-detail/15MM-8-ohm-0-5w-95DB_1600587479460.html) showed EUR 0.2291 at 10–4,999 pieces; this is seller-advertised pricing, not a delivered USD quote or quality certification. Budget above allows more than that advertised unit price, but shipping and rejects remain separate. Require confirmation that the ordered variant actually includes wires and obtain its drawing/datasheet. "1511" is a size family, not an interchangeable qualified part number.

Use a clamped/gasketed mounting with the acoustic chamber/baffle appropriate to that speaker. Expect less bass/headroom than a larger speaker; assess creature sounds, melodies and speech-like samples at the intended volume. Check buzz/rattle, clipping and consistency across samples. Do not infer crispness from wattage or the listing's SPL number. Avoid spring-contact and unwired SMD variants for the student kit. The prior $2.81 Same Sky speaker is no longer the purchasing preference.

## Evidence and unresolved choices

- [Amazon screen](https://www.amazon.com/dp/B0DFWL25RB): retained by explicit user choice; price supplied by user. Verify delivered pinout and mechanical revision before layout.
- [UTC TDA2822L-D08-T at LCSC](https://www.lcsc.com/product-detail/C73295.html): DIP-8 amplifier candidate, listings approximately $0.14–0.23 per IC across quantities/retrievals. The row above includes support parts, not just the IC. [UTC datasheet](https://datasheet.lcsc.com/datasheet/pdf/8599ab4088134d37b4be13f0dc390034.pdf?productCode=C73295) specifies 1.8–12 V operation; qualify clean output at the actual supply and power-gate its idle current. No obsolete HT82V739 substitution or bare SMD amplifier on the main PCB.
- [Pololu S7V8F3](https://www.pololu.com/product/2122) is the documented regulator reference, not a proven final solution. Lower-cost module remains a sourcing target; reject buck-only/boost-only substitutes that cannot handle battery voltage crossing 3.3 V. Advertised module current is not established low-battery output capacity.
- [Waveshare S3 Zero family](https://www.waveshare.com/esp32-s3-zero.htm?sku=33879) provides a price/memory reference: an 8 MB-flash/8 MB-PSRAM version is advertised at $6.99 without headers. This is not the preferred 16 MB capacity, nor an approved kit core. Count only GPIO available through the actual THT headers; underside pads cannot be used to justify compatibility. Do not silently enlarge the toy or reduce storage to fit a cheap board.
- Existing power-module switch/current capacity, module USB backfeed, actual motor startup/stall, exact amplifier output and complete schematic/BOM remain qualification gates. No hardware or power-board files changed.

## What should feel premium

Spend effort on consistent switch force, a pivoted D-pad that avoids accidental opposite directions, closely guided caps without rattle, a flush supported screen window, a properly mounted speaker, short intentional vibration patterns, clean silkscreen and replaceable socketed modules. These are design objectives to validate in a physical kit; they are not achieved by a shopping list alone.
