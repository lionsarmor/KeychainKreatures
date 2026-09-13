"""Package documentation supplements only; keep issued hardware ZIPs immutable."""
from pathlib import Path
import hashlib,json,re,subprocess,tempfile,zipfile
from markdown_it import MarkdownIt
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'docs/troubleshooting'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
report=json.loads((OUT/'GUIDE_VERIFICATION.json').read_text())
for p,h in report['source_and_issued_packages_unchanged'].items():assert sha(ROOT/p)==h,p
for p,h in report['artifacts'].items():assert sha(ROOT/p)==h,p
template=OUT/'FACTORY_FAULT_REPORT.md'
style=re.search(r'<style>([\s\S]*?)</style>',(ROOT/'KK_main_module/assembly/TROUBLESHOOTING_MAIN_C6.html').read_text()).group(1)
html=template.with_suffix('.html');pdf=template.with_suffix('.pdf')
html.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Factory fault report</title><style>'+style+'</style></head><body>'+MarkdownIt('commonmark').enable('table').render(template.read_text())+'</body></html>')
subprocess.run(['python3',str(ROOT/'tools/print_guide_pdf.py'),str(html),str(pdf),'C6 / P4 factory fault report'],check=True,timeout=60)
included=[ROOT/p for p in report['artifacts']]+[template,html,pdf,OUT/'README.md',OUT/'GUIDE_VERIFICATION.json']
inventory={rel(p):sha(p) for p in included}
manifest=OUT/'PACKET_MANIFEST.json'
manifest.write_text(json.dumps({'scope':'Troubleshooting documentation only; not new manufacturing files or physical test results','files':inventory},indent=2)+'\n')
included.append(manifest)
target=OUT/'KK_C6_P4_TROUBLESHOOTING_PACKET.zip'
with tempfile.TemporaryDirectory(prefix='kk-guide-packet-') as tmp:
    draft=Path(tmp)/target.name
    with zipfile.ZipFile(draft,'w',zipfile.ZIP_DEFLATED,compresslevel=4) as z:
        for p in included:z.write(p,rel(p))
    with zipfile.ZipFile(draft) as z:
        assert z.testzip() is None
        for name,h in inventory.items():assert hashlib.sha256(z.read(name)).hexdigest()==h
    import shutil
    shutil.copy2(draft,target)
for p,h in report['source_and_issued_packages_unchanged'].items():assert sha(ROOT/p)==h,p
print(json.dumps({'packet':rel(target),'sha256':sha(target),'files':len(included),'hardware_files_unchanged':True},indent=2))
