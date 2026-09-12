# Keychain Kreatures main module

## Start here — one-sheet schematic

[Open the main KiCad project](KK_main_module.kicad_pro) · [View the single-page schematic PDF](KK_main_module.pdf)

The current drawing groups **power input, ESP32 header, screen/SD/backlight, buttons/expander, IR, motor and audio** on one sheet, with physical wire connections inside each group. Signal labels connect groups. This is the C.1 readability redraw: all 91 components and all 267 pin connections are unchanged from C.0; KiCad ERC reports zero errors/warnings. Still an engineering prototype, not a fabrication release.

The older five-sheet capture below is retained as a backup, not the current drawing. Open the files directly in `KK_main_module`, not the old project inside `schematic/`.

## Main PCB — placement draft, not routed

[Open the PCB](KK_main_module.kicad_pcb) · [Footprint/placement status and fit checks](pcb/README.md) · [Per-component footprint audit](pcb/FOOTPRINT_AUDIT.csv)

The trial board is 80 × 100 mm with 4 mm rounded corners, front/back GND pours and all 91 schematic components assigned THT footprints. **MOD1 now uses the user-supplied ESP32-S3-SuperMini footprint, with matching GPIO/power pad names. No fabrication files are released.** Actual socket/module fit, display geometry and stack clearances still need checking. The separate power board is unchanged.

## Prior capture and supporting documents

**BACKUP — revision C five-sheet capture:** [five-sheet schematic PDF](schematic/KK_main_module.pdf) · [editable KiCad project](schematic/KK_main_module.kicad_pro) · [circuit decisions and validation](schematic/README.md) · [schematic-derived draft BOM](schematic/SCHEMATIC_BOM.csv). Use the one-sheet files above for current schematic and footprint work. Existing power PCB unchanged.

**Main-board datasheets:** [clickable index](component_review/DATASHEET_AUDIT.html) · [download packet](component_review/MAIN_BOARD_DATASHEETS.zip). All main-board list rows are accounted for, with manufacturer documents separated from seller-module evidence and not-yet-selected items.

**Printable main-board review list:** [open and print](component_review/MAIN_BOARD_PRINT.html). Charging/protection and all added voltage regulators are assigned to the later power-board revision. Main PCB retains local bypass capacitors, actuator drivers and suppression. Remaining part/count checks are marked; no fabrication or complete purchase release yet.

**Latest storage decision:** keep the original 240 × 280 XIITIA screen; add the header-connected **B0F82XWT4F microSD reader**, with under-screen placement to be checked. [Storage amendment](component_review/SD_STORAGE.md) · [updated component table](component_review/MASTER_BOM.md).

**CURRENT — revision B:** [SuperMini + separate power + wireless software](component_review/REVISION_B.md). The user has returned to a socketed ESP32-S3 SuperMini and authorized a later revision of their separate power PCB with regulation. Focus now is the THT main PCB with a defined SYS_IN interface. Browser Wi-Fi uploads/OTA and device-to-device trading are the software direction. [Current component table](component_review/MASTER_BOM.md). All Waveshare pin assignments and integrated-charger requirements below are superseded historical notes. The existing power PCB is untouched.

## Historical revision A and earlier notes

Everything below is historical context, including statements about which files existed at the time. It does not override the current one-sheet schematic or PCB status above.

Status: mechanical feasibility / architecture revision, 2026-09-10. NOT a fabrication release.

**Current design baseline:** [whole-kit component table](component_review/MASTER_BOM.md), [spreadsheet](component_review/MASTER_BOM.csv), and [initial circuit design](component_review/CIRCUIT_START.md). Selected MCU: **Waveshare ESP32-S3-DEV-KIT-N16R8-M, SKU 28836**, direct from Waveshare, with two 22-way sockets. Full-size is accepted. These documents override all historical selection notes below. Full THT battery charging/power remains unresolved; this is not a fabrication release.

**Supporting component register:** [single-board review](component_review/README.md), [parts CSV](component_review/parts.csv), and [archived datasheets/drawings](component_review/DATASHEETS.md). The battery may be chosen later against a defined electrical interface; old MakerHawk retention is no longer binding.

**Current architecture supersedes the power assumptions below:** [integrated through-hole power revision](INTEGRATED_THT_POWER_REVISION.md). The user now wants charging/protection/regulation on the main board with actual THT parts, no separate power/regulator module, and one external USB-C port for charging and data. Size is secondary to student assembly. The existing power-board project remains untouched. Earlier kit power selections/CSV rows are NOT current purchasing instructions; the new circuit is still at feasibility stage.

