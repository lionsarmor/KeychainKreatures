"""Export candidate-footprint geometry for vectorized, conservative THT placement."""
from pathlib import Path
import json,pcbnew as k
root=Path(__file__).resolve().parent.parent;out=root/'C5_relayout'
b=k.LoadBoard(str(out/'C5_blank.kicad_pcb'))
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
def bounds(g):
 q=g.GetBoundingBox();return [k.ToMM(q.GetX()),k.ToMM(q.GetY()),k.ToMM(q.GetRight()),k.ToMM(q.GetBottom())]
d={}
front={'J2','D3',*[f'SW{i}' for i in range(1,10)]}
for f in b.GetFootprints():
 r=f.GetReference();side='front' if r in front else 'back'
 if (f.GetLayer()==k.F_Cu)!=(side=='front'):f.Flip(f.GetPosition(),k.FLIP_DIRECTION_LEFT_RIGHT)
 variants={}
 for a in [0,90,180,270]:
  f.SetOrientationDegrees(a);f.SetPosition(v(0,0))
  boxes=[bounds(g) for g in f.GraphicalItems() if g.GetLayer() in (k.F_CrtYd,k.B_CrtYd)]
  if not boxes:boxes=[bounds(p) for p in f.Pads()]
  bb=[min(q[0] for q in boxes),min(q[1] for q in boxes),max(q[2] for q in boxes),max(q[3] for q in boxes)]
  variants[a]={'box':bb,'pads':[{'pin':p.GetNumber(),'net':p.GetNetname(),'xy':xy(p.GetPosition()),'box':bounds(p)} for p in f.Pads()]}
 d[r]={'side':side,'variants':variants,'value':f.GetValue(),'footprint':str(f.GetFPID())}
(out/'geometry.json').write_text(json.dumps(d,indent=2))
print('Exported',len(d),'footprint variants')
