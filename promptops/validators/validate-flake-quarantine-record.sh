#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" flake-quarantine-record --formats "$@"
