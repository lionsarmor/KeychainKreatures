# Keychain Kreatures — one-board fault report

Complete one copy per board. Photograph before repair. Do not attach a real battery just to fill in this form. Mark unavailable tests BLOCKED or NOT RUN.

## Identification

- Board: MAIN C.6 / POWER P.4 (circle one).
- Serial, supplier, order and batch/lot: ____________________
- Date received / tester / instructor: ____________________
- Bare PCB, partly assembled or fully assembled: ____________________
- Exact release ZIP name and SHA-256: ____________________
- Factory-approved BOM substitutions: ____________________
- Main: ESP32, display and SD-reader markings: ____________________
- Main: diagnostic firmware version/hash and known-good evidence: ____________________

## First failure

- What was expected; what actually happened? ____________________
- First failed guide step and preceding passing step: ____________________
- Repeatable or intermittent? ____________________
- Did another unit pass the identical setup? Its serial: ____________________
- Smoke, smell, abnormal heat or current-limit event? ____________________
- Was a real cell connected? Approved part and condition: ____________________
- Any rework, reflash/erasure, jumper, substitution or forced connector? ____________________

## Setup — attach a labeled photograph/diagram

- Source model, voltage, current limit and isolation: ____________________
- Attached cables, loads, modules and instruments: ____________________
- Where does every instrument ground/earth connect? ____________________
- Power: how is BAT_NEG kept free of an external bypass to GND? ____________________
- Ambient temperature and temperature-measurement method: ____________________
- Meter/scope model, ranges, probe attenuation and test state: ____________________

Write both probe points. A number without its operating state or reference is not enough.

| Test / signal | Red / reference points | Source, switch, load, firmware state | Expected context | Reading / units |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

Attach the completed checklist and measurement CSV. Scope captures must show channel scales, timebase, trigger, probe setup and board identity. Do not include Wi-Fi passwords or unrelated personal data.

## Requested factory response

- Compare the first failing stage with the exact schematic, BOM and Gerbers.
- Supply bare-board electrical-test results, assembly/hidden-joint inspection images and all substitutions for the lot.
- Power: confirm the approved via-in-pad process and WCSP/QFN assembly details.
- Identify the cause before proposing a part swap or undocumented jumper.
- Advise whether to preserve the unit untouched for return; obtain approval before rework.
- Provide corrective action, affected lot scope and post-repair test results.

## Repair and retest

| Date / person | Confirmed cause | Approved repair / part and lot | Retested steps | Outcome |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

Final status: PASS AT RECORDED CONDITIONS / FAIL / BLOCKED / NOT RUN.

Instructor signature/date: ____________________

Passing is not production, battery-safety, USB, EMC or toy certification. Coordinate damaged-battery handling/return with the responsible lab and supplier; do not put it in an ordinary PCB return parcel.
