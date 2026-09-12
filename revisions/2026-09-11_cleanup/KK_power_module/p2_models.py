"""Collect exact KiCad library models; report missing models instead of guessing."""
from pathlib import Path
import re,json,urllib.request,concurrent.futures,shutil,hashlib
out=Path(__file__).resolve().parent/'P2_compact';dest=out/'3dmodels';dest.mkdir(exist_ok=True)
roots=list(Path('/home/legion/.local/share/flatpak/runtime/org.kicad.KiCad.Library.Packages3D/x86_64/stable').glob('*/files/3dmodels'))
names=set()
for fp in (out/'KK_Power.pretty').glob('*.kicad_mod'):
    names.update(re.findall(r'\(model "\$\{KICAD10_3DMODEL_DIR\}/([^"]+)"',fp.read_text()))
names.add('Package_TO_SOT_SMD.3dshapes/SOT-23-6.step')
def fetch(name):
    target=dest/name;target.parent.mkdir(exist_ok=True)
    row={'model':name,'source':'https://gitlab.com/kicad/libraries/kicad-packages3D/-/raw/master/'+name}
    try:
        if not target.exists():
            local=next((root/name for root in roots if (root/name).exists()),None)
            if local:shutil.copy2(local,target);row['source']='Installed KiCad Packages3D library: '+name
            else:
                with urllib.request.urlopen(row['source'],timeout=12) as r:data=r.read()
                assert b'ISO-10303' in data[:1000], 'Not STEP'
                target.write_bytes(data)
        row.update(saved=True,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    except Exception as e:row.update(saved=False,error=str(e))
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,sorted(names)))
(dest/'MANIFEST.json').write_text(json.dumps(rows,indent=2)+'\n')
(dest/'README.md').write_text('Exact KiCad library models, when available. Models are nominal visualization aids, not enclosure approval. Source and hashes in MANIFEST.json. KiCad library assets use CC-BY-SA-4.0 with its library exception: https://www.kicad.org/libraries/license/ . Missing models are explicitly recorded. FS8205 uses the SOT-23-6 family body model, not a vendor-specific marking model.\n')
print('Models available:',sum(r['saved'] for r in rows),'/',len(rows))
