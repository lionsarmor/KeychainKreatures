"""Nominal rear-mounted TSAL6200 with formed leads, aimed toward top edge."""
from pathlib import Path
import ast,json
src=Path(__file__).with_name('c4_build_models.py')
tree=ast.parse(src.read_text())
# Reuse CAD helpers without regenerating or overwriting the C.4 model set.
nodes=[]
for n in tree.body:
 if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)):nodes.append(n)
 elif isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) for t in n.targets) and any(t.id in ['V','BLACK','BLUE','models'] for t in n.targets):nodes.append(n)
 elif isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='sys.path.append':nodes.append(n)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'))
root=src.parent.parent;out=root/'3dmodels';METAL=(.7,.72,.74)
parts=[]
for s,c in led_body(1.27,1,2.5,2.9,8.7,(.16,.18,.22)):
 s.rotate(V(0,0,0),V(1,0,0),90);s.translate(V(0,0,5));parts.append((s,c))
for x in [0,2.54]:
 parts.extend([(lead((x,0,-2.5),(x,0,5),.25),METAL),(lead((x,0,5),(x,1,5),.25),METAL)])
save('TSAL6200_C5_edge_formed',parts,'Vishay TSAL6200 body drawing; proposed hand-formed leads','PROVISIONAL assembly geometry','Rear footprint angle 0: lens points to board top (-Y). 5mm axis height from rear surface, 1mm horizontal base offset. Do not bend at epoxy; qualify sample and optical opening. Not a factory lead-form variant.')
(root/'C5_relayout/IR_MODEL.json').write_text(json.dumps(models,indent=2))
