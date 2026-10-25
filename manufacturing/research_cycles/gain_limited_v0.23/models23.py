"""Finite causal predictors and auditable l-infinity constraints."""
import numpy as np
import torch
from torch import nn

START=100

def lagged(x,lags):
    x=np.asarray(x,float);out=np.zeros((len(x),lags*x.shape[1]))
    for lag in range(1,lags+1):
        out[lag:,(lag-1)*x.shape[1]:lag*x.shape[1]]=x[:-lag]
    return out

def context(u):
    previous=lagged(u,1);difference=np.zeros_like(previous);difference[1:]=np.diff(previous,axis=0)
    return np.column_stack([previous,difference])

def fit_scale(ys,us):
    yy=np.concatenate([x[START:] for x in ys]);uu=np.concatenate([x[START:] for x in us])
    return dict(y_mean=yy.mean(0),y_std=np.maximum(yy.std(0),1e-6),u_mean=uu.mean(0),u_std=np.maximum(uu.std(0),1e-6))

def ridge(x,y,penalty):
    x=np.asarray(x,float);y=np.asarray(y,float);a=x.T@x/len(x);d=np.eye(x.shape[1])*penalty;d[-1,-1]=0.
    return np.linalg.solve(a+d,x.T@y/len(x))

def reference_fit(ys,us,lags=16,penalty=.001):
    xx=[np.column_stack([lagged(u,lags),np.ones(len(u))]) for u in us]
    w=ridge(np.concatenate([x[START:] for x in xx]),np.concatenate([y[START:] for y in ys]),penalty)
    return w

def reference_predict(u,w,lags=16):
    return np.column_stack([lagged(u,lags),np.ones(len(u))])@w

def l1_project(row,radius):
    row=np.asarray(row,float)
    if radius<0:raise ValueError('Negative l1 radius')
    if np.abs(row).sum()<=radius:return row.copy()
    if radius==0:return np.zeros_like(row)
    ordered=np.sort(np.abs(row))[::-1];shift=(np.cumsum(ordered)-radius)/np.arange(1,len(row)+1)
    active=np.flatnonzero(ordered>shift);theta=shift[active[-1]]
    return np.sign(row)*np.maximum(np.abs(row)-theta,0.)

def fir_fit(zs,cs,kappa,lags=5,ridge_value=.001,max_iterations=5000,tol=1e-7):
    xr=np.concatenate([lagged(z,lags)[START:] for z in zs]);xc=np.concatenate([np.column_stack([c,np.ones(len(c))])[START:] for c in cs]);yy=np.concatenate([z[START:] for z in zs])
    x=np.column_stack([xr,xc]);nr=xr.shape[1];g=x.T@x/len(x);g+=np.diag(np.r_[np.full(x.shape[1]-1,ridge_value),0.]);rhs=x.T@yy/len(x)
    w=np.linalg.solve(g,rhs);step=1./np.linalg.eigvalsh(g)[-1]
    if kappa is None:
        return dict(weight=w,lag=lags,kappa_budget=None,K=float(np.max(np.abs(w[:nr]).sum(0))),converged=True,iterations=0,gradient_mapping=0.)
    for j in range(w.shape[1]):w[:nr,j]=l1_project(w[:nr,j],kappa)
    momentum=w.copy();alpha=1.;converged=False;gap=None
    for iteration in range(1,max_iterations+1):
        new=momentum-step*(g@momentum-rhs)
        for j in range(new.shape[1]):new[:nr,j]=l1_project(new[:nr,j],kappa)
        nextalpha=(1+np.sqrt(1+4*alpha*alpha))/2
        momentum=new+(alpha-1)/nextalpha*(new-w);w=new;alpha=nextalpha
        if iteration%10==0 or iteration==max_iterations:
            probe=w-step*(g@w-rhs)
            for j in range(probe.shape[1]):probe[:nr,j]=l1_project(probe[:nr,j],kappa)
            gap=float(np.max(np.abs(probe-w))/step)
            if gap<=tol:converged=True;break
    return dict(weight=w,lag=lags,kappa_budget=kappa,K=float(np.max(np.abs(w[:nr]).sum(0))),converged=converged,iterations=iteration,gradient_mapping=gap)

def fir_predict(z,c,model,cap=None):
    x=lagged(z,model['lag']);nr=x.shape[1];obs=x@model['weight'][:nr];trusted=np.column_stack([c,np.ones(len(c))])@model['weight'][nr:]
    if cap is not None:obs=np.clip(obs,-cap,cap)
    return obs+trusted

def leaky(z,kappa,rho):
    result=np.zeros_like(z,dtype=float);state=np.zeros(z.shape[1])
    for t in range(1,len(z)):
        state=rho*state+(1-rho)*kappa*z[t-1];result[t]=state
    return result

def kalman(z,ratio):
    # Independent residual random walks, steady-state prior variance p solves
    # p^2-q*p-q=0 with measurement variance 1; scale cancels in gain.
    prior=.5*(ratio+np.sqrt(ratio*ratio+4*ratio));gain=prior/(prior+1)
    return leaky(z,1.,1.-gain),float(gain)

