#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" ownership-dispute-record --formats "$@"
