"""Synthetic checks for the exact serialization defect and lossless conversion."""
import json
import unittest
import numpy as np
from recover_reporting import portable
from observer import outcome

class Reporting(unittest.TestCase):
    def test_preserves_native_scalar_values(self):
        data={'i':np.int64(250),'f':np.float64(.125),'b':np.bool_(True),'x':[None,np.int32(0)]}
        self.assertEqual(json.loads(json.dumps(portable(data),allow_nan=False)),{'i':250,'f':.125,'b':True,'x':[None,0]})

    def test_frozen_outcome_can_be_exported(self):
        a=np.zeros(70,dtype=bool);a[20:50]=True;attack=np.zeros(70,dtype=bool);attack[20:40]=True
        row=outcome(a,np.zeros(70,dtype=bool),attack,np.zeros(70,dtype=bool),np.zeros((70,4)),np.zeros((70,4)),np.ones(4),{'warmup':10,'recovery_dwell':3})
        with self.assertRaises(TypeError):json.dumps(row)
        decoded=json.loads(json.dumps(portable(row),allow_nan=False))
        for k,v in row.items():self.assertEqual(decoded[k],v)

if __name__=='__main__':unittest.main()
