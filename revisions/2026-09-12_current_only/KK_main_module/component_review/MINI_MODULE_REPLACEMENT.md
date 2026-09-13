# Mini-module replacement review

**NEWER DECISION — [revision B](REVISION_B.md):** user has returned to the ESP32-S3 SuperMini, with power moved to a future separate board revision. Waveshare selections below are no longer current. Use [MASTER_BOM.md](MASTER_BOM.md).

**Historical review — superseded:** the user has now selected the full-size **Waveshare ESP32-S3-DEV-KIT-N16R8-M, SKU 28836**, directly from Waveshare. See the [current component table](MASTER_BOM.md) and [initial circuit design](CIRCUIT_START.md). Mini-only, Nano and WROOM proposals below are retained as history, not current selections. Battery power is still unqualified.

2026-09-10. Engineering shortlist, **not a purchasing or fabrication release**.

**Latest amendment:** the user now accepts a full-size module and proposes [Amazon B08D5ZD528](https://www.amazon.com/dp/B08D5ZD528?th=1). This supersedes the mini-only restriction in the original review below. The listing identifies an ESP-WROOM-32 board, not ESP32-S3; its [product photo](https://m.media-amazon.com/images/I/61JiwY9v5FL._AC_SL1001_.jpg) shows micro-USB. Espressif's [ESP32-WROOM-32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf) specifies 520 KB SRAM and 4 MB flash, with no onboard PSRAM. These are module specifications, not verification of the delivered seller board. Its USB-serial interface can support firmware uploads; native USB device functionality must not be assumed. No matching carrier schematic or safe battery/USB power path was established. Do not freeze this candidate or its footprint. Keep S3 with PSRAM as the recommendation unless the user knowingly accepts the memory/interface tradeoffs. No full-kit power qualification follows from accepting a larger board.

Original review scope: the user authorized another mini module. Inexpensive parts, PSRAM, header-only student connections, one module USB-C port, and THT main-board power electronics were retained. The new size permission does not authorize SMD rework, a second USB port, or an additional power breakout.

## Preferred budget candidate: Waveshare ESP32-S3-Nano-M

- Exact variant: **ESP32-S3-Nano-M**, with pre-soldered headers. Manufacturer family pricing retrieved today: **$8.99–$9.99**, before tax/shipping; confirm variant price at checkout. This is more than the user's $16.99/three SuperMini benchmark.
- PCB: **43.18 × 17.78 mm**, from the manufacturer's dimension drawing. USB connector projects beyond the PCB; this is not the full connector/cable clearance envelope. It is substantially longer than a SuperMini, despite its narrow width. No enclosure fit is claimed.
- **16 MB flash and 8 MB PSRAM**, ESP32-S3R8. Advertised flash is not all available for downloadable games.
- Two 15-pin, 2.54 mm header rows. Existing two nine-way socket selections do not fit. New socket part numbers and footprint must be qualified; do not purchase the old MCU sockets for this candidate.
- Its published schematic exposes raw **VUSB at JP1 pin 12** and separate **VIN at JP1 pin 15**. D3, PMEG6020AELRX, conducts VUSB toward VIN, not VIN toward USB. VIN supplies the onboard MP2322 regulator. This is a useful documented isolation boundary, unlike the direct VBUS/header connection in the examined SuperMini reference.

Sources: [manufacturer product and options](https://www.waveshare.com/product/esp32-s3-nano.htm), [manufacturer wiki](https://www.waveshare.com/wiki/ESP32-S3-Nano), [manufacturer schematic](https://files.waveshare.com/wiki/ESP32-S3-Nano/ESP32-S3-Nano-Schematic.pdf), [manufacturer guide mirrored on Amazon, dimension drawing page 7](https://m.media-amazon.com/images/I/B1HV0j%2BdWpL.pdf). Local copies: [schematic](replacement_sources/nano.pdf), [guide](replacement_sources/nano-guide.pdf).

## What this resolves—and does not

The schematic gives accessible, separate USB input and system supply nodes. It supports investigating this architecture without underside-pad soldering:

1. Module VUSB supplies a current-budgeted main-board THT charger.
2. A protected 1S battery supplies a main-board THT step-up stage and controlled power path into VIN.
3. USB data remains connected entirely on the processor module.

**VIN is documented as 6–21 V; do not connect a raw 1S cell to it or assume a 5 V battery converter meets that specification.** A nominal 6 V design would also need tolerance margin above the documented minimum. The onboard regulator converts this down to 3.3 V. This extra conversion costs parts, board area, and efficiency; compare total kit cost, not only module price.

The boost stage must not simply run continuously during USB operation: its higher output can keep the toy drawing from the battery while USB charges it. Define source selection, boost disable/disconnect and transitions. Verify converter reverse paths, diode leakage, startup and shutdown, USB detection, source-current limits, suspend behavior, load transients and sleep current. Do not source battery power into VUSB or externally parallel the 3V3 rail.

The complete THT charger, charge supervision, battery protection, converter and current budget remain unresolved. Selecting this candidate does **not** complete the power BOM or establish safe charging. Hardware sample/revision checks remain required before schematic freeze.

## Other candidates examined

- **Waveshare ESP32-S3-Zero:** its [schematic](https://files.waveshare.com/wiki/ESP32-S3-Zero/ESP32-S3-Zero-Sch.pdf) retains direct USB/header supply coupling. Not adopted as an isolation fix.
- **LOLIN S3 MINI V1.0.0:** its [schematic](https://www.wemos.cc/en/latest/_static/files/sch_s3_mini_v1.0.0.pdf) directly connects USB VBUS, header VBUS and regulator input. Not adopted as an isolation fix; no qualified reverse-isolated 3V3 injection circuit established.
- **Waveshare ESP32-S3-Pico:** its [schematic](https://files.waveshare.com/upload/a/a7/ESP32-S3-Pico-SCH.pdf) exposes separate VBUS/VSYS and a buck-boost regulator. Not selected; its longer Pico-format board conflicts with the preference for mini size.
- **Unexpected Maker TinyS3[D]:** [current retail listing](https://www.adafruit.com/product/6401) was $21.50. Not selected for this budget kit. The older TinyS3 schematic must not be treated as qualification of the current D revision; onboard charging also needs reconciliation with the main-board THT charger requirement.

## Project disposition

Processor selection is reopened. Nano-M is the preferred candidate for further electrical and mechanical evaluation, **not silently substituted into the purchase register**. The historical Teyleten row and nine-way sockets are on replacement hold. No PCB/schematic, reusable power-board files, hardware, purchases or supplier communications were changed by this review.
