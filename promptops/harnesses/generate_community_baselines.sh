#!/usr/bin/env bash
set -euo pipefail
echo '{"status":"unsupported","reason":"Community baselines require measured runs. Use apastra baseline with a passing run and an approved adapter."}' >&2
exit 3
