"""Prepare local P.1 footprints and audit the physical pad numbers.

This generates CAD artifacts, never alters the root or main-board project.
Run after p1_design.py on host Python.
"""
from pathlib import Path
import json,re,importlib.util
spec=importlib.util.spec_from_file_location('design',Path(__file__).with_name('p1_design.py'))
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
out=d.OUT;lib=Path(d.META['libraries']['Footprints']);local=out/'KK_Power.pretty';local.mkdir(exist_ok=True)
(local/'MountingHole_2.2mm_M2.kicad_mod').write_text((lib/'MountingHole.pretty/MountingHole_2.2mm_M2.kicad_mod').read_text())
usb=d.parse((lib/'Connector_USB.pretty/USB_C_Receptacle_HCTL_HC-TYPE-C-16P-01A.kicad_mod').read_text())
usb[1]='"USB_C_HCTL"'
for pad in d.kids(usb,'pad'):
    if d.val(pad[1])=='SH':pad[1]='"S1"'
(local/'USB_C_HCTL.kicad_mod').write_text(d.dump(usb)+'\n')
fs=d.parse((d.ROOT/'backups/pre_P1/FS8205.pretty/SOT95P280X145-6N.kicad_mod').read_text());fs[1]='"FS8205"'
(local/'FS8205.kicad_mod').write_text(d.dump(fs)+'\n')
# TI YBH0006-C02 land pattern, datasheet pp. 21-23: 0.4mm pitch,
# 0.2mm NSMD copper; 0.05mm mask expansion; 0.21mm paste apertures.
wcsp='(footprint "TPS22950_YBH" (version 20260206) (generator "pcbnew") (layer "F.Cu") (attr smd) (descr "TI TPS22950YBHR YBH0006-C02; land drawing 4226594/A; factory SMT only") (property "Reference" "REF**" (at 0 -1.2 0) (layer "F.SilkS") (effects(font(size 0.8 0.8)(thickness 0.1)))) (property "Value" "TPS22950YBHR" (at 0 1.2 0) (layer "F.Fab") (effects(font(size 0.8 0.8)(thickness 0.1))))'
wcsp+='(fp_rect(start -0.363 -0.563)(end 0.363 0.563)(stroke(width 0.1)(type solid))(fill none)(layer "F.Fab"))'
wcsp+='(fp_rect(start -0.65 -0.85)(end 0.65 0.85)(stroke(width 0.05)(type solid))(fill none)(layer "F.CrtYd"))'
wcsp+='(fp_circle(center -0.62 -0.65)(end -0.57 -0.65)(stroke(width 0.1)(type solid))(fill solid)(layer "F.SilkS"))'
for row,letter in enumerate('ABC'):
    for col in [1,2]:
        x=-.2+(col-1)*.4;y=-.4+row*.4
        wcsp+=f'(pad "{letter}{col}" smd circle(at {x} {y})(size 0.2 0.2)(layers "F.Cu" "F.Mask" "F.Paste")(solder_mask_margin 0.05)(solder_paste_margin 0.005))'
(local/'TPS22950_YBH.kicad_mod').write_text(wcsp+')\n')
for p in d.PARTS:
    name,fp=p['source_footprint'].split(':')
    if name!='KK_Power':
        (local/(fp+'.kicad_mod')).write_text((lib/(name+'.pretty')/(fp+'.kicad_mod')).read_text())
# Exposed-pad thermal holes are not through-hole component leads. Mark their
# mechanical purpose explicitly without changing their copper, drills or nets.
thermal=local/'Texas_S-PWSON-N10_ThermalVias.kicad_mod'
data=d.parse(thermal.read_text())
for pad in d.kids(data,'pad'):
    if d.val(pad[1])=='11' and pad[2]=='thru_hole':
        pad.append(['property','pad_prop_heatsink'])
thermal.write_text(d.dump(data)+'\n')
(out/'datasheets/sources.json').write_text(json.dumps(d.DATASHEETS,indent=2)+'\n')
(out/'fp-lib-table').write_text('(fp_lib_table\n (version 7)\n (lib (name "KK_Power") (type "KiCad") (uri "${KIPRJMOD}/KK_Power.pretty") (options "") (descr "P.1 local footprints"))\n)\n')
issues=[];audit=[]
for p in d.PARTS:
    name,fp=p['footprint'].split(':');path=(local if name=='KK_Power' else lib/(name+'.pretty'))/(fp+'.kicad_mod')
    if not path.exists():issues.append(p['ref']+': missing '+str(path));continue
    data=d.parse(path.read_text());pads={d.val(x[1]) for x in d.kids(data,'pad') if d.val(x[1])}
    expected=set(p['nets'])
    if pads!=expected:issues.append(f'{p["ref"]}: footprint pads {sorted(pads)} != schematic pins {sorted(expected)}')
    audit.append(dict(ref=p['ref'],footprint=p['footprint'],pads=sorted(pads),symbol_pins=sorted(expected),models=[d.val(x[1]) for x in d.kids(data,'model')]))
(out/'footprint_audit.json').write_text(json.dumps(dict(issues=issues,components=audit),indent=2)+'\n')
print('\n'.join(issues) if issues else 'All electrical symbol pin numbers match footprint pad sets.')
if issues:raise SystemExit(1)
