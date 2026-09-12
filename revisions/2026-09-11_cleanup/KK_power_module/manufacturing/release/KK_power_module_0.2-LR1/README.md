# KK Power Module 0.2-LR1 Factory Package

This directory contains the machine-generated outputs for the controlled five-unit pilot build.

## Fabrication inputs

- `KK_power_module-F_Cu.gbr`, `KK_power_module-B_Cu.gbr`
- `KK_power_module-F_Mask.gbr`, `KK_power_module-B_Mask.gbr`
- `KK_power_module-F_Silkscreen.gbr`, `KK_power_module-B_Silkscreen.gbr`
- `KK_power_module-F_Paste.gbr`, `KK_power_module-B_Paste.gbr`
- `KK_power_module-Edge_Cuts.gbr`
- `KK_power_module-PTH.drl`, `KK_power_module-NPTH.drl`
- `KK_power_module-job.gbrjob`

## Assembly and review inputs

- `positions_smt.csv`: use for factory SMT placement
- `positions.csv`: complete placement reference, including hand-installed parts
- `design_bom.csv`: CAD-generated design cross-check only
- `assembly_top.pdf`, `assembly_bottom.pdf`
- `schematic.pdf`

The authoritative purchasing BOM is `../../production_bom.csv`. Fabrication, assembly, and test instructions are in the surrounding `manufacturing` directory and are also included in the factory ZIP archive.

## Verification evidence

- `ERC.rpt`
- `DRC.rpt`
- `drill_report.txt`
- PTH and NPTH drill-map PDFs

Do not release more than five pilot units until the first-article hold point and test procedure are complete.
