"""Direct author-model imports with a past-only forecast interface."""
from pathlib import Path
from types import SimpleNamespace
import importlib,sys
import numpy as np

P=Path(__file__).resolve().parents[2]
REPOS={'ModernTCN':P/'baselines/vendor/ModernTCN/ModernTCN-Long-term-forecasting',
       'iTransformer':P/'baselines/vendor/iTransformer','TimeMixer':P/'baselines/vendor/TimeMixer'}
_loaded=None

def configuration(kind):
    c=dict(seq_len=96,pred_len=1,enc_in=9,c_out=9,dec_in=9,label_len=0,
           task_name='long_term_forecast',freq='h',embed='timeF',dropout=.1,
           output_attention=False,use_norm=True)
    if kind=='ModernTCN':
        c.update(stem_ratio=6,downsample_ratio=2,ffn_ratio=1,num_blocks=[1],large_size=[51],small_size=[5],
                 dims=[64,64,64,64],dw_dims=[256,256,256,256],small_kernel_merged=False,
                 dropout=.3,head_dropout=0.,use_multi_scale=False,revin=1,affine=0,subtract_last=0,
                 individual=0,kernel_size=25,patch_size=8,patch_stride=4,decomposition=0)
    elif kind=='iTransformer':
        c.update(d_model=256,d_ff=256,e_layers=2,n_heads=8,factor=1,activation='gelu',class_strategy='projection')
    elif kind=='TimeMixer':
        c.update(d_model=16,d_ff=32,e_layers=2,down_sampling_layers=3,down_sampling_window=2,
                 down_sampling_method='avg',channel_independence=1,decomp_method='moving_avg',moving_avg=25,
                 top_k=5,use_future_temporal_feature=0)
    else:raise ValueError('Unknown author model')
    return c

def create(kind,seed):
    global _loaded
    import torch,random
    if _loaded not in (None,kind):raise ValueError('Use a separate process for each author repository')
    _loaded=kind;torch.manual_seed(seed);np.random.seed(seed);random.seed(seed)
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    sys.path.insert(0,str(REPOS[kind]))
    package='model.iTransformer' if kind=='iTransformer' else 'models.'+kind
    return importlib.import_module(package).Model(SimpleNamespace(**configuration(kind))).float()

def forecast(kind,model,x):
    out=model(x) if kind=='ModernTCN' else model(x,None,None,None)
    if out.shape!=(len(x),1,9):raise ValueError('Wrong output shape '+str(out.shape))
    return out[:,0,:]

def batches(values,endpoints,batch_size=64):
    import torch
    values=np.asarray(values)
    if values.ndim!=2 or values.shape[1]!=9 or not np.isfinite(values).all():raise ValueError('Invalid data')
    for i in range(0,len(endpoints),batch_size):
        ix=np.asarray(endpoints[i:i+batch_size])
        if np.any(ix<96) or np.any(ix>=len(values)):raise ValueError('Invalid target')
        x=np.stack([values[t-96:t] for t in ix]).astype(np.float32)
        y=values[ix].astype(np.float32)
        yield torch.from_numpy(x),torch.from_numpy(y),ix

def predict(kind,model,values,endpoints):
    import torch
    model.eval()
    with torch.no_grad():return np.concatenate([forecast(kind,model,x).numpy() for x,_,_ in batches(values,endpoints)])
