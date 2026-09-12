# C.6 populated models — current flat-part revision

All 98 fitted electrical positions have resolving model attachments. R1–R43 use horizontal 10.16 mm-pitch axial models, not upright models. Ten electrolytics use Panasonic KA-A maximum envelopes lying horizontally; Q1–Q6 use flat-body TO-92 envelopes.

- [C6_flat_models_manifest.json](C6_flat_models_manifest.json): new capacitor/TO-92 STEP and VRML dimensions, provenance and hashes.
- [MODEL_MANIFEST.json](MODEL_MANIFEST.json): inherited socket/module/optical geometry history; old Nichicon/upright assets may remain in this library but are NOT the current capacitor/resistor selection. Actual attachments in the C.6 PCB govern.
- Each project-owned VRML has a same-name STEP twin for mechanical export. Stock model references use KiCad 10 standard libraries and retain their upstream license/exception.

Horizontal capacitor maximum heights including 0.5 mm support: 100uF ECEA1CKA101 = 7.3 mm; 10uF ECEA1CKA100 = 5.0 mm. Maximum can length 8 mm. Form and support leads without stressing seals or blocking vents.

The socketed RGB remains about 22.1 mm above the front; ESP32 rear envelope is about 15.3 mm. Display, MCU and SD seller envelopes and offsets are provisional. DIP/screen/module/RGB sockets retain functional height. Bare debug holes and mounting holes have no fitted body.

Speaker, motor, battery, wires, mating JST plugs and case are not shown at invented positions. All need a physical fit mock-up; 20 mm trial inter-board spacers do not prove plugged-connector clearance. RGB socket grip on real LED leads remains unqualified. Do not force or tin mating contacts. Trim solder tails to <=2.5 mm.

These are visualization/clearance aids, not vendor-certified assemblies, RF approval or powered tests. Main is student through-hole assembly; power remains a separate factory SMT subassembly.
