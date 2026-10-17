"""Separate-prefix, train-only preprocessing for the normal feasibility pilot."""
import numpy as np

FEATURES = ['accX','accY','accZ','gyroX','gyroY','gyroZ','magX','magY','magZ']


def prepare_prefix(values, history=45, train_targets=8192, dev_targets=2048):
    values=np.asarray(values,dtype=np.float64)
    train_n=train_targets+history; dev_n=dev_targets+history
    if values.shape!=(train_n+dev_n,9) or not np.isfinite(values).all():
        raise ValueError('Unexpected finite nine-channel population')
    train_raw=values[:train_n].copy();dev_raw=values[train_n:].copy()
    mean=train_raw.mean(axis=0); scale=train_raw.std(axis=0)
    if np.any(scale<=0):raise ValueError('Constant/nonfinite training channel')
    def windows(raw):
        z=(raw-mean)/scale
        x=np.stack([z[i:i+history] for i in range(len(z)-history)]).astype(np.float32)
        y=z[history:].astype(np.float32)
        return x,y
    x_train,y_train=windows(train_raw);x_dev,y_dev=windows(dev_raw)
    return {'mean':mean,'scale':scale,'train_x':x_train,'train_y':y_train,
            'dev_x':x_dev,'dev_y':y_dev,'dev_raw_targets':dev_raw[history:],
            'train_target_indices':np.arange(history,train_n),
            'dev_target_indices':np.arange(train_n+history,train_n+dev_n)}
