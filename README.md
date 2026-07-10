# Keychain Kreatures

**Keychain Kreatures** is an ESP32-C3-powered virtual-pet and tiny handheld game platform.

The current Rev. A prototype includes:

- ESP32-C3 Super Mini
- 1.69-inch 240×280 ST7789 IPS display
- MAX98357A I²S audio amplifier
- PCF8574 I²C button expander
- Six game buttons
- Infrared transmitter and receiver
- Vibration feedback
- Rechargeable battery power

This repository currently contains the hardware test firmware used to verify an assembled unit.

## Factory Test

The factory test checks:

- ST7789 display output
- MAX98357A audio output
- PCF8574 detection
- Direction buttons
- A and B buttons
- Vibration module
- IR transmission
- IR receiver activity
- Serial logging
- On-screen event logging

### Factory Test Controls

| Control | Test action |
|---|---|
| UP | Logs the button and plays a tone |
| DOWN | Logs the button and plays a tone |
| LEFT | Logs the button and plays a tone |
| RIGHT | Logs the button and plays a tone |
| A | Plays a tone and activates vibration |
| B | Plays a tone and sends an IR test burst |

> The IR receiver is connected through PCF8574 P7. This is suitable for detecting IR activity, but it is not ideal for decoding fast consumer remote-control protocols.

## Wiring

### ST7789 Display

| ST7789 | ESP32-C3 Super Mini |
|---|---|
| GND | GND |
| VCC | 3V3 |
| BLK | 3V3 |
| SCL | GPIO4 |
| SDA | GPIO6 |
| RES | GPIO7 |
| DC | GPIO2 |
| CS | GPIO10 |

### MAX98357A Audio Amplifier

| MAX98357A | ESP32-C3 Super Mini |
|---|---|
| VIN | 3.3V |
| GND | GND |
| DIN | GPIO20 |
| BCLK | GPIO21 |
| LRC / WS | GPIO0 |
| SD | GPIO5 |
| GAIN | Not connected |

### PCF8574

| PCF8574 | ESP32-C3 Super Mini |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO8 |
| SCL | GPIO9 |

### Buttons and IR Receiver

Each button connects between its assigned PCF8574 pin and GND.

| Function | PCF8574 pin |
|---|---|
| UP | P0 |
| DOWN | P1 |
| LEFT | P2 |
| RIGHT | P3 |
| A | P4 |
| B | P5 |
| Spare | P6 |
| IR receiver OUT | P7 |

### IR Transmitter

| IR transmitter | Connect to |
|---|---|
| VCC | 3.3V |
| GND | GND |
| DATA | GPIO1 |

### IR Receiver

| IR receiver | Connect to |
|---|---|
| VCC | 3.3V |
| GND | GND |
| OUT | PCF8574 P7 |

### Vibration Module

| Vibration module | Connect to |
|---|---|
| VCC | 3V3 |
| GND | GND |
| IN | GPIO3 |

## PlatformIO Setup

PlatformIO automatically installs the required display libraries from `platformio.ini`.

Required libraries:

- Adafruit GFX Library
- Adafruit ST7735 and ST7789 Library

### Repository layout

```text
KeychainKreatures/
├── platformio.ini
├── README.md
└── src/
    └── main.cpp
```

Place the factory-test source in:

```text
src/main.cpp
```

If the code currently exists as an Arduino `.ino` sketch, copy it into `src/main.cpp`.

PlatformIO accepts Arduino-style `setup()` and `loop()` functions inside `main.cpp`, but the file should contain:

```cpp
#include <Arduino.h>
```

The generated factory-test source already includes this header.

## Build and Upload

Install the PlatformIO extension in Visual Studio Code, open the repository folder, and use the PlatformIO toolbar.

Or use the terminal:

```bash
pio run
```

Upload over USB:

```bash
pio run --target upload
```

Open the serial monitor:

```bash
pio device monitor
```

Build, upload, and monitor:

```bash
pio run --target upload && pio device monitor
```

The serial monitor runs at:

```text
115200 baud
```

## Finding the USB Port

On Linux:

```bash
pio device list
```

The ESP32-C3 commonly appears as:

```text
/dev/ttyACM0
```

If automatic port detection fails, add this under the environment in `platformio.ini`:

```ini
upload_port = /dev/ttyACM0
monitor_port = /dev/ttyACM0
```

## Arduino IDE

The same firmware can also be compiled with Arduino IDE.

Install:

- ESP32 board support by Espressif Systems
- Adafruit GFX Library
- Adafruit ST7735 and ST7789 Library

Select:

```text
ESP32C3 Dev Module
```

Set the Serial Monitor to:

```text
115200 baud
```

## Project Goals

Keychain Kreatures is intended to become:

- A virtual-pet platform
- A tiny game system
- A beginner-friendly embedded programming device
- A hackable open hardware project
- A home for WonderBasic Mini applications
- An IR-enabled creature trading and battle platform

## Hardware Revision

This pinout currently targets:

```text
Keychain Kreatures Rev. A
ESP32-C3 Super Mini
```

Future revisions should keep their own documented pin maps and factory-test environments.
