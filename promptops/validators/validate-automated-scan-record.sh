#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" automated-scan-record --formats "$@"
