# 🐣 Keychain Kreatures

> **A tiny open-source virtual pet, handheld game system, and embedded learning platform powered by the ESP32-C3.**

![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Open%20Source-blue)
![Platform](https://img.shields.io/badge/Platform-ESP32--C3-orange)
![IDE](https://img.shields.io/badge/IDE-Arduino-blue)

---

# 🌟 About

**Keychain Kreatures** is an open hardware and open source handheld designed to bring together the nostalgia of classic virtual pets with modern electronics.

Rather than being a closed toy, Keychain Kreatures is designed to be:

- 🐣 A Virtual Pet
- 🎮 A Tiny Game Console
- 💻 A Programming Platform
- 📚 A Learning Tool
- 🛠️ Completely Hackable

The project is intended for makers, students, hobbyists, and anyone interested in learning embedded systems.

---

# ✨ Features

- 🧠 ESP32-C3 Super Mini
- 🖥️ 1.69" 240×280 IPS Display
- 🔊 MAX98357A I²S Audio
- 🔈 Speaker Output
- 🎮 Six-Button Game Controls
- 📡 Infrared Transmitter
- 📡 Infrared Receiver
- 📳 Vibration Feedback
- 🔋 Rechargeable LiPo Battery
- 🔌 USB Charging
- 🛠️ Open Hardware
- 💻 Open Source Firmware

---

# 📦 Hardware

## 🧠 Microcontroller

- ESP32-C3 Super Mini
- RISC-V CPU
- Wi-Fi
- Bluetooth LE
- USB Programming
- 4 MB Flash

---

## 🖥️ Display

- 1.69" IPS LCD
- ST7789 Controller
- Resolution: **240 × 280**
- SPI Interface

---

## 🔊 Audio

- MAX98357A Digital I²S Amplifier
- Mono Speaker
- Sound Effects
- Music Playback

---

## 🎮 Controls

Buttons are connected using a **PCF8574 I²C GPIO Expander**.

| Button | PCF8574 Pin |
|---------|-------------|
| ⬆️ UP | P0 |
| ⬇️ DOWN | P1 |
| ⬅️ LEFT | P2 |
| ➡️ RIGHT | P3 |
| 🅰️ A | P4 |
| 🅱️ B | P5 |
| ⭐ Spare | P6 |
| 📡 IR Receiver | P7 |

---

## 📳 Haptic Feedback

A vibration module provides feedback for:

- Battle hits
- Menu selection
- Notifications
- Creature reactions

---

## 📡 Infrared

### 📤 Transmitter

GPIO1

### 📥 Receiver

Connected to:

PCF8574 P7

Future firmware will support:

- Creature Battles
- Creature Trading
- Multiplayer
- Secret Codes
- Mini Games

---

# 🔌 Wiring

## 🖥️ ST7789 Display

| Display Pin | ESP32-C3 |
|--------------|-----------|
| GND | GND |
| VCC | 3V3 |
| BLK | 3V3 |
| SCL | GPIO4 |
| SDA | GPIO6 |
| RES | GPIO7 |
| DC | GPIO2 |
| CS | GPIO10 |

---

## 🔊 MAX98357A Audio

| Amplifier Pin | ESP32-C3 |
|---------------|-----------|
| VIN | 3.3V |
| GND | GND |
| DIN | GPIO20 |
| BCLK | GPIO21 |
| LRC / WS | GPIO0 |
| SD | GPIO5 |
| GAIN | NC |

---

## 🎮 PCF8574

| PCF8574 Pin | ESP32-C3 |
|--------------|-----------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO8 |
| SCL | GPIO9 |

---

## 📡 IR Transmitter

| Pin | Connect To |
|------|------------|
| VCC | 3.3V |
| GND | GND |
| DATA | GPIO1 |

---

## 📡 IR Receiver

| Pin | Connect To |
|------|------------|
| VCC | 3.3V |
| GND | GND |
| OUT | PCF8574 P7 |

---

## 📳 Vibration Module

| Pin | Connect To |
|------|------------|
| VCC | 3.3V |
| GND | GND |
| IN | GPIO3 |

---

# 🔋 Power

The device is powered from a single-cell LiPo battery.

```
🔋 Battery
      │
      ▼
⚡ Charger Board
      │
      ▼
🔘 Power Switch
      │
      ▼
🧠 ESP32-C3
```

---

# 📌 GPIO Assignment

| GPIO | Function |
|------|----------|
| GPIO0 | Audio LRC |
| GPIO1 | IR Transmitter |
| GPIO2 | TFT DC |
| GPIO3 | Vibration Motor |
| GPIO4 | TFT Clock |
| GPIO5 | Amplifier Shutdown |
| GPIO6 | TFT MOSI |
| GPIO7 | TFT Reset |
| GPIO8 | I²C SDA |
| GPIO9 | I²C SCL |
| GPIO10 | TFT Chip Select |
| GPIO20 | Audio DIN |
| GPIO21 | Audio BCLK |

---

# 🧪 Factory Test Firmware

Every assembled board should first run the **Factory Test**.

The test verifies:

✅ Display

✅ Speaker

✅ Audio Amplifier

✅ Buttons

✅ PCF8574

✅ IR Transmitter

✅ IR Receiver Activity

✅ Vibration Motor

✅ GPIO Operation

All events are displayed on the LCD and logged to the Serial Monitor.

---

## 🎮 Factory Test Controls

| Button | Action |
|---------|--------|
| ⬆️ UP | Button Test |
| ⬇️ DOWN | Button Test |
| ⬅️ LEFT | Button Test |
| ➡️ RIGHT | Button Test |
| 🅰️ A | Vibration Test |
| 🅱️ B | IR Transmission Test |

---

# 🚀 Quick Start

## 1️⃣ Install Arduino IDE

Download the latest version:

https://www.arduino.cc/en/software

---

## 2️⃣ Install ESP32 Support

Open:

```
Tools
    ↓
Board
    ↓
Boards Manager
```

Search for:

```
ESP32
by Espressif Systems
```

Install the latest version.

---

## 3️⃣ Install Required Libraries

Open:

```
Sketch
    ↓
Include Library
    ↓
Manage Libraries...
```

Install:

✅ Adafruit GFX Library

✅ Adafruit ST7735 and ST7789 Library

These are the **only external libraries** currently required.

---

## 4️⃣ Select Your Board

```
ESP32C3 Dev Module
```

---

## 5️⃣ Open

```
factory_test.ino
```

---

## 6️⃣ Upload

Click:

```
➡ Upload
```

Wait for the upload to finish.

Done! 🎉

---

## 📺 Serial Monitor

Set the Serial Monitor to:

```
115200 baud
```

---

# 📂 Repository Layout

```
KeychainKreatures/

│
├── firmware/
│   ├── factory_test/
│   └── creature_os/
│
├── hardware/
│   ├── KiCad/
│   ├── Gerbers/
│   └── BOM/
│
├── docs/
│   ├── Wiring.md
│   ├── Pinout.md
│   └── FactoryTest.md
│
├── images/
│
├── README.md
│
├── LICENSE
│
└── .gitignore
```

---

# 🛣️ Roadmap

## 🟢 Phase 1

- ✅ Factory Test
- ✅ Display
- ✅ Audio
- ✅ Buttons
- ✅ IR
- ✅ Vibration

---

## 🟡 Phase 2

- Creature Engine
- Save Files
- Animation System
- Menus
- Sound Engine

---

## 🔵 Phase 3

- Creature Trading
- Creature Battles
- IR Multiplayer
- OTA Updates
- Sleep Mode
- Battery Monitoring

---

## 🟣 Future Ideas

- 💾 SD Card Support
- 📶 Bluetooth Multiplayer
- 🌈 RGB Status LED
- 🌡️ Temperature Sensor
- ☀️ Light Sensor
- 🎲 Mini Games
- 🧩 Puzzle Games
- 🐉 Creature Evolution
- 📚 WonderBasic Mini Runtime

---

# 🎯 Project Goals

Keychain Kreatures is designed to be:

- 🎮 Fun
- 📚 Educational
- 🔓 Open Source
- 🛠️ Repairable
- 💰 Affordable
- 👨‍💻 Beginner Friendly
- 🧠 Easy to Learn From
- 🔧 Easy to Modify

---

# 🤝 Contributing

Contributions are always welcome!

Ideas include:

- Firmware
- Games
- New Creatures
- PCB Improvements
- Documentation
- Artwork
- Sound Effects
- Bug Fixes

If you build your own Keychain Kreatures, we'd love to see it!

---

# ❤️ Acknowledgements

Special thanks to the amazing open-source communities behind:

- Espressif
- Arduino
- Adafruit
- KiCad
- GitHub

Without these projects, Keychain Kreatures would not exist.

---

# 📜 License

This project is intended to be released under an open-source license.

License selection is currently in progress.

---

# 🐣 Build One. Learn Something. Make It Your Own.

Keychain Kreatures isn't just another virtual pet.

It's a tiny computer designed to teach programming, electronics, hardware design, and creativity—all while being fun to play.

**Hack it. Improve it. Share it.**
