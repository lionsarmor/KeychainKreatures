# Main-board circuit design — revision A

**WITHDRAWN AS A CURRENT WIRING GUIDE:** see [revision B](REVISION_B.md). The MCU is now SuperMini and charging is on a future separate power board. Every Waveshare P1/P2/GPIO assignment and USB supply instruction below is historical, not applicable to the new module. The generated connection CSV now uses logical MCU ports only. Peripheral topology may be reused after reassignment and validation.

2026-09-10. Initial electrical design and pin-level connection table; **not a KiCad schematic, fabrication release or complete powered toy**. The first circuit covers the processor interface, nine controls, GPIO expander and IR transmit/receive. Display/audio/motor pins are reserved, but those loads are not connected in this revision. No battery or charger connection is approved.

## Authoritative inputs

- Processor: Waveshare **ESP32-S3-DEV-KIT-N16R8-M, SKU 28836**, with factory headers, 16 MB flash and 8 MB PSRAM. [Official family documentation](https://docs.waveshare.com/ESP32-S3-DEV-KIT-N8R8) identifies the SKU and common interface.
- [Published family schematic](https://files.waveshare.com/wiki/ESP32-S3-DEV-KIT-N8R8/ESP32-S3-DEV-KIT-N8R8-schematic.pdf), visually reviewed: header numbering below follows its **P1/P2**, not the WROOM module's pin numbers. The drawing is named N8R8; confirm delivered N16R8-M revision before footprint release.
- Main-board parts, including power circuitry, must be genuinely through-hole. MCU and display are the only preassembled electronic exceptions. No supplier modification of the MCU is assumed authorized.
- Display: retained XIITIA Amazon B0DFWL25RB, advertised ST7789V2 SPI 240 × 280. Sample pin order, logic/power requirements and backlight circuit are unresolved.
- Battery: proposed conventional 1S Li-ion/LiPo, 3.6/3.7 V nominal and 4.2 V maximum. Not LiFePO4 or a higher-voltage lithium chemistry. Shape/capacity deferred by user; protection, cell limits and charger compatibility still mandatory before operation.

## 1. Supply boundary and the open power problem

The module schematic shows raw USB **VBUS → D1 B5819WS → VDDUSB**, with **P1 pin 21, labelled VCC_5V**, connected to VDDUSB. Its onboard 3.3 V regulator is fed from that same rail. P2 pin 1 is ground, not raw VBUS.

Consequently, the normal 5 V header is **not an independent USB-only charger input** once a battery converter also feeds that rail. A charger connected there can otherwise consume battery-derived power and feed it back into the battery. The onboard diode alone does not solve that loop. Injecting external 3.3 V is also not qualified because it parallels/reverse-drives the onboard regulator.

This does not establish that the requirements are impossible, but it does prevent declaring the supply circuit finished. A hardware-qualified source-selection/charger-inhibit arrangement is needed; voltage discrimination would require proven, non-overlapping worst-case supply windows and transient behavior. USB enumeration or MCU firmware alone is not a safe charger-enable mechanism, particularly with a wall adapter or crashed firmware. Do not assume raw VBUS can be obtained by soldering onto an SMD component.

LT1512CN8#PBF is only a through-hole CC/CV converter candidate, **not a complete autonomous lithium charger**. Its selection would still require precharge, termination, restart, time limits, cell-temperature interlocks, protections, magnetics and a USB input-current budget. MCP1826S is an LDO, not a battery buck-boost solution. Neither is released for purchasing as the power solution.

For the initial circuit only: use the MCU's USB port as the sole source; take LOGIC_3V3 from P1.1 and ground from P1.22. Leave P1.21 and all external battery/charger inputs unconnected. Verify the delivered module regulator and available current/thermal margin before bench bring-up. No motor, screen or amplifier loads in this first test. Do not connect two supply sources.

## 2. GPIO allocation

| Function | ESP32 GPIO | Manufacturer header | Current state |
|---|---:|---|---|
| I2C SDA | 8 | P1.12 | Initial circuit |
| I2C SCL | 9 | P1.15 | Initial circuit |
| Expander interrupt | 4 | P1.4 | Initial circuit, active-low |
| Function button / wake candidate | 5 | P1.5 | Initial circuit, active-low |
| Expander reset | 7 | P1.7 | Initial circuit, active-low |
| IR transmit | 17 | P1.10 | Initial circuit |
| IR receive | 18 | P1.11 | Initial circuit |
| TFT chip select | 10 | P1.16 | Reserved, unconnected |
| TFT MOSI | 11 | P1.17 | Reserved, unconnected |
| TFT clock | 12 | P1.18 | Reserved, unconnected |
| TFT data/command | 13 | P1.19 | Reserved, unconnected |
| TFT reset | 14 | P1.20 | Reserved, unconnected |
| Backlight control | 15 | P1.8 | Reserved for qualified driver, not direct LED drive |
| Audio PWM | 16 | P1.9 | Reserved for filter/attenuator |
| Motor control | 6 | P1.6 | Reserved for qualified driver |
| Battery ADC | 1 | P2.4 | Reserved for switched divider/protection |
| Power status | 2 | P2.5 | Reserved for level-safe interface |
| Audio enable | 21 | P2.18 | Reserved for supply gating |

Reserve GPIO19/20 for onboard native USB, GPIO0/3/45/46 for boot-strapping concerns, GPIO35/36/37 for module memory restrictions, GPIO38 for onboard RGB, and GPIO43/44 for UART service. Do not connect the TFT to a guessed eight-pin physical order. Native USB application/game loading still requires firmware; storage is not automatically presented as a drag-and-drop disk.

## 3. Controls and GPIO expander

U1 = **MCP23017-E/SP**, narrow DIP-28, in **ED281DT** socket. [Datasheet](datasheets/mcp23017.pdf).

| Pin(s) | Connection |
|---|---|
| 9 VDD / 10 VSS | LOGIC_3V3 / GND |
| 12 SCL / 13 SDA | GPIO9 / GPIO8; R2/R1 respectively, 4.7 kohm pull-ups |
| 15 A0 / 16 A1 / 17 A2 | GND; I2C address 0x20 |
| 18 RESET | GPIO7 and R3 10 kohm pull-up |
| 20 INTA | GPIO4 and R4 10 kohm pull-up |
| 19 INTB | Unconnected; configure mirrored open-drain interrupts |
| 21 GPA0 / 22 GPA1 / 23 GPA2 / 24 GPA3 | SW1 Up / SW2 Down / SW3 Left / SW4 Right |
| 1 GPB0 / 2 GPB1 / 3 GPB2 / 4 GPB3 | SW5 A / SW6 B / SW7 X / SW8 Y |
| 5–8 and 25–28 | Unconnected spare ports; firmware initializes unused ports safely |
| 11 / 14 | NC, no connection |

SW9 Function connects directly to GPIO5 for a possible RTC wake input. All nine switches close to GND and have individual 10 kohm pull-ups R5–R13. Four-leg Adafruit 3101 switches have two logical contacts: **verify which physical legs are internally paired before assigning footprint pad numbers**. The CSV uses logical A/B contacts deliberately.

C1 = 100 nF at U1 supply pins; C2 = 10 uF local bulk, positive pin toward LOGIC_3V3. Start at 100 kHz I2C. With 4.7 kohm pull-ups, assumed 100 pF bus capacitance gives approximately 0.40 us rise time; 400 kHz is not automatically qualified. Measure the assembled bus and include module capacitance.

Firmware initialization: reset U1 with the datasheet pulse timing; set output latches low before enabling unused outputs; configure eight used button bits as inputs. **GPA7 and GPB7 are output-only on the current datasheet and are not button inputs.** Configure IOCON MIRROR=1 and ODR=1, interrupt-on-change on the eight button bits, and read capture/port registers to clear interrupts. Suggested software debounce: sample every 5 ms, accept after 15–20 ms stable; validate game feel and simultaneous presses. No button matrix means no matrix ghosting.

## 4. Conservative IR starter circuit

| Part | Connection / value |
|---|---|
| R14 | 100 ohm, LOGIC_3V3 to D1 anode |
| D1 TSAL6200 | Anode at R14; cathode to Q1 collector |
| Q1 KSP2222ABU | Pin 1 emitter GND; pin 2 base IR_BASE; pin 3 collector D1 cathode |
| R15 | 220 ohm, GPIO17 to Q1 base |
| R16 | 100 kohm, Q1 base to GND, default-off bias |
| C5 | 100 nF between LOGIC_3V3 and GND near emitter driver supply path |
| R17 | 100 ohm, LOGIC_3V3 to filtered IR_RX_3V3 |
| U2 TSOP38238 | Pin 1 output GPIO18; pin 2 GND; pin 3 IR_RX_3V3 |
| C3 / C4 | 100 nF / 10 uF between IR_RX_3V3 and GND; electrolytic positive toward supply |

[Emitter datasheet](datasheets/tsal6200.pdf) · [transistor datasheet](datasheets/ksp2222a.pdf) · [receiver datasheet](datasheets/tsop382.pdf).

This is a low-current bring-up circuit, not a promised remote-control range. Assuming LED Vf=1.35 V and transistor VCE=0.2 V gives about **17.5 mA peak** at 3.3 V. These are illustrative assumptions, not guaranteed device corners. Under a provisional 3.3 V ±5% supply envelope and 1% resistance, even a shorted LED would be limited to about 35 mA by R14; maximum resistor dissipation is about 0.122 W, below its 0.25 W rating before ambient derating. Recheck against actual rail limits and enclosure temperature.

R15's theoretical upper bound is 15.9 mA at the same assumed high rail if the base node were at ground; real base current is lower. Review MCU drive strength/VOH at load and measure saturation. Drive pulses with ESP32 RMT or a timer, not the expander. Start with 38 kHz carrier around one-third duty and bounded bursts that follow receiver AGC gap rules. GPIO18 is an input without an external pull-up; the receiver has an internal pull-up. Locate receiver away from direct emitter spill and switching noise.

TSOP38238 is a **38 kHz demodulating receiver**, not a universal raw-IR capture front end. Optical range, protocol coverage and eye-safety assessment remain untested. IR does not replace the ESP32's built-in Wi-Fi/BLE pet-trading options; sub-GHz hardware remains excluded.

## 5. Remaining circuit sheets before a complete BOM freeze

1. Power architecture: USB input limits including enumeration/suspend, source isolation, charge control/protection, temperature checks, off-state charging, system regulation, startup, deep discharge and fault tests. Define cell electrical envelope before layout.
2. Display: inspect actual module header order, supply regulator/level shifting, backlight current and mounting. Then commit connector orientation and driver parts.
3. Audio: TDA2822L bridge circuit, roughly 40 dB gain compensated by PWM filtering/attenuation, input coupling, stability networks and supply gating. **Neither bridge speaker terminal is GND.** Obtain a controlled FS1511P08-H3.0 speaker drawing/rating before setting power.
4. Haptics: check MCP1700 headroom/thermal behavior, motor starting/stall current, transistor drive, flyback placement and suppression. Keep motor return current out of audio/IR reference paths.
5. Finish schematic capture, derive all remaining individual passive quantities and footprints, perform independent pin review and ERC, place components, then select enclosure hardware and battery dimensions.

No substitutions, firmware-only lithium safety, SMD adapter or MCU-module rework are silently introduced to clear these holds. The whole-kit table records each open category so it is not forgotten.

## Reproducible outputs and limits

Run `node KK_main_module/component_review/build_design_tables.mjs` from the project root. It regenerates the master Markdown/CSV tables, per-pin connections, GPIO allocation and validation summary. The generator is the source for the initial circuit topology; `parts.csv` is the source for baseline component identities. See [validation](VALIDATION.md).

No KiCad CLI is installed in this environment. Accordingly this revision provides a reviewable electrical connection schedule, **not a falsely claimed ERC-checked schematic**. Prototype verification and actual KiCad capture remain required. The existing `KK_power_module` and unrelated workspace changes are untouched.
