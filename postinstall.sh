#!/usr/bin/env bash
# npm postinstall — runs when someone does: npm install apastra
#
# Security posture:
# - default postinstall is disclosure-only and does not mutate the consumer repo
# - set APASTRA_POSTINSTALL_SETUP=1 to opt into project-local setup from npm install
# - set APASTRA_INSTALL_PY_DEPS=1 to allow pip installs
# - set APASTRA_INSTALL_AGENT_HOOKS=1 to allow hook config and receipt-ignore writes

set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${INIT_CWD:-$(pwd)}"
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"

# Don't run if we're inside the apastra package itself (dev mode)
if [ "$PROJECT_ROOT" = "$PACKAGE_DIR" ]; then
  exit 0
fi

cat <<EOF
Apastra npm postinstall preflight

Package:
  $PACKAGE_DIR

Project root:
  $PROJECT_ROOT

Default behavior:
  No project files were created or modified by this postinstall.

To install Apastra into this repo from npm, rerun with:
  APASTRA_POSTINSTALL_SETUP=1 npm install apastra

That opt-in setup will create or update:
  .agent/skills/apastra/         agent-facing SKILL.md files
  .agent/scripts/apastra/        runtime, schemas, validators, harnesses, hooks
  .agent/bin/apastra             project-local CLI
  .claude/skills/apastra         symlink, unless APASTRA_NO_SKILL_SYMLINKS=1
  .agents/skills/apastra         symlink, unless APASTRA_NO_SKILL_SYMLINKS=1

Additional opt-in actions:
  APASTRA_INSTALL_PY_DEPS=1       allow pip install pyyaml jsonschema
  APASTRA_INSTALL_AGENT_HOOKS=1   write hook config plus the local receipt .gitignore entry

EOF

if [ "${APASTRA_POSTINSTALL_SETUP:-}" != "1" ]; then
  exit 0
fi

# Use exactly the same non-destructive install and opt-ins as cloned setup.
cd "$PROJECT_ROOT"
APASTRA_ASSUME_YES=1 bash "$PACKAGE_DIR/setup"
