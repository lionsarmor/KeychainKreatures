# Keychain Kreatures — entire-kit component selection

Prepared 2026-09-10. **Prototype selection / complete scope checklist, NOT a released manufacturing BOM.**

**Current register:** use the [single-board component review](component_review/README.md) and its CSV/datasheet archive for new schematic work. This older report retains historical power/battery and harness assumptions; they are not current purchasing instructions.

**Power selection superseded:** the user now requires [integrated THT power](INTEGRATED_THT_POWER_REVISION.md), excluding the separate power/regulator modules and retaining one external USB-C connection. Power-related rows in this report and `kit_component_selection.csv` are historical; do not purchase them for the new revision. Other candidates need requalification against the new supply and layout.

This is the current selection record, superseding the older supplier shortlists in this folder. It retains the Amazon screen, compact legged ESP32-S3, GPIO expander, nine soft buttons, through-hole student assembly, separate reusable power module, speaker, haptics and IR. No separate sub-GHz radio. **Latest user decision: NO XIAO; prioritize inexpensive off-brand modules.** The earlier XIAO selection and its dependent power/pin plan are withdrawn. See [machine-readable scope list](kit_component_selection.csv).

“Selected” means the exact catalog item is the proposed baseline, not that its circuit or fit has passed testing. “Hold” means there is a specific unresolved sourcing, electrical or mechanical requirement. Unknown quantities are deliberately not disguised as a finished kit bag count.

## 1. Main electronics and external assemblies

| Qty per kit | Item | Exact selection | Assembly / qualification |
|---|---|---|---|
| 1 | Processor | **Teyleten Robot ESP32S3SuperMini, Amazon B0D47HBFDY**, three-pack | User-supplied exact listing; selected for prototype qualification. Listing close-up shows ESP32-S3FH4R2: 4 MB flash / 2 MB PSRAM, NOT the previous 16/8 target. Photos show two nine-pin THT rows and included male headers; onboard antenna. One three-pack supplies three kits. Confirm actual chip identity, PSRAM initialization, header measurements and power schematic on received boards. |
| Included | Wireless antenna | Processor board's onboard antenna | No separate Seeed antenna or antenna purchase. Keep clearance around the actual antenna location. |
| 1 | GPIO expander | Microchip **MCP23017-E/SP** | 28-pin narrow DIP, student THT. This replaces the smaller eight-bit expander shortlist. |
| 1 | Display | **XIITIA Amazon B0DFWL25RB** | Retain user's 1.69-inch 240 × 280 SPI screen. An ASIN is a seller identity, not a controlled manufacturer revision: inspect delivered pinout and backlight circuitry. |
| 9 | Soft switches | **Adafruit 3101**, pack of ten | Actual elastomer soft-action THT switches, approximately 7.8 × 7.8 × 4.9 mm. One pack gives nine controls plus one spare. Operating force is not specified; sample before freezing the footprint/cap travel. |
| 1 | Main-board converter | **Selection reopened** after processor change | The $9.95 Pololu S7V8F5 / 2123 is only a documented comparison, not an active kit purchase. Seek lower-cost fixed-output buck-boost module with THT pins, documented input range/current and suitable power-off behavior. Output voltage depends on the exact SuperMini supply circuit. |
| 1 | Audio amplifier | UTC **TDA2822L-D08-T**, LCSC **C73295** | DIP-8 THT. Proposed mono bridge configuration with PWM filtering, attenuation and switched supply. Requires circuit/audio test, not a guaranteed 0.5 W clean output. |
| 1 | Small speaker | FUET / Taizhou Fusheng **FS1511P08-H3.0**, wired version | 15 × 11 mm micro-speaker, 8 ohm. Request drawing, thickness, nominal power and sample: listing mixes 0.5 W and 1 W. Advertised price is not a delivered quote. |
| 1 | Haptic motor | LEADER **LCM0827A3038F**, LCSC **C2759981** | Sample candidate. Manufacturer specification gives 3 V nominal, 2.7–3.3 V operation, 80 mA maximum rated current and 120 mA starting current under its test conditions. Confirm lead-wire version and mechanical drawing; do not substitute contact-pad termination. |
| 1 | IR emitter | Vishay **TSAL6200** | 940 nm, 5 mm leaded LED; transistor driver and current limiting required. |
| 1 | IR receiver | Vishay **TSOP38238** | Leaded, demodulating 38 kHz receiver. Supports a defined remote-control/IR-trading protocol; not an arbitrary-frequency IR analyzer. |
| Schematic-set | NPN drivers/buffers | onsemi **KSP2222ABU** | TO-92. IR, motor, status conditioning and high-side-switch control. Exact count and drive resistors await schematic. |
| Schematic-set | PNP high-side switches | onsemi **BC32725BU** | TO-92. Proposed audio/peripheral/battery-sense switching. Check voltage drop, base drive, off-state leakage and different pin order from KSP2222A. |
| At least 1 | Motor flyback diode | Vishay **1N5819-E3/54** | Axial DO-41. Additional protection-diode count depends on the final supply circuit. |
| 1 | Main PCB | Custom **KK_main_module**, revision not assigned | Bare two-layer THT PCB. Trial 50 × 65 mm outline only; final outline, finish, holes and fabrication files do not exist yet. |

