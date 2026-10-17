import tempfile
import unittest
from pathlib import Path
from io_utils import sha256, load_prefix


class LoaderTests(unittest.TestCase):
    def test_only_requested_prefix_is_parsed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.csv"
            path.write_text("name,time,a,b\n" + "".join(f"synthetic,{i},1,2\n" for i in range(20)) + "synthetic,NaN,NaN,NaN\n")
            result = load_prefix(path, sha256(path), 20, ["a", "b"])
            self.assertEqual(len(result), 20)
            self.assertEqual(result["time"].iloc[-1], 19)

    def test_identity_change_rejected_before_parse(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.csv"; path.write_text("not csv")
            with self.assertRaisesRegex(ValueError, "identity"):
                load_prefix(path, "0" * 64, 20, ["a", "b"])

    def test_schema_population_and_nonfinite_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.csv"
            for text, count in [("name,time,a\nsynthetic,0,1\n", 1),
                                ("name,time,a,b\nsynthetic,0,1,2\n", 2),
                                ("name,time,a,b\nsynthetic,0,NaN,2\n", 1)]:
                path.write_text(text)
                with self.assertRaises(ValueError): load_prefix(path, sha256(path), count, ["a", "b"])


if __name__ == "__main__": unittest.main()
