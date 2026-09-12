# Keychain Kreatures

An ESP32-S3 virtual-pet and small handheld-game hardware project, designed around a repairable through-hole main-board kit and a separate factory-assembled power board.

**Current hardware: main C.6 + power P.3. Engineering prototypes—not a tested, certified or production-ready toy.** Both boards are 96 × 105 × 1.6 mm with matching mounting holes for a removable stack. Physical component fit, battery/case selection, factory DFM approval and powered qualification remain open.

## Current projects and downloads

| Board | Editable KiCad 10 project | Five-prototype review package | Gerbers and drills |
|---|---|---|---|
| Main C.6 · 2 copper layers | [Open main project](KK_main_module/C6_flat_stack/KK_main_module.kicad_pro) | [Full main ZIP](KK_main_module/manufacturing/KK_MAIN_C6_5_PROTOTYPE_REVIEW_2026-09-12.zip) | [Main fabrication ZIP](KK_main_module/manufacturing/KK_MAIN_C6_GERBERS.zip) |
| Power P.3 · 4 copper layers | [Open power project](KK_power_module/P3_matching_stack/KK_power_module.kicad_pro) | [Full power ZIP](KK_power_module/manufacturing/KK_POWER_P3_5_PROTOTYPE_REVIEW_2026-09-12.zip) | [Power fabrication ZIP](KK_power_module/manufacturing/KK_POWER_P3_GERBERS.zip) |

Download the repository or a **full review ZIP** to open a project with its local libraries, models and documentation. Install the KiCad 10 standard footprint and 3D libraries as well. For GitHub ZIP downloads, use the file page's download/raw action. The full review packages include fabrication files, BOMs, placement and test-point maps, schematic/assembly PDFs, source CAD, datasheets and verification evidence. The separate fabrication ZIPs do not replace the assembler's full review package.

[Start here](START_HERE.md) · [Documentation index](docs/README.md) · [Release notes](CHANGELOG.md) · [Release hashes](docs/C6_P3_RELEASE_INDEX.json)

## Hardware in this revision

- Socketed **ESP32-S3 SuperMini**. Confirm the delivered seller revision, pinout and actual flash/PSRAM; do not infer N16R8 specifications from the SuperMini name.
- Existing ST7789V2 screen in landscape, **280 × 240 pixels**, and a separate socketed 3.3 V microSD reader. SD storage is not extra executable RAM.
- Nine soft controls: D-pad left, four action buttons right, one center function button, all below the screen. MCP23017 GPIO expansion.
- PWM audio with a TDA2822L amplifier, speaker connector and switched amplifier supply; vibration motor output with suppression.
- TSAL6200 infrared transmitter and TSOP38238 receiver, aimed toward the case opening. No sub-GHz radio.
- Separate socketed common-anode RGB LED and TLC5916 driver.
- Main board: **98 fitted through-hole positions**, all **43 resistors horizontal**, ten horizontal low-profile electrolytics, six flat-mounted TO-92 devices, removable IC/module sockets, JST connectors and **25 bare debug holes**.
- Power board: **108 fitted positions**, 28 rear test pads, USB-C charging input, battery protection, temperature interlock and three regulated output rails. This board is a **factory SMT subassembly**, not a student SMT soldering exercise.

All fitted electrical positions have resolving 3D model links. Some module and connector envelopes remain provisional; model coverage does not prove fit. Sockets, buttons and optical components necessarily retain height. The proposed 20 mm inter-board spacing is for a mock-up, not an approved enclosure dimension.

## Assembly and first power-up

Read these before buying parts, soldering or powering a board:

