import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from model import make_model, weights_bytes, load_weights_artifact


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((Path(__file__).parent / "config.json").read_text())

    def test_architecture_and_zero_output_initialization(self):
        model = make_model(self.config, 17)
        self.assertEqual(model.count_params(), 1369)
        output = model(np.ones((2, 45, 9), dtype=np.float32), training=False).numpy()
        self.assertEqual(output.shape, (2, 1, 9))
        np.testing.assert_array_equal(output, 0)

    def test_saved_trained_fixture_has_exact_inference_parity(self):
        # Synthetic software fixture, unrelated to robot observations.
        rng = np.random.default_rng(17)
        x = rng.normal(size=(8, 45, 9)).astype(np.float32)
        y = (0.4 * x[:, -1:, :]).astype(np.float32)
        model = make_model(self.config, 42)
        model.train_on_batch(x, y)
        expected = model(x, training=False).numpy()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weights.npz"; path.write_bytes(weights_bytes(model))
            restored = load_weights_artifact(self.config, path)
            np.testing.assert_array_equal(expected, restored(x, training=False).numpy())

    def test_invalid_weight_inventory_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weights.npz"; np.savez(path, wrong=np.zeros(1))
            with self.assertRaises(ValueError): load_weights_artifact(self.config, path)


if __name__ == "__main__": unittest.main()
