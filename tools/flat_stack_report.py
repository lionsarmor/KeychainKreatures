"""Small, printable mechanical review sheet; no manufacturing output."""
from pathlib import Path
import json, hashlib, csv, html, base64, subprocess
# Dependency-free SVG pages; existing Inkscape/Poppler tools produce the PDF.
mm=1;A4=(210,297)
class Canvas:
    def __init__(self,path,pagesize):
        self.path=Path(path);self.parts=[];self.pdfs=[];self.font=10;self.color='black';self.stroke=.2;self.dash=''
    def setFont(self,name,size):self.font=size*.352778
    def drawString(self,x,y,t):self.parts.append(f'<text x="{x}" y="{297-y}" font-family="sans-serif" font-size="{self.font}" fill="black">{html.escape(t)}</text>')
    def setLineWidth(self,w):self.stroke=w
    def setStrokeColorRGB(self,r,g,b):self.color=f'rgb({round(r*255)},{round(g*255)},{round(b*255)})'
    def setDash(self,*args):self.dash=','.join(map(str,args))
    def style(self):return f'fill="none" stroke="{self.color}" stroke-width="{self.stroke}" stroke-dasharray="{self.dash}"'
    def roundRect(self,x,y,w,h,r,**kw):self.parts.append(f'<rect x="{x}" y="{297-y-h}" width="{w}" height="{h}" rx="{r}" {self.style()}/>')
    def rect(self,x,y,w,h,**kw):self.roundRect(x,y,w,h,0)
    def circle(self,x,y,r,**kw):self.parts.append(f'<circle cx="{x}" cy="{297-y}" r="{r}" {self.style()}/>')
    def line(self,x1,y1,x2,y2):self.parts.append(f'<line x1="{x1}" y1="{297-y1}" x2="{x2}" y2="{297-y2}" {self.style()}/>')
    def drawImage(self,path,x,y,width,height,**kw):
        data=base64.b64encode(Path(path).read_bytes()).decode()
        self.parts.append(f'<image x="{x}" y="{297-y-height}" width="{width}" height="{height}" href="data:image/png;base64,{data}"/>')
    def showPage(self):
        if not self.parts:return
        stem=self.path.with_name(self.path.stem+f'-{len(self.pdfs)+1}')
        svg=stem.with_suffix('.svg');pdf=stem.with_suffix('.pdf')
        svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">'+'\n'.join(self.parts)+'</svg>')
        subprocess.run(['inkscape',str(svg),'--export-type=pdf','--export-filename='+str(pdf)],check=True,capture_output=True)
        self.pdfs.append(pdf);self.parts=[]
    def save(self):
        self.showPage();subprocess.run(['pdfunite',*[str(p) for p in self.pdfs],str(self.path)],check=True)

ROOT=Path(__file__).resolve().parent.parent
MAIN=ROOT/'KK_main_module/C6_flat_stack';POWER=ROOT/'KK_power_module/P3_matching_stack'
OUT=ROOT/'docs/C6_P3_STACK_REVIEW.pdf'
c=Canvas(str(OUT),pagesize=A4)
def line(t,x,y,size=10):
    c.setFont('Helvetica',size);c.drawString(x*mm,y*mm,t)
def page(title):
    line(title,12,284,15);line('C.6 / P.3 PROTOTYPE REVIEW - PHYSICAL / BENCH QUALIFICATION PENDING',12,276,9)

