# SD storage amendment — keep the original display

2026-09-10. User-selected addition to revision B; **selection recorded, electrical and mechanical qualification pending**. No PCB placement or SD circuit is claimed complete.

## Parts and assembly decision

| Item | Quantity per toy | Decision |
|---|---:|---|
| XIITIA B0DFWL25RB, 240 × 280 display | 1 | Retain; do not replace with 128 × 160 hiBCTR |
| Amazon B0F82XWT4F microSD reader module | 1 | Add; package contains five modules, not five per toy |
| Module male header | 1 six-pin strip | Pictured as supplied; verify bundle and pitch |
| Sullins PPTC061LFBN-RC carrier socket | 1 proposed | Candidate six-way THT socket; qualify module fit and stack height |
| microSD card | 1 | Required separately; brand/capacity not chosen |
| Support/insulation hardware and external passives | TBD | Derive from actual module, supply budget and stack-up |

This user request explicitly adds the SD reader to the permitted preassembled electronics exceptions. Students still solder only through-hole header/socket connections; they do not solder the microSD socket's tiny surface-mount contacts. It does not authorize unrelated SMD components on the main PCB.

## Evidence checked

[Exact Amazon listing](https://www.amazon.com/dp/B0F82XWT4F) describes a pop-up card interface and **17.9 × 17.9 mm** board. The [seller's dimension photo](https://m.media-amazon.com/images/I/612fmkYugOL._AC_SL1500_.jpg), visually inspected, shows six header holes, a loose six-pin strip, a mounted card socket and small populated passives. The user's subsequent screenshots identify the listing brand as **GODIYMODULES**, show **USD 5.99 per five-pack** (about USD 1.20 per reader before tax/shipping; not a live quote), and clearly show the back-side power/signal labels. Pictured PCB marking: V474. These are seller dimensions/photos, not a controlled drawing or guaranteed delivered revision. No controlled module circuit, input tolerance, current rating or regulator/level-shifter specification was recovered.

### Header labels confirmed from the user's back-side photo

Viewing the **back of the module, card socket opening to the left, header holes to the right**, the labels run top to bottom as follows. Row numbers below describe photo order, not an already-released carrier footprint pad numbering.

| Photo row | Printed label | Intended circuit connection |
|---|---|---|
| 1, square pad | 3V3 | Qualified regulated 3.3 V supply; never SYS_IN 5 V |
| 2 | CS | SD_CS, separate from display chip select |
| 3 | MOSI | Shared ESP32-to-display/card SPI data |
| 4 | CLK | Shared SPI clock |
| 5 | MISO | SD_MISO, card-to-ESP32 data |
| 6 | GND | Main-board signal/power ground |

This resolves the pictured header's nominal supply marking and signal order. Confirm continuity, header pitch and connector orientation on the delivered sample before footprint release; flipping to the front view mirrors the arrangement. The labels alone do not establish component ratings or verified operating performance.

## Electrical integration plan

- Use the photographed **3V3 input**, with a regulated 3.3 V supply and 3.3 V logic. Trace the delivered module's supply path and all header signals before first power; its input tolerance and current requirements still need qualification. Do not infer 5 V compatibility from “Arduino”, and do not connect this input to the proposed 5 V SYS_IN. Confirm operation at the intended rail without rework.
- Share the display's SPI clock and MOSI with the card. Add **SD_MISO** and a separate **SD_CS** to the revised MCU pin budget. Keep high-speed data on the ESP32, not on the I2C expander. No physical GPIO assignment or new wiring is released here.
- TFT_CS and SD_CS are independent. The display CS can no longer be permanently tied low. Keep other devices deselected while initializing the SD card into SPI mode, then arbitrate bus transactions with the driver. Verify MISO release behavior, board loading and module pull-ups. [Espressif shared-SPI instructions](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/sdspi_share.html).
- Inspect existing pull-ups and decoupling before choosing additional components. Include card initialization/write peaks, voltage droop and brownout behavior in the power budget. Begin at conservative SPI rates; screen and storage share bandwidth, so cache/stream content rather than assuming concurrent maximum throughput.
- No hardware card-detect contact is verified on the pictured six-pin interface. Plan for a normally installed card and software error handling, not unrestricted hot removal.

## Under-screen placement and build order

Use the area beneath the display as the preferred placement region, **not a proven fit**. A 17.9 mm square outline can fit within the display board's nominal footprint, but socket height, solder tails, card protrusion and ejection travel all matter.

1. Fit and solder the reader's header/socket before mounting the display; inspect joints and clean residues.
2. Electrically test reader enumeration, read/write and shared-bus operation before the screen obstructs access.
3. Install a qualified card and verify it cannot contact the display's conductive backplate. Use proper stand-offs and clearance; insulation is supplemental, not a substitute for preventing mechanical contact.
4. Mount the screen without pressing on the reader, card latch or LCD glass/flex. Retain a service path for replacing a failed card, either an accessible edge or removal of the socketed screen. No screen adhesive seal that makes card failure irreparable.
5. Keep reader, card, display metalwork and routing out of the SuperMini antenna keepout.

## Storage behavior

Core firmware, OTA slots and a minimal recovery UI stay in onboard flash. The card holds game packages, graphics, audio and saves/backups; it does not increase PSRAM or automatically run arbitrary C files. Browser uploads can stream to it through the firmware.

Handle absent/full/failed cards gracefully and provide browser save backups. Stage downloads, validate them before activation, flush writes, and design restart recovery. Ordinary FAT storage is not power-loss proof; metadata updates and pet trades need a recovery protocol, not an assumption that file close guarantees an atomic trade. Do not make the only firmware-recovery path depend on a working card.

The master BOM and GPIO requirements include the reader, card and two added signals. Nominal 3.3 V supply and signal order are confirmed from the user's photo; delivered-board continuity/pitch, supply margin, exact card choice, shared-bus tests and under-screen clearance remain pre-layout gates. The existing power-board files remain untouched.
