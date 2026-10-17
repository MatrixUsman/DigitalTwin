"""Receive the original public release unchanged; no observation parsing."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,time,urllib.request
P=Path(__file__).resolve().parents[2]
out=P/'datasets/raw/voraus_ad'
out.mkdir(parents=True,exist_ok=True)
target=out/'voraus-ad-dataset-100hz.parquet'
if target.exists():raise SystemExit('Original file already exists')
partial=out/(target.name+'.part')
if partial.exists():raise SystemExit('Preserved partial download exists')
url='https://media.vorausrobotik.com/voraus-ad-dataset-100hz.parquet'
receipt=dict(url=url,utc=datetime.now(timezone.utc).isoformat(),purpose='authorized release identification; no training or protected observation inspection')
h=hashlib.sha256();size=0;start=time.monotonic()
try:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Academic-source-audit/1.0'}),timeout=45) as response, partial.open('xb') as output:
        receipt['headers']=dict(response.headers);receipt['final_url']=response.url
        while True:
            block=response.read(4*1024*1024)
            if not block:break
            size+=len(block)
            if size>1500000000 or time.monotonic()-start>300:raise ValueError('Download bound exceeded')
            output.write(block);h.update(block)
    expected=receipt['headers'].get('Content-Length')
    if expected and int(expected)!=size:raise ValueError('Incomplete transfer')
    with partial.open('rb') as data:
        if data.read(4)!=b'PAR1':raise ValueError('Wrong Parquet header')
        data.seek(-4,2)
        if data.read(4)!=b'PAR1':raise ValueError('Wrong Parquet trailer')
    partial.rename(target);receipt['status']='received'
except Exception as error:
    receipt['status']='failed';receipt['error']=repr(error)
finally:
    receipt.update(bytes=size,sha256=h.hexdigest(),seconds=time.monotonic()-start)
    local=P/'local/evidence_admission_v0.15';local.mkdir(parents=True,exist_ok=True)
    (local/'DATA_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','bytes','sha256','seconds']}))
if receipt['status']!='received':raise SystemExit(1)
