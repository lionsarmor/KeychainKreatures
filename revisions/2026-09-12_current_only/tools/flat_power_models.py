"""Repair missing P3 model links with documented project-owned envelopes."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent.parent
source=ROOT/'KK_main_module/pcb/c4_build_models.py'
helpers=source.read_text().split('# Manufacturer maximum body envelope;')[0]
helpers=helpers.replace("root=Path(__file__).resolve().parent.parent;out=root/'3dmodels'", "root=ROOT/'KK_power_module/P3_matching_stack';out=root/'3dmodels'")
exec(compile(helpers,str(source),'exec'))
src=ROOT/'KK_power_module/P2_compact/datasheets'
for name in ['JST_VH.pdf','HC-TYPE-C-16P-01A.pdf','XFL4020-102MEC.pdf','TPS259530DSGR.pdf','BQ24075TRGTR.pdf','TUSB320LAIRWBR.pdf','TPS63060DSCR.pdf','TPS386000RGPR.pdf']:
    shutil.copy2(src/name,root/'datasheets'/name)
shutil.copy2(src/'TPS22950YBHR.pdf',root/'datasheets/TPS22950YBHR.pdf')

# USB nominal footprint center; maximum shell size from the HCTL drawing.
shell=box(-4.545,-3.75,0,9.09,7.5,3.36).cut(box(-3.7,-2.75,.45,7.4,6.6,2.35))
p=[(shell,METAL),(box(-3.25,-2.2,1.3,6.5,5.7,.7),BLACK)]
for x in [-4.32,4.32]:
    for y in [-2.75,1.43]:p.append((box(x-.18,y-.35,-2.5,.36,.7,2.6),METAL))
save('P3_USB_HCTL_envelope',p,'datasheets/HC-TYPE-C-16P-01A.pdf','manufacturer MAX shell + simplified contacts','9.09 x 7.5 x 3.36mm shell envelope includes tolerance. Mouth local +Y. Tabs and cavities simplified; trimmed tails 2.5mm. Check actual mating cable and case recess.')

# JST VH B2P-VH: pitch3.96, width7.86, front-back envelope8.5, height10.9.
p=[(box(-1.95,-2,0,7.86,6.8,2.5),WHITE),(box(-.75,-3.7,0,5.46,1.7,10.9),WHITE)]
for x in [0,3.96]:p.append((box(x-.57,-.57,-2.5,1.14,1.14,12.7),METAL))
save('P3_JST_VH2_envelope',p,'datasheets/JST_VH.pdf, header drawing page3','manufacturer nominal header envelope','B2P-VH top-entry; pin1 at local(0,0), pin2(3.96,0). Housing/latch/contact detail simplified. 10.9mm header height DOES NOT include mating plug or wire bend. Trimmed tails2.5mm.')

p=[(box(-4.5,-1.8,0,9,3.6,3.5),METAL),(box(-4.2,-1.5,3.05,8.4,3,.4),BLACK),(box(-2,1.8,.8,1.5,2,1.5),BLACK)]
save('P3_JS102_envelope',p,'https://www.littelfuse.com/assetdocs/littelfuse-ck-slide-js-series-datasheet?assetguid=aba42b08-0d2c-423b-813d-a2faa5a3bb14, page4','manufacturer nominal envelope','JS102011SAQN: 9 x3.6 x3.5mm body, 2mm side actuator/travel area. Actuator illustrated in one position; retain full sweep and finger/case clearance.')

p=[(box(-2.15,-2.15,.1,4.3,4.3,2),(.19,.19,.2))]
for y in [-1.625,1.625]:p.append((box(-.785,y-.41,0,1.57,.82,.12),METAL))
save('P3_XFL4020_max',p,'datasheets/XFL4020-102MEC.pdf, drawing document745-3','manufacturer maximum body envelope','4.0 +/-0.3mm square; 2.10mm maximum mounted height. Winding and terminal detail simplified; not a substitute inductor.')

for name,d,h,sourcefile,confidence in [
 ('P3_RGT16_max',3.1,1,'BQ24075TRGTR.pdf','manufacturer maximum body'),
 ('P3_DSG8_max',2.1,.8,'TPS259530DSGR.pdf','manufacturer maximum body'),
 ('P3_RWB12_max',1.65,.4,'TUSB320LAIRWBR.pdf','manufacturer maximum body'),
 ('P3_DSC10_envelope',3.15,1.1,'TPS63060DSCR.pdf','conservative package envelope'),
 ('P3_RGP20_envelope',4.1,1.1,'TPS386000RGPR.pdf','conservative package envelope')]:
    p=[(box(-d/2,-d/2,.05,d,d,h),BLACK),(cylinder(-d/2+.25,-d/2+.25,h+.05,.1,.01),GREY)]
    save(name,p,'datasheets/'+sourcefile,confidence,'Package body +0.05mm solder stand-off. Pin1 dot illustrative; use footprint/pad1 and manufacturer pinout for orientation. Contacts/thermal pad omitted from model; electrical pads unchanged.')
p=[(box(-.363,-.563,.16,.726,1.126,.24),BLACK),(cylinder(-.2,-.4,.4,.045,.005),GREY)]
for x in [-.2,.2]:
    for y in [-.4,0,.4]:p.append((Part.makeSphere(.1,V(x,-y,.1)),METAL))
save('P3_YBH6_max',p,'datasheets/TPS22950YBHR.pdf, drawing4226594/A','manufacturer maximum body envelope','0.726 x1.126 x0.4mm DSBGA envelope, six0.4mm-pitch balls. Ball detail nominal; A1 marker agrees with footprint. Factory assembly only.')
(out/'P3_MODEL_REPAIR_MANIFEST.json').write_text(json.dumps(models,indent=2)+'\n')
print('Ten missing model families rebuilt; baseline models untouched.')
