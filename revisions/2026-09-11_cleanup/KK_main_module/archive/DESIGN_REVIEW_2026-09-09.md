# Archived breadboard-to-main-board review

Historical only. Current findings and requirements are in ../DESIGN_REVIEW.md. Eight-button, large-WROOM and SMT-audio recommendations below are superseded.

2026-09-09. Evidence and proposed changes; not a fabrication release.

## Findings

| Priority | Evidence | Implication | Proposed correction |
|---|---|---|---|
| High | Both documents route IR receiver OUT to PCF8574 P7 | Expander reads do not preserve a timestamped pulse stream; reliable decoding becomes vulnerable to I2C latency and other work | Connect IR receiver directly to an ESP32 RMT-capable GPIO |
| High | The listed C3 map uses GPIO0–10 and GPIO20–21 | All 13 listed exposed GPIOs are consumed | Prefer an S3 module with PSRAM; prepare a fresh pin allocation |
| High | C3 GPIO2 drives display DC; GPIO8/9 serve I2C | These are boot strapping pins; attached pulls, buttons, and powered peripherals can affect reset | Verify reset states if retaining C3; keep boot straps separate in the new allocation |
| High | Modules all use the Super Mini 3V3 rail | Breadboard success does not establish regulator headroom during radio, display, audio, and motor peaks | Add a dedicated regulator and budget power at minimum battery voltage |
| High | Power board J3 is SYS_OUT/GND | SYS_OUT is neither a guaranteed 3.3 V supply nor always limited to battery voltage | Regulate it locally; account for operation near USB input voltage |
| High | Power board J5 has VBAT and charger status nets also connected to LED branches from VBUS | MCU pins cannot connect directly to these voltage domains | Add battery sensing with power-off isolation and status input conditioning |
| High | Existing power switch is C&K JS102011SAQN in series with SYS_OUT | Its 0.3 A at 6 V DC rating can constrain this larger product | Establish total load before approving the power interface; a new power switch/load-switch design may be needed |
| High | IR and motor are described as three-pin modules | Their drive transistors/protection may exist only on the breakout boards | Integrate the complete driver circuits, including current limiting and reset-state control |
| Medium | BLK is permanently tied to 3V3 | No brightness control or independent backlight shutdown | Add PWM control appropriate to the exact display backlight interface |
| Medium | Six buttons are specified | Gameboy-style controls usually also need Start and Select | Plan eight inputs; keep a separate direct wake button |
| Medium | No programming path for the integrated chip is specified | A custom board loses the Super Mini's USB/reset/support circuits | Add native USB or programming pads, EN/BOOT access, and a recoverable boot path |
| Medium | No pet-state persistence, application ABI, or trade protocol is specified | Hardware alone will not provide installable apps or reliable pet ownership transfer | Define these as firmware services before committing flash/RAM capacity |
| Medium | Exact display board, motor, speaker, and enclosure dimensions are absent | Names such as ST7789 do not uniquely define connector, voltage, current, or mounting | Obtain exact mechanical/electrical interfaces before PCB routing |

The PCF8574 remains usable for buttons. The problem is its use for time-sensitive IR capture, not the idea of an I/O expander. TI specifies a 100 kHz I2C clock; even an address plus one data byte costs roughly 180 microseconds of clock time before software overhead. Its interrupt indicates a change, not a queue of timestamped transitions. This timing assessment is an engineering inference from the [TI PCF8574 datasheet](https://www.ti.com/lit/ds/symlink/pcf8574.pdf). ESP32 RMT hardware provides pulse-duration capture: [Espressif RMT documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/rmt.html).

The C3 strapping restrictions are documented in [Espressif's schematic checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html). These pin uses can work with proper reset biasing; their presence alone does not prove the prototype boots incorrectly.

## Corrections that replace missing breakout-board circuitry

- IR transmitter: logic-level transistor/MOSFET, gate/base resistor, default-off bias, LED current-setting resistor, and pulse-current/duty limits matched to the emitter. A GPIO supplies control, not emitter power.
- IR receiver: select a demodulating receiver for the intended carrier/protocol; add its recommended supply filter. A fixed-carrier demodulator is not a general raw optical waveform receiver.
- Vibration: an ERM motor needs a transistor, flyback suppression, local decoupling, and stall-current budgeting. An LRA needs an appropriate haptic driver instead; do not assume the two are interchangeable.
- Audio: retain the MAX98357A IC, add its complete reference circuit, and choose an actual speaker. Keep the two bridge outputs separate from ground. Floating GAIN is a documented setting, not automatically an error; SD_MODE also selects channel behavior. Use a deterministic muted reset state. See [Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max98357a-max98357b.pdf).
- Buttons: use pull-ups, debounce, and simultaneous-button support. Avoid boot straps for game buttons. External pulls are needed for an expander that lacks them.
- Display: the SCL/SDA names in these notes refer to SPI clock/MOSI, not I2C. Confirm resolution, voltage, pin order, backlight circuit, and connector before assigning a footprint.
- Supply: decouple the MCU and every IC; keep audio/motor/IR return currents away from ADC and RF sections while preserving a continuous ground plane.

## Product optimization

An ESP32-S3-WROOM-1-N16R8 is the preferred candidate: 16 MB flash and 8 MB PSRAM provide room for graphics, audio, saves, and an application runtime. Its module footprint and antenna placement must fit the enclosure; it is not yet the approved choice. GPIO35–37 are unavailable with this octal-PSRAM configuration. The S3 provides Wi-Fi and Bluetooth LE, not Bluetooth Classic. See [module datasheet](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf).

I recommend a four-layer main PCB if the dimensions are tight: signal/components, ground, power/secondary signals, and bottom signals. The external power board's two-layer construction does not require the main board to be two layers. Place the antenna at an enclosure edge with the manufacturer's keepout, including clearance from the screen, battery, metal keyring, and adjacent boards.

Start with original small 2D games and a pet launcher. Game Boy/Game Boy Color emulation can be evaluated later against frame rate and power targets; Game Boy Advance compatibility is not implied by this architecture.

## Power board dependency discovered during this review

The existing output switch's rating is a concrete integration issue. C&K lists JS102011SAQN in its 0.3 A / 6 V DC family: [manufacturer selection guide](https://www.ckswitches.com/media/2222/shortform.pdf). The main-board architecture cannot assume a 1–2 A upstream supply simply because its own regulator can support that current. The earlier power-board DRC pass does not establish system current capacity. The power board has not been changed in this review.

## Before schematic completion and placement

Accepted: ESP32-S3 with PSRAM. Required: exact display part/interface; IR versus additional radio requirements; board outline; mounting and button coordinates; battery model/capacity/current limits; speaker impedance/power/dimensions; vibration actuator type/rating; and programming-port access. These choices determine actual circuitry and geometry, so candidate parts and pin assignments remain provisional.
