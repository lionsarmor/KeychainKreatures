# C.5 bare-board engineering prototype — not a qualified toy kit

Only use this package with the C.5 BOM and schematic. Board: **84 × 95 mm, two copper layers, 1.6 mm nominal FR-4, 35 µm nominal copper, rounded corners**. Separate plated and non-plated drill files are included. Suggested finish: lead-free HASL; confirm tolerances, plating, mask and silkscreen capabilities with the fabricator.

The export generator refuses to package a board with ERC, DRC, open connections or schematic-parity issues. See the included reports/manifest for the exact source hashes and inherited rule exclusions. This does not test function, fit, RF, thermals, audio, firmware or product compliance.

**Supply interface:** J1 requires coordinated 5 V / GND / 3.3 V / 3.2 V. No charger, regulator or battery protection is on this board. Never connect a raw battery, an arbitrary two-wire supply, or simultaneous module USB and SYS_IN without qualified source isolation.

**Physical holds:** seller-module dimensions/header offsets; upright lead forms; top-facing IR lead form; actual RGB socket contact retention; screen support; JST/card access; roughly 39 mm nominal full component envelope before case clearance. Test one assembly before a kit batch. Speaker rating, permitted volume, power module and battery remain unqualified.

No manufacturing order was placed. The KiCad and open-gear logos are not product certification marks.
