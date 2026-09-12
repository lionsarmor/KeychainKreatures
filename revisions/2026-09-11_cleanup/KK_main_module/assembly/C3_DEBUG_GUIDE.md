# C.3 debug pads and safe measurements

25 bare plated holes: 2.0 mm exposed copper diameter, 0.8 mm drill. No additional component is purchased or installed. TP numbering deliberately has gaps where no useful, clearly labelled site fitted. Coordinates below use the normal PCB editor front-view axes; the rear print is mirrored.

## Access and repair limits

- Probe only from the listed face. Front access may require removing the socketed screen, SD reader or MCU. The carrier does not guarantee access through the finished enclosure.
- These holes have no fitted wire loops or test-point posts. Some lie beneath a component on the opposite face. Do not push a long lead through into that component; keep any repair solder/wire clear of its body and pins. Prefer a surface-soldered insulated wire on the accessible face.
- Pads expose existing nets; they do NOT disconnect miswired traces. Power off before continuity checks or soldering. Correcting a short may still require cutting and verifying a trace.
- Never clip an earth-referenced scope ground to speaker outputs, MOTOR_RETURN, BLK or MOSFET gates. Scope ground clips go only to a GND point. Use differential measurement for the bridge speaker.
- Do not use these as extra power inputs. No raw battery and no USB plus SYS_IN together. Use the coordinated, current-limited source described in the assembly guide.
- MCU TX/RX header positions serve the TFT; they are not a spare debug UART. EN/BOOT remain on the removable MCU. Initial/recovery flashing is performed with that module removed from the carrier.

## Coverage

Supply rails, three GND access points, I2C, button interrupt/function, SPI clock/MOSI/SD-CS, display controls/backlight, audio PWM/filter output, motor return, IR transmit/receive/filtered supply and expander reset. MISO, amplifier VCC/input/enable, speaker outputs and motor gate/enable retain accessible component solder joints; this pass does not claim a separate test hole for every circuit node.

| Pad | Signal | Same net as | Probe face | X, Y (mm) |
|---|---|---|---|---|
| TP1 | 5V | J1:1 | front | 60.00, 49.00 |
| TP2 | 3V3 | J1:3 | back | 58.50, 71.00 |
| TP3 | 3V2 | J1:4 | back | 76.00, 52.50 |
| TP4 | GND-P | J1:2 | back | 66.00, 68.00 |
| TP6 | GND-A | U3:4 | front | 41.00, 35.00 |
| TP8 | GND-M | Q4:1 | back | 61.00, 29.00 |
| TP9 | SDA | MOD1:4 | front | 34.00, 18.50 |
| TP10 | SCL | MOD1:5 | back | 60.50, 23.50 |
| TP11 | KEY-IRQ | MOD1:1 | back | 69.00, 22.00 |
| TP12 | FN | MOD1:2 | back | 71.00, 24.00 |
| TP13 | SCK | MOD1:13 | front | 53.00, 11.50 |
| TP14 | MOSI | MOD1:11 | back | 28.50, 7.00 |
| TP16 | SD-CS | MOD1:10 | front | 53.00, 17.00 |
| TP17 | TFT-CS | MOD1:RX | back | 71.50, 28.50 |
| TP18 | TFT-DC | MOD1:TX | back | 66.00, 25.00 |
| TP19 | TFT-RST | U1:7 | back | 28.00, 12.50 |
| TP20 | BL-PWM | MOD1:9 | back | 55.50, 9.00 |
| TP21 | BLK | J2:8 | front | 51.00, 62.50 |
| TP22 | AUD-PWM | MOD1:8 | front | 53.50, 26.50 |
| TP23 | AUD-LP2 | R31:2 | front | 46.00, 56.00 |
| TP29 | MOT-RET | J4:2 | front | 72.50, 42.50 |
| TP30 | IR-TX | MOD1:7 | back | 66.00, 28.00 |
| TP31 | IR-RX | MOD1:6 | back | 52.50, 8.50 |
| TP32 | IR-V | U2:3 | back | 14.50, 12.00 |
| TP33 | IO-RST | U1:18 | front | 21.00, 24.50 |

## Expected observations

TP1: nominal 5 V. TP2: nominal 3.3 V. TP3: nominal 3.2 V. Ground points read near 0 V relative to J1 pin 2. TP32 is the IR receiver supply after its series resistor, slightly below the logic rail depending on load.
Logic pads use 3.3 V signaling; activity and idle states depend on firmware. TP23 carries filtered, DC-biased audio, not a speaker output. TP29 is the switched motor return: not a permanent ground. Do not infer a working firmware protocol from a DC meter reading.

## CAD review exception

The C.3 custom courtyard rule applies only to bare TP footprints. KiCad normally assumes a physical lead passes through every plated component hole; that assumption does not apply to these unpopulated probe holes. Opposite-face body intersections are deliberately allowed, while copper, drill, mask and edge clearances remain enforced. Never populate these holes with posts or loops without a new mechanical review. No general DRC category was disabled for this addition.
