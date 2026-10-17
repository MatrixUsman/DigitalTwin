"""Inspect only original partition/group/clock metadata, never process signals."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib,json,math,sys,time
import pyarrow.parquet as pq
import pyarrow

P=Path(__file__).resolve().parents[2]
raw=P/'datasets/raw/voraus_ad/voraus-ad-dataset-100hz.parquet'
out=P/'local/evidence_admission_v0.15'
if (out/'METADATA_AUDIT.json').exists():raise SystemExit('Metadata audit already recorded')
start=time.monotonic();f=pq.ParquetFile(raw)
allowed=['sample','time','setting','category','anomaly']
assert set(allowed).issubset(f.schema_arrow.names)
episodes={};rows=0;clock_nonpositive=0;dtmin=float('inf');dtmax=0.;changes=[]
for batch in f.iter_batches(batch_size=8192,columns=allowed,use_threads=False):
    b=batch.to_pydict()
    for s,t,v,c,a in zip(*(b[k] for k in allowed)):
        assert s is not None and t is not None and math.isfinite(t)
        item=episodes.get(s)
        if item is None:
            episodes[s]=dict(sample=s,setting=v,category=c,anomaly=a,rows=1,time_first=t,time_last=t)
        else:
            if (v,c,a)!=(item['setting'],item['category'],item['anomaly']):changes.append(s)
            dt=t-item['time_last'];clock_nonpositive+=dt<=0;dtmin=min(dtmin,dt);dtmax=max(dtmax,dt)
            item['rows']+=1;item['time_last']=t
        rows+=1
train=[x for x in episodes.values() if x['setting']==72]
test=[x for x in episodes.values() if x['setting']!=72]
summary=dict(utc=datetime.now(timezone.utc).isoformat(),python=sys.version,pyarrow=pyarrow.__version__,
    columns_read=allowed,signals_read=[],raw_bytes=raw.stat().st_size,rows=rows,footer_rows=f.metadata.num_rows,
    row_groups=f.metadata.num_row_groups,schema=[dict(name=x.name,type=str(x.type)) for x in f.schema_arrow],
    episodes=len(episodes),normal=sum(not x['anomaly'] for x in episodes.values()),
    anomalous=sum(bool(x['anomaly']) for x in episodes.values()),train_episodes=len(train),
    train_anomalies=sum(bool(x['anomaly']) for x in train),test_episodes=len(test),
    test_normal=sum(not x['anomaly'] for x in test),test_anomalous=sum(bool(x['anomaly']) for x in test),
    metadata_changed_within_episode=sorted(set(changes)),clock_nonpositive=clock_nonpositive,
    min_step=dtmin,max_step=dtmax,train_max_rows=max(x['rows'] for x in train),test_max_rows=max(x['rows'] for x in test),
    test_longer_than_train=sum(x['rows']>max(q['rows'] for q in train) for x in test),
    seconds=time.monotonic()-start)
assert rows==f.metadata.num_rows
(out/'EPISODE_METADATA.json').write_text(json.dumps(sorted(episodes.values(),key=lambda x:x['sample']),indent=2)+'\n')
(out/'METADATA_AUDIT.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['schema','python']},indent=2))
