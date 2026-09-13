"""Package selected main-board evidence; explicitly distinguish module evidence."""
from pathlib import Path
import json,hashlib,zipfile,argparse
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['C2','C3','C4'],default='C2');revision=parser.parse_args().revision
root=Path(__file__).resolve().parent.parent;review=root/'component_review';out=root/'assembly'
names=['esp32-s3.pdf','mcp23017.pdf','tsal6200.pdf','tsop382.pdf','ksp2222a.pdf','bc327.pdf','tn0702.pdf','lp0701.pdf','1n5819.pdf','jst-ph.pdf','jst-xh.pdf','mfr-resistors.pdf','tda2822.pdf','dip-sockets.pdf','sullins-female-headers.pdf','sullins-order-codes.pdf','nichicon-uvr.pdf','soft-buttons.png','motor.pdf','kemet-100nf.pdf','kemet-10nf.pdf','kemet-1uf.pdf','st7789v2-controller.pdf','transcend-usd300s.pdf']
if revision in ['C3','C4']:names+=['tlc5916.pdf','rgb-wp154a4sej3vbdzgw-ca.pdf']
manifest=[]
for name in names:
    p=review/'datasheets'/name;assert p.exists()
    assert p.read_bytes().startswith(b'%PDF') if name.endswith('.pdf') else True
    manifest.append({'file':'datasheets/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for name in ['sd-pinout.jpg','sd-dimensions.jpg']:
    p=review/'source_evidence'/name
    if p.exists():manifest.append({'file':'module_evidence/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(out/f'{revision}_DATASHEET_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
text='# C.2 main-board documentation packet\n\nThe purchased ICs/discretes/connectors are covered by the following documents. MCU and screen **chip** datasheets do not establish an exact seller-module schematic, header offset or delivered memory configuration. The SD module uses the supplied seller pinout photo. The exact speaker continuous-power rating remains missing. No document is presented as a substitute for a powered test.\n\n'
text+='New C.2 selections: [LP0701 manufacturer sheet](https://ww1.microchip.com/downloads/en/DeviceDoc/LP0701-P-Channel-Enhancement-Mode-Lateral-MOSFET-Data-Sheet-20005447A.pdf), [Transcend microSD sheet](https://cdn.transcend-info.com/products/images/modelpic/948/Transcend-USD300S_202404_a2.pdf), [Alpha 3050 wire specification](https://www.alphawire.com/products/wire/hook-up-wire/premium/3050), [Samtec replacement header](https://www.samtec.com/products/tsw-109-07-g-s), [TE insulation sleeve](https://www.te.com/en/product-5052892055.html). No price or availability is guaranteed.\n\n'
text+='\n'.join('- ['+n+'](../component_review/datasheets/'+n+')' for n in names)
text+='\n\n[Module/speaker evidence limitations](../component_review/MODULE_SOURCE_NOTES.md) · [Per-reference datasheet URLs](C2_BOM_BY_REFERENCE.csv) · [Packet checksum manifest](C2_DATASHEET_MANIFEST.json). Other source URLs remain in the historical documentation index; the C.2 BOM controls population.\n'
if revision in ['C3','C4']:
    text=text.replace('C.2',revision.replace('C','C.')).replace('C2_',revision+'_')
    text+='\nRGB: TLC5916IN PDIP16 with ED16DT socket, Kingbright common-anode LED with formed 2.54 mm lead pitch. See the assembly guide for safe startup and lead forming.\n'
    if revision=='C4':text+='C.4 adds Sullins PPTC041LFBN-RC for D3. Its housing drawing is included; actual LED contact retention is not qualified by that drawing.\n'
(out/f'{revision}_DATASHEETS.md').write_text(text)
with zipfile.ZipFile(out/f'{revision}_DATASHEETS.zip','w',zipfile.ZIP_DEFLATED) as z:
    for n in names:z.write(review/'datasheets'/n,'datasheets/'+n)
    for n in ['sd-pinout.jpg','sd-dimensions.jpg']:
        if (review/'source_evidence'/n).exists():z.write(review/'source_evidence'/n,'module_evidence/'+n)
    z.write(out/f'{revision}_DATASHEET_MANIFEST.json',f'{revision}_DATASHEET_MANIFEST.json')
    z.writestr(f'{revision}_DATASHEETS.md',text.replace('../component_review/datasheets/','datasheets/'))
print('Archived',len(names),'selected documents plus SD-module photos; limitations explicit.')
