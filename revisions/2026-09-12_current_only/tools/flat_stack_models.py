"""Project-owned maximum-envelope flat parts, host FreeCAD, one CPU."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
source=ROOT/'KK_main_module/pcb/c4_build_models.py'
helpers=source.read_text().split('# Manufacturer maximum body envelope;')[0]
helpers=helpers.replace("root=Path(__file__).resolve().parent.parent;out=root/'3dmodels'", "root=ROOT/'KK_main_module/C6_flat_stack';out=root/'3dmodels'")
exec(compile(helpers,str(source),'exec'))
for name,diam,pitch,native,start in [('KA_100u_horizontal_max',6.8,2.5,2.5,3),('KA_10u_horizontal_max',4.5,2.54,1.5,4)]:
    cx=pitch/2;z=.5+diam/2
    body=Part.makeCylinder(diam/2,8,V(cx,-start,z),V(0,-1,0))
    stripe=Part.makeCylinder(diam/2+.015,7.9,V(cx,-start,z),V(0,-1,0)).common(box(cx+diam/2-.55,start,.5,1,8,diam))
    pieces=[(body,BLUE),(stripe,WHITE)]
    # Insulating support is an assembly requirement, not an electrical part.
    pieces.append((box(cx-1,start+1,0,2,5,.5),(.32,.32,.32)))
    for n in range(2):
        a=(n*pitch,0,-2.5);b=(n*pitch,0,z);c=(cx+(n-.5)*native,start,z)
        pieces.extend([(lead(a,b,.225),METAL),(lead(b,c,.225),METAL)])
    save(name,pieces,'datasheets/Panasonic_KA_A.pdf, 01-Sep-2025, pp1-2','manufacturer MAXIMUM can envelope + proposed lead form','ECEA1CKA101 / ECEA1CKA100; unchanged 16V. Sideways D+0.5mm and L+1mm envelope, 0.5mm insulating support, 2.5mm trimmed tails. Native 1.5mm leads spread for 10u. Seal-supported forming and ripple qualification required.')

# Conservative TO-92 envelope, flat face +Z. No claim of vendor-exact curved mold.
pieces=[(box(-.16,-9.4,.5,5.4,5.4,4.5),BLACK)]
for n in range(3):
    pieces.extend([(lead((n*2.54,0,-2.5),(n*2.54,0,2),.25),METAL),
                   (lead((n*2.54,0,2),(1.27+n*1.27,-4,2),.25),METAL)])
save('TO92_horizontal_envelope',pieces,'Existing per-device TO-92 datasheets; worst-case family envelope','CONSERVATIVE envelope; sample lead forming required','Body local -Y, marked flat face up, no pin swapping; 4mm lead form run. Keep full body area free of copper exposure and other parts.')
(out/'C6_flat_models_manifest.json').write_text(json.dumps(models,indent=2)+'\n')
print('Flat-part STEP and VRML models generated; no baseline model overwritten.')