Core references: [exact user-supplied processor listing](https://www.amazon.com/dp/B0D47HBFDY), [seller's chip-marking photo](https://m.media-amazon.com/images/I/71ydnDe+WTL._AC_SL1500_.jpg), [Espressif chip datasheet, Table 1-1](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf), [MCP23017 datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP23017-Data-Sheet-DS20001952.pdf), [soft switches](https://www.adafruit.com/product/3101), [screen retained by user](https://www.amazon.com/dp/B0DFWL25RB). Amazon's single-core/160 MHz and SRAM claims conflict with the photographed chip and Espressif data: the S3 is dual-core, up to 240 MHz. Treat advertised 22.52 × 18 mm dimensions and 43 µA board sleep current as unverified. A listing photo is evidence for selection, not incoming inspection of every delivered board. Do not assume the similar NOLOGO/TENSTAR power schematic matches this exact assembly.

Audio/haptics: [UTC amplifier datasheet](https://www.unisonic.com.tw/uploadfiles/836/part_no_pdf/TDA2822.pdf), [amplifier supplier](https://www.lcsc.com/product-detail/C73295.html), [speaker manufacturer's storefront](https://korean.alibaba.com/product-detail/15-11MM-8-Ohm-0-5W-1600442871788.html), [motor supplier](https://lcsc.com/product-detail/Micro-Motor-Motor_LEADER-LCM0827A3038F_C2759981.html), [indexed manufacturer motor specification](https://datasheet.lcsc.com/lcsc/2103261932_LEADER-LCM0827A3038F_C2759981.pdf). The last PDF link redirected during direct download; recover and archive the actual supplier drawing before footprint release. No acoustic or haptic sample has been tested.

Discrete specifications: [IR emitter](https://www.vishay.com/docs/81010/tsal6200.pdf), [IR receiver](https://www.vishay.com/docs/82491/tsop382.pdf), [NPN](https://www.onsemi.com/pdf/datasheet/ksp2222a-d.pdf), [PNP](https://www.onsemi.com/pub/Collateral/BC327-D.PDF), [diode](https://www.vishay.com/docs/88525/1n5817.pdf).

## 2. Sockets, headers and harnesses

| Qty | Exact selection | Use / condition |
|---|---|---|
| 2 | Nine-way THT female sockets, exact order code pending | Must match the sampled SuperMini, not the withdrawn seven-way XIAO sockets. Include full mated height in the stack. |
| 2 | Nine-way male headers included with sample reference | Verify low-cost supplier includes them; otherwise add exact matching headers. No underside SMD wiring. |
| 1 | On Shore **ED281DT** | 28-pin **7.62 mm row spacing** DIP socket for MCP23017; not the wider ED28DT. |
| 1 | On Shore **ED08DT** | Eight-pin DIP socket for amplifier. |
| 1 | Sullins **PPTC081LFBN-RC** | Eight-way THT display socket, conditional on measured screen header orientation/stack. |
| 1 | Sullins **PPTC041LFBN-RC** | Four-way THT regulator socket. The converter includes a male header; do not buy a second one unnecessarily. |
| 3 | JST **S2B-PH-K-S(LF)(SN)** | Main-board SYS input, speaker and motor connectors. Clearly differentiate electrically incompatible two-pin ports with labeling and harness routing. |
| 4 | JST **PHR-2** | Two SYS-cable ends, one speaker plug and one motor plug. Battery plug is additional only if not already supplied on the pack. |
| 8 | JST **SPH-002T-P0.5S** | Contacts for the four housings above. Factory-prepared cables preferred; verify the actual speaker/motor wire gauge fits this contact before crimping. |
| 1 | Samtec **TSW-105-07-G-S** | Main-board five-pin status header matching the existing power-board header system. |
| 2 housings | Pololu **1904**, ten-pack | 1×5 status-cable housings, 2.54 mm. NOT a five-pin JST PH cable. |
| 5 wires | Pololu **1810**, ten-pack | 6-inch female/female pre-crimped wires for the prototype status harness. Number both ends; use a shorter controlled harness for the finished enclosure. |
| 1 harness | Custom SYS cable | 24–26 AWG stranded pair, pin 1 SYS_OUT to main VIN and pin 2 GND to GND; length follows placement. PHR-2/contact quantities included above. |
| 1 harness each | Custom speaker / motor leads | Factory-attached actuator wires plus compatible crimp termination and strain relief. Do not have students solder microscopic actuator pads. |

Sources: [On Shore socket family](https://www.on-shore.com/part/ed-xxdt-connector-stamped-dip-socket-thru-hole/), [JST PH drawings](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), [status housings](https://www.pololu.com/product/1904/), [pre-crimped status wires](https://www.pololu.com/product/1810). Header lengths/plating, socket drawings and mated heights require footprint review before purchase release. Regulator socket pin count must be revisited if a different converter is selected.

## 3. Supporting passives — exact selection pool, NOT final bag quantities

These are proposed THT order codes for the schematic, not instructions to populate every value. A real per-kit resistor/capacitor count requires the calculated schematic. All resistors below are Yageo MFR-25, axial, 1%, 0.25 W. Verify exact packaging/stock at checkout; sample quantities are not a production order.

| Exact order code | Value | Intended role |
|---|---|---|
| MFR-25FBF52-4R7 | 4.7 ohm | Amplifier output stability networks |
| MFR-25FBF52-39R | 39 ohm | Starting IR-current resistor candidate; recalculate for actual switched rail |
| MFR-25FBF52-100R | 100 ohm | IR receiver supply filtering candidate |
| MFR-25FBF52-220R | 220 ohm | Motor transistor drive candidate, subject to expander drive limits |
| MFR-25FBF52-680R | 680 ohm | IR transistor drive candidate |
| MFR-25FBF52-1K | 1 kohm | Audio filter/attenuator and switch-drive candidates |
| MFR-25FBF52-4K7 | 4.7 kohm | Two I2C pull-ups; verify bus rise time at 400 kHz |
| MFR-25FBF52-10K | 10 kohm | Reset, Function button, logic bias and audio support |
| MFR-25FBF52-100K | 100 kohm | Default-off bias, status input resistors and switched battery divider |
| KEMET C315C104K5R5TA | 100 nF, 50 V X7R, radial | Local IC/rail decoupling, motor suppression, ADC and amplifier networks |
| KEMET C315C103J1G5TA | 10 nF, 100 V C0G, radial | Audio PWM reconstruction / bridge support candidates |
| Nichicon UVR1C100MDD | 10 µF, 16 V, radial | Audio coupling/bridge and receiver filtering candidates |
| Nichicon UVR1C101MDD | 100 µF, 16 V, radial | Converter input and audio/rail bulk capacitance candidates |

Example checked listings: [39-ohm resistor](https://www.digikey.com/es/products/detail/yageo/MFR-25FBF52-39R/9138146), [100 nF manufacturer specification](https://yageogroup.com/download/specsheet/C315C104K5R5TA), [10 nF family and stocked alternate](https://www.digikey.com/en/products/detail/kemet/C315C103J5G5TA/6646386), [Nichicon manufacturer-authored VR table](https://www.digikey.jp/htmldatasheets/production/42672/0/0/1/uvr2f010mea.pdf). Remaining resistor order codes follow the selected family; individual supplier stock is not verified for every value. Capacitor polarization, height and ripple rating must be checked in their actual circuit positions.

## 4. The rest of the kit

| Qty | Item | Selection / release condition |
|---|---|---|
| 1 | Assembled reusable power module | Existing **KK_power_module 0.2-LR1**; include as an assembled/tested subassembly, not a student SMD bag. Its complete exact component list is [production_bom.csv](../KK_power_module/manufacturing/production_bom.csv). That includes charger, protection, USB-C, hard switch, status LEDs and board connectors: do not double-count them. |
| 1 | Battery pack | Retain **MakerHawk 102050**, stated 1S 3.7 V / 1000 mAh. **Hold:** this designation alone is not a fully controlled cell MPN; obtain seller identity, cell datasheet, charge/discharge limits, actual protected dimensions, connector polarity and transport documentation. No silent pack substitution. |
| 1 | Battery temperature sensor assembly | Proposed Vishay **NTCLE100E3103JB0** leaded NTC plus insulated factory-prepared leads. **Hold:** verify its resistance/temperature curve against the actual charger network and cell charging limits. No default NO_NTC shunt for the student product. |
| 1 housing + 2 leads | Temperature-sensor connection | Pololu **1901** 1×2 housing plus two **1810** pre-crimp wires, cut and factory-spliced to NTC with insulation/strain relief. Fits the power-board 2.54 mm J4; final cable length and attachment to cell remain custom. |
| 1 | Front shell | User-designed after board placement; include screen recess, control guides, IR openings and antenna clearance. Custom part, no commercial MPN. |
| 1 | Rear shell | Custom; captive battery compartment and protected PCB mounts. No loose screw tips or solder leads facing the pouch. |
| 1 | D-pad cap | Custom guided D-pad over four soft switches. Pivot/travel/anti-diagonal behavior require sample test. |
| 4 | A/B/X/Y caps | Custom guided caps matching selected switch height and travel. |
| 1 | Function cap | Custom guided cap. Power switch actuator opening/extension is separate. |
| 1 | Screen lens/bezel | Cut clear lens plus perimeter gasket; drawing and material thickness follow screen stack. Keep adhesive off the active area. |
| 1 | Speaker gasket/baffle | Die-cut foam gasket and retention pocket; no blocked acoustic vent. Qualify by listening in the actual shell. |
| 1 set | Motor mount | Insulated pocket/retainer, adhesive if the qualified motor requires it; no extra haptic breakout. |
| 1 set | Battery insulation/retention | Insulating barrier and retained cradle/pull-tab system with cell expansion allowance; never compress or puncture pouch. |
| 1 set | PCB mounts / screws | Prefer molded/printed standoffs; screw diameter, count and length MUST follow actual PCB holes and shell bosses. Unspecified fasteners are not released purchase items. |
| 1 | Keychain attachment | Captive shell anchor plus split ring or short loop; exact hardware follows anchor design and pull test. Avoid relying on a thin decorative printed tab. |
| 1 | USB data/charging cable | USB-A to USB-C or C-to-C data cable appropriate to the supplied/classroom power source; exact product not yet selected. Charging uses power-module USB. MCU programming has the restrictions below. |
| 1 set | Kit packaging | Labeled resistor/capacitor bags, antistatic electronics bag, protected battery packaging, assembly guide, wiring/polarity card and test checklist. Supplier/dimensions await kit bag count. |
| 1 image | Firmware | Factory test + pet firmware + example games; program during kit preparation. Not yet implemented or released by this sourcing task. |

Temperature-sensor reference: [Vishay application listing for exact NTC](https://www.vishay.com/en/landingpage/et4/et4_ind/et4_ind_36/). Battery and power-module qualification are not established by a shopping listing or clean PCB DRC.

Not included as extra electronics: camera, microphone, SD card/reader, sub-GHz, NFC, RFID, extra battery charger, or another GPIO breakout. The baseline uses flash for games. No separate battery-backed real-time clock is selected: timekeeping through a complete hard-power-off is not guaranteed; firmware needs resynchronization. Tools such as soldering iron, cutters, eye protection and multimeter are shared classroom equipment, not counted once per toy.

## 5. Tiny module plus GPIO expander

Use the MCP23017 for eight gameplay buttons, conditioned power-status inputs and slow enable/reset controls. Keep Function/wake, display SPI, audio PWM, IR timing and ADC on the processor. A dedicated SPI screen may allow CS to remain low if needed, but this is not a frozen wiring decision. The previous XIAO-specific GPIO mapping must not be transferred to a SuperMini.

Important limits: GPA7 and GPB7 are output-only in Microchip's current datasheet; neither may receive a button. Confirm actual header-exposed GPIO, strapping pins, onboard voltage dividers/LEDs and USB reservations for the exact purchased board. The older [functional I/O budget](io_requirements.csv) is historical; its PCF8574 assignments are superseded by this MCP23017 direction. A SuperMini-specific pin map has not been released.

The 4 MB flash / 2 MB PSRAM candidate is a real reduction from the earlier 16/8 recommendation. A 240 × 280 RGB565 framebuffer occupies 134400 bytes; memory capacity alone does not prove the app runtime fits. Benchmark firmware, double buffering, networking and saves; partition space for recovery/update and downloads is limited. Prefer a verified 8 MB-flash variant if its delivered price is close, but do not silently claim the cheap 4/2 board has 8/8 or 16/8.

The GPIO expander reduces processor-pin demand, not automatically total board area: its narrow DIP/socket is about 35 mm long and must be placed with the nine switches and other THT parts.

## 6. Power and release holds

The supply remains power-module SYS_OUT → qualified local regulation → main electronics. The exact low-cost SuperMini determines whether to feed its 5 V input or use a reviewed isolated 3.3 V arrangement. Do not carry over the rejected XIAO's regulator characteristics or pinout. The [Pololu 5 V converter](https://www.pololu.com/product/2123) remains only a documented cost/specification comparison while a cheaper compatible module is sought.

Do not parallel regulators or connect the SuperMini's onboard battery charger to the existing power module's cell. Leave onboard battery pads unused. Review USB VBUS backfeed and powered-off pins using the delivered module's schematic; a diode upstream alone may not isolate the computer. Until a proper power-selection/isolation circuit is designed, program the processor module **removed from the kit**, with its other connections detached. Simultaneous kit power and processor USB is not approved. The final student workflow must resolve this explicitly.

The existing power-board **C&K JS102011SAQN** is rated 0.3 A and remains a system-load gate. A larger converter does not fix it. Measure/calculate Wi-Fi peaks, backlight, IR, audio and motor startup/stall together with conversion losses. If the path is inadequate, seek approval for a precisely scoped power-board change; this task has not changed it. Motor maximum voltage is also a gate: a nominal 3.3 V rail's positive tolerance is not automatically acceptable for a 3.3 V maximum motor.

Additional holds: actual display BLK interface and powered-off pin injection, audio filtering/limiting/anti-pop, transistor drive at 3.3 V, safe status-level conversion, default-off battery sensing, battery/NTC charge limits, exact harness crimps, complete footprint/stack check and prototype tests. Then compile exact passive/transistor quantities from the schematic, finalize fasteners/cable lengths, run ERC/DRC and issue a new purchasing BOM. **The entire kit is not yet component-frozen or factory-ready.**

## 7. Price snapshot, not a complete quote

Retrieved supplier pages vary with stock, region and caching. USD before shipping, tax, tariffs and purchasing minimums:

| Item | Price basis |
|---|---|
| Teyleten S3 SuperMini | Amazon B0D47HBFDY is a three-pack; cost per kit = actual pack price / 3. Current checkout price was not exposed reliably; no invented dollar quote. |
| MCP23017-E/SP | Approximately $1.69 at quantity one; verify exact package at checkout |
| Nine soft buttons | $1.95 for one ten-pack; $1.76/pack at ten packs |
| Screen | $7.50 each from user's two-for-$15 purchase benchmark |
| Regulator | Reopened; $9.95 Pololu comparison is NOT the current budget selection |
| Speaker | Advertised $0.50 each at minimum ten; shipping quote/sample confirmation needed |
| Motor | Supplier snapshots approximately $0.56–0.62 each, about $0.46–0.52 at ten |
| Amplifier | Supplier snapshot approximately $0.23 each; verify stock/packaging |

The previous approximately $30.3 partial subtotal is withdrawn because it included the rejected XIAO and a now-reopened regulator choice. A reliable entire-kit total requires the processor/converter quote, schematic quantities, battery identity, power-board assembly quote and custom mechanical costs. Do not present promotional first-order prices or unselected variants as repeatable kit costs.

No orders, supplier messages, hardware modifications, schematic capture or PCB routing were performed in this selection update.
