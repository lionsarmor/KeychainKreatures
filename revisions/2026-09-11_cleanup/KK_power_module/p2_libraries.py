"""Local P.2 libraries, including documented USB land corner refinement."""
from pathlib import Path
s=Path(__file__).with_name('p1_libraries.py').read_text().replace("with_name('p1_design.py')","with_name('p2_design.py')")
s=s[:s.index('# Exposed-pad thermal holes')]+s[s.index("(out/'datasheets/sources.json')"):]
exec(compile(s,str(Path(__file__).with_name('p1_libraries.py')),'exec'),globals())
# Ground contacts keep the same centre and width/length. Rounded ends increase
# their copper clearance to the locating holes without altering mechanical fit.
usb=d.parse((local/'USB_C_HCTL.kicad_mod').read_text())
for pad in d.kids(usb,'pad'):
    if d.val(pad[1]) in ['A1','A12','B1','B12']:
        d.child(pad,'roundrect_rratio')[1]='0.5'
(local/'USB_C_HCTL.kicad_mod').write_text(d.dump(usb)+'\n')
