"""Project-owned nominal 3D assemblies. No electronic or footprint geometry edits.
Run with /usr/bin/python3 (FreeCAD library installed). VRML colors + STEP twins.
Dimensions are in mm; public helpers accept footprint X/Y (Y down), Z above PCB.
Do not interpret seller-module approximations as qualified enclosure drawings.
"""
from pathlib import Path
import sys,json,math,hashlib
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as A,Part
root=Path(__file__).resolve().parent.parent;out=root/'3dmodels';out.mkdir(exist_ok=True)
V=A.Vector
BLACK=(.055,.06,.065);METAL=(.7,.72,.74);GOLD=(.82,.61,.18);WHITE=(.87,.89,.88)
BLUE=(.025,.12,.34);PCB=(.035,.16,.13);GREY=(.45,.47,.48)
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,-y-d,z))
def cylinder(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,-y,z))
def lead(a,b,r=.25):
    p=V(a[0],-a[1],a[2]);q=V(b[0],-b[1],b[2]);v=q-p
    return Part.makeCylinder(r,v.Length,p,v)
models=[]
def save(name,pieces,source,confidence,notes):
    solid=Part.makeCompound([s for s,c in pieces]);Part.export([solid],str(out/(name+'.step')))
    vrml=['#VRML V2.0 utf8','# Project-owned nominal model; units 0.1 inch for KiCad.']
    for shape,color in pieces:
        vertices,faces=shape.tessellate(.07)
        verts=',\n'.join(' '.join(f'{v[i]/2.54:.6f}' for i in range(3)) for v in vertices)
        inds=',\n'.join(' '.join(map(str,f))+' -1' for f in faces)
        vrml.append('Shape { appearance Appearance { material Material { diffuseColor '+' '.join(map(str,color))+' } } geometry IndexedFaceSet { solid FALSE coord Coordinate { point [ '+verts+' ] } coordIndex [ '+inds+' ] } }')
    (out/(name+'.wrl')).write_text('\n'.join(vrml)+'\n')
    b=solid.BoundBox
    models.append({'name':name,'source':source,'confidence':confidence,'notes':notes,'local_bounds_mm':[b.XMin,-b.YMax,b.ZMin,b.XMax,-b.YMin,b.ZMax],'sha256':{ext:hashlib.sha256((out/(name+ext)).read_bytes()).hexdigest() for ext in ['.wrl','.step']}})
    print(name,flush=True)

# Manufacturer maximum body envelope; deliberately not a random generic capacitor.
p=[(box(-.635,-1.27,1,3.81,2.54,3.14),(.67,.4,.14))]
p += [(cylinder(x,0,-2.5,.255,3.6),METAL) for x in [0,2.54]]
save('KEMET_C315_max',p,'component_review/datasheets/kemet-100nf.pdf; kemet-10nf.pdf; kemet-1uf.pdf','manufacturer body envelope','3.81 x 2.54 x 3.14 max body; illustrative 1mm board standoff and trimmed tails.')

p=[(cylinder(1,0,.5,2.5,11),BLUE),(cylinder(1,0,11.5,2.25,.05),METAL)]
# Negative side stripe is at pad2 (x=2mm), not at positive pad1.
stripe=cylinder(1,0,.5,2.515,10.9).common(box(2.85,-2.6,.5,1,5.2,11))
p.append((stripe,WHITE));p.extend((cylinder(x,0,-2.5,.25,3.1),METAL) for x in [0,2])
save('Nichicon_UVR_D5_H11',p,'component_review/datasheets/nichicon-uvr.pdf','manufacturer nominal envelope','5mm body diameter, 11mm body length; illustrative 0.5mm seating gap.')

# Soft silicone tactile switch, not the unrelated hard-click 6mm tact model.
p=[(box(-3.9,-3.9,0,7.8,7.8,3),BLACK),(cylinder(0,0,3,3.35,.25),GREY),
   (Part.makeCone(2.65,1.75,1.25,V(0,0,3.25)),GREY),(cylinder(0,0,4.5,1.75,1),GREY)]
for x in [-4,4]:
    for y in [-2.25,2.25]:p.append((box(x-.15,y-.35,-2.5,.3,.7,4),METAL))
save('Adafruit3101_soft',p,'component_review/datasheets/soft-buttons.png','manufacturer drawing nominal','7.8mm square body; 5.5mm total height from drawing. Seller 4.9mm conflicts; sample required. Leads simplified.')

