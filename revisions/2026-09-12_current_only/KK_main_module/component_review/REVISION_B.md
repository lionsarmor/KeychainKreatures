# Revision B — socketed SuperMini, separate power, wireless software

**Superseded circuit status:** [revision C](../schematic/README.md) now contains an actual five-sheet KiCad capture, working GPIO allocation and a proposed three-rail external power interface. Use that capture for ongoing circuit work; the earlier TBD pin tables below are historical. Revision B's user-selected modules and separate power-board ownership remain unchanged.

**Latest storage amendment:** retain the XIITIA 240 × 280 screen and add the user-selected **Amazon B0F82XWT4F microSD module**, preferably under the screen. It is now a permitted preassembled header-connected part. See [SD integration and assembly plan](SD_STORAGE.md). Onboard-flash capacity limits below still apply to firmware/OTA, but game assets can now live on the separate card.

2026-09-10. Current user-directed architecture; supersedes revision A's Waveshare selection and integrated THT charging requirement. Main-board design may proceed at block level; this is not a fabrication release.

## Scope now agreed

| Item | Current baseline |
|---|---|
| MCU | ESP32-S3 SuperMini; assume original Teyleten Robot Amazon B0D47HBFDY pending delivered-board checks |
| Mounting | Two nine-way 2.54 mm THT sockets, Sullins PPTC091LFBN-RC candidate; verify sample fit |
| Main PCB | THT student assembly: expander, nine soft buttons, display connector, IR, audio, haptics, sockets, signal conditioning and supply interface |
| Power PCB | Reuse the user's power-board design as the starting point for a **future revision** with suitable regulation; charging, battery protection and associated cell sensing live there |
| Power boundary | SYS_IN and GND; voltage/current/connector contract below is proposed, not yet qualified |
| Software transfer | Browser over Wi-Fi; OTA firmware and game package uploads are separate software functions |
| Trading | Device-to-device wireless; no computer or USB required for routine use |
| USB | Retain module USB, BOOT and RESET for initial programming and recovery; future power-board USB data is optional for routine wireless operation |
| Unchanged | Screen choice, soft controls, IR-only remote hardware, no sub-GHz hardware; battery dimensions may follow board placement |

The existing `KK_power_module` circuit/layout has **not** been edited or requalified. Permission to make a later revision does not make the existing output regulated or safe to connect to any new input.

## Proposed SYS_IN contract — freeze before routing

**Latest ownership decision:** all added voltage regulation, including the 3.0 V motor regulator, moves to the power board. The main PCB retains only supply distribution, local decoupling, signal/actuator drivers and suppression. Accordingly the earlier single regulated 5 V input proposal below is **reopened**, not a frozen two-wire interface: the power board may need to supply multiple rails. The screen/SD require regulated 3.3 V, the selected motor requires a qualified supply in its 2.7–3.3 V range, and the exact SuperMini input route needs verification. Define rail values/current and connector pins before routing; do not feed the complete main board from 5 V alone and assume the small MCU regulator powers everything. No power-board redesign is being undertaken now.

- Working target: **regulated 5.0 V, ±5% at the main-board connector**, separate GND return. Not a raw 1S cell and not a guarantee that existing SYS_OUT matches this range. A 3.3 V SYS_IN architecture is an alternative only after the exact module's regulator isolation is qualified; never substitute it by name alone.
- Working source-capacity target: 1 A continuous with stable transient response. This is an engineering budget, not a measured load or certified rating; recalculate from actual screen, Wi-Fi, speaker, motor startup/stall, IR and rail-conversion losses. The battery path, protection, switch, connectors, wiring and regulator must all support it. Check power dissipation and runtime, not just current rating.
- Main-board rail distribution and local bypass remain design tasks. Do not assume the tiny MCU regulator can supply every peripheral. All additional rail generation belongs to the power board; maintain short local return paths and decoupling at main-board loads.
- Future power board owns battery undervoltage cutoff, charging safety and source selection. Proposed PG/low-battery status signals, if used, must be 3.3 V-safe and safe when either board is off. They are optional signal-interface requirements, not connections to unconditioned old status nets.
- Select the exact keyed THT input connector, polarity, wire gauge, local capacitors, reverse-polarity behavior, input current protection and service-source isolation before PCB routing. Avoid actuator/battery connector interchangeability.
- Until source isolation is proven, **disconnect SYS_IN before plugging in the SuperMini USB**. Leave module B+/B− pads unconnected; do not parallel its possible onboard charger with the separate power board. Do not apply external 3.3 V to an unqualified regulator output.

Deferring the power PCB removes charger design from the main-board work queue; it does not remove the need for this electrical interface agreement before fabrication.

## Browser workflow — feasible, firmware still to be written

Recommended first implementation:

