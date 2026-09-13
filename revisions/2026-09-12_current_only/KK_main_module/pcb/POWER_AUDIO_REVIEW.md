# Main-board power and audio review

**Historical pre-C.2 review.** For the corrective placement, MOSFET switch, routing and prototype status, use [the C.2 report](../C2_PROTOTYPE_REPORT.md). The measurements below describe the earlier unrouted board, not the current revision.

2026-09-10. Review of the current single-sheet schematic, freshly exported `review_netlist.xml`, rounded/ground-filled PCB and project routing settings. **Review only: no schematic, PCB, BOM or power-module changes made.** The future power module is explicitly outside this review.

Subsequent footprint update: MOD1 now uses the user's supplied ESP32-S3-SuperMini footprint with signal-labelled pads. The power/audio findings below are unchanged. The earlier note that its row spacing was only assumed is superseded by the supplied footprint geometry; physical stack/fit remains untested.

## Verdict

The checked power/audio connections are coherent, but **placement is not ready to send unchanged to an autorouter**. Several supposedly local components are tens of millimetres from their loads, including parts of the amplifier feedback and output-stability networks. The current packing study needs electrically informed rearrangement and routing constraints. This is a concrete layout problem, not an unresolved shopping list.

No powered test or amplifier transistor-level simulation was performed. Ground connectivity and clean clearance checks cannot establish audio stability or startup behavior.

## Findings, in priority order

### 1. High: regroup the amplifier and its support components

The following are direct pad-centre distances measured in the saved PCB, not routed lengths. Actual routing cannot be shorter.

| Connection | Distance | Required action |
|---|---:|---|
| C25 positive → U3 supply pin 2 | 28.9 mm | Put the 100 µF reservoir beside the amplifier supply/return |
| C26 supply pad → U3 pin 2 | 6.2 mm | Keep this 100 nF bypass close; minimize its complete supply/ground loop |
| C21 negative → U3 feedback pin 5 | 33.3 mm | Put C21 beside U3 pins 8/5, not across the board |
| C22 signal pad → U3 feedback pin 5 | 37.8 mm | Place directly beside that feedback node and local ground |
| C23 signal pad → U3 output pin 1 | 29.3 mm | Cluster C23/R34 at this output |
| C24 signal pad → U3 output pin 3 | 35.7 mm | Cluster C24/R35 at this output |
| R34 → its series capacitor C23 | 23.4 mm | These must form one compact stability branch |
| R35 → its series capacitor C24 | 16.2 mm | Same requirement on the second output |

Long feedback and stability-branch wiring increases susceptibility to coupling and oscillation; it does not prove the amplifier will oscillate. Route the input/filter separately from speaker outputs, motor switching and fast SPI lines. Keep the ground plane continuous while managing where load currents flow; do not arbitrarily split it into isolated analog/digital islands. This is an engineering layout recommendation, not a claim that KiCad DRC checks analog behavior.

### 2. High: put motor suppression at the motor connector

C16 positive → J4 positive is **42.1 mm**. C17 positive → J4 positive is **45.1 mm**. C16 is the 100 nF across the motor; C17 is the local actuator-rail reservoir. Move both into the J4/Q4/D2 group. Keep the diode/motor/switch loop compact, and assess an additional capacitor directly at the actual motor terminals if the cable is long. Do not route the motor's return through the amplifier input reference area.

### 3. High: assign power and audio routing constraints before autorouting

The project currently has only the **Default 0.2 mm track width**, with no netclass assignments/patterns. There is no current-based sizing policy for the three incoming rails, amplifier supply, motor path or speaker pair.

Set explicit widths for those nets based on expected peak current, final copper weight, route length and acceptable voltage drop/temperature rise. Reserve short routes for the local bypass/feedback/stability connections above. A generic 0.2 mm autoroute is not an electrical qualification of the power paths. No numerical current capacity for a hypothetical trace is claimed here.

### 4. Medium: review the amplifier power-switch drive and startup

Current values: Q5 KSP2222ABU, R36 4.7 kΩ, Q6 BC32725BU, R38 100 Ω and R39 100 kΩ. With illustrative VBE = 0.7 V and Q5 VCE = 0.2 V:

- R38 current ≈ `(3.2 − 0.7 − 0.2) / 100` = **23 mA**, while enabled.
- Q5 base current ≈ `(3.3 − 0.7) / 4700` = **0.55 mA**.
- This implies a Q5 collector/base-current ratio around **42**, not a demonstrated low-drop switch condition.
- R38 dissipation is about **53 mW** at that illustrative operating point, not an obvious ¼ W resistor overload.

The nominal drive current is material battery overhead. These assumptions do not prove Q5 saturation or Q6's voltage drop during audio peaks and C25 charging. Review both transistor drive stages against the desired amplifier peak load; choose revised drive values or a suitable THT switch arrangement before calling the power gate qualified. No replacement has been selected or applied in this review. The [KSP2222A datasheet](https://www.onsemi.com/pdf/datasheet/ksp2222a-d.pdf) specifies saturation at particular collector/base currents; its active-region gain must not be treated as a saturation guarantee. See also the [BC327 data](https://www.onsemi.com/pdf/datasheet/bc327-d.pdf).

