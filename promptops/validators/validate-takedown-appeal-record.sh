#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" takedown-appeal-record --formats "$@"
