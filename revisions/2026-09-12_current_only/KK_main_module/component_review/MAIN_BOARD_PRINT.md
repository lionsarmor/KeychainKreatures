# Keychain Kreatures — printable main-board list

2026-09-10 — main-board review checklist, not a final purchasing/bagging list. Charging, battery protection and ALL added voltage regulation, including the motor regulator, belong to the separate power board. MCU, display and SD reader are permitted preassembled modules with THT student connections. Local bypass capacitors and actuator drivers remain on the main PCB. No hardware has been ordered or fabricated.

Quantity is per toy. “TBD total” means the schematic must determine the count; starter counts are subtotals, not extra parts. Zero-use candidate values are not instructions to buy a resistor bag. Module-bundled headers must not be purchased twice.

| Item | Exact part / candidate | Quantity | Status |
|---|---|---|---|
| CORE | ESP32-S3 SuperMini / original Amazon B0D47HBFDY | 1 | User-selected module family; exact revision check |
| DISPLAY | B0DFWL25RB | 1 | User-selected; interface HOLD |
| GPIO | MCP23017-E/SP | 1 | Design baseline |
| CONTROLS | 3101 | 9 | Design baseline; mechanical check |
| AUDIO | TDA2822L-D08-T | 1 | Design baseline |
| SPEAKER | FS1511P08-H3.0 wired | 1 | HOLD drawing and power rating |
| HAPTIC | LCM0827A3038F | 1 | Design baseline; drive qualification |
| IR_TX | TSAL6200 | 1 | Design baseline |
| IR_RX | TSOP38238 | 1 | Design baseline |
| NPN_DRIVER | KSP2222ABU | TBD total; 1 in starter circuit | Design baseline; quantity/calculation pending |
| PNP_SWITCH | BC32725BU | TBD | Peripheral candidate only |
| FLYBACK | 1N5819-E3/54 | 1 minimum | Design baseline; total TBD |
| MCU_SOCKET | PPTC091LFBN-RC | 2 | Design baseline; SuperMini fit check |
| MCU_HEADER | 9-pin male strips supplied with selected module | 2 strips if not factory-fitted | Bundle contents / fit verification |
| GPIO_SOCKET | ED281DT | 1 | Design baseline |
| AUDIO_SOCKET | ED08DT | 1 | Design baseline |
| DISPLAY_SOCKET | PPTC081LFBN-RC | 1 | Design baseline; screen-dependent |
| ACTUATOR_CONNECTOR | S2B-PH-K-S(LF)(SN) | 2 | Design baseline |
| ACTUATOR_HOUSING | PHR-2 | 2 | Design baseline |
| MOTOR_CONTACT | SPH-004T-P0.5S | 2 | Candidate; insulation check |
| RESISTOR | MFR-25FBF52-4R7 | TBD | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-39R | TBD | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-100R | TBD total; 2 in starter circuit | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-220R | TBD total; 1 in starter circuit | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-680R | TBD | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-1K | TBD | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-4K7 | TBD total; 2 in starter circuit | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-10K | TBD total; 11 in starter circuit | Value pool; not a bag count |
| RESISTOR | MFR-25FBF52-100K | TBD total; 1 in starter circuit | Value pool; not a bag count |
| CAPACITOR | C315C104K5R5TA | TBD total; 3 in starter circuit | Value pool |
| CAPACITOR | C315C103J1G5TA | TBD | Value pool |
| CAPACITOR | C315C105K5R5TA | TBD | Value pool |
| CAPACITOR | UVR1C100MDD | TBD total; 2 in starter circuit | Value pool |
| CAPACITOR | UVR1C101MDD | TBD | Value pool |
| SD_MODULE | Amazon B0F82XWT4F | 1 | User-selected; 3V3 and signal labels confirmed in photo; sample test pending |
| SD_SOCKET | PPTC061LFBN-RC | 1 proposed | Series candidate; delivered pitch / stack-height check |
| SD_HEADER | Six-pin male strip pictured with B0F82XWT4F | 1 strip included if supplied | Bundle contents / fit verification |
| BACKLIGHT_DRIVER | Backlight control and default-off network | TBD | HOLD — display sample |
| AUDIO_NETWORK | PWM filter / attenuation / coupling / bridge stability | TBD | HOLD — calculations |
| AUDIO_GATE | Amplifier supply gating network | TBD | HOLD — calculations |
| MOTOR_NETWORK | Motor drive / suppression | TBD | HOLD — startup and stall |
| SPEAKER_CONTACT | Speaker harness crimp contacts | 2 | HOLD — wire gauge |
| MAIN_PCB | KK main-board custom PCB | 1 | Design pending |
| TEST_ACCESS | PCB test pads and optional service header | TBD pads | Design pending |
| SCREEN_RETENTION | Display retention hardware / spacers | 1 set | Mechanical design pending |
| PCB_HARDWARE | PCB spacers and fasteners | TBD | Mechanical design pending |
| ACTUATOR_MOUNT | Speaker gasket and motor retention | 1 set | Mechanical design pending |
| MICROSD | microSD card; exact brand/capacity pending | 1 | Storage now included; card selection pending |
| SYS_IN_CONNECTOR | Keyed THT regulated-power input connector | 1 | Interface selection pending |
| SYS_IN_HARNESS | Power-board to main-board harness and mating contacts | 1 set | Interface selection pending |
| MAIN_RAIL_INTERFACE | Main-board rail distribution / local bypass capacitors | TBD | Main-board engineering pending |
| SD_SUPPORT | SD supply bypass / bus pull-ups / optional series resistors | TBD | Circuit inspection pending |
| SD_RETENTION | Reader support and display clearance / insulation | 1 set if needed | Mechanical design pending |

## Remaining work

Before final release: (1) verify SuperMini pinout and fit, display/backlight interface and SD socket stack; (2) select a documented speaker, exact microSD card and remaining harness/mating parts; (3) finish GPIO allocation and audio/motor/SD circuits, then count every resistor/capacitor/driver; (4) agree incoming regulated rails and connector pinout with the power board. Only its interface is needed now, not the completed charger design. Enclosure/battery/packaging are outside this main-board print view and remain in the master kit register. No ERC or prototype qualification has been completed.

[Full register and datasheets](MASTER_BOM.md) · [Printable HTML](MAIN_BOARD_PRINT.html)