page('Keychain Kreatures - flat, removable board stack')
line('Shared outline: 96 x 105 mm; 4 mm corner radius; 1.6 mm PCB.',12,265)
line('Four 2.2 mm clearance holes: (4,4), (92,4), (4,101), (92,101) mm.',12,259)
line('Coordinates below: top-left origin, X right, Y down. Both boards use this pattern.',12,253,9)
x0,y0=55*mm,131*mm
c.setLineWidth(.2*mm);c.roundRect(x0,y0,96*mm,105*mm,4*mm,stroke=1,fill=0)
for x,y in [(4,4),(92,4),(4,101),(92,101)]:c.circle(x0+x*mm,y0+(105-y)*mm,1.1*mm,stroke=1,fill=0)
c.setStrokeColorRGB(.7,.1,.1);c.setDash(2,2)
c.rect(x0+18*mm,y0+(105-38)*mm,60*mm,38*mm,stroke=1,fill=0)
c.setDash();c.setStrokeColorRGB(0,0,0)
line('ANTENNA: NO METAL / CELL / WIRES',77,218,7)
line('Common mounting template - 1:1',70,174,9)
line('100 mm calibration line:',12,121,9)
c.line(12*mm,116*mm,112*mm,116*mm)
c.line(12*mm,114*mm,12*mm,118*mm);c.line(112*mm,114*mm,112*mm,118*mm)
line('PRINT AT 100% / ACTUAL SIZE. Disable fit-to-page. Measure the line first.',12,107,9)
for i,t in enumerate([
 'Stack orientation: main display/buttons outward at the front of the case.',
 'Power component side faces the rear cover; its test-pad face points toward main.',
 'Power-board front view is X-mirrored relative to main-front physical coordinates.',
 'Start a fit mock-up with FOUR 20 mm M2 insulating standoffs between PCB faces.',
 'This spacing is provisional: check plugged JST bodies, cable bends and solder tails.',
 'Clip solder tails to <=2.5 mm, inspect every joint, and keep loose wires restrained.',
 'Unscrew and unplug the rear power board to expose the student main-board parts.',
 'Do not trap a battery between solder tails and components. Cell position is not frozen.',
 'Keep a protective insulating barrier; never use battery foil as an electrical insulator.'
]):line(t,12,94-i*6,9)
c.showPage()
page('Flat parts and assembly limits')
rows=[('R1-R43','Existing Yageo MFR-25 values','All horizontal, 10.16 mm lead pitch'),
      ('C1,C3,C5,C13,C17,C25','Panasonic ECEA1CKA101','100 uF / 16 V; max flat height 7.3 mm*'),
      ('C9,C11,C15,C21','Panasonic ECEA1CKA100','10 uF / 16 V; max flat height 5.0 mm*'),
      ('Q1-Q6','Existing exact transistor MPNs','Flat marked face up; preserve pin order')]
y=263
for ref,part,note in rows:
    line(ref,12,y,10);line(part,12,y-6,10);line(note,12,y-12,9);y-=24
for i,t in enumerate([
 '* Manufacturer maximum can diameter plus 0.5 mm insulating support; not scaled artwork.',
 'Both capacitor types use the full 8 mm maximum body-length courtyard.',
 'Capacitor square pad 1 is POSITIVE. Sleeve stripe marks NEGATIVE pad 2.',
 '10 uF native lead pitch is 1.5 mm: form to the 2.54 mm PCB pitch without crossing.',
 'Support leads at the seal while bending; do not pull, twist, or stress the rubber seal.',
 'Use nonconductive support under horizontal cans. Do not obstruct the pressure vent.',
 'TO-92 bodies extend toward the footprint body rectangle; marked flat face stays up.',
 'Q6 is LP0701N3-G, not BC327. Verify actual pinout before forming or soldering.',
 'IR lenses must still face the case opening; optical parts are not flattened blindly.',
 'Sockets, screen, buttons and the front RGB retain their actual functional height.',
 'The socketed ESP32 rear envelope is about 15.3 mm; it, not the caps, limits spacing.',
 'The socketed RGB front envelope remains about 22.1 mm. Case depth is NOT final.',
 'Power board remains a factory-assembled SMT subassembly, not a student SMT kit.'
]):line(t,12,160-i*6,9)
line('Prototype checks still required',12,69,12)
for i,t in enumerate([
 'Measure delivered screen, ESP32, SD module, sockets, plugs and standoffs.',
 'Check horizontal capacitor ripple/rail transients during Wi-Fi, audio and motor bursts.',
 'Check component temperatures, charging, rail sequencing and battery protection.',
 'Confirm antenna performance with the actual rear board, battery, harness and case.',
 'Prototype files issued separately; approve physical fit and factory DFM before ordering.'
]):line(t,12,60-i*6,9)
c.showPage()
page('Main-board rear - populated mechanical preview')
preview=MAIN/'reports/main_back.png'
if preview.exists():c.drawImage(str(preview),10*mm,57*mm,width=190*mm,height=190*mm,preserveAspectRatio=True)
line('Preview is not a powered test. Seller-module envelopes and formed leads need sample checks.',12,43,9)
line('Use C6_flat_stack and P3_matching_stack, not the old manufacturing ZIPs.',12,36,9)
c.showPage()
page('Power-board rear-cover side - matching outline')
preview=POWER/'reports/power_front.png'
if preview.exists():c.drawImage(str(preview),10*mm,57*mm,width=190*mm,height=190*mm,preserveAspectRatio=True)
line('Routed power core preserved. Empty upper antenna region must stay clear of metal.',12,49,9)
line('Power J3 -> main J1: 1=5V, 2=GND, 3=3.3V, 4=3.2V. Keyed pin-to-pin harness.',12,42,9)
line('This is the power FRONT view; mirror X to compare with the main FRONT in the stack.',12,35,9)
c.save()
print(OUT)
