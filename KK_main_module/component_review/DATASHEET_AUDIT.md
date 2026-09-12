# Main-board datasheets — complete coverage index

2026-09-10. Audited all 53 rows of the current main-board print list. Verified 23 existing archive hashes. This packet contains 23 distinct source documents/images (19 PDFs); shared family documents cover multiple exact parts. Photos and reference-board diagrams are explicitly distinguished from exact-module datasheets. No component substitutions, purchases or schematic changes were made.

[Downloadable packet](MAIN_BOARD_DATASHEETS.zip) · [Printable index](DATASHEET_AUDIT.html) · [CSV](DATASHEET_AUDIT.csv) · [integrity manifest](main_datasheet_manifest.json) · [module evidence and search notes](MODULE_SOURCE_NOTES.md)

## Results

| Documentation category | BOM rows |
|---|---:|
| PARTIAL_MODULE | 3 |
| DOCUMENT_FOUND | 30 |
| DRAWING_FOUND | 1 |
| DATASHEET_NOT_FOUND | 1 |
| BUNDLED_NO_MPN | 2 |
| DESIGN_PENDING | 6 |
| PART_NOT_SELECTED | 4 |
| CUSTOM_DESIGN | 6 |

DOCUMENT_FOUND includes manufacturer series documents and order-code tables, not necessarily a separate PDF for every resistor value. PARTIAL_MODULE means useful evidence exists but not a controlled schematic for the exact seller assembly. DESIGN_PENDING is unfinished engineering, not a failed internet search.

## Every main-board row

