"""Read public source metadata and author code; never execute upstream code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,urllib.request

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
OUT=PROJECT/'local/evidence_admission_v0.15/sources'
OUT.mkdir(parents=True,exist_ok=True)
records=[]

def fetch(name,url,limit=10_000_000):
    target=OUT/name
    if target.exists():
        raise FileExistsError(target)
    started=datetime.now(timezone.utc).isoformat()
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Academic-source-audit/1.0'}),timeout=40) as response:
        body=response.read(limit+1)
        if len(body)>limit:raise ValueError('Source exceeds bound')
        headers=dict(response.headers)
        final=response.url
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(body)
    records.append(dict(name=name,url=url,final_url=final,utc=started,bytes=len(body),
                        sha256=hashlib.sha256(body).hexdigest(),headers=headers))
    (OUT/'RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
    print(name,len(body),flush=True)
    return body

v=json.loads(fetch('voraus_commit.json','https://api.github.com/repos/vorausrobotik/voraus-ad-dataset/commits/main'))['sha']
for name in ['README.md','LICENSE.txt','configuration.py','coupling_layers.py','graph_inn.py','normalizing_flow.py','train.py','voraus_ad.py','requirements.txt']:
    fetch('voraus/'+name,f'https://raw.githubusercontent.com/vorausrobotik/voraus-ad-dataset/{v}/{name}')
fetch('voraus_manuscript.pdf','https://arxiv.org/pdf/2311.04765v1')
f=json.loads(fetch('factory_commit.json','https://api.github.com/repos/Forgis-Labs/factorynet/commits/main'))['sha']
fetch('factory_README.md',f'https://raw.githubusercontent.com/Forgis-Labs/factorynet/{f}/README.md')
fetch('factory_tree.json',f'https://api.github.com/repos/Forgis-Labs/factorynet/git/trees/{f}?recursive=1')
fetch('factory_dataset_info.json','https://huggingface.co/api/datasets/Forgis/FactoryNet')
fetch('factory_dataset_tree.json','https://huggingface.co/api/datasets/Forgis/FactoryNet/tree/main?recursive=false&expand=false')
fetch('factory_manuscript.pdf','https://arxiv.org/pdf/2605.09081v5')
print(json.dumps(dict(voraus_revision=v,factory_revision=f)))
