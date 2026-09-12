# C.4 RGB assembly packet

Use these files together for the 80 × 115 mm engineering prototype:

- [Printable complete BOM](C4_BOM_PRINT.html)
- [Grouped PCB purchasing BOM](C4_PCB_BOM.csv)
- [All 98 references, placement and datasheets](C4_BOM_BY_REFERENCE.csv)
- [Modules, sockets, mating plugs, wiring and hardware](C4_KIT_EXTRAS.csv)
- [Assembly, orientation, wiring and startup](ASSEMBLY_GUIDE.md)
- [25-point debug guide](C4_DEBUG_GUIDE.md)
- [Bench acceptance record — all tests initially pending](C4_BENCH_TEST_RECORD.csv)
- [26-document datasheet packet](C4_DATASHEETS.zip)

J2/J3 already count their female sockets: do not purchase them twice. D1 is IR, D3 is RGB. J4/J5 use B2B-PH top-entry parts, not historical S2B side-entry parts. U4 needs the added ED16DT socket. Bare TP holes remain unpopulated.

Power module, battery and enclosure are outside this main-board package. Speaker power rating, delivered module revisions, physical dry-fit and powered qualification remain open. Historical C.2 lists must not be mixed into this BOM.

D3's new PPTC041LFBN-RC socket is an additional kit part. Actual LED lead/contact retention is a prototype qualification hold. Do not force oversized leads or tin the socket mating portions. See [model dimensions and limitations](../3dmodels/README.md).
