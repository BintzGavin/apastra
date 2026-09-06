#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" delivery-target-receipt --formats "$@"
