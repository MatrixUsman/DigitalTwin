"""Synthetic fixtures only; author-model shape, isolation and gradient tests."""
import sys,io,numpy as np,torch
from adapter import create,forecast,batches,predict

kind=sys.argv[1];model=create(kind,17);rng=np.random.default_rng(17)
v=rng.normal(size=(120,9));ends=np.arange(96,112)
x,y,ix=next(batches(v,ends,16));assert x.shape==(16,96,9)
np.testing.assert_array_equal(x[0].numpy(),v[:96].astype('float32'))
alter=v.copy();alter[96:]+=1000
x2,_,_=next(batches(alter,[96]));torch.testing.assert_close(x[:1],x2)
model.train();optim=torch.optim.Adam(model.parameters(),lr=.001)
loss=(forecast(kind,model,x)-y).square().mean();loss.backward()
assert torch.isfinite(loss) and all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
optim.step();optim.zero_grad()
before={k:t.clone() for k,t in model.state_dict().items()}
a=predict(kind,model,v,ends);b=predict(kind,model,v,ends)
assert np.isfinite(a).all();np.testing.assert_array_equal(a,b)
for k,t in model.state_dict().items():torch.testing.assert_close(t,before[k],rtol=0,atol=0)
copy=create(kind,42);copy.load_state_dict(model.state_dict());c=predict(kind,copy,v,ends);np.testing.assert_array_equal(a,c)
print(kind+': synthetic past-only alignment, finite forward/backward, no evaluation mutation, exact reload parity PASS; parameters='+str(sum(p.numel() for p in model.parameters())))
