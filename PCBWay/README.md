# PCBWay — C.6 main + P.4 power prototype submission

Start with [00_Order_Setup/START_HERE.md](00_Order_Setup/START_HERE.md). This folder prepares **two separate PCBWay jobs**: five bare main boards and five assembled power boards. It does not place an order or authorize fabrication.

| Step | Folder | What to do |
| --- | --- | --- |
| 0 | [Order setup](00_Order_Setup/START_HERE.md) | Read specifications and copy the quote-request message. |
| 1 | [Main Gerbers](01_Main_C6/01_Gerber_Upload/README.md) | Upload the main Gerber ZIP to its own PCB job. |
| 2 | [Power Gerbers](02_Power_P4/01_Gerber_Upload/README.md) | Upload the power Gerber ZIP to a separate four-layer PCB + assembly job. |
| 3 | [Power BOM](02_Power_P4/02_BOM_Upload/README.md) | Upload the fitted-parts BOM; ask for sourcing/attrition quote. |
| 4 | [Power placement](02_Power_P4/03_Pick_and_Place_Upload/README.md) | Upload SMT centroid and attach mixed-operations file. |
| 5 | [Assembly drawings](02_Power_P4/04_Assembly_Drawings/README.md) | Attach polarity, schematic and assembly references. |
| 6 | [Manufacturing review](03_Factory_DFM_and_Questions/README.md) | Resolve process, sourcing and inspection questions. |
| 7 | [Approval and payment](04_Approval_and_Payment/README.md) | Review final quote and CAM/BOM approvals before payment/release. |
| 8 | [Delivery and testing](05_Delivery_and_Testing/README.md) | Retain inspection results and test samples safely on arrival. |

Use the files listed in [UPLOAD_MAP.csv](00_Order_Setup/UPLOAD_MAP.csv). The complete package ZIPs under each board's `05_Full_Review_Package` folder are supplemental engineering references, **not** the Gerber-upload ZIPs. Folder numbering follows this project's workflow, not a promise of PCBWay's exact current screen order.

**Do not upload the entire project or this whole folder to a Gerber field.** Do not mix the two board designs in one upload or order five of each archive separately. Main assembly is not requested; its extra BOMs are reference only. No shell, battery, firmware programming or finished toy is ordered here.

Current source-of-truth remains the root KiCad projects and issued manufacturing packages. The PCBWay copies are a submission snapshot. `SOURCE_COPY_MANIFEST.json` records byte-identical source copies; `PACKAGE_MANIFEST.json` inventories the prepared files. Recheck these if the design changes. Keep supplier responses and receipts in the provided folders; never overwrite issued Gerbers with returned CAM changes without review.

Status: **ready for quote/DFM submission, not manufacturer-approved, not powered-tested**. Copies of saved verification reports are evidence of static checks, not functional certification.

Prepared against [PCBWay's assembly file requirements](https://www.pcbway.com/assembly-file-requirements.html) and [via-in-pad guidance](https://www.pcbway.com/helpcenter/ordering_parameter_instruction/Via_in_Pad.html). Technical approval is still required for this particular design.