**Latest selection:** [entire-kit report](ENTIRE_KIT_PARTS.md) and [scope CSV](kit_component_selection.csv). User rejected XIAO and supplied **Teyleten Robot S3 SuperMini, Amazon B0D47HBFDY**. Use that as the prototype candidate with MCP23017-E/SP and nine soft Adafruit 3101 switches. Photographed FH4R2 chip implies 4 MB flash / 2 MB PSRAM; verify delivered boards. Earlier 16/8, XIAO and regulator assumptions are not current selections. The report lists all kit categories and marks unresolved exact items/counts; it is not a finalized purchasing BOM.

Current purchasing brief: [budget parts list](BUDGET_PARTS_LIST.md). User has now retained the Amazon screen, opened sourcing beyond Mouser and requested a smaller cheaper speaker. This supersedes the earlier display-open/supplier-shortlist wording below.

Latest amendments: [component decisions](COMPONENT_DECISIONS.md). The display is no longer fixed at 1.69 inches/240 × 280; a preassembled regulator with THT pins is approved on the main board. Recommended memory and replacement speaker/motor candidates are documented, not released. These supersede the older fixed-display wording below.

Goal: RODDY.WORLD KEYCHAIN KREATURES, a compact handheld pet with a separate 1.69-inch 240 × 280 display, nine gameplay inputs, original games/apps, pet trading, IR transmit/receive, speaker audio and haptics. Preserve the independent RODDY power PCB, battery, and through-hole DIY/repairability priority. Latest user amendment: size a comfortable board first; the user will model the shell around it. Start with a provisional 50 × 65 mm board, not the old hard shell envelope.

Reviewed source material:

- `../KC NOTES.txt`
- `../WIRING DIAGRAM.odt` (all extracted text)
- `../Keychain_Kreatures_Main_PCB_Astra_Specification.docx` (all extracted text; older C3/six-button assumptions superseded by latest request)
- Actual pad/net connections in `../KK_power_module/KK_power_module.kicad_pcb`

The user explicitly designated the latest pasted brief as their request; [DESIGN_BRIEF.md](DESIGN_BRIEF.md) records it. The older wiring documents are evidence, not independent instructions. Their battery-switch disagreement is resolved against the actual power PCB.

Files:

- [Mandatory student-kit assembly rules](STUDENT_KIT_REQUIREMENTS.md): all main-board parts mount through holes; ESP32 is a preassembled module with legs. No direct-mounted main-board SMD exceptions.
- [Design brief](DESIGN_BRIEF.md): current requirements and acceptance gates.
- [Board-first sizing plan](BOARD_FIRST_PLAN.md): latest size/workflow amendment and eventual shell handoff.
- [Design review/report](DESIGN_REVIEW.md): fit conflicts, electronics choices, power budget and next steps.
- [Earlier mechanical worksheet](mechanical/fit-study.svg): historical 46 × 62 mm shell study; NOT the new outline or enclosure CAD.
- [Earlier worksheet PDF](mechanical/fit-study.pdf): historical comparison only; not the new board or print-ready enclosure parts.
- [Proposed architecture](ARCHITECTURE.md): revised hardware, firmware and trading design.
- [Power interface](POWER_INTERFACE.md): actual connector nets and integration constraints.
- [Functional I/O budget](io_requirements.csv): nine-button mapping and MCU needs; no frozen GPIO numbers.
- [Cost estimate](COST_ESTIMATE.md): small-run engineering allowances, not purchasing quotes.
- [Change log](CHANGELOG.md): changes from the preliminary proposals and outstanding deliverables.
- [Historical proposals](archive/): superseded; never use the archived GPIO CSV for wiring.

Accepted: ESP32-S3 with PSRAM on a compact **legged/pin-header module**, through-hole-only main-board assembly for students, IR without separate sub-GHz, D-pad + A/B/X/Y + Function, separate hard power switch. Exact compact processor assembly is NOT selected. Previous bare-module and direct-mounted SMT-core/regulator proposals are withdrawn. RODDY stays separate and preassembled; local supply compatibility remains unresolved.

Open: exact physical screen/battery/speaker/motor assemblies, complete stack clearances, compact MCU assembly and flash budget, audio sourcing, and upstream current capacity. No main-module schematic, routed PCB, printable enclosure, or manufacturing files exist yet. Finalize board geometry with component/stack checks, then supply the user mechanical data for shell modeling; full enclosure CAD is no longer a prerequisite. This review does not change or re-release the RODDY power board.
