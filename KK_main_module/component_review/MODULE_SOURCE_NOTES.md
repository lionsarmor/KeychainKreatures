# Module documentation evidence — not manufacturer datasheets

Current C.3 supplement (2026-09-11): module/speaker evidence limits below still apply. The older paragraph saying a microSD card and replacement headers are unselected is superseded: TS32GUSD300S and Samtec TSW-10x-07-G-S are now listed in the C.3 kit BOM. Current population and socket/connector selections are controlled by `../assembly/C3_BOM_BY_REFERENCE.csv` and `../assembly/C3_KIT_EXTRAS.csv`.

2026-09-10. These notes distinguish exact seller-module evidence from chip/family datasheets. They do not invent a manufacturer schematic or authorize substitutions. The public-source searches below did not locate controlled documents for the exact three Amazon module revisions or the chosen FUET speaker.

## ESP32-S3 SuperMini — Teyleten B0D47HBFDY

[Exact seller listing](https://www.amazon.com/dp/B0D47HBFDY) · [Espressif silicon datasheet](datasheets/esp32-s3.pdf) · [NOLOGO reference schematic](datasheets/nologo-reference-schematic.png) · [reference-board documentation](https://wiki.nologo.tech/product/esp32/esp32s3/esp32s3supermini/esp32S3SuperMini.html).

The earlier seller photo's FH4R2 marking corresponds to 4 MB flash / 2 MB PSRAM in Espressif's ordering table. The NOLOGO diagram describes a similar module, not a verified Teyleten revision. Seller/reference prose contains conflicting processor specifications; use Espressif for chip architecture. Missing: controlled Teyleten carrier circuit, board drawing and confirmation of the actual header/supply route. Chip datasheet availability does not eliminate this module-level gap.

## XIITIA display — B0DFWL25RB

[Exact listing](https://www.amazon.com/dp/B0DFWL25RB) · [ST7789V2 chip datasheet](datasheets/st7789v2-controller.pdf).

Listing identifies 240 × 280 pixels, nominal 3.3 V power/logic, an eight-pin SPI header and a 31 × 48 mm board. Signal labels: GND, VCC, SCL, SDA, RES, DC, CS and BLK. Seller describes BLK low as backlight off. These are seller interface claims, not proof of allowable BLK current or a controlled footprint drawing. The Sitronix chip PDF documents the display controller, not this carrier's backlight circuit or exact panel initialization. No matching XIITIA circuit/drawing was located.

## GODIYMODULES SD reader — B0F82XWT4F

[Exact listing](https://www.amazon.com/dp/B0F82XWT4F) · [archived seller pinout photo](source_evidence/sd-pinout.jpg) · [archived dimension photo](source_evidence/sd-dimensions.jpg).

In the user's rear-view orientation (socket left, header right), the printed order is 3V3, CS, MOSI, CLK, MISO, GND; the 3V3 pad is square. Seller size is 17.9 × 17.9 mm. Nominal supply and signal labels are documented; exact circuit, tolerances/current, component population and controlled pad dimensions remain unavailable. This is **photo evidence**, not a manufacturer datasheet. [Integration notes](SD_STORAGE.md) retain the assembly and shared-SPI checks.

## FUET FS1511P08-H3.0 wired speaker

[Manufacturer seller listing](https://korean.alibaba.com/product-detail/15-11MM-8-Ohm-0-5W-1600442871788.html) · [manufacturer site](https://www.jstzfsdz.com/) · [manufacturer speaker catalog](https://www.jstzfsdz.com/products_list/1.html).

The exact model is identified in the manufacturer's marketplace listing, but its title mixes 0.5 W and 1 W without establishing continuous versus maximum rating. Public exact-model/PDF searches and all 21 pages of the manufacturer speaker catalog were checked; no controlled exact-model datasheet was recovered. The catalog does contain a similarly named [FS1511TP08-H3.0](https://www.jstzfsdz.com/Speakeproductdetail/294.html), but that adds a `T` and lists different electrical specifications. It is not evidence for the selected FS1511P08-H3.0. Do not substitute a similarly sized FUET speaker drawing or claim its rating applies. No supplier was contacted and no alternate speaker was selected in this audit.

## What a datasheet cannot provide

Final passive counts, a custom PCB outline, enclosure hardware, harness lengths and a connector that has not yet been selected are design outputs, not missing downloadable documents. A microSD card has not yet been assigned an exact model, so no model-specific card datasheet can be retrieved yet. Bundled male headers have no verified separate order code. All are tracked individually in the audit instead of being labelled as failed datasheet searches.

## Useful facts confirmed while auditing existing documents

- Adafruit's linked button drawing shows A/B as one internally connected contact pair and C/D as the other, an 8 × 4.5 mm recommended hole pattern, and up to 200 ohm contact resistance. Its 5.5 mm height conflicts with the listing's 4.9 mm; that fit check remains. With the proposed 10 kohm pull-up, 200 ohm closed resistance gives about 0.065 V at a nominal 3.3 V supply, before other tolerances/leakage. Do not rely only on a continuity buzzer for these switches. [Drawing](datasheets/soft-buttons.png) · [seller page](https://www.adafruit.com/product/3101).
- The UTC ordering table explicitly includes TDA2822L-D08-T in DIP-8. [Datasheet](datasheets/tda2822.pdf).
- The LEADER specification identifies LCM0827A3038F and includes its mechanical/electrical requirements. [Datasheet](datasheets/motor.pdf).
- Sullins' manufacturer list explicitly contains PPTC061LFBN-RC, PPTC081LFBN-RC and PPTC091LFBN-RC. Their common LFB drawing establishes nominal 2.54 mm pitch, 8.50 mm housing height and 3.20 mm tails. This confirms the exact family choices, not their fit under the LCD. [Part list](datasheets/sullins-order-codes.pdf) · [series drawing](datasheets/sullins-female-headers.pdf).
- On Shore's ordering rule adds the extra `1` for 7.62 mm row spacing on a 28-position socket: ED281DT is the narrow choice; ED28DT is not interchangeable. [Drawing](datasheets/dip-sockets.pdf).
