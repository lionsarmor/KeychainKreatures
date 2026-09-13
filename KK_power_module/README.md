# Power board — current P.4 compact module

[Troubleshooting PDF](assembly/TROUBLESHOOTING_POWER_P4.pdf) · [Guide and worksheets](../docs/troubleshooting/README.md). Live power tests require a qualified instructor/technician.

Open [KK_power_module.kicad_pro](KK_power_module.kicad_pro) or [KK_power_module.kicad_pcb](KK_power_module.kicad_pcb) directly from this folder. P2_compact and old work directories are archived.

50 × 50 × 1.6 mm, four copper layers, R3 corners, four 2.2 mm holes at (3,3), (47,3), (3,47), (47,47) mm. It needs independent case supports; main C.6 remains 96 × 105 mm. The routed electrical core is preserved. There are 108 fitted parts, 14 ICs and 28 rear bare test pads. Power remains a factory SMT subassembly, not a student SMT soldering kit.

- [Assembly/electrical review and first-power-up](assembly/P4_REVIEW_AND_TEST.md)
- [Factory fabrication requirements](FABRICATION_REQUIREMENTS.md)
- [BOM, coordinates, connector/test-pad maps and reports](release_checks/)
- [Manufacturing packages](manufacturing/README.md) · [Both projects](../START_HERE.md)

J3 → main J1: pin1 MCU_5V, pin2 GND, pin3 LOGIC_3V3, pin4 ACT_3V2. Battery return BAT_NEG is not GND. Charger USB carries no data. USB-A/default charging is deliberately slow; do not combine ESP32 USB power and external main rails until qualified.

Before ordering, obtain factory approval of the fine-pitch WCSP/QFN packages and filled/capped/planarized via-in-pad process. Actual plug/stack clearance, selected battery/NTC, load margin, charging/thermal behavior, rail sequencing and backfeed need physical and powered tests. Screening targets are not validated ratings.

The project uses KiCad 10 standard libraries plus the local libraries/models. All fitted model paths resolve, but models are not certified mating assemblies.
