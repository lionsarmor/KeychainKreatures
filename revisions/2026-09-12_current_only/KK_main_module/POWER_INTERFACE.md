# Main module connection to the existing power board

**Current revision B:** the user has reauthorized the separate power board and a future revision adding suitable regulation, with possible USB data. Focus now is the SuperMini main PCB with SYS_IN. See the [proposed electrical contract](component_review/REVISION_B.md). The old board has not been modified or requalified; its SYS_OUT must not be assumed to equal regulated SYS_IN. The extracted facts below describe the existing board, not a released new interface. Older paragraphs requiring an unchanged power architecture or a main-board USB connector are superseded.

Extracted from the current PCB pad/net assignments on 2026-09-09. Connector pin numbers are authoritative; wire colors are not.

| Existing power-board connector | Pin | Net | Main-board treatment |
|---|---|---|---|
| J3 SYS OUT | 1 | /SYS_OUT | Main input to local 3.3 V regulator |
| J3 SYS OUT | 2 | GND | Main ground |
| J5 STATUS | 1 | /PG | Conditioned active-low power-good input |
| J5 STATUS | 2 | /STAT1{slash}LBO | Conditioned status input |
| J5 STATUS | 3 | /STAT2 | Conditioned status input |
| J5 STATUS | 4 | GND | Signal reference |
| J5 STATUS | 5 | /VBAT | Battery sense only through a reviewed sensing circuit |
| J4 BAT_TEMP | 1 | /THERM | Battery thermistor; keep with battery/power assembly |
| J4 BAT_TEMP | 2 | GND | Thermistor return |
| J2 BATTERY | 1 | /VBAT | Remains connected to battery positive |
| J2 BATTERY | 2 | /BAT_NEG | Remains connected to battery negative |

Do not bridge BAT_NEG to main-board GND: they are separated by the battery-protection circuit. The main board must receive power from J3, not directly from J2.

SW1 on the power board connects /SYS to /SYS_OUT. It already performs the system power disconnect. A main-board wake/sleep button has a different role from this hard switch.

The notes' older switch arrangement is superseded by their updated ODT arrangement and the actual PCB. The ODT's generic 3.0–4.2 V charger-output estimate does not cover the MCP73871 system output when USB supplies the load.

The PCB ties U1 SEL low and PROG2 to VBUS, selecting 500 mA USB mode. R5 is 3.3 kOhm on PROG1, corresponding to a nominal 303 mA programmed fast-charge setting, subject to available supply and thermal conditions. The system load takes priority and charging is reduced as needed; the battery can supplement system demand. These are circuit-derived expectations, not measured ratings. See [MCP73871 datasheet, sections 3 and 5](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP73871-Data-Sheet-DS20002090F.pdf).

The three status signals have VBUS-fed LED/resistor branches on the power board. Their open-drain designation does not by itself make these populated nets safe for direct ESP32 connection. Select a buffer/level interface with appropriate input-voltage and powered-off tolerance, and verify both USB-on/main-off and battery-only states. Never rely on the MCU's protection diodes to absorb current.

Battery measurement must also be safe with the main switch off. A permanent resistor divider may inject current into an unpowered ADC or drain the cell through the sensing path. Prefer a switched divider with default-off isolation or a properly reviewed fuel-gauge interface. Voltage-only battery percentage is an estimate under load, not a fuel-gauge measurement.

## Proposed local supply

Latest user decision: a preassembled regulator module with through-hole pins on the main board is explicitly approved. This resolves the assembly-permission question in the earlier discussion below, not the converter/current/isolation qualification. The separate power module is unchanged. See [component decisions](COMPONENT_DECISIONS.md).

The supply must accommodate battery voltage crossing 3.3 V without relying on an LDO outside its headroom. **The latest student-kit requirement excludes bare TPS63802 or any other SMT regulator directly on the main PCB.** That earlier candidate is withdrawn as a direct-mounted part. First establish whether the exact legged MCU module's supply circuitry meets the full input range/current/runtime requirements; an onboard regulator must not be assumed sufficient or suitable for all peripherals. Otherwise qualify a compliant THT supply implementation. An additional preassembled through-hole regulator module or a RODDY change requires an explicit decision before adoption. No supply solution has yet passed this gate; keeping charging on a separate PCB does not make its SYS_OUT regulated 3.3 V.

Build the final load budget from the selected display backlight, Wi-Fi bursts, speaker power, motor stall current, IR pulse load and converter losses. No separate sub-GHz radio is in scope. Check the battery, protection MOSFETs, connector, output switch, and PCB traces as a complete path.

2026-09-10 scope constraint: keep the RODDY electrical architecture intact. A current limit conflict is a review gate, not authority to bypass SW1 or redesign the charger/protection circuit. If measured peaks exceed the rated path, propose a specifically rated component substitution or other minimal correction for approval before modifying it. Local 3.3 V regulation on the main board remains necessary. Do not parallel an MCU development board's charger with RODDY or connect its battery pads to the cell.

Illustration, not a measured load: 3.3 V at 0.5 A is 1.65 W. At 3.0 V input and 90% conversion efficiency that alone requires about 0.61 A upstream. This exceeds a 0.3 A series-switch rating and shows why selecting a larger regulator alone is insufficient.

## Programming power

The existing USB-C power connector has no routed USB data connection to the future main MCU. Provide a main-board data/programming connector or accessible programming pads. Initially prefer power from the power module during programming; do not connect two USB VBUS supplies together. Any ability to power the main board from its own USB port needs deliberate isolation/power multiplexing and VBUS detection.
