"""Download linked manufacturer datasheets when available; retain failure log."""
from pathlib import Path
import json,urllib.request,concurrent.futures,subprocess
OUT=Path(__file__).resolve().parent/'P2_compact'
sources=json.loads((OUT/'datasheets/sources.json').read_text())
def download(item):
    name,url=item;dest=OUT/'datasheets'/(name.replace('/','_')+'.pdf')
    try:
        if not dest.exists():
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=15) as r:data=r.read()
            assert data.startswith(b'%PDF'),'Not a PDF'
            dest.write_bytes(data)
        subprocess.run(['pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],check=True)
        return {'mpn':name,'url':url,'saved':True}
    except Exception as e:return {'mpn':name,'url':url,'saved':False,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(download,sources.items()))
(OUT/'datasheets/download_log.json').write_text(json.dumps(results,indent=2)+'\n')
print('Saved',sum(r['saved'] for r in results),'of',len(results),'linked datasheets')
