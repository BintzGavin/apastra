"""Compatibility entry point: regression requires complete run directories."""
import argparse
import importlib
from pathlib import Path
import sys

package = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(package.parent))
sys.modules.setdefault("promptops", importlib.import_module(package.name))
from promptops.runtime.cli import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate")
    parser.add_argument("baseline")
    parser.add_argument("policy")
    parser.add_argument("output")
    parser.add_argument("--adapter", required=True)
    args = parser.parse_args()
    sys.argv = [sys.argv[0], "gate", args.candidate, "--baseline", args.baseline, "--policy", args.policy, "--output", args.output, "--adapter", args.adapter]
    raise SystemExit(main())
