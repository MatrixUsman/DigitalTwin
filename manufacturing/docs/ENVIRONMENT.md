# Manufacturing software-check environment

Created locally on 16 October 2026 for the authorized loader/metric implementation. The ignored `manufacturing/.venv/` is separate from the other projects. No system package was changed and no third-party package was installed.

Actual successful test environment:

- Python **3.15.0**, Clang 21.0.0, ARM64 macOS.
- Standard library only; no installed package distributions in the test receipt.
- `sys.prefix != sys.base_prefix` verified true.
- Package metadata requests Python >=3.11 syntax compatibility; only the recorded 3.15.0 interpreter was tested. Compatibility with other versions is not yet demonstrated.

Creation command actually used from the workspace root:

```sh
python3 -m venv --without-pip manufacturing/.venv
```

Test command from the manufacturing directory:

```sh
.venv/bin/python scripts/run_synthetic_tests.py
```

This uses Python's [isolated virtual-environment mechanism](https://docs.python.org/3/library/venv.html) without bootstrapping pip, and its [standard-library test framework](https://docs.python.org/3/library/unittest.html). Native timestamp parsing uses [Decimal](https://docs.python.org/3/library/decimal.html); metric time arithmetic is isolated from mutable Decimal contexts. The exact interpreter/build/platform and source hashes live in the [software test report](../experiments/SOFTWARE_TEST_REPORT.json) and its ignored detailed receipt. There is no third-party dependency lock because none is installed. Future ML dependencies need a separately validated environment/lock; do not assume this interpreter is compatible with an unselected ML stack.

Recreate an environment from the recorded interpreter rather than copying its directory. Do not install dependencies, train models or enable final access merely because these software tests pass.
