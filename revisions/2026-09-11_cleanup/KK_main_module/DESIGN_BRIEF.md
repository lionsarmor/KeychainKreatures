# Current design brief — 2026-09-10

Source: user-designated request in attachment `f7efe836-a9ef-45ee-9e2b-540e9a3c1718/pasted-text.txt`, read in full, amended by the subsequent user request to size a comfortable compact board first and model the shell around it. Requirements below are design inputs, not claims of achieved performance. See [board-first plan](BOARD_FIRST_PLAN.md).

## Product and mechanical constraints

- Brand RODDY.WORLD; product KEYCHAIN KREATURES. Friendly virtual pet with original games, utilities, downloadable content and creature communication/trading.
- Small handheld-toy size with rounded rectangular mini Game Boy / Dreamcast VMU proportions; no egg silhouette or direct clone. Screen above controls, restrained late-80s/90s technical typography. Gray, black, translucent purple and clear are possible finishes; visible/understandable PCB in DIY version. The earlier strict Giga Pet-size requirement is relaxed, not replaced by unlimited growth.
- Earlier **46 × 62 × 19 mm** shell and **19–20 mm** maximum depth are superseded as hard constraints. Prioritize comfortable controls, repairable assembly and an appropriately small handheld toy. Final shell dimensions follow the component stack and board; avoid unnecessary growth.
- Engineering starting proposal: main PCB **50 × 65 × 1.6 mm**, approximately R4 corners, with mounting provisions. This is a trial placement envelope, not a user-approved final dimension or a demonstrated fit. Four M2-class mounting points if practical; account for boss space, walls and tool access while arranging the board.
- Separate affordable color TFT; the user relaxed the 1.69-inch/240 × 280 requirement. Larger displays are permitted if suitable for a small handheld; choose resolution for readable creature art and mini games. Exact display remains open. See [component decisions](COMPONENT_DECISIONS.md).
- Exactly **nine digital gameplay inputs**: four D-pad directions, A/B/X/Y, one centered Function/Menu/Home button. Cross-shaped D-pad lower left; four distinct action caps lower right (X/Y above A/B); Function centered below. Hard power switch separate. Ergonomic refinement allowed, not removal of buttons.
- Battery: separate MakerHawk 102050, 1S LiPo, nominal 3.7 V / 1000 mAh / 10 × 20 × 50 mm. Real protected-pack dimensions, lead exit and connector must be measured.
- RODDY power PCB stays separate, approximately 40 × 30 mm, two layers. Preserve USB-C, MCP73871 power path/charging, DW01A/FS8205 protection, thermistor, battery connector, switch and status architecture. Minor connector location/orientation or outline refinement only when justified by fit; no convenience redesign.
- Initial order is display → main PCB → power PCB → battery → rear cover, but offset/nested arrangements are allowed. Do not assume a simple four-layer stack fits.
- Verify exact display, battery, connectors/mated cables, cap travel, speaker, actuator, mounting provisions and antenna clearance before finalizing the board. Full shell CAD is no longer a prerequisite; retain a simple stack/clearance model and give the user mechanical constraints for their shell design.

## Electronics and software

- ESP32-S3 with PSRAM on a **preassembled compact module with through-hole legs/pin headers**, preferably socketable. No bare SMT MCU/RF module mounted directly to the main board. The previous large WROOM default is withdrawn; “Super Mini” is not an exact part specification.
- IR transmit and receive; **no added sub-GHz transceiver**. Built-in ESP32 wireless remains available for trading.
- Keep actual small **8-ohm speaker**, melodies/music, sound effects and simple sampled audio; no piezo-only substitution. NJM2073D DIP-8 is a candidate to evaluate, not mandatory. Prefer a better through-hole alternative if needed and verified.
- Keep haptics; no existing motor or speaker must be retained. Compact wired speaker and simple ERM motor candidates are recorded in [component decisions](COMPONENT_DECISIONS.md); drivers and physical performance remain unqualified.
- Approved additional assembly exception: preassembled regulator module with THT pins on the main board. Final kit remains through-hole. Recommended memory target is 16 MB flash/8 MB PSRAM, subject to compact module cost, accessible GPIO and power qualification; not an exact processor selection.
- **Mandatory student through-hole assembly:** all components mounted directly to the main PCB must have THT leads/pins, including the processor module's connection. No SMD parts on the main PCB, even factory-populated ones. SMD inside the preassembled ESP32 module and separate RODDY/display assemblies is outside student soldering. Additional module exceptions require an explicit decision. See [student-kit requirements](STUDENT_KIT_REQUIREMENTS.md). Justify footprint growth using actual THT parts, sockets and accessible joints.
- Original games/apps, not original Game Boy ROM compatibility. Aim for separately installable/updatable app packages, a filesystem/loader, persistent pet/user data and adequate storage. Do not promise arbitrary native binary compatibility.
- Target about one week of normal, mostly sleeping pet use and several hours continuous screen-on play. Aggressively disable backlight, audio, vibration, IR and unused peripherals at idle. Runtime requires measurement under a defined usage profile.

## FDM enclosure and release gates

- Design for FDM from the start: obvious flat print faces, minimal supports, no major visible support scars or coarse stair-stepping. Prefer removable cosmetic front plate printed bed-down, midframe, rear cover and optional separate bezel.
- Separate D-pad, four action caps, Function cap, and possibly a replaceable keyring attachment. Screws/snaps instead of glue; replaceable shell pieces. No injection-molding assumptions.
- Prototype/DIY architecture, quality, battery life and repairability take precedence over an invented retail price. Provide estimated electronics BOM, PCB/assembly cost, cost outliers and later savings.
- **Board-first workflow:** establish actual component envelopes, comfortable controls and stack/connector clearances; finalize board outline/placement and reviewed circuitry, then routing and verification. The user will model the shell around the finalized board using supplied mechanical drawings/3D data. No finished enclosure CAD is required before board work. Physical assembly tests remain necessary before any manufacturing-readiness claim.
