"""Preserve the last power design; work in an explicit unreleased P.1 revision."""
from pathlib import Path
import hashlib,json,shutil,subprocess,urllib.request
root=Path(__file__).resolve().parent
out=root/'P1_revision'; out.mkdir(exist_ok=True)
backup=root/'backups'/'pre_P1'; backup.mkdir(parents=True,exist_ok=True)
files=['KK_power_module.kicad_sch','KK_power_module.kicad_pcb','KK_power_module.kicad_pro','KK_power_module.kicad_sym','FS8205.kicad_sym','fp-lib-table','sym-lib-table']
for n in files:
    if not (backup/n).exists(): shutil.copy2(root/n,backup/n)
if not (backup/'manufacturing').exists(): shutil.copytree(root/'manufacturing',backup/'manufacturing')
if not (backup/'FS8205.pretty').exists(): shutil.copytree(root/'FS8205.pretty',backup/'FS8205.pretty')
meta={'source_sha256':{n:hashlib.sha256((backup/n).read_bytes()).hexdigest() for n in files},'libraries':{}}
for kind,folder in [('Symbols','symbols'),('Footprints','footprints'),('Packages3D','3dmodels')]:
    loc=subprocess.check_output(['flatpak','info','--show-location','org.kicad.KiCad.Library.'+kind],text=True).strip()
    meta['libraries'][kind]=loc+'/files/'+folder
(out/'stage.json').write_text(json.dumps(meta,indent=2)+'\n')
(out/'datasheets').mkdir(exist_ok=True)
urls={name:'https://www.ti.com/lit/ds/symlink/'+name+'.pdf' for name in ['bq24074','tusb320lai','tps63070','tps63802','tlv3012','tps22919']}
for name,url in urls.items():
    p=out/'datasheets'/(name+'.pdf')
    if not p.exists():
        try:
            with urllib.request.urlopen(url,timeout=10) as r: data=r.read()
            assert data.startswith(b'%PDF'),name
            p.write_bytes(data)
        except Exception as e:
            print('PDF download unavailable; retain verified primary-source URL:',name,type(e).__name__)
    if p.exists(): subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
(out/'datasheets'/'sources.json').write_text(json.dumps(urls,indent=2)+'\n')
print('Protected original in',backup,'; P.1 workspace:',out)
