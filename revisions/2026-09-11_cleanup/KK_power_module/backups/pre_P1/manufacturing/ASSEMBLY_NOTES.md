# KK Power Module — Assembly Notes

Release: `0.2-LR1`

## Assembly split for a low run

1. Reflow all top-side SMD components using lead-free no-clean solder paste.
2. Inspect U1, Q1, U2, J1 signal contacts, D1, LEDs, and SW1 under magnification.
3. Hand-solder J1 shield tabs after reflow; confirm complete wetting on both sides where accessible.
4. Hand-install J2, J3, J4, J5, and JP1 after cleaning/inspection. J2 is mounted from the bottom side exactly as shown by the placement data and assembly view.
5. Install a 2.54 mm shunt on JP1 only when the product configuration intentionally disables the external NTC input.

## Controlled orientation checks

- U1: align package pin 1 with the PCB pin-1 mark; exposed pad must be soldered.
- Q1 and U2: verify pin 1 before placement; substitutes require pin-for-pin and package approval.
- D1: install the cathode to the footprint cathode marking.
- LED1: POWER GOOD indicator; verify polarity.
- LED2: CHARGE/LBO indicator; verify polarity.
- LED3: CHARGE STATUS 2 indicator; verify polarity.
- J1: connector mouth faces the board edge.
- J2/J3: confirm pin 1 and cable polarity against the product wiring drawing before shipment.

## Process controls

- Workmanship target: IPC-A-610 Class 2.
- Use ESD controls for all handling.
- Do not wash unless every installed switch and connector is approved for the wash process.
- No-clean flux residue is acceptable only when non-corrosive and visually clean.
- Do not substitute U1, U2, Q1, D1, J1, J2, J3, SW1, or LEDs without engineering approval.
- Commodity passive substitutions must meet or exceed every specification in `production_bom.csv` and fit the listed footprint.

## First-article hold point

Build one board first. Do not complete the remaining pilot units until its polarity, shorts check, current-limited power-up, charger function, and thermal behavior pass `TEST_PROCEDURE.md`.