| Item | Exact part / requirement | Documentation | Local source | Remaining issue |
|---|---|---|---|---|
| CORE | ESP32-S3 SuperMini / original Amazon B0D47HBFDY | PARTIAL_MODULE | [esp32-s3.pdf](datasheets/esp32-s3.pdf) / [nologo-reference-schematic.png](datasheets/nologo-reference-schematic.png) | Chip datasheet and another supplier reference schematic available; exact Teyleten carrier schematic not found. |
| DISPLAY | B0DFWL25RB | PARTIAL_MODULE | [st7789v2-controller.pdf](datasheets/st7789v2-controller.pdf) | Exact advertised controller datasheet archived; XIITIA panel/carrier drawing and backlight circuit not found. |
| GPIO | MCP23017-E/SP | DOCUMENT_FOUND | [mcp23017.pdf](datasheets/mcp23017.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| CONTROLS | 3101 | DRAWING_FOUND | [soft-buttons.png](datasheets/soft-buttons.png) | Adafruit-linked drawing available; height conflict with product-page dimensions remains. |
| AUDIO | TDA2822L-D08-T | DOCUMENT_FOUND | [tda2822.pdf](datasheets/tda2822.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| SPEAKER | FS1511P08-H3.0 wired | DATASHEET_NOT_FOUND | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Exact FUET model listing found, but no controlled datasheet/rating drawing. Do not substitute another 1511 model. |
| HAPTIC | LCM0827A3038F | DOCUMENT_FOUND | [motor.pdf](datasheets/motor.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| IR_TX | TSAL6200 | DOCUMENT_FOUND | [tsal6200.pdf](datasheets/tsal6200.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| IR_RX | TSOP38238 | DOCUMENT_FOUND | [tsop382.pdf](datasheets/tsop382.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| NPN_DRIVER | KSP2222ABU | DOCUMENT_FOUND | [ksp2222a.pdf](datasheets/ksp2222a.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| PNP_SWITCH | BC32725BU | DOCUMENT_FOUND | [bc327.pdf](datasheets/bc327.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| FLYBACK | 1N5819-E3/54 | DOCUMENT_FOUND | [1n5819.pdf](datasheets/1n5819.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| MCU_SOCKET | PPTC091LFBN-RC | DOCUMENT_FOUND | [sullins-female-headers.pdf](datasheets/sullins-female-headers.pdf) / [sullins-order-codes.pdf](datasheets/sullins-order-codes.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| MCU_HEADER | 9-pin male strips supplied with selected module | BUNDLED_NO_MPN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Supplier-pictured accessory, not separately identified by manufacturer part number. |
| GPIO_SOCKET | ED281DT | DOCUMENT_FOUND | [dip-sockets.pdf](datasheets/dip-sockets.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| AUDIO_SOCKET | ED08DT | DOCUMENT_FOUND | [dip-sockets.pdf](datasheets/dip-sockets.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| DISPLAY_SOCKET | PPTC081LFBN-RC | DOCUMENT_FOUND | [sullins-female-headers.pdf](datasheets/sullins-female-headers.pdf) / [sullins-order-codes.pdf](datasheets/sullins-order-codes.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| ACTUATOR_CONNECTOR | S2B-PH-K-S(LF)(SN) | DOCUMENT_FOUND | [jst-ph.pdf](datasheets/jst-ph.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| ACTUATOR_HOUSING | PHR-2 | DOCUMENT_FOUND | [jst-ph.pdf](datasheets/jst-ph.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| MOTOR_CONTACT | SPH-004T-P0.5S | DOCUMENT_FOUND | [jst-ph.pdf](datasheets/jst-ph.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-4R7 | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-39R | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-100R | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-220R | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-680R | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-1K | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-4K7 | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-10K | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| RESISTOR | MFR-25FBF52-100K | DOCUMENT_FOUND | [mfr-resistors.pdf](datasheets/mfr-resistors.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| CAPACITOR | C315C104K5R5TA | DOCUMENT_FOUND | [kemet-100nf.pdf](datasheets/kemet-100nf.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| CAPACITOR | C315C103J1G5TA | DOCUMENT_FOUND | [kemet-10nf.pdf](datasheets/kemet-10nf.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| CAPACITOR | C315C105K5R5TA | DOCUMENT_FOUND | [kemet-1uf.pdf](datasheets/kemet-1uf.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| CAPACITOR | UVR1C100MDD | DOCUMENT_FOUND | [nichicon-uvr.pdf](datasheets/nichicon-uvr.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| CAPACITOR | UVR1C101MDD | DOCUMENT_FOUND | [nichicon-uvr.pdf](datasheets/nichicon-uvr.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| SD_MODULE | Amazon B0F82XWT4F | PARTIAL_MODULE | [sd-pinout.jpg](source_evidence/sd-pinout.jpg) / [sd-dimensions.jpg](source_evidence/sd-dimensions.jpg) | Exact seller photos document 3V3 and pin labels; no controlled module datasheet recovered. |
| SD_SOCKET | PPTC061LFBN-RC | DOCUMENT_FOUND | [sullins-female-headers.pdf](datasheets/sullins-female-headers.pdf) / [sullins-order-codes.pdf](datasheets/sullins-order-codes.pdf) | Manufacturer component/series document archived; circuit quantity and assembly fit are separate checks. |
| SD_HEADER | Six-pin male strip pictured with B0F82XWT4F | BUNDLED_NO_MPN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Supplier-pictured accessory, not separately identified by manufacturer part number. |
| BACKLIGHT_DRIVER | Backlight control and default-off network | DESIGN_PENDING | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Individual component/MPN or circuit quantity not yet specified; no exact-part datasheet to retrieve. |
| AUDIO_NETWORK | PWM filter / attenuation / coupling / bridge stability | DESIGN_PENDING | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Individual component/MPN or circuit quantity not yet specified; no exact-part datasheet to retrieve. |
| AUDIO_GATE | Amplifier supply gating network | DESIGN_PENDING | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Individual component/MPN or circuit quantity not yet specified; no exact-part datasheet to retrieve. |
| MOTOR_NETWORK | Motor drive / suppression | DESIGN_PENDING | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Individual component/MPN or circuit quantity not yet specified; no exact-part datasheet to retrieve. |
| SPEAKER_CONTACT | Speaker harness crimp contacts | PART_NOT_SELECTED | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Exact card/contact/connector/harness not yet selected; cannot attach an unrelated datasheet as if final. |
| MAIN_PCB | KK main-board custom PCB | CUSTOM_DESIGN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Custom layout, mounting or test-access item; dimensions/design must be created before hardware can be specified. |
| TEST_ACCESS | PCB test pads and optional service header | CUSTOM_DESIGN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Custom layout, mounting or test-access item; dimensions/design must be created before hardware can be specified. |
| SCREEN_RETENTION | Display retention hardware / spacers | CUSTOM_DESIGN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Custom layout, mounting or test-access item; dimensions/design must be created before hardware can be specified. |
| PCB_HARDWARE | PCB spacers and fasteners | CUSTOM_DESIGN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Custom layout, mounting or test-access item; dimensions/design must be created before hardware can be specified. |
| ACTUATOR_MOUNT | Speaker gasket and motor retention | CUSTOM_DESIGN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Custom layout, mounting or test-access item; dimensions/design must be created before hardware can be specified. |
| MICROSD | microSD card; exact brand/capacity pending | PART_NOT_SELECTED | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Exact card/contact/connector/harness not yet selected; cannot attach an unrelated datasheet as if final. |
| SYS_IN_CONNECTOR | Keyed THT regulated-power input connector | PART_NOT_SELECTED | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Exact card/contact/connector/harness not yet selected; cannot attach an unrelated datasheet as if final. |
| SYS_IN_HARNESS | Power-board to main-board harness and mating contacts | PART_NOT_SELECTED | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Exact card/contact/connector/harness not yet selected; cannot attach an unrelated datasheet as if final. |
| MAIN_RAIL_INTERFACE | Main-board rail distribution / local bypass capacitors | DESIGN_PENDING | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Individual component/MPN or circuit quantity not yet specified; no exact-part datasheet to retrieve. |
| SD_SUPPORT | SD supply bypass / bus pull-ups / optional series resistors | DESIGN_PENDING | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Individual component/MPN or circuit quantity not yet specified; no exact-part datasheet to retrieve. |
| SD_RETENTION | Reader support and display clearance / insulation | CUSTOM_DESIGN | [Evidence/selection notes](MODULE_SOURCE_NOTES.md) | Custom layout, mounting or test-access item; dimensions/design must be created before hardware can be specified. |

## Original source URLs

- [datasheets/1n5819.pdf](https://www.vishay.com/docs/88525/1n5817.pdf) — 4 pages; local copy [here](datasheets/1n5819.pdf).
- [datasheets/bc327.pdf](https://www.onsemi.com/pub/Collateral/BC327-D.PDF) — 6 pages; local copy [here](datasheets/bc327.pdf).
- [datasheets/dip-sockets.pdf](https://www.on-shore.com/wp-content/uploads/EDXXXDT-1.pdf) — 1 pages; local copy [here](datasheets/dip-sockets.pdf).
- [datasheets/esp32-s3.pdf](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) — 87 pages; local copy [here](datasheets/esp32-s3.pdf).
- [datasheets/jst-ph.pdf](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) — 5 pages; local copy [here](datasheets/jst-ph.pdf).
- [datasheets/kemet-100nf.pdf](https://yageogroup.com/download/specsheet/C315C104K5R5TA) — 4 pages; local copy [here](datasheets/kemet-100nf.pdf).
- [datasheets/kemet-10nf.pdf](https://yageogroup.com/download/specsheet/C315C103J1G5TA) — 1 pages; local copy [here](datasheets/kemet-10nf.pdf).
- [datasheets/kemet-1uf.pdf](https://yageogroup.com/download/specsheet/C315C105K5R5TA) — 1 pages; local copy [here](datasheets/kemet-1uf.pdf).
- [datasheets/ksp2222a.pdf](https://www.onsemi.com/pdf/datasheet/ksp2222a-d.pdf) — 5 pages; local copy [here](datasheets/ksp2222a.pdf).
- [datasheets/mcp23017.pdf](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP23017-Data-Sheet-DS20001952.pdf) — 40 pages; local copy [here](datasheets/mcp23017.pdf).
- [datasheets/mfr-resistors.pdf](https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf) — 17 pages; local copy [here](datasheets/mfr-resistors.pdf).
- [datasheets/motor.pdf](https://atta.szlcsc.com/upload/public/pdf/source/20251110/A6D51E996DED36DE7FC15C3D341F1E6E.pdf) — 12 pages; local copy [here](datasheets/motor.pdf).
- [datasheets/nichicon-uvr.pdf](https://www.nichicon.co.jp/english/series_items/catalog_pdf/e-uvr.pdf) — 4 pages; local copy [here](datasheets/nichicon-uvr.pdf).
- [datasheets/nologo-reference-schematic.png](https://wiki.nologo.tech/assets/img/esp32/esp32s3supermini/1.png) — image; local copy [here](datasheets/nologo-reference-schematic.png).
- [datasheets/soft-buttons.png](https://cdn-shop.adafruit.com/product-files/3101/C4817-001+datasheet.png) — image; local copy [here](datasheets/soft-buttons.png).
- [datasheets/st7789v2-controller.pdf](https://www.waveshare.com/w/upload/c/c9/ST7789V2.pdf) — 319 pages; local copy [here](datasheets/st7789v2-controller.pdf).
- [datasheets/sullins-female-headers.pdf](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/937/Female_Headers.100_DS.pdf) — 2 pages; local copy [here](datasheets/sullins-female-headers.pdf).
- [datasheets/sullins-order-codes.pdf](https://www.sullinscorp.com/images/AllRoHSParts.pdf) — 223 pages; local copy [here](datasheets/sullins-order-codes.pdf).
- [datasheets/tda2822.pdf](https://datasheet.lcsc.com/datasheet/pdf/8599ab4088134d37b4be13f0dc390034.pdf) — 6 pages; local copy [here](datasheets/tda2822.pdf).
- [datasheets/tsal6200.pdf](https://www.vishay.com/docs/81010/tsal6200.pdf) — 5 pages; local copy [here](datasheets/tsal6200.pdf).
- [datasheets/tsop382.pdf](https://www.vishay.com/docs/82491/tsop382.pdf) — 8 pages; local copy [here](datasheets/tsop382.pdf).
- [source_evidence/sd-dimensions.jpg](https://m.media-amazon.com/images/I/612fmkYugOL._AC_SL1500_.jpg) — image; local copy [here](source_evidence/sd-dimensions.jpg).
- [source_evidence/sd-pinout.jpg](https://m.media-amazon.com/images/I/61qrQGhmcEL._AC_SL1500_.jpg) — image; local copy [here](source_evidence/sd-pinout.jpg).

Files passed PDF parsing and SHA-256 checks. Some legacy PDFs produce nonfatal metadata warnings; these are recorded in the manifest. Parsing is not a full technical design review. Final resistor/capacitor counts and power/interface qualification remain schematic work, not documentation gaps.
