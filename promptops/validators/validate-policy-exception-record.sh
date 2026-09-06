#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" policy-exception-record --formats "$@"