1. User selects a Connect/Install mode on the toy. It joins a configured 2.4 GHz home network, or creates a password-protected local access point.
2. A phone/computer opens the toy's local web page. Provide a displayed address as a fallback; automatic captive-portal/mDNS discovery is a convenience, not a guaranteed cross-platform requirement. Local AP use does not require internet.
3. The page lists installed content and lets the user upload a compatible package, remove a game, or back up saves. Stream uploads to bounded storage, rather than buffering whole files in RAM.
4. The toy checks package size, format, target hardware, compatibility, integrity and authorization before activation. Use staged writes and an atomic activation record so an interrupted upload does not destroy existing games or saves.
5. A separate firmware-update action writes an inactive OTA application slot, validates it, then reboots. Confirm health after boot and configure rollback if the new build fails. Reject writes with inadequate power/storage; do not enable firmware update mode during a pet trade.

Espressif supplies the building blocks, not the finished product UI: [HTTP server and file-serving examples](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/protocols/esp_http_server.html), [Wi-Fi capabilities](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf), and [OTA APIs, partition requirements and rollback](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/ota.html).

Use a unique device password or physical pairing confirmation, an explicit update mode, strict upload bounds and trusted/signed firmware. Do not expose an unauthenticated flash endpoint to the whole network or internet. Device-hosted pages avoid depending on a public website's permission to contact private-network devices. A cloud game catalog is optional, not needed for the first local workflow. Turn Wi-Fi off outside connection/trading windows as practical for runtime.

## Memory and C applications

The earlier photo appears to show **ESP32-S3FH4R2**, which Espressif specifies as **4 MB flash and 2 MB PSRAM**. This is smaller than the abandoned N16R8 baseline. Verify actual chip markings, flash capacity and PSRAM detection on each accepted seller revision. The NOLOGO reference board is not proof of Teyleten wiring; its prose also contains processor-spec errors, so use Espressif for silicon facts. [Espressif datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf).

Four megabytes can support a deliberately small pet/game system, but available game storage depends on the measured firmware build, web UI, two OTA slots, metadata and saves. PSRAM is working memory, not persistent game storage. Do not promise the previous 8–16 MB storage target or freeze partition sizes before a representative build fits.

Uploading an arbitrary `.c` file or desktop executable does **not** make it runnable on the toy. Separate the transfer mechanism from execution:

- Simplest C-first milestone: compile the game into a complete compatible firmware build, then upload it through the browser's OTA page. This replaces firmware, not an independent game file; preserve the save partition and validate schema compatibility.
- Swappable library milestone: define a game runtime/API and versioned package format. C-authored games can target an explicitly chosen bytecode/VM runtime, or a carefully designed native loader. Neither is automatic; runtime footprint and performance must be demonstrated on the actual 4/2 MB board. An untrusted native game is not sandboxed merely because it arrived as a package.

Retain offline initial/recovery programming through the module USB and accessible BOOT/RESET. A failed Wi-Fi configuration, full storage or broken updater must not require discarding the toy. A removable socketed module makes service possible without a second user-facing data port.

## Pet trading

Recommend investigating **ESP-NOW** for nearby toy-to-toy trading; it uses the ESP32 radio directly without a Wi-Fi router. A browser cannot speak ESP-NOW directly, so the browser upload path remains ordinary Wi-Fi/IP. BLE or ordinary Wi-Fi are alternatives. [Espressif ESP-NOW documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/network/esp_now.html).

Implement physical confirmation on both toys, paired/encrypted communication, unique trade IDs, application-level acknowledgments, persistent pending/committed records and reconnect recovery. Radio delivery alone does not guarantee that a pet is transferred exactly once or that a counterparty is trustworthy. Avoid simultaneous home-Wi-Fi/ESP-NOW complexity initially; channel coordination and battery cost require testing.

## What changed in the circuit records

- [Master component table](MASTER_BOM.md) now selects SuperMini/nine-way sockets. Former integrated charging/power rows are zero on the main PCB and deferred, not approved parts for the future power board.
- **All former Waveshare GPIO/header assignments are withdrawn.** The SuperMini has fewer exposed pins; bottom-only pads are not student-accessible THT signals. A new GPIO budget must move slow resets/enables to the MCP23017 where appropriate while keeping SPI, audio PWM and IR timing directly on the MCU. Continue respecting GPA7/GPB7 output-only restrictions.
- [Connection CSV](STARTER_CONNECTIONS.csv) retains the expander/buttons/IR logical topology, but MOD1 ports are explicitly logical, with no physical pad assignment. Their resistor/capacitor counts are retained design subtotals, not a ready-to-wire SuperMini circuit.
- [GPIO CSV](GPIO_ALLOCATION.csv) explicitly marks assignments TBD. [Revision A circuit notes](CIRCUIT_START.md) remain historical only. No new physical pinout, KiCad capture, USB data routing or firmware is claimed implemented.
- Next main-board work: inspect the actual SuperMini headers/supply circuitry, finish the smaller pin budget and rail interface, then complete display/audio/motor circuitry and schematic capture. Future power-board USB D+/D− routing must be assessed separately: on some SuperMinis native USB GPIO19/20 are not exposed on the normal header legs. Do not promise that adding data wires to the power board alone solves the connection.
