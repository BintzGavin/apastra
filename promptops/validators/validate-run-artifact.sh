#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" run-artifact "$@"
