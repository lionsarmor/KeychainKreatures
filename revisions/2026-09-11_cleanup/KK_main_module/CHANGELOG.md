# Design revision log — 2026-09-10

## Entire-kit sourcing and exact budget processor

Added ENTIRE_KIT_PARTS.md and scope CSV covering main electronics, sockets, harnesses, passive value pool, existing assembled power board, battery/NTC, enclosure components and kit preparation. User rejected XIAO, requested low-cost off-brand components, then supplied Teyleten Robot Amazon B0D47HBFDY. Inspected listing photos: FH4R2 chip marking and THT header rows; cross-checked 4 MB flash / 2 MB PSRAM against Espressif Table 1-1. Selected as prototype candidate, not qualified production assembly. Retained MCP23017 and selected soft elastomer Adafruit 3101 buttons. Withdrew XIAO-specific power/pin assumptions and its partial price subtotal; regulator selection reopened. Marked current-path, USB isolation, memory, sample/footprint, passive quantity and custom mechanical holds. No circuit, PCB, power-board or purchase changes.

## Budget-first sourcing amendment

User retained Amazon screens, removed the Mouser-only preference and rejected the Same Sky speaker on cost. Added BUDGET_PARTS_LIST.md: wired 1511 micro-speaker sample direction, generic wired ERM, complete block-level target budget and assembled-feel priorities. Clearly separated wholesale advertisements/user screen price from unquoted procurement targets, and kept THT, compact size, memory and supply qualification constraints. No purchasing, circuit changes or final BOM release.

## Latest component clarification

User approved a preassembled THT-pin regulator module on the main board, preserving the through-hole kit and separate reusable power module. User allows new speaker/motor selection and asked for a premium/cost-effective memory recommendation. Added COMPONENT_DECISIONS.md with a proposed 16 MB flash/8 MB PSRAM target, wired Same Sky speaker and SparkFun ERM shortlist, source links, price caveats and remaining qualification gates. Also recorded the preceding relaxation of display size/resolution and rejection of the expensive Adafruit option. Updated current requirements and precedence notices; no exact processor, regulator, audio driver, display or manufacturing BOM is released. No power-board or hardware files changed.

## Latest clarification: student through-hole kit is mandatory

User clarified that separating RODDY is specifically to enable student THT assembly, and the ESP32 must be on a module with legs. Withdrew the direct-mounted fine-pitch MCU/regulator island and any bare-SMT audio fallback. Added STUDENT_KIT_REQUIREMENTS.md and updated current brief/architecture/board-first plan/power interface and historical report/cost notices. All components directly mounted to the main PCB must be THT; only the already assembled ESP32 module, RODDY and other external assemblies carry their own internal SMT. Additional module exceptions are not assumed. Exact header GPIO, regulation, module/socket dimensions, sourcing and student-assembly verification remain open. No schematic, PCB or released BOM was changed or claimed qualified.

## Subsequent user amendment: board first

The user now prefers a comfortable, small handheld-toy board and will model the shell around the finalized board. This overrides the original shell-first sequence and fixed size limits described in the historical table below. Updated brief, README, architecture and review/cost notices; added BOARD_FIRST_PLAN.md. Proposed trial PCB: 50 × 65 × 1.6 mm, not a verified fit or final outline. Features, THT priorities and separate RODDY architecture remain unchanged. No actual PCB or electrical circuitry was changed in this amendment.

## Source precedence

Read the latest user-designated pasted request in full, plus the root `KC NOTES.txt`, `WIRING DIAGRAM.odt` and `Keychain_Kreatures_Main_PCB_Astra_Specification.docx`. Inspected the existing power PCB and production BOM for integration evidence. Instructions embedded in older specifications do not override the user's latest request or independently authorize unrelated changes.

The DOCX is useful engineering context, but its C3 and six-control baseline is superseded by the accepted compact S3/PSRAM and nine-input brief. Its detailed transistor/filter/resistor values are candidates, not verified circuit values.

## Changes

| Preliminary choice | Current treatment | Reason |
|---|---|---|
| Large S3-WROOM-N16R8 default | Withdrawn; compact module comparison, no exact selection yet | User's keychain-size constraint |
| Six buttons in source docs; eight in prior proposal | Nine: D-pad, A/B/X/Y, Function | Explicit final user layout |
| Optional sub-GHz | Removed from current hardware/I/O budget | User selected IR only; built-in ESP wireless retained |
| TCA9535 SMT expander default | Direct GPIO versus THT expander study | THT assembly and tight volume |
| DOCX MCP23008-E/P PDIP-18 | Remains a candidate to compare; not implicitly approved or rejected | Need compare interrupt/wake behavior, footprint and sourcing with PCF8574N/direct GPIO |
| PCF8574 used for IR in breadboard | Buttons only; direct RMT for IR | Pulse timing must not depend on I2C polling |
| MAX98357A integrated SMT default | Explicit fallback, not baseline; DIP audio qualification first | User's THT/repairability priority |
| NJM2073D | Existing-stock experiment; qualify HT82V739 DIP alternative | Obsolete listing and need for low idle consumption; neither replacement nor pinout finalized |
| Display resolution uncertain | 240 × 280 confirmed by user | Assembly dimensions/pinout still unknown |
| Display backlight always powered | Controlled backlight/peripheral shutdown planned | Week-of-pet-use target |
| PCB-first layout | Mechanical measurements/CAD first | Explicit latest sequencing constraint |
| RODDY convenient supply assumption | Preserve architecture; flag real interface/current gates | SYS_OUT unregulated, status levels, switch rating and mated connector heights |

DOCX candidates retained for schematic qualification: TSAL6200 emitter, TSOP38238 receiver, KSP2222ABU drivers, 1N5819 flyback diode, 3 V motor, THT tact switches and optional service header. No base resistor, IR current resistor, receiver filter or battery divider value is approved by this feasibility report. Their exact datasheets, current/thermal calculations and reset states must be reviewed during schematic design. Do not order from the inventory list as if it were a released BOM.

## Deliverables and limits

Delivered: current brief, architecture, feasibility/report, functional I/O counts, power-interface constraints, budgetary cost report, 1:1 SVG/PDF worksheet and source/change traceability. Archived old architecture/review/radio/pin-map files rather than discarding them. Existing user changes outside this folder were left untouched.

Verified: local document links, eight distinct expander buttons plus direct Function, 20 base direct MCU interface signals, framebuffer/runtime/fit arithmetic, successful SVG/PDF export and visual inspection. These checks do not verify hardware.

Still required after measured mechanics: source-qualified exact BOM, complete calculated circuits and schematic, final module GPIO mapping, actual screen interface, placed/routed PCB, ERC/DRC and manufacturing/assembly instructions. Physical runtime/RF/audio/thermal/reliability tests remain open. These are not claimed complete or factory-ready.