## Checks that look consistent

- J1 is a four-pin JST-XH input, with separate MCU_5V, GND, LOGIC_3V3 and ACT_3V2 connections. MOD1's own 3V3 output is not tied to the external 3.3 V rail. No charging/regulator circuitry was added to the main board.
- The two GND pours connect the current ground pads; the saved DRC has no remaining GND open connections. Other nets remain unrouted. Future routing requires a refill and a new DRC.
- U3's supply, ground, bridged outputs, grounded second input, C21/C22 feedback network and C23/R34 plus C24/R35 output networks match the topology of the [UTC TDA2822 bridge application, page 4](https://www.unisonic.com.tw/uploadfiles/836/part_no_pdf/TDA2822.pdf). J5 goes between outputs 1 and 3: **neither speaker wire is ground**. The amplifier's specified 1.8–12 V operating range includes the proposed low-voltage supply, but switch drop and output headroom still require checks.
- The audio input contains two RC filtering stages, DC blocking and attenuation. A fresh linear nodal calculation using the current netlist and a 100 kΩ amplifier input load gives −40.46 dB at 1 kHz and −84.33 dB at 200 kHz. That is about 43.9 dB relative carrier rejection, conditional on a 200 kHz carrier. This is passive-network analysis only, not an amplifier/speaker simulation. With nominal 40 dB amplifier gain and a full-range 3.3 V PWM-derived sine, the ideal 1 kHz output would be about 1.57 V peak; actual clipping and speaker power cannot be inferred from that alone. Start with reduced firmware volume and test.
- Q4's source/gate/drain nets and D2's flyback polarity are correct. The [TN0702 datasheet](https://www.microchip.com/content/dam/mchp/documents/APID/ProductDocuments/DataSheets/TN0702-N-Channel-Enhancement-Mode-Vertical-DMOS-FET-Data-Sheet-20005941A.pdf) gives 2.5 Ω maximum at VGS = 3 V, ID = 200 mA, 25°C. Conditional on at least 3 V gate drive and 120 mA starting current, the proposed minimum 3.168 V rail leaves about 2.87 V at the motor. This does not establish hot/cold startup margin or gate-drive guarantees. See the [selected motor specification, PDF page 3](../component_review/datasheets/motor.pdf).

## Other main-board items to close

- C15 is about **57.8 mm** from U2's supply pin. Regroup the receiver's R27/C14/C15 filter. Input-rail and display/SD bulk capacitors also need sensible local placement: C3/C5 are about 28/31 mm from their respective J1 supply pins, C11 about 32 mm from J3's supply and C13 about 30 mm from J2's supply.
- R23 = 100 Ω remains a conservative backlight bring-up value. The actual display BLK circuitry/current must be inspected before selecting final brightness drive. Do not simply short out that resistor.
- J4 motor and J5 speaker use the same two-pin PH connector family. Add clear function labels and harness identification; a keyed plug does not prevent swapping two identical sockets.
- Speaker impedance is specified as 8 Ω in the schematic, but the selected small speaker's continuous power rating is not yet documented. Test volume, differential DC, pops and thermal behavior with the actual speaker.
- The future source must satisfy the interface and safe sequencing/backfeed requirements. Designing that source can wait; none of the placement changes above require redesigning the power module now. Do not connect module USB and external power concurrently until the source paths are qualified.

## Physical fit check without ordering a PCB

1. Print [front](front-fit-check.pdf) and [mirrored rear](back-fit-check.pdf) at **100% / actual size**, not fit-to-page. Confirm the outline's overall width/height is 80 × 100 mm with a ruler. Copper is omitted on these fit sheets intentionally.
2. Lay the actual sockets, module headers, buttons and connectors on the print. Check **all pin centres**, pin-1 orientation, body outlines, latches and cable/card access. Paper alignment is a coarse check; verify hole/lead diameters and tight spacings with calipers and package drawings. Do not force leads to fit an incorrect pattern.
3. Dry-stack the intended sockets and modules over a 1.6 mm mock board/spacers. Check side-on clearance over trimmed rear-component leads, display support, USB access, SD extraction and button-cap travel. A correct 2D hole pattern does not establish stack clearance or insulation.

| Item | Pattern currently drawn |
|---|---|
| SuperMini | Supplied footprint: two rows of 9, 15.24 mm row separation, nominal 2.54 mm pitch; GPIO13 retains supplied 0.04 mm offset |
| Screen socket J2 | One row of 8, 2.54 mm pitch; first-to-last centres 17.78 mm |
| SD socket J3 | One row of 6, 2.54 mm pitch; first-to-last centres 12.70 mm |
| Soft buttons | 8.0 × 4.5 mm between hole centres |

The supplied module photos do not confirm row spacing, header offset or assembled height. Actual samples or controlled mechanical drawings are needed to close those holds. For uncertain contact orientation, perform continuity checks only with the assembly unpowered. No fabrication or functional release is implied by a paper fit check.
