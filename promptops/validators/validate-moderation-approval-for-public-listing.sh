#!/usr/bin/env bash
exec bash "$(dirname "$0")/lib/validate.sh" moderation-approval-for-public-listing --formats "$@"
