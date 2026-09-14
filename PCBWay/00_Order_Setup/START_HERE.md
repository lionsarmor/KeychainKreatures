# Start here — two jobs, one prototype project

1. Create a **main C.6 bare-PCB** quote, quantity 5: 96 × 105 mm, two copper layers, 1.6 mm.
2. Create a **power P.4 PCB + assembly** quote for **five finished assemblies**: 50 × 50 mm, four copper layers, 1.6 mm. Ask PCBWay to quote any extra bare boards/parts needed for assembly attrition separately.
3. Upload each board's Gerber ZIP from its own `01_Gerber_Upload` folder. Upload power BOM and placement separately when prompted.
4. Attach fabrication requirements, assembly references and the complete review ZIP for the correct board to engineering correspondence.
5. Send [QUOTE_REQUEST.txt](QUOTE_REQUEST.txt). Review the factory's response before authorizing manufacturing.

Use [ORDER_SETTINGS.csv](ORDER_SETTINGS.csv) for the quote form. Fields marked **proposed** or **confirm** are not approved final process specifications. Prefer standard green mask/white silkscreen for this prototype; those colors are a proposed cosmetic selection only. Lead-free HASL is proposed for main THT; ENIG is proposed for the power board's fine-pitch lands. PCBWay must approve finish, copper, stackup and via process.

Do not select ordinary via tenting in place of filled/capped/planarized component-pad vias on power. Do not silently accept a two-layer power-board quote. No impedance-control certification is requested; no approved custom fabrication stackup is supplied.

The main board is a student soldering kit: no main-board assembly or main stencil is requested. The power board is factory assembled. Ask PCBWay to handle stencil, assembly panel tooling and any connector secondary operations in its quote, with no changes to finished outlines or hole locations without approval.

Open items that do not disappear when the factory accepts the files: actual module/connector fit, cell and NTC selection, regulated-rail load/thermal/startup testing, the 3.3 V reservation discrepancy (0.5 A main versus 0.4 A power screening), and firmware. These are engineering samples, not a classroom-ready toy.

No account, shipping address, payment information, factory approval or order number is prefilled. Complete those yourself in the later folders/site.
