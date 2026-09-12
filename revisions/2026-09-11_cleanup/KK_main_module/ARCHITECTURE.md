# Compact architecture — current candidate

2026-09-10. Current requirements are in [DESIGN_BRIEF.md](DESIGN_BRIEF.md); parts, GPIO numbers, schematic and mechanical outline are not released. Latest [component decisions](COMPONENT_DECISIONS.md) approve a THT-pin regulator module, relax the fixed screen and recommend 16 MB flash/8 MB PSRAM plus wired speaker/ERM candidates. These supersede earlier candidate assumptions below, not qualification gates.

## Hardware partition

RODDY power PCB → reviewed main-board 3.3 V regulation → compact ESP32-S3/PSRAM core. Separate TFT, battery, speaker and motor have defined connectors/retention rather than being assumed part of the MCU module. Charger/protection stays on RODDY. No separate sub-GHz radio or expansion connector is reserved.

Mandatory assembly strategy: **through-hole-only main PCB for student assembly**, including a preassembled ESP32-S3/PSRAM module attached by legs/pin headers or THT sockets. The former proposal to factory-place a fine-pitch MCU/regulator section directly on the main PCB is withdrawn. No required signals may rely on student soldering to hidden underside/SMD pads. Audio, GPIO, IR and haptics use THT circuitry, not assumed extra breakouts. Regulation remains a qualification gate; no bare SMT regulator on the main PCB and no unapproved power-board redesign. See [student-kit requirements](STUDENT_KIT_REQUIREMENTS.md). Start with two-layer routing and sensible ground continuity; layer count cannot excuse an assembly-method violation.

