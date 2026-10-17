"""Illustrative replay of saved synthetic physics; no new experiment or fit."""
from datetime import datetime,timezone
from pathlib import Path
import json
import os
import resource
import signal
import sys
import time

from inspect_virtual_lab import PROJECT,CYCLE,RUN,sha,inspect

LOCAL=PROJECT/'local/virtual_lab_demo'
LOCAL.mkdir(parents=True,exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(LOCAL/'matplotlib_cache'))
os.environ.setdefault('XDG_CACHE_HOME',str(LOCAL/'font_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter
import numpy as np
from PIL import Image

def main():
    start=time.monotonic();inspection=inspect();resource.setrlimit(resource.RLIMIT_CPU,(120,120));signal.alarm(180)
    output=PROJECT/'output/virtual_lab_demo'
    output.mkdir(parents=True,exist_ok=False)
    cfg=json.loads((CYCLE/'config.json').read_text());states=[];sources={}
    cases=[('normal','Normal motion'),('authorized_offset','Legitimate program change'),
           ('persistent_offset','Unauthorized command change'),('context_gap_offset','Unauthorized change + context gap')]
    for key,_ in cases:
        path=RUN/f'evaluation_light_17_{key}.npz';sources[str(path.relative_to(PROJECT))]=sha(path)
        with np.load(path,allow_pickle=False) as a:states.append({k:a[k] for k in a.files})
    def arm(q):
        a,b=q;l1,l2=cfg['nominal']['l1'],cfg['nominal']['l2']
        return np.array([[0.,0.],[l1*np.cos(a),l1*np.sin(a)],
                         [l1*np.cos(a)+l2*np.cos(a+b),l1*np.sin(a)+l2*np.sin(a+b)]])
    # Check rendering geometry against the simulator's saved endpoint coordinates.
    for ep in states:
        np.testing.assert_allclose(np.stack([arm(q[:2])[-1] for q in ep['state']]),ep['tip'],rtol=0,atol=2e-15)
    np.testing.assert_array_equal(states[1]['state'],states[2]['state'])
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(9,6.8),dpi=100)
    fig.subplots_adjust(top=.84,bottom=.14,hspace=.57,wspace=.22)
    heading=fig.suptitle('Virtual robot lab | synthetic data | t = 0.00 s',fontsize=14,y=.98)
    fig.text(.5,.93,'Dark arm: simulated plant   |   Dashed blue: approved-command reference   |   Orange: noisy sensed tip',ha='center',fontsize=9)
    fig.text(.5,.035,'Top-down view, metres. Light plant / seed17; mass and friction differ from the observer.\nReplay of saved data at 5 fps; no hardware, training or new test generation.',ha='center',fontsize=9)
    artists=[]
    for ax,(_,title) in zip(axes.flat,cases):
        ax.set(xlim=(-.07,1.),ylim=(-.55,.55),aspect='equal',xlabel='x (m)',ylabel='y (m)')
        ax.set_title(title,fontsize=10,pad=33)
        ax.grid(alpha=.18);line,=ax.plot([],[],'o-',color='#263b4a',lw=4,ms=6,zorder=4)
        reference,=ax.plot([],[],'o--',color='#438db5',lw=2,ms=4,alpha=.8,zorder=3)
        sensor,=ax.plot([],[],'o',color='#dd9340',ms=4,zorder=5)
        trail,=ax.plot([],[],color='#263b4a',lw=1,alpha=.2)
        label=ax.text(.5,1.03,'',transform=ax.transAxes,fontsize=8,ha='center',va='bottom')
        artists.append((line,reference,sensor,trail,label))
    def update(t):
        heading.set_text(f'Virtual robot lab | synthetic data | t = {t*cfg["dt"]:.2f} s')
        for ep,(line,reference,sensor,trail,label) in zip(states,artists):
            true=arm(ep['state'][t,:2]);ref=arm(ep['reference'][t,:2]);seen=arm(ep['measurements'][t,:2])[-1]
            line.set_data(true[:,0],true[:,1]);reference.set_data(ref[:,0],ref[:,1]);sensor.set_data([seen[0]],[seen[1]])
            trail.set_data(ep['tip'][max(0,t-100):t+1,0],ep['tip'][max(0,t-100):t+1,1])
            event='unauthorized command active' if ep['attack'][t] else 'legitimate change active' if ep['authorized'][t] else 'approved program active'
            available='available' if ep['valid'][t] else 'UNAVAILABLE'
            label.set_text(f'{event}\nContext: {available}')
            label.set_color('#a3453c' if ep['attack'][t] else '#326b56')
        return []
    update(400);fig.savefig(output/'virtual_lab_overview.png',dpi=160)
    animation=FuncAnimation(fig,update,frames=range(0,cfg['steps'],10),interval=200,blit=False,cache_frame_data=False)
    animation.save(output/'virtual_robot_lab.gif',writer=PillowWriter(fps=5));plt.close(fig)
    with Image.open(output/'virtual_robot_lab.gif') as im:
        frames=im.n_frames;dimensions=im.size
        if frames!=100:raise ValueError('Unexpected animation frame count')
        for index in [0,30,40,55,99]:
            im.seek(index);im.convert('RGB').save(LOCAL/f'frame_{index:03d}.png')
    size=sum(p.stat().st_size for p in output.iterdir())
    if size>10*1024*1024:raise ValueError('Demonstration output exceeded 10 MiB')
    inspection_after=inspect()
    if inspection!=inspection_after:raise ValueError('Source inspection changed')
    usage=resource.getrusage(resource.RUSAGE_SELF);signal.alarm(0)
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv,'cwd':str(Path.cwd()),
        'role':'Visualization of already exposed synthetic data; not new evidence',
        'input_sha256':sources,'code_sha256':sha(Path(__file__)),'inspection':inspection,
        'frames':frames,'dimensions':dimensions,'fps':5,'sample_stride':10,'shown_interval_seconds':[0.,19.8],
        'geometry_checks':'4000 saved end-effector coordinates agree; authorized and unauthorized offset physical states identical',
        'wall_seconds':time.monotonic()-start,'cpu_seconds':usage.ru_utime+usage.ru_stime,
        'peak_rss_bytes':usage.ru_maxrss if sys.platform=='darwin' else usage.ru_maxrss*1024,
        'output_bytes':size,'versions':{'numpy':np.__version__,'matplotlib':matplotlib.__version__},
        'output_sha256':{str(p.relative_to(PROJECT)):sha(p) for p in output.iterdir()}}
    with (LOCAL/'render_receipt.json').open('x') as f:f.write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['frames','wall_seconds','cpu_seconds','peak_rss_bytes','output_bytes']}))

if __name__=='__main__':main()
