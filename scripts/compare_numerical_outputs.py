"""Compare regenerated numerical outputs with their committed versions, on scientific content.

    python scripts/compare_numerical_outputs.py BASE NEW [BASE NEW ...]

Works on JSON and CSV files. Three kinds of value are environment-dependent
and are not compared:

- the `environment` block (package versions);
- QUADPACK error estimates (keys ending in `_error_estimate`);
- float64 round-off diagnostics (keys or columns containing
  `float64_relative_difference`). These are |float64 result / exact - 1|,
  so their value is a rounding error and changes with the platform.

Every other number must agree to within 8 units in the last place. Strings,
integers and booleans must be equal. The evidence: a Windows run and an
Ubuntu 24.04 run with the same package versions (numpy 2.5.4, scipy 1.18.1,
matplotlib 3.11.2) differed in exactly these diagnostics and by 1 ulp in one
Monte Carlo RMSE, and in nothing else (.agent/reports/R6.md).
"""
from __future__ import annotations

import csv
import io
import json
import math
import struct
import sys

ULPS = 8


def _skipped(key):
    return key == "environment" or key.endswith("_error_estimate") or "float64_relative_difference" in key


def _close(a, b):
    # Nonfinite outputs cannot be evidence of reproducibility, even inf == inf.
    if not (math.isfinite(a) and math.isfinite(b)):
        return False
    if a == b:  # includes the two representations of zero
        return True

    def ordered(x):
        bits = struct.unpack('>Q', struct.pack('>d', x))[0]
        magnitude = bits & ((1 << 63) - 1)
        return -magnitude if bits >> 63 else magnitude

    return abs(ordered(a) - ordered(b)) <= ULPS


def differences(a, b, path=""):
    """Paths at which a and b differ, outside the skipped keys."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            if _skipped(key):
                continue
            where = f"{path}.{key}" if path else key
            if key not in a or key not in b:
                out.append(f"{where}: present on one side only")
            else:
                out += differences(a[key], b[key], where)
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: {len(a)} items != {len(b)}"]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in differences(x, y, f"{path}[{i}]")]
    if isinstance(a, float) and isinstance(b, float):
        return [] if _close(a, b) else [f"{path}: {a!r} != {b!r}"]
    return [] if type(a) is type(b) and a == b else [f"{path}: {a!r} != {b!r}"]


def _number(text):
    for kind in (int, float):
        try:
            return kind(text)
        except ValueError:
            pass
    return text


def _load(path):
    text = open(path, encoding="utf-8").read()
    if path.endswith(".json"):
        return json.loads(text)
    rows = list(csv.DictReader(io.StringIO(text)))
    return [{k: _number(v) for k, v in row.items()} for row in rows]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or len(argv) % 2:
        print(__doc__)
        return 2
    found = []
    for base, new in zip(argv[::2], argv[1::2]):
        found += [f"{new}: {d}" for d in differences(_load(base), _load(new))]
    for line in found:
        print(line)
    print(f"{len(found)} scientific differences in {len(argv) // 2} file(s) "
          "(environment, *_error_estimate and float64 round-off diagnostics skipped; floats to 8 ulp)")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