1. [Main BOM and assembly/wiring guide](KK_main_module/C6_flat_stack/assembly/ASSEMBLY_GUIDE.md), [reference BOM](KK_main_module/C6_flat_stack/assembly/C6_BOM_BY_REFERENCE.csv), and [complete paired-kit extras](KK_main_module/C6_flat_stack/assembly/C6_COMPLETE_KIT_EXTRAS.csv). Extras cover sockets, modules, mating plugs, wiring and provisional hardware; count them once per main+power pair.
2. [Print the stack review at actual size](docs/C6_P3_STACK_REVIEW.pdf), [front fit sheet](KK_main_module/C6_flat_stack/assembly/C6_front_FIT_100_PERCENT.pdf) and [rear fit sheet](KK_main_module/C6_flat_stack/assembly/C6_back_FIT_100_PERCENT.pdf). Measure the calibration line and dry-fit actual parts and plugged harnesses.
3. [Power fabrication/assembly requirements](KK_power_module/P3_matching_stack/FABRICATION_REQUIREMENTS.md). Obtain manufacturer approval of the 0.4 mm WCSP, fine-pitch packages and **filled/capped/planarized via-in-pad** process. Ordinary via tenting is not equivalent.
4. [Power electrical review and current-limited first-power-up procedure](KK_power_module/P3_matching_stack/assembly/P3_REVIEW_AND_TEST.md). Qualify power independently before attaching the populated main board. Real-cell testing requires a selected, documented cell and bonded thermistor.

Power **J3 → main J1**, keyed pin-for-pin:

| Pin | Rail |
|---|---|
| 1 | MCU_5V |
| 2 | GND |
| 3 | LOGIC_3V3 |
| 4 | ACT_3V2 |

**Never connect raw battery voltage to main J1. Power TP3/BAT_NEG is not TP4/GND; do not bypass battery protection with test-equipment grounds. Neither speaker output is ground.**

Charger USB carries **no data** to the ESP32. Do not combine ESP32 USB power and external main rails until exact-module reverse-feed behavior is qualified. Program the removable MCU separately for recovery. USB-A/default charging is deliberately slow and may not cover a running toy's load.

## Verification and remaining work

The issued C.6/P.3 sources passed fresh native ERC/DRC, connectivity and schematic-parity checks with **zero reported violations or opens**. [Static audit](docs/C6_P3_STATIC_AUDIT.json), [matching drill audit](docs/C6_P3_DRILL_ALIGNMENT_AUDIT.json) and package manifests identify exactly what was checked. Existing ignored-check settings are included in the native reports; clean reports are not a claim that every possible check was performed.

Run this lightweight saved-release consistency check from the repository root:

```sh
node tools/check_project.mjs
```

It verifies current source/package hashes, local assets, saved netlists and the inter-board interface. It does **not** rerun KiCad checks or simulate the circuit. See [tool instructions](tools/README.md) before running anything else. Do not rerun historical placement/route generators on finished CAD.

Remaining qualification includes physical socket/plug/case fit, battery/NTC selection, speaker power rating, simultaneous-load capacity, capacitor transient/ripple behavior, regulator/charger temperatures, USB behavior, rail sequencing, GPIO back-powering, RF performance and applicable product safety/EMC review. In particular, the older main 3.3 V reservation was 0.5 A while power screening used 0.4 A; reconcile measured peak demand and margin before approving the complete toy. Screening targets are not measured ratings.

## Firmware status

The planned virtual pet, games/apps, browser/Wi-Fi uploads, trading, save recovery and OTA workflow are **not implemented or validated by this hardware release**. Follow the current schematic and assembly guide for bring-up firmware. The historical ESP32-C3/MAX98357A/PCF8574 test sketch from earlier Git history is not compatible with this S3/MCP23017/TDA2822L board and must not be used as its factory test.

## History, contributions and licensing

The unversioned main CAD, C5_relayout, P2_compact and [revisions](revisions/README.md) preserve earlier work. They are not current fabrication sources. Archived reports retain their original findings and must not be read as today's status. See [contribution guidance](CONTRIBUTING.md).

The project is intended for open development, but a project-wide license has **not yet been selected**. The OSHW silkscreen logo is not a certification or a substitute for license terms. Third-party KiCad assets and manufacturer documents retain their respective terms; do not assume this repository relicenses them. Thanks to the KiCad, Espressif and component-library communities.
