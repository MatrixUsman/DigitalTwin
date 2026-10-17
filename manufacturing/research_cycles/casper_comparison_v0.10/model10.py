"""Independent implementations from published architectural descriptions."""
import io
import numpy as np
from core import Scaler, batches, finite_matrix

def prepare_raw(values,times,training_rows,c):
    values=finite_matrix(values);times=np.asarray(times)
    if values.shape[1]!=9 or times.shape!=(len(values),) or not np.issubdtype(times.dtype,np.integer):raise ValueError('Schema')
    if not 0<training_rows<len(values):raise ValueError('Split')
    delta=np.diff(times[:training_rows]);positive=delta[delta>0]
    if not len(positive):raise ValueError('No training clock increments')
    gap=float(np.median(positive))*c['gap_multiple'];w=c['median_width'];h=c['common_history']
    outputs=[]
    for sl in [slice(0,training_rows),slice(training_rows,None)]:
        part=values[sl];dt=np.diff(times[sl])
        if np.any(dt<=0) or np.any(dt>gap) or len(part)<=w+h:raise ValueError('Gap or insufficient block')
        filtered=np.median(np.lib.stride_tricks.sliding_window_view(part,w,axis=0),axis=-1)
        outputs.append(filtered)
    scaler=Scaler.fit(outputs[0]);train,dev=[scaler.transform(v) for v in outputs]
    ti=np.arange(h,len(train));di=np.arange(h,len(dev))
    return dict(training=train,development=dev,training_indices=ti,development_indices=di,
                mean=scaler.mean,scale=scaler.scale,maximum_gap=gap,
                training_raw_indices=c['raw_start']+w-1+ti,
                development_raw_indices=c['training_raw_stop']+w-1+di)

def make_model(kind,seed,compile=True):
    import tensorflow as tf
    tf.keras.utils.set_random_seed(seed);tf.config.experimental.enable_op_determinism()
    if kind not in ['casper_cnn','edge_cnn']:raise ValueError('Architecture')
    history=755 if kind=='casper_cnn' else 45;filters=32 if history==755 else 8;kernel=5 if history==755 else 3
    layers=[tf.keras.layers.Input(shape=(history,9))]
    for _ in range(2 if kind=='casper_cnn' else 1):
        layers.extend([tf.keras.layers.Conv1D(filters,kernel,activation='relu',padding='valid'),
                       tf.keras.layers.Conv1D(filters,kernel,activation='relu',padding='valid'),
                       tf.keras.layers.MaxPooling1D(3)])
    layers.extend([tf.keras.layers.Flatten(),tf.keras.layers.Dense(9,kernel_initializer='zeros'),tf.keras.layers.Reshape((1,9))])
    model=tf.keras.Sequential(layers)
    if compile:model.compile(optimizer=tf.keras.optimizers.Adamax(.001),loss='mse')
    return model

def predict(model,values,endpoints,history,batch_size):
    return np.concatenate([model(x,training=False).numpy()[:,0,:] for x,_ in batches(values,endpoints,history,batch_size)])

def pack_weights(model):
    stream=io.BytesIO();np.savez(stream,**{f'w{i}':w for i,w in enumerate(model.get_weights())});return stream.getvalue()

def restore(kind,path):
    model=make_model(kind,0,False);expected=model.get_weights()
    with np.load(path,allow_pickle=False) as ar:
        if set(ar.files)!={f'w{i}' for i in range(len(expected))}:raise ValueError('Weights inventory')
        weights=[ar[f'w{i}'] for i in range(len(expected))]
    if any(w.shape!=e.shape or w.dtype!=e.dtype or not np.isfinite(w).all() for w,e in zip(weights,expected)):raise ValueError('Weights mismatch')
    model.set_weights(weights);return model

def aggregate(scores,width=755):
    scores=np.asarray(scores,dtype=float)
    if scores.ndim!=1 or len(scores)<width or width<1 or not np.isfinite(scores).all():raise ValueError('Scores')
    # Direct convolution avoids catastrophic cancellation of successive prefix sums.
    return np.convolve(scores,np.ones(width),mode='valid')

def admit_epoch(elapsed,last_epoch,c):
    return last_epoch is None or elapsed+c['next_epoch_cost_factor']*last_epoch+1<c['fit_cpu_seconds_per_model']