def socket(pins,x0=0,y0=0,z=0):
    p=[];body=box(x0-1.27,y0-1.525,z,2.54,pins*2.54+.51,8.5)
    for i in range(pins):body=body.cut(box(x0-.4,y0+i*2.54-.4,z+7.5,.8,.8,1.1))
    p.append((body,BLACK))
    for i in range(pins):
        p.append((box(x0-.32,y0+i*2.54-.32,z-2.5,.64,.64,2.5),METAL))
    return p
def male(pins,x0=0,y0=0,z=8.5):
    p=[(box(x0-1.27,y0-1.27,z,2.54,pins*2.54,2.54),BLACK)]
    for i in range(pins):p.append((box(x0-.32,y0+i*2.54-.32,z-5.5,.64,.64,9),GOLD))
    return p
for n in [6,8,9]:
    save('Sullins_LFB_'+str(n),socket(n),'component_review/datasheets/sullins-female-headers.pdf','manufacturer housing envelope','8.50mm housing; cavities/contact detail and trimmed tail length illustrative.')

# Socket and IC depicted together. Internal contact mechanics are simplified.
for n in [8,16,28]:
    count=n//2;length=count*2.54;cy=(count-1)*2.54/2
    frame=box(-1.27,-1.27,0,10.16,length,5.2)
    frame=frame.cut(box(1.1,.3,0,5.42,max(length-3.14,.5),5.3))
    for x in [0,7.62]:
        for j in range(count):frame=frame.cut(cylinder(x,j*2.54,4.1,.55,1.2))
    chip=box(.51,cy-(length-.63)/2,5.7,6.6,length-.63,3.3)
    chip=chip.cut(cylinder(3.81,-1.2,8.5,1,.6))
    p=[(frame,BLACK),(chip,(.1,.105,.11)),(cylinder(1.35,-.1,8.98,.35,.04),GREY)]
    for x in [0,7.62]:
        for j in range(count):
            y=j*2.54;p.append((box(x-.25,y-.15,-2.5,.5,.3,2.5),METAL))
            p.append((box(x-.25,y-.15,3,.5,.3,3.5),METAL))
            p.append((lead((x,y,6.5),(.51 if x==0 else 7.11,y,6.5),.15),METAL))
    save('Socketed_DIP'+str(n),p,'component_review/datasheets/dip-sockets.pdf; IC package drawings','nominal socket + generic DIP family','On Shore socket envelope; generic IC detail and illustrative seated height 9mm. Not vendor mating-stack certification.')

# IR receiver lens faces +Y in footprint, in agreement with its F.Fab marker.
p=[(box(.04,-1.4,2,5,2.8,8.25),(.06,.04,.07))]
lens=Part.makeSphere(2,V(2.54,-1.4,6.125)).common(box(.04,1.4,2,5,2,8.25))
p.append((lens,(.13,.06,.13)))
for x in [0,2.54,5.08]:p.append((box(x-.3,-.25,-2.5,.6,.5,5.8),METAL))
save('TSOP38238',p,'component_review/datasheets/tsop382.pdf','manufacturer body envelope','5 x 4.8 x 8.25mm body/lens envelope; selected 2mm seating gap; lead shape simplified.')

def led_body(cx,base,r,flange,height,color):
    body=cylinder(cx,0,base,flange,1).fuse(cylinder(cx,0,base+1,r,height-r-1))
    dome=Part.makeSphere(r,V(cx,0,base+height-r)).common(box(cx-r,-r,base+height-r,2*r,2*r,r))
    return [(body.fuse(dome),color)]
p=led_body(1.27,1,2.5,2.9,8.7,(.16,.18,.22))
p.extend((box(x-.25,-.25,-2.5,.5,.5,3.5),METAL) for x in [0,2.54])
save('TSAL6200_IR',p,'component_review/datasheets/tsal6200.pdf','manufacturer nominal envelope','5mm IR lens, 5.8mm flange, 8.7mm height; grey unpowered appearance, not visible red emission.')

p=led_body(3.81,5,2.5,2.95,8.6,WHITE)
for i in range(4):
    x=i*2.54;native=3.81+(i-1.5)*1.27
    p.append((lead((x,0,-2.5),(x,0,1),.25),METAL))
    p.append((lead((x,0,1),(native,0,2.5),.25),METAL))
    p.append((lead((native,0,2.5),(native,0,5),.25),METAL))
