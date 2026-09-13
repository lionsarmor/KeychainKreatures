# Troubleshooting — start with the correct board

These guides are for first-time students and supervising instructors. Read from the beginning on the first attempt; use the symptom tables afterward. The power board is factory SMT; its live tests require a qualified instructor/technician.

| Board | Printable guide | Editable source | Recording sheets |
|---|---|---|---|
| Main C.6 | [Main PDF](../../KK_main_module/assembly/TROUBLESHOOTING_MAIN_C6.pdf) | [Markdown](../../KK_main_module/assembly/TROUBLESHOOTING_MAIN_C6.md) · [HTML](../../KK_main_module/assembly/TROUBLESHOOTING_MAIN_C6.html) | [Checklist](../../KK_main_module/assembly/TROUBLESHOOTING_C6_CHECKLIST.csv) · [Measurements](../../KK_main_module/assembly/TROUBLESHOOTING_C6_MEASUREMENTS.csv) |
| Power P.4 | [Power PDF](../../KK_power_module/assembly/TROUBLESHOOTING_POWER_P4.pdf) | [Markdown](../../KK_power_module/assembly/TROUBLESHOOTING_POWER_P4.md) · [HTML](../../KK_power_module/assembly/TROUBLESHOOTING_POWER_P4.html) | [Checklist](../../KK_power_module/assembly/TROUBLESHOOTING_P4_CHECKLIST.csv) · [Measurements](../../KK_power_module/assembly/TROUBLESHOOTING_P4_MEASUREMENTS.csv) |

[Factory fault-report PDF](FACTORY_FAULT_REPORT.pdf) · [Editable form](FACTORY_FAULT_REPORT.md) · [Guide/source verification](GUIDE_VERIFICATION.json)

[Download the complete troubleshooting packet](KK_C6_P4_TROUBLESHOOTING_PACKET.zip). It contains both guides, editable versions, worksheets and the factory form; unzip it and open the PDFs. The supporting schematic/datasheet links in PDFs point to the published hardware revision, so those links need internet access. The packet is not a replacement manufacturing package.

Print the PDFs double-sided if convenient. Keep one checklist and measurement sheet per serial-numbered board. Open CSVs in LibreOffice Calc or another spreadsheet editor; widen and wrap columns before printing. Retain blank templates. Record **PASS, FAIL, BLOCKED or NOT RUN**, along with the setup and evidence—not just a tick mark.

The main guide covers meter use, incoming/assembly state, harness/power, ESP32 isolation, buttons/I²C, display/backlight, SD, RGB, IR, motor, audio and integration. The power guide traces each stage and covers source/ground isolation, USB modes, charging/NTC, supervision/gating, loads, sequencing and factory escalation. Both include every released test pad and explicit stop conditions.

**A compatible diagnostic program is required for main functional tests and is not supplied by this hardware release.** Missing software is BLOCKED, not proof of a factory defect. Power itself needs no ESP32 firmware. No physical/powered tests were performed to create these guides.

Power TP3 is BAT_NEG; main TP3 is ACT_3V2. Never transfer a remembered pad number between boards. Do not bypass protection or connect ESP32 USB alongside external main power.

These are documentation supplements: CAD and issued manufacturing ZIPs remain unchanged. Printable source links refer to the published hardware commit used for verification. The older C.6 bench record in issued snapshots may mention P.3/shared mounting; use these C6/P4 troubleshooting worksheets for current tests. See [current release files](../CURRENT_RELEASE_INDEX.json).
