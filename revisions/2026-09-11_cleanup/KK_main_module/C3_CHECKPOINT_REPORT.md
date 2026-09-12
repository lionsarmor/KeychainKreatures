> Historical checkpoint, superseded by the approved 80 × 115 mm [C.3 RGB prototype report](C3_PROTOTYPE_REPORT.md). The pending size decision below is resolved; do not use this report as current build status.

# C.3 — debug pads, assembly markings and connector access

Status: checked engineering-prototype checkpoint, **not a fabrication release**. RGB layout is awaiting the user's board-size choice. No power-board changes or fabrication orders were made.

## Applied to the root project

- 25 bare plated test points, 2.0 mm copper / 0.8 mm drill. Three are GND points. They cover power, controls, display/SD buses, audio filter/PWM, motor return and IR. See the [map and measurement precautions](assembly/C3_DEBUG_GUIDE.md).
- 25 short tap tracks, longest 3.44 mm; all 840 existing track segments and 24 vias retained. The board now has 865 segments, 24 vias, 316 plated holes including vias, and four mounting holes.
- Added silkscreen TP identifiers, pin-1 marks at ICs/connectors/transistors, cathode marks, IR TX/RX identification, USB-end identification and connector pinout legends. Existing capacitor +/hatched-negative marks, diode bands, transistor flats, IC notches and component reference labels remain. The supplied MCU footprint is unchanged.
- J1 is the four-pin regulated-power input: 1=5 V, 2=GND, 3=3.3 V, 4=3.2 V. It was already top-entry, not a side-entry battery connector.
- J4 is the motor and J5 the bridge speaker. Both now use **B2B-PH-K-S(LF)(SN)** top-entry through-hole connectors, replacing inward-facing S2B parts. Existing PHR-2 plugs and crimp terminals still apply. J5 moved 0.25 mm left to clear C24; all other original components retain their positions.

## Checks and remaining physical limits

Fresh KiCad ERC: 0 violations. DRC: 0 unresolved violations, 0 unconnected items. Schematic parity: 0 issues. Native verification confirms the original copper was retained and the added pads are on their specified nets. Reports are in `pcb/c3_final_*.json` and `pcb/C3_FINAL_VERIFICATION.json`.

The [updated rear 3D view](pcb/c3-back-3d.png) was inspected for the connector direction and visible assembly labels. It shows connector bodies, not the complete mating plugs, wire harness or final shell.

A scoped courtyard rule permits **unpopulated TP holes only** under an opposite-face component body. This does not disable electrical, hole, mask or board-edge checks. Do not fit test posts/wire loops through those holes. The map specifies the accessible probe face; modules may need to be removed for front-side access. Debug pads do not isolate a bad net automatically: trace cuts may still be required for a repair.

The top-entry PH connector's nominal mated height is about 8 mm above its mounting face, per the [JST drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf). Allow additional rear clearance for wires, gentle bends, fingers/tools and strain relief. J1 also needs rear insertion access. Board courtyards pass, but no final shell or mating harness has been physically tested. Do not claim a verified enclosure fit from the connector-only 3D model.

J4/J5 plugs are physically interchangeable: label their harnesses MOTOR and SPEAKER. Speaker minus is **not ground**. Existing power sequencing/backfeed, speaker rating, motor startup, display backlight, thermal, RF and firmware qualification requirements still apply.

## RGB proposal — approved feature, pending layout decision

D1 is the TSAL6200 940 nm infrared transmitter and remains unchanged. A separate diffused RGB lamp is proposed:

| Ref | Proposed part | Function |
|---|---|---|
| D3 | Kingbright WP154A4SEJ3VBDZGW/CA | 5 mm diffused RGB, common anode; 1=red cathode, 2=common anode, 3=blue cathode, 4=green cathode |
| U4 | TI TLC5916IN, PDIP-16 | Socketed constant-current driver; 3.3 V logic, LED anode on 5 V |
| R40 | MFR-25FBF52-1K8, 1.8 kΩ | About 10.4 mA/channel default current; low-current mode can reduce brightness |
| R41 | MFR-25FBF52-10K, 10 kΩ | Output-disable pull-up |
| C27 | C315C104K5R5TA, 100 nF | Local driver bypass |
| Additional | 16-pin narrow DIP socket, exact purchase selection pending | Student-friendly replacement/service |

The proposed schematic passes ERC. The new components are **not** installed in the root PCB or included in its checkpoint BOM. The attempted 80 × 100 mm RGB placement was rejected and remains explicitly unrouted/unqualified in `routing/`.

Pending question: permit a **15 mm bottom extension (80 × 115 mm)** for an uncluttered through-hole RGB assembly area, or retain 80 × 100 mm and defer RGB? The extension has not been applied. Exact placement/routing and the socket purchasing selection follow that decision.

The RGB driver uses spare MCP23017 GPA4=DATA, GPA5=CLK, GPA6=LATCH, GPA7=OE_N; it does not consume an ESP32 strapping pin. Firmware must blank outputs, initialize the shift register/latch and select brightness before enabling. Basic RGB combinations and global brightness control are supported; smooth independent-channel fades are not automatically provided by this hardware. The proposed RGB footprint requires supervised lead forming from the LED's 1.27 mm pitch to the 2.54 mm assembly jig pitch; sample fit remains to be tested.

Primary documentation: [RGB LED drawing](https://www.kingbrightusa.com/images/catalog/SPEC/WP154A4SEJ3VBDZGW-CA.pdf), [TI driver datasheet](https://www.ti.com/lit/ds/symlink/tlc5916.pdf). Both were downloaded to `component_review/datasheets/`.

## Handoff

Use the root project for the checked debug/connector board and the C.3 checkpoint BOM for its component selections. Manufacturing is held until the RGB size decision, final layout and repeat checks. The old C.2 fabrication package is archived, not current. Reload KiCad from disk before editing to avoid overwriting changes from a stale IDE tab.
