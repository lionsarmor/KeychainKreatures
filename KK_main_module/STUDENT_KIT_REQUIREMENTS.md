# Mandatory through-hole student-kit requirements

2026-09-10, latest user clarification. Integrate power functions onto the student-assembled main board with through-hole parts. The existing separate power project is excluded from this revision and remains unchanged. Through-hole assembly takes priority over the earlier board-size target. See [integrated power revision](INTEGRATED_THT_POWER_REVISION.md).

## Assembly boundary

- **Every component mounted directly on the main PCB must use through-hole leads/pins.** No factory-populated SMD island on the main board; no student SMD work, reflow, exposed-pad soldering or underside-pad jumpers.
- **ESP32 is a complete preassembled module with legs**, connected through plated holes or THT sockets on the main board. SMD parts inside this module are not student assembly tasks. A bare castellated/LGA RF module is not a compliant substitute by itself.
- Charging, battery protection, power routing and regulation now belong on the main PCB using THT parts; a complete safe implementation is not yet qualified. Display and ESP32 remain preassembled modules; battery remains connectorized. Speaker and motor remain electromechanical parts with suitable connections. Do not require students to solder directly to LiPo cell tabs.
- The earlier regulator-breakout permission is superseded by the new request. No extra SMD charger/regulator board or hidden main-board SMD island is authorized. Any necessary exception must be explained and explicitly agreed before adoption.

## Component qualification gates

| Block | Required implementation | Still to verify |
|---|---|---|
| ESP32-S3 + PSRAM | Compact preassembled pin-header module; prefer 2.54 mm pitch and replaceable THT sockets | Exact flash/PSRAM, usable header GPIO, straps, supply path, antenna, socket height, current and sleep behavior |
| GPIO expansion if needed | Actual PDIP part and THT socket | Exact order suffix, voltage, input/wake behavior and source availability |
| Audio | Actual THT low-voltage amplifier and THT filter/support components | Qualified supply, clean output into chosen speaker, shutdown and sourcing; no bare MAX98357A on main |
| IR / haptic / backlight drivers | Suitable leaded transistors/MOSFETs, diodes, resistors and capacitors | Current, drive strength at MCU voltage, losses, transient handling and real lead order |
| Buttons / indicators | THT switches, LEDs and IR receiver/emitter | Actual footprint, force/travel, polarity and lead order |
| Connectors / service access | THT headers, sockets or leaded connectors | Mating polarity, locking/keying, accessibility and assembled height |
| Charging, protection, regulation and sensing | Actual THT components on the main PCB; no separate regulator/charger module | Full charge-safety design, cell qualification, regulation/headroom, current budget, thermal limits and one-port USB isolation remain unresolved |

Do not infer package compliance from a generic part family name. Every eventual BOM line must specify exact manufacturer part number, package, footprint, assembly owner and sourcing status. Distinguish `STUDENT_THT`, `PREASSEMBLED_ESP_MODULE`, `PREASSEMBLED_RODDY` and other external assemblies. Exclude `MAIN_BOARD_SMD` entirely. No exact BOM is released yet, so this is a selection/release gate, not a claim that all parts are already qualified.

## Student assembly and verification

- Prefer standard-pitch, accessible joints; generous pads/spacing appropriate to each lead, visible polarity/orientation markings and readable reference designators. Do not pack parts so tightly that students cannot inspect or rework them.
- Socket DIP ICs and the processor module where practical; include actual socket/lead heights in the stack. Provide clear module orientation and prevention of one-row-offset insertion where feasible.
- Use keyed or unmistakably labeled connections, insulated battery retention, strain relief and no sharp lead/screw contact with the battery.
- Supply an illustrated staged assembly guide: low parts first, polarity checks, unpowered continuity/short checks, supervised current-limited first power-up, then modules/peripherals and a functional self-test. Battery remains disconnected during soldering and inspection.
- Final release checks include a footprint/package audit, no SMD footprints directly on the main PCB, accessible module pins for every required net, and a representative student assembly trial. ERC/DRC alone do not establish kit suitability.

The provisional 50 × 65 mm board size is no longer a target to enforce. Establish an outline after the integrated THT power solution, legged module and sockets are qualified. Preserve comfortable handheld intent, but do not conceal an SMD substitution to meet the earlier dimensions.
