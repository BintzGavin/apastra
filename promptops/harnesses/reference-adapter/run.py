#!/usr/bin/env python3
"""Compatibility entry point for the retired synthetic reference adapter."""

import json
import sys


if __name__ == "__main__":
    print(json.dumps({
        "status": "unsupported",
        "reason": "The reference adapter does not execute a target. Configure a measured harness adapter.",
    }), file=sys.stderr)
    raise SystemExit(3)
