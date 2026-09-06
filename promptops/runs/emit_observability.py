"""Retired placeholder: no provider-compatible delivery adapter is shipped."""
import json
import sys


def main():
    print(json.dumps({"status": "unsupported", "reason": "Observability delivery is not implemented; no artifacts were sent.", "receipts": []}), file=sys.stderr)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
