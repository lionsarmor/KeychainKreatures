# Datasheets and drawings

**Current main-board packet:** [all 53 rows mapped to documentation](DATASHEET_AUDIT.md) · [printable clickable index](DATASHEET_AUDIT.html) · [download ZIP](MAIN_BOARD_DATASHEETS.zip). The packet contains 19 PDFs and four drawings/photos, with a [separate integrity manifest](main_datasheet_manifest.json). Manufacturer documents cover 31 BOM entries; three exact seller modules have partial chip/photo evidence, and the exact speaker datasheet was not recovered. Unselected/custom items and unfinished circuits are tracked separately from missing documents.

Newly archived: [ST7789V2 controller datasheet](datasheets/st7789v2-controller.pdf), [Sullins order-code list](datasheets/sullins-order-codes.pdf), [SD pinout photo](source_evidence/sd-pinout.jpg), [SD dimension photo](source_evidence/sd-dimensions.jpg). These supplements are not added to the original archive manifest below; the new main-board manifest covers them.

**Current architecture:** [revision B](REVISION_B.md) returns to ESP32-S3 SuperMini and separate power. The ESP32-S3 chip datasheet and archived NOLOGO schematic are reference material; the latter is not a verified schematic for the exact Teyleten module. Confirm delivered FH4R2 memory and module wiring before design release.

## Historical Waveshare processor supplement

Selected assembly: **ESP32-S3-DEV-KIT-N16R8-M, SKU 28836**; [official family documentation](https://docs.waveshare.com/ESP32-S3-DEV-KIT-N8R8), [direct ordering page](https://www.waveshare.com/product/mcu-tools/esp32-s3-dev-kit-n8r8.htm), and [published family circuit diagram](https://files.waveshare.com/wiki/ESP32-S3-DEV-KIT-N8R8/ESP32-S3-DEV-KIT-N8R8-schematic.pdf). These are external links, not additions to the original file-integrity manifest. The schematic is named N8R8; delivered N16R8-M revision must be checked. New MCU sockets: **Sullins PPTC221LFBN-RC**, covered by the female-header series drawing below and listed in [Sullins' manufacturer part list](https://www.sullinscorp.com/images/AllRoHSParts.pdf). Series documentation does not establish module row spacing or physical fit.

## Original archive

Retrieved 2026-09-10. Publisher-authored documents retained for design review. Archiving a document does not qualify a circuit. The NOLOGO schematic and ME6217 datasheet are reference evidence, not proof of the exact Teyleten board revision. Motor document is LEADER's 2025 update; amplifier is UTC TDA2822, including the L-D08-T order code.

- [esp32-s3.pdf](datasheets/esp32-s3.pdf): [original source](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf); 87 pages.
- [mcp23017.pdf](datasheets/mcp23017.pdf): [original source](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP23017-Data-Sheet-DS20001952.pdf); 40 pages.
- [tsal6200.pdf](datasheets/tsal6200.pdf): [original source](https://www.vishay.com/docs/81010/tsal6200.pdf); 5 pages.
- [tsop382.pdf](datasheets/tsop382.pdf): [original source](https://www.vishay.com/docs/82491/tsop382.pdf); 8 pages.
- [ksp2222a.pdf](datasheets/ksp2222a.pdf): [original source](https://www.onsemi.com/pdf/datasheet/ksp2222a-d.pdf); 5 pages.
- [bc327.pdf](datasheets/bc327.pdf): [original source](https://www.onsemi.com/pub/Collateral/BC327-D.PDF); 6 pages.
- [1n5819.pdf](datasheets/1n5819.pdf): [original source](https://www.vishay.com/docs/88525/1n5817.pdf); 4 pages.
- [jst-ph.pdf](datasheets/jst-ph.pdf): [original source](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf); 5 pages.
- [ntcle100.pdf](datasheets/ntcle100.pdf): [original source](https://www.vishay.com/docs/29049/ntcle100.pdf); 17 pages.
- [mcp1826s.pdf](datasheets/mcp1826s.pdf): [original source](https://ww1.microchip.com/downloads/en/DeviceDoc/22057B.pdf); 38 pages.
- [mfr-resistors.pdf](datasheets/mfr-resistors.pdf): [original source](https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf); 17 pages.
- [tda2822.pdf](datasheets/tda2822.pdf): [original source](https://datasheet.lcsc.com/datasheet/pdf/8599ab4088134d37b4be13f0dc390034.pdf); 6 pages.
- [dip-sockets.pdf](datasheets/dip-sockets.pdf): [original source](https://www.on-shore.com/wp-content/uploads/EDXXXDT-1.pdf); 1 pages.
- [sullins-female-headers.pdf](datasheets/sullins-female-headers.pdf): [original source](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/937/Female_Headers.100_DS.pdf); 2 pages.
- [nichicon-uvr.pdf](datasheets/nichicon-uvr.pdf): [original source](https://www.nichicon.co.jp/english/series_items/catalog_pdf/e-uvr.pdf); 4 pages.
- lt1512.pdf — online-only; download unsuccessful: [original source](https://www.analog.com/media/en/technical-documentation/data-sheets/1512fc.pdf).
- [soft-buttons.png](datasheets/soft-buttons.png): [original source](https://cdn-shop.adafruit.com/product-files/3101/C4817-001+datasheet.png).
- [motor.pdf](datasheets/motor.pdf): [original source](https://atta.szlcsc.com/upload/public/pdf/source/20251110/A6D51E996DED36DE7FC15C3D341F1E6E.pdf); 12 pages.
- [kemet-100nf.pdf](datasheets/kemet-100nf.pdf): [original source](https://yageogroup.com/download/specsheet/C315C104K5R5TA); 4 pages.
- [kemet-10nf.pdf](datasheets/kemet-10nf.pdf): [original source](https://yageogroup.com/download/specsheet/C315C103J1G5TA); 1 pages.
- [mcp1700.pdf](datasheets/mcp1700.pdf): [original source](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP1700-Data-Sheet-20001826F.pdf); 32 pages.
- [kemet-1uf.pdf](datasheets/kemet-1uf.pdf): [original source](https://yageogroup.com/download/specsheet/C315C105K5R5TA); 1 pages.
- [me6217.pdf](datasheets/me6217.pdf): [original source](https://www.huazhoucn.com/upFiles/common/2022/12/ME6217%20Series_E5.0.pdf); 13 pages.
- [nologo-reference-schematic.png](datasheets/nologo-reference-schematic.png): [original source](https://wiki.nologo.tech/assets/img/esp32/esp32s3supermini/1.png).

LT1512 could be read through web retrieval but its direct file download did not complete. It is not represented by HTML named .pdf. No controlled Teyleten module schematic, XIITIA module datasheet, FUET speaker drawing or final battery datasheet is archived. See the review for the resulting holds.

[Source URLs](datasheet_sources.json) · [File integrity manifest](datasheet_manifest.json)
