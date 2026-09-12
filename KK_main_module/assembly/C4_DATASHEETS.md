# C.4 main-board documentation packet

The purchased ICs/discretes/connectors are covered by the following documents. MCU and screen **chip** datasheets do not establish an exact seller-module schematic, header offset or delivered memory configuration. The SD module uses the supplied seller pinout photo. The exact speaker continuous-power rating remains missing. No document is presented as a substitute for a powered test.

New C.4 selections: [LP0701 manufacturer sheet](https://ww1.microchip.com/downloads/en/DeviceDoc/LP0701-P-Channel-Enhancement-Mode-Lateral-MOSFET-Data-Sheet-20005447A.pdf), [Transcend microSD sheet](https://cdn.transcend-info.com/products/images/modelpic/948/Transcend-USD300S_202404_a2.pdf), [Alpha 3050 wire specification](https://www.alphawire.com/products/wire/hook-up-wire/premium/3050), [Samtec replacement header](https://www.samtec.com/products/tsw-109-07-g-s), [TE insulation sleeve](https://www.te.com/en/product-5052892055.html). No price or availability is guaranteed.

- [esp32-s3.pdf](../component_review/datasheets/esp32-s3.pdf)
- [mcp23017.pdf](../component_review/datasheets/mcp23017.pdf)
- [tsal6200.pdf](../component_review/datasheets/tsal6200.pdf)
- [tsop382.pdf](../component_review/datasheets/tsop382.pdf)
- [ksp2222a.pdf](../component_review/datasheets/ksp2222a.pdf)
- [bc327.pdf](../component_review/datasheets/bc327.pdf)
- [tn0702.pdf](../component_review/datasheets/tn0702.pdf)
- [lp0701.pdf](../component_review/datasheets/lp0701.pdf)
- [1n5819.pdf](../component_review/datasheets/1n5819.pdf)
- [jst-ph.pdf](../component_review/datasheets/jst-ph.pdf)
- [jst-xh.pdf](../component_review/datasheets/jst-xh.pdf)
- [mfr-resistors.pdf](../component_review/datasheets/mfr-resistors.pdf)
- [tda2822.pdf](../component_review/datasheets/tda2822.pdf)
- [dip-sockets.pdf](../component_review/datasheets/dip-sockets.pdf)
- [sullins-female-headers.pdf](../component_review/datasheets/sullins-female-headers.pdf)
- [sullins-order-codes.pdf](../component_review/datasheets/sullins-order-codes.pdf)
- [nichicon-uvr.pdf](../component_review/datasheets/nichicon-uvr.pdf)
- [soft-buttons.png](../component_review/datasheets/soft-buttons.png)
- [motor.pdf](../component_review/datasheets/motor.pdf)
- [kemet-100nf.pdf](../component_review/datasheets/kemet-100nf.pdf)
- [kemet-10nf.pdf](../component_review/datasheets/kemet-10nf.pdf)
- [kemet-1uf.pdf](../component_review/datasheets/kemet-1uf.pdf)
- [st7789v2-controller.pdf](../component_review/datasheets/st7789v2-controller.pdf)
- [transcend-usd300s.pdf](../component_review/datasheets/transcend-usd300s.pdf)
- [tlc5916.pdf](../component_review/datasheets/tlc5916.pdf)
- [rgb-wp154a4sej3vbdzgw-ca.pdf](../component_review/datasheets/rgb-wp154a4sej3vbdzgw-ca.pdf)

[Module/speaker evidence limitations](../component_review/MODULE_SOURCE_NOTES.md) · [Per-reference datasheet URLs](C4_BOM_BY_REFERENCE.csv) · [Packet checksum manifest](C4_DATASHEET_MANIFEST.json). Other source URLs remain in the historical documentation index; the C.4 BOM controls population.

RGB: TLC5916IN PDIP16 with ED16DT socket, Kingbright common-anode LED with formed 2.54 mm lead pitch. See the assembly guide for safe startup and lead forming.
C.4 adds Sullins PPTC041LFBN-RC for D3. Its housing drawing is included; actual LED contact retention is not qualified by that drawing.
