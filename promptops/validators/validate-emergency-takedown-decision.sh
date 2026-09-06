#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" emergency-takedown-decision --formats "$@"
