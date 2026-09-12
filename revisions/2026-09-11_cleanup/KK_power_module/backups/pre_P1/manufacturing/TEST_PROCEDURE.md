# KK Power Module — First-Article Test Procedure

Release: `0.2-LR1`

## Equipment

- Current-limited 5.0 V bench supply
- Calibrated multimeter
- Electronic load suitable for the intended SYS output
- Known-good single-cell 4.2 V Li-ion/Li-polymer battery or battery simulator
- Thermocouple or thermal camera
- USB-C cable/breakout known to provide 5 V

## Safety

- Perform initial tests on a nonflammable surface with eye protection.
- Use a current-limited supply before connecting a real cell.
- Stop immediately for unexpected heating, odor, swelling, smoke, or unstable current.
- Never reverse the battery connector.

## Inspection and unpowered checks

1. Record board revision, serial/lot number, and inspector.
2. Inspect component identity, orientation, solder joints, bridges, tombstones, and connector alignment.
3. Confirm U1 exposed-pad solder coverage by X-ray if available; otherwise validate the reflow process on the first article and monitor temperature closely.
4. Measure resistance between VBUS and GND, VBAT and GND, and SYS and GND. Investigate any reading that settles below 100 Ω before power-up.
5. Confirm J2/J3 cable polarity against the product harness.

## Current-limited bring-up

1. Disconnect the battery and external load.
2. Apply 5.0 V to VBUS with a 100 mA current limit.
3. Confirm no component overheats and the supply does not remain in current limit.
4. Verify the expected POWER GOOD indication and record idle input current.
5. Increase the current limit only after the initial check passes.

## Charger and power-path checks

1. Attach the approved cell or simulator at a safe mid-state voltage.
2. Verify correct charge-state indication and positive charge current.
3. Record charge current, battery voltage, SYS voltage, and U1 case temperature after 1, 5, and 15 minutes.
4. Apply the maximum intended SYS load and confirm SYS remains within the product requirement.
5. Remove VBUS and confirm uninterrupted battery-powered SYS operation.
6. Restore VBUS and confirm stable transition and charging behavior.
7. Verify charge termination near the approved cell's 4.2 V limit; do not accept a board that exceeds the battery manufacturer's maximum charge voltage.

## Protection checks

Use a battery simulator or protected test fixture for these checks. Do not deliberately abuse a bare cell.

1. Verify undervoltage load disconnect and recovery behavior.
2. Verify overcharge cutoff/recovery behavior.
3. Verify short-circuit/overcurrent protection using a current-limited fixture.
4. Exercise SW1 and both JP1 configurations intended for sale.
5. Verify all external status/header signals used by the product.

## Acceptance

- No visible assembly defects
- No persistent current-limit event or unexpected heating
- Correct connector polarity and indicator behavior
- Charge, termination, power-path, and protection behavior meet the product requirements
- U1 remains thermally stable at worst-case intended input, battery, ambient, and SYS load
- Pass results are recorded for every shipped unit; the first five units also receive a complete charge/discharge-cycle test

The numerical charge-current, SYS-load, temperature, and protection thresholds must be filled from the final product specification before sale. Until then this release is approved for controlled pilot manufacture, not unrestricted production.
