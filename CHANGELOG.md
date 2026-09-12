# Hardware release notes

## 2026-09-12 — main C.6 / power P.3 prototype review

- Matched both board outlines at 96 × 105 × 1.6 mm, R4 corners, with common M2 mounting-hole centers. Main remains two-layer; power remains four-layer.
- Main: all 43 resistors horizontal; ten Panasonic KA-A electrolytics and six TO-92 bodies mounted flat. Updated matching BOM, footprints, model envelopes and student lead-form/orientation instructions.
- Retained landscape display, below-screen controls, socketed S3/SD/DIP/RGB parts, IR transmitter and receiver, JST connectors and 25 main debug holes.
- Re-routed main with restored explicit power/audio classes and independent width audit. Power's routed electrical core was rigidly repositioned; added matching outline/holes and rear-stack antenna clearance region without changing its circuit.
- Repaired missing power 3D attachments. All 98 main and 108 power fitted positions have resolving model files; actual fit is still unqualified.
- Issued current Gerbers, drills, IPC-D-356, BOMs, placement/maps, assembly/schematic PDFs, source CAD and hash manifests for five-prototype review. Verified matching outline Gerbers and mounting-hole drill coordinates.
- Both boards: fresh native ERC/DRC, opens and schematic parity reported zero. Preserved exact reports and existing ignored-check settings; this is not a powered or production qualification.
- Archived superseded manufacturing outputs; updated the desktop print sheet and current project entry points.
- GitHub documentation now describes the S3/MCP23017/TDA2822L design, not the legacy C3/MAX98357A/PCF8574 prototype. Documented firmware-not-supplied status and unresolved project license.

Open gates: factory fine-pitch/via-in-pad and supply approval, physical stack/plug/module fit, battery/NTC/case selection, speaker rating, integrated peak-load margin (including the 0.5 A logic reservation versus 0.4 A screening target), charging/thermal/sequence/backfeed tests, firmware and product safety/EMC assessment. No board order or certification is implied.

## Earlier revisions

See [historical revisions and recovery map](revisions/README.md). C.5/P.2 and older files remain preserved evidence, not current manufacturing sources.