save('Kingbright_RGB_formed',p,'component_review/datasheets/rgb-wp154a4sej3vbdzgw-ca.pdf','manufacturer lens + proposed formed leads','White-diffused 5mm lens, 5.9mm flange, 8.6mm height. 5mm standoff reserves straight lead below body before forming; fixture/sample qualification required.')

# Socket under the LED; electrical pin order is unchanged. Contact retention
# with the purchased LED batch is explicitly unqualified (not a header pin).
sp=[]
for s,c in socket(4):
    s.rotate(V(0,0,0),V(0,0,1),90);sp.append((s,c))
for s,c in p:
    s=s.copy();s.translate(V(0,0,8.5));sp.append((s,c))
save('Kingbright_RGB_socketed',sp,'Kingbright PDF + Sullins LFB drawing','nominal assembly; CONTACT FIT PENDING','Sullins PPTC041LFBN-RC 8.5mm housing under formed LED; lens top 22.1mm. Actual LED lead fit/retention must be verified; do not force or tin mating portions.')

# Purchased modules: controlled mechanical CAD was not available. Explicitly
# label these envelopes provisional, and do not invent individual SMD parts.
p=socket(9,-7.62,-10.16)+socket(9,7.62,-10.16)+male(9,-7.62,-10.16)+male(9,7.62,-10.16)
board=box(-9,-11.75,11.04,18,23.5,1)
for x in [-7.62,7.62]:
    for j in range(9):board=board.cut(cylinder(x,-10.16+j*2.54,10.9,.5,1.4))
p += [(board,(.07,.075,.085)),(box(-3.5,-3,12.04,7,7,1),BLACK),
      (box(-3.5,8,12.04,7,2.5,1.1),(.65,.22,.2))]
usb=box(-4.47,-13,12.04,8.94,7.5,3.2).cut(box(-3.6,-13.1,12.54,7.2,6.7,2))
p.append((usb,METAL));p.append((box(-3.1,-12.5,13.25,6.2,5,.5),BLACK))
for x in [-5,5]:p.extend([(box(x-1.5,-4,12.04,3,3,1.5),METAL),(cylinder(x,-2.5,13.54,.9,.5),BLACK)])
save('SuperMini_socketed_envelope',p,'User footprint + seller photo; component_review/MODULE_SOURCE_NOTES.md','PROVISIONAL seller-module envelope','18 x 23.5mm outline from user footprint; 1mm PCB assumed, SMD detail approximate. Socket 8.5mm + header 2.54mm; USB at -Y local. Verify delivered revision and engagement.')

# Screen header is horizontal on the carrier after 90deg footprint rotation.
# Panel extends in local -X; panel faces the viewer, header at top of device.
p=socket(8)+male(8)
p += [(box(-46,-6.61,11.04,48,31,1.2),PCB),
      (box(-43,-4.6,12.24,42,27,1.5),BLACK),
      (box(-37,-4.95,13.74,32.34,27.72,.2),(.045,.065,.08))]
save('XIITIA_screen_socketed_envelope',p,'component_review/MODULE_SOURCE_NOTES.md','PROVISIONAL seller-module envelope','31 x 48mm seller board; header-to-edge 2mm, PCB/panel thickness and optical aperture provisional. No display image implies running firmware. Includes actual nominal socket/header stack.')

p=socket(6)+male(6)
p += [(box(-1.5,-2.6,11.04,17.9,17.9,1.2),(.035,.1,.33))]
shell=box(2,-.15,12.24,14.4,14.5,1.5).cut(box(2.8,.45,12.24,13.7,13.3,1.1))
p += [(shell,METAL),(box(5,1.6,12.24,12,11,.8),BLACK)]
save('GODIYMODULES_SD_socketed_envelope',p,'component_review/source_evidence/sd-pinout.jpg; sd-dimensions.jpg','PROVISIONAL seller-module envelope','17.9mm square seller outline. Header offset, thickness and socket height approximate. Card extends +X for insertion access; verify actual orientation before soldering.')

(out/'MODEL_MANIFEST.json').write_text(json.dumps(models,indent=2)+'\n')
print('Created',len(models),'STEP/VRML pairs. Provisional dimensions explicitly recorded.')
