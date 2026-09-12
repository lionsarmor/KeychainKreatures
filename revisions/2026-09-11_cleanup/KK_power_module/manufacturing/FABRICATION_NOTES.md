# KK Power Module — Fabrication Notes

Release: `0.2-LR1`  
Date: 2026-09-09

## Board specification

- Two-layer rigid PCB, FR-4
- Finished thickness: 1.60 mm
- Finished copper: 35 µm / 1 oz on both sides
- Surface finish: ENIG, RoHS-compatible
- Solder mask: green, both sides
- Silkscreen: white, both sides
- Minimum finished hole-to-copper clearance: 0.25 mm except geometry accepted by the fabricator's DFM review
- Vias: tented from both sides; no filled, capped, or via-in-pad process required
- Route the board to the supplied `Edge_Cuts` data; do not scale fabrication data
- PTH and NPTH drill data are supplied separately
- Electrical test: 100% flying-probe or equivalent netlist test
- IPC production class: IPC Class 2 workmanship target

## Release handling

- Gerbers use extended attributes (Gerber X2).
- Fabricator must run DFM and return production artwork for approval before manufacture.
- Any aperture, drill, outline, copper-clearance, or solder-mask change requires written approval.
- Panelization may be performed by the fabricator; add tooling rails outside the finished outline only.

## Nominal order configuration

- Quantity: 5 first-article boards, then 20–50 after acceptance testing
- Board color may change without electrical impact, but green is the controlled default
- ENIG is controlled because the design contains a 0.5 mm-pitch QFN and fine-pitch USB-C contacts
