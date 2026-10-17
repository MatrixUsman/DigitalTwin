"""Synthetic arithmetic/shape checks; no upstream execution or dataset signal access."""
import ast,json
from pathlib import Path
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parents[2]
root=P/'local/evidence_admission_v0.15'
s=root/'sources/voraus'
tree=ast.parse((s/'normalizing_flow.py').read_text())
fn={n.name:ast.get_source_segment((s/'normalizing_flow.py').read_text(),n) for n in tree.body if isinstance(n,ast.FunctionDef)}
assert 'torch.sum(z_space**2, dim=sum_dimension) - jac' in fn['get_loss']
assert '0.5 * torch.sum(z_space**2, dim=sum_dimension) - jac' in fn['get_loss_per_sample']
q=np.array([2.,2.,8.]);j=np.array([0.,1.,1.]);train=q-j;paper=.5*q-j
assert not np.allclose(train,2*paper)
original=pd.DataFrame({'x':[1.,2.,3.,4.,5.]});limit=3
assigned=original.loc[:limit]
pad=pd.DataFrame(0,index=range(len(original),limit),columns=original.columns)
assigned=pd.concat([original,pad])
assert len(assigned)==5 and len(assigned)>limit
metadata=json.loads((root/'METADATA_AUDIT.json').read_text())
assert metadata['test_longer_than_train']==0
record=dict(synthetic_only=True,source_functions=['get_loss','get_loss_per_sample','load_pandas_dataframes'],
    quadratic_examples=q.tolist(),jacobian_examples=j.tolist(),unnormalized_training_terms=train.tolist(),
    paper_scoring_terms=paper.tolist(),source_weights_differ=True,long_input_rows=5,target_rows=3,actual_rows=len(assigned),
    original_release_test_longer_than_train=0,interpretation='source correspondence concern, not demonstrated paper-performance failure')
(root/'SYNTHETIC_SOURCE_CHECKS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