class Adapter(nn.Module):
    def __init__(self,kappa,rho,width=8,seed=17,kind='constrained'):
        super().__init__();torch.manual_seed(seed);self.kappa=kappa;self.rho=rho;self.kind=kind;self.width=width
        self.wh=nn.Parameter(torch.randn(width,width)*.05);self.wz=nn.Parameter(torch.randn(width,4)*.05)
        self.wc=nn.Parameter(torch.randn(width,8)*.05);self.bias=nn.Parameter(torch.zeros(width));self.wo=nn.Parameter(torch.randn(4,width)*.05)
        if kind=='context':self.wz.requires_grad_(False)
        self.project()
    @torch.no_grad()
    def project(self):
        def bound(w,cap):
            sums=w.abs().sum(1,keepdim=True);w.mul_(torch.minimum(torch.ones_like(sums),torch.as_tensor(cap*(1-1e-6),dtype=w.dtype)/torch.clamp(sums,min=1e-20)))
        if self.kind!='unconstrained':bound(self.wh,self.rho)
        if self.kind=='context':self.wz.zero_()
        elif self.kind=='constrained':bound(self.wz,1.-self.rho);bound(self.wo,self.kappa)
    def forward(self,previous,ctx):
        h=torch.zeros((previous.shape[0],self.width),dtype=previous.dtype,device=previous.device);output=[]
        for t in range(previous.shape[1]):
            h=torch.tanh(h@self.wh.T+previous[:,t]@self.wz.T+ctx[:,t]@self.wc.T+self.bias);output.append(h@self.wo.T)
        return torch.stack(output,dim=1)
    def certificate(self):
        rho,beta,gamma=[float(x.detach().double().abs().sum(1).max()) for x in [self.wh,self.wz,self.wo]]
        if not np.isfinite([rho,beta,gamma]).all() or any(not torch.isfinite(p).all() for p in self.parameters()):raise ValueError('Nonfinite learned weight/certificate')
        if self.kind=='context':gain,cap=0.,0.
        else:gain=gamma*beta/(1-rho) if rho<1 else None;cap=gamma
        return dict(rho=rho,beta=beta,gamma=gamma,K=gain,C=cap,kappa_budget=self.kappa,rho_budget=self.rho,kind=self.kind)

def windows(zs,cs,window=96,burnin=48,stride=48):
    previous=[];contexts=[];targets=[];masks=[]
    for z,c in zip(zs,cs):
        zp=lagged(z,1)
        for start in range(START,len(z),stride):
            lo=start-burnin;hi=min(start+stride,len(z));n=hi-lo
            pp=np.zeros((window,4),np.float32);cc=np.zeros((window,8),np.float32);yy=np.zeros((window,4),np.float32);mask=np.zeros((window,1),np.float32)
            pp[:n]=zp[lo:hi];cc[:n]=c[lo:hi];yy[:n]=z[lo:hi];mask[burnin:n]=1
            previous.append(pp);contexts.append(cc);targets.append(yy);masks.append(mask)
    return tuple(torch.tensor(np.stack(x),dtype=torch.float32) for x in [previous,contexts,targets,masks])

def objective(model,batch):
    p,c,y,m=batch;return (((model(p,c)-y)**2)*m).sum()/(m.sum()*y.shape[-1])

def train_adapter(model,train_batch,dev_batch,epochs=12,lr=.01,weight_decay=.0001):
    optimizer=torch.optim.Adam([p for p in model.parameters() if p.requires_grad],lr=lr,weight_decay=weight_decay);history=[]
    for epoch in range(1,epochs+1):
        optimizer.zero_grad();loss=objective(model,train_batch)
        if not torch.isfinite(loss):raise ValueError('Nonfinite training objective')
        loss.backward();optimizer.step();model.project()
        with torch.no_grad():a=float(objective(model,train_batch));b=float(objective(model,dev_batch))
        if not np.isfinite([a,b]).all():raise ValueError('Nonfinite epoch objective')
        history.append(dict(epoch=epoch,training_window_mse=a,development_window_mse=b,certificate=model.certificate()))
    late=min(len(history)-1,3*len(history)//4)
    underfit=epochs>=4 and (history[late]['training_window_mse']-history[-1]['training_window_mse'])/max(abs(history[late]['training_window_mse']),1e-12)>.01
    return history,underfit

@torch.no_grad()
def adapter_predict(model,z,c):
    previous=torch.tensor(lagged(z,1)[None],dtype=torch.float32);ctx=torch.tensor(c[None],dtype=torch.float32)
    return model(previous,ctx)[0].numpy().astype(float)

@torch.no_grad()
def adapter_predict_many(model,zs,cs):
    if len({len(z) for z in zs})!=1:raise ValueError('Batch inference requires equal-length separate episodes')
    previous=torch.tensor(np.stack([lagged(z,1) for z in zs]),dtype=torch.float32);ctx=torch.tensor(np.stack(cs),dtype=torch.float32)
    return list(model(previous,ctx).numpy().astype(float))

def metrics(residuals,certificate,quantile=.99):
    rr=np.concatenate([x[START:] for x in residuals])
    if rr.ndim!=2 or rr.shape[1]!=4 or not len(rr) or not np.isfinite(rr).all():raise ValueError('Invalid residual population')
    if any(v is not None and (not np.isfinite(v) or v<0) for v in [certificate.get('K'),certificate.get('C')]):raise ValueError('Invalid gain/cap certificate')
    scores=np.max(np.abs(rr),axis=1);e=float(np.max(scores));rank=int(np.ceil(quantile*len(scores)))-1;tau=float(np.sort(scores)[rank]);a=e+tau
    k,c=certificate.get('K'),certificate.get('C');rg=a/(1-k) if k is not None and k<1 else None;rc=a+2*c if c is not None else None
    valid=[v for v in [rg,rc] if v is not None];radius=min(valid) if valid else None
    rmse=float(np.sqrt(np.mean(rr**2)));episodes=[float(np.sqrt(np.mean(x[START:]**2))) for x in residuals]
    if not np.isfinite([rmse]+episodes+valid).all():raise ValueError('Nonfinite derived metric')
    return dict(points=len(scores),Edev=e,tau_dev=tau,rank=rank,rmse=rmse,episode_rmse=episodes,
                gain_radius=rg,cap_radius=rc,primary_radius=radius,certificate=certificate)
