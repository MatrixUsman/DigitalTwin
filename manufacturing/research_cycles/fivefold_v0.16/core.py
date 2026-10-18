"""Retrospective normal-only temporal folds; existing model equations unchanged."""
from pathlib import Path
import importlib.util
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
arx = load_module('cv16_arx', PROJECT/'research_cycles/commissioning_v0.9/models.py')
rbf = load_module('cv16_rbf', PROJECT/'research_cycles/residual_twin_v0.13/model.py')

SETTINGS = {'Q1': (8, 1., .01), 'Q2': (16, .5, .001), 'Q3': (32, 1., .001)}
WARMUP = 100

def bounds(fold, length=1200):
    if type(fold) is not int or not 1 <= fold <= 5 or length != 1200:
        raise ValueError('Expected one of five 1200-observation folds')
    stop = 200*fold
    return {'train': [0, stop], 'validation': [stop, stop+200], 'scored': [stop+100, stop+200]}

def cut(observation, interval):
    lo, hi = interval
    return arx.Observation(observation.measurements[lo:hi], observation.commands[lo:hi], observation.valid[lo:hi])

def fit_pair(training, plant):
    order, width, ridge = SETTINGS[plant]
    base = arx.fit(training, {'kind':'arx', 'order':order, 'ridge':1e-7}, WARMUP)
    if float(base['radius']) >= 1:
        raise ValueError('Unstable ARX recurrence: '+str(float(base['radius'])))
    xx, yy = [], []
    for e in training:
        reference = arx.predict(e, base, WARMUP)
        xx.append(rbf.features(reference, e.commands, WARMUP))
        yy.append(((e.measurements-reference)/base['scale'])[WARMUP:])
    head = rbf.fit(np.concatenate(xx), np.concatenate(yy), kind='rbf', count=32, width_factor=width, ridge=ridge)
    return base, head

def score_pair(validation, base, head):
    reference = arx.predict(validation, base, WARMUP)
    corrected = rbf.correct(reference, validation.commands, head, base['scale'], WARMUP)
    native = np.stack([reference[WARMUP:]-validation.measurements[WARMUP:],
                       corrected[WARMUP:]-validation.measurements[WARMUP:]], axis=1)
    standardized = native/base['scale']
    if not np.isfinite(standardized).all():
        raise ValueError('Nonfinite scores')
    return native, standardized

def metrics(native, standardized):
    return {'targets':len(native), 'standardized_rmse':np.sqrt(np.mean(standardized**2, axis=(0,2))).tolist(),
            'native_channel_rmse':np.sqrt(np.mean(native**2, axis=0)).tolist()}