- Display: separate affordable SPI color module; diagonal and resolution are now open. SPI clock/data/CS/DC, reset and controlled backlight remain the interface starting point. Exact backlight circuit, supply requirements and connector remain open.
- Buttons: four directions, A/B/X/Y and Function. First compare direct GPIO for all nine against PCF8574N DIP-16 for eight plus direct Function/wake. Avoid adding the DIP expander if the selected core has sufficient GPIO and direct routing fits better.
- Candidate PCF8574 map: P0 UP, P1 DOWN, P2 LEFT, P3 RIGHT, P4 A, P5 B, P6 X, P7 Y. Write all ones before input use (quasi-bidirectional port), run at ≤100 kHz, apply external pulls as needed, poll every ~2 ms during play and debounce per measured switches. Do not spend any of these eight bits on IR or status. Verify all simultaneous-button combinations. Source: [TI PCF8574](https://www.ti.com/lit/ds/symlink/pcf8574.pdf). The DOCX's MCP23008-E/P PDIP-18 remains a separate candidate; its register/reset/interrupt behavior is different. Compare before selecting an expander; do not treat these devices as drop-in equivalents.
- Function connects directly to a verified wake-capable, non-strapping pin with a defined idle bias. Only Function wake is initially promised. Expander INT is optional notification, not timestamped capture. [S3 sleep/wake documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/sleep_modes.html).
- For the MCP23008 alternative, define RESET/address pins and pull-ups explicitly. Its interrupt-capture register holds a port snapshot until cleared; it is not a timestamped pulse queue either. Verify any-button wake sequencing independently. [Microchip datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP23008-and-MCP23S08-Data-Sheet-DS20001919.pdf).
- IR receiver: direct MCU RMT capture, filtered supply, correct carrier/protocol. IR LED: RMT-controlled current-limited transistor driver. Both shut down safely at idle; emitter off through reset.
- Audio: qualify a DIP-8 low-voltage amp with filtered PWM input. NJM2073D is an obsolete-stock experiment; HT82V739 DIP is a sourcing/bench candidate, not an approved drop-in. Keep room for THT filter/bias/bulk components. Any alternate conversion/amplifier path must meet the THT requirement; do not adopt bare SMT I2S audio as a fallback.
- Haptics: driver chosen for actual ERM or LRA actuator. ERM needs flyback handling and stall-current limit; do not apply the same circuit blindly to an LRA.
- Battery/status: protected sensing and level conditioning; never direct J5-to-MCU wiring. RODDY hard switch remains distinct from Function sleep/wake. Details: [POWER_INTERFACE.md](POWER_INTERFACE.md).
- Programming: prefer the preassembled processor module's USB port or a THT service header with EN/BOOT/recovery access. Do not add an SMT USB receptacle to the main PCB. No second charger or uncontrolled USB power connection; review the module's regulator input/output and powered-off paths rather than blindly driving a rail backward.

The [functional I/O budget](io_requirements.csv) totals 20 direct functional signals with a single-PWM audio path and button expander, before optional expander INT. Native USB adds two fixed pins; UART recovery adds two if retained. Three-wire I2S adds two signals versus single PWM. Direct nine-button wiring adds six net signals compared with I2C + Function, while removing the expander. This count intentionally keeps status, shutdown and resets independent; some could be consolidated after a circuit-level review, not guessed away to fit a tiny development board.

Select final GPIOs only against the exact module's flash/PSRAM occupancy, boot straps, USB mapping and exposed pads. The archived WROOM map is not compatible evidence for a new core. Preserve antenna keepouts in all three dimensions including display metal, battery, adjacent board and keyring.

## Software and memory

Firmware owns the launcher, pet state, input, display, audio, time, power and trading. Original games use a small stable C host API. Do not make Game Boy ROM emulation part of the acceptance criteria.

Store app packages/assets in a filesystem separately from protected/versioned pet saves and settings. Install to staging, validate ID/API version/checksum/size, then atomically activate using a recoverable manifest. Apply quotas and preserve old package or recovery metadata through interrupted updates. Add authenticity/signature policy before accepting untrusted network packages.

Prototype separately installable C-compiled WebAssembly apps using a narrow host API; benchmark one scrolling game with sampled audio before choosing the runtime and flash capacity. [ESP-WASMachine](https://github.com/espressif/esp-wasmachine) is an experimental starting point, not proof of a finished safe app platform. Arbitrary native C binaries cannot simply be copied into a filesystem and executed. Restrict host imports, filesystem access, memory and execution time; pet ownership stays firmware-owned.

One RGB565 full framebuffer is 240 × 280 × 2 = 134400 bytes; two are 268800 bytes. At 30 full frames/s the raw pixel payload is 32.256 Mbit/s, excluding command/transfer overhead. Use partial updates, bounded frame rates and sprites to save power. Keep DMA buffers in memory supported by the chosen driver; PSRAM presence does not make every buffer DMA-compatible.

Aim for 8–16 MB flash and ≥2 MB PSRAM where compact implementation permits. The MINI-N4R2 actually has only 4 MB flash. Do not issue a partition table until firmware/runtime builds establish space for update/recovery, pet data and several realistic games. Extra SPI storage is not free in area, power or GPIO; microSD is not assumed.

## Trading and power behavior

Use paired encrypted ESP-NOW for nearby trading with on-screen consent and a compatible Wi-Fi channel. Built-in radio remains despite rejecting sub-GHz. The radio's send callback is not proof that the other application saved a transfer. Source: [Espressif ESP-NOW](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/network/esp_now.html).

Persist transaction/peer/pet IDs and state digests; lock offered pets before commit. Durably record received commits before application acknowledgement. Make retries idempotent and resume reconciliation after power loss. Do not unlock an in-doubt pet merely on timeout when the peer may have committed. Test interruption at every step. This addresses ordinary failures, not cheating by modified firmware or restored flash snapshots.

Keep simulation event-driven; checkpoint meaningful changes instead of every frame. Disable backlight, audio, haptics and IR at idle, bound wireless windows, and prevent back-powering switched-off peripherals through GPIO. Deep sleep while powered can preserve timekeeping; elapsed real time through a hard disconnect needs an independent RTC or later time sync. No always-on RTC is currently included.

## Implementation gate

Latest workflow: actual component envelopes and exact part/circuit qualification → trial board placement, control ergonomics and stack clearances → final board outline/placement and schematic review → routing → ERC/DRC and assembly review → mechanical handoff for the user's shell modeling → physical integration tests. See [board-first plan](BOARD_FIRST_PLAN.md). Full enclosure CAD is no longer a prerequisite for board work. Unresolved power-path capacity and battery-life targets remain gates. No step is represented as completed simply because a preceding document exists.
