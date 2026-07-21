#!/usr/bin/env bash
# npm postinstall — runs when someone does: npm install apastra
#
# Security posture:
# - default postinstall is disclosure-only and does not mutate the consumer repo
# - set APASTRA_POSTINSTALL_SETUP=1 to opt into project-local setup from npm install
# - set APASTRA_INSTALL_PY_DEPS=1 to allow pip installs
# - set APASTRA_INSTALL_AGENT_HOOKS=1 to allow Codex/Claude hook config writes

set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${INIT_CWD:-$(pwd)}"
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"

# Don't run if we're inside the apastra package itself (dev mode)
if [ "$PROJECT_ROOT" = "$PACKAGE_DIR" ]; then
  exit 0
fi

SKILLS_DEST="$PROJECT_ROOT/.agent/skills/apastra"
SCRIPTS_DEST="$PROJECT_ROOT/.agent/scripts/apastra"
BIN_DEST="$PROJECT_ROOT/.agent/bin"

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
  APASTRA_INSTALL_AGENT_HOOKS=1   write .codex/config.toml, .codex/hooks.json, .claude/settings.json

EOF

if [ "${APASTRA_POSTINSTALL_SETUP:-}" != "1" ]; then
  exit 0
fi

echo "🔧 Installing apastra..."

# Copy skill directories (anything containing a SKILL.md)
mkdir -p "$SKILLS_DEST"
cp "$PACKAGE_DIR/SKILL.md" "$SKILLS_DEST/" 2>/dev/null || true
for dir in "$PACKAGE_DIR"/*/; do
  name="$(basename "$dir")"
  if [ -f "$dir/SKILL.md" ]; then
    cp -r "$dir" "$SKILLS_DEST/$name"
  fi
done

# Copy runtime scripts
mkdir -p "$SCRIPTS_DEST"
cp -r "$PACKAGE_DIR/promptops/runtime"    "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/request_log" "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/runs"       "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/resolver"   "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/schemas"    "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/validators" "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/harnesses"  "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/hooks"      "$SCRIPTS_DEST/"
cp    "$PACKAGE_DIR/promptops/__init__.py" "$SCRIPTS_DEST/"
mkdir -p "$BIN_DEST"
cp    "$PACKAGE_DIR/bin/apastra" "$BIN_DEST/apastra"
chmod +x "$BIN_DEST/apastra"

find "$SCRIPTS_DEST" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$SCRIPTS_DEST" -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.orig" -o -name "*.rej" \) -exec rm -f {} +
find "$SCRIPTS_DEST" -name "*.sh" -exec chmod +x {} \;
find "$SCRIPTS_DEST/hooks" -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

# Check Python dependencies. Installing them is opt-in because npm postinstall
# should not invoke another package manager unless the user explicitly allowed it.
echo "📦 Checking Python dependencies..."
PY="$(command -v python3 || command -v python || true)"
PIP_DEPS_OK=0
if [ -n "$PY" ] && "$PY" -c "import yaml, jsonschema" &>/dev/null; then
  echo "   pyyaml + jsonschema already present."
  PIP_DEPS_OK=1
elif [ "${APASTRA_INSTALL_PY_DEPS:-}" = "1" ]; then
  PIP="$(command -v pip3 || command -v pip || true)"
  if [ -n "$PIP" ]; then
    if "$PIP" install --quiet pyyaml jsonschema 2>/dev/null \
      || "$PIP" install --quiet --user pyyaml jsonschema 2>/dev/null; then
      PIP_DEPS_OK=1
    fi
  fi
fi

if [ "$PIP_DEPS_OK" -ne 1 ]; then
  echo ""
  echo "⚠️  pyyaml + jsonschema are not available to python."
  echo "   Apastra did not install them automatically."
  echo "   To let npm postinstall use pip, rerun with APASTRA_INSTALL_PY_DEPS=1."
  echo "   Or install manually via one of:"
  echo "     pipx install pyyaml && pipx install jsonschema"
  echo "     python3 -m venv .venv && source .venv/bin/activate && pip install pyyaml jsonschema"
  echo "     pip install --user pyyaml jsonschema"
  echo "     pip install --break-system-packages pyyaml jsonschema   # not recommended"
  echo ""
fi

if [ "${APASTRA_INSTALL_AGENT_HOOKS:-}" = "1" ] && [ "${APASTRA_NO_AGENT_HOOKS:-}" != "1" ]; then
  if [ -n "$PY" ] && [ -f "$SCRIPTS_DEST/hooks/agent_hook.py" ]; then
    echo "🪝 Installing Codex and Claude Code hooks..."
    "$PY" "$SCRIPTS_DEST/hooks/agent_hook.py" --install-agent-configs "$PROJECT_ROOT" "$SCRIPTS_DEST/hooks/agent_hook.py"
  else
    echo "⚠️  Skipping agent hooks: python3 or agent_hook.py was not available."
  fi
else
  echo "🪝 Skipping agent hooks. Set APASTRA_INSTALL_AGENT_HOOKS=1 to install them."
fi

# Same symlink layout as ./setup (see vercel-labs/skills Supported Agents table).
_symlink_target_rel="../../.agent/skills/apastra"
if [ "${APASTRA_NO_SKILL_SYMLINKS:-}" != "1" ]; then
  echo "🔗 Linking skills → .claude/skills/ and .agents/skills/"
  for _root in .claude .agents; do
    _parent="$PROJECT_ROOT/$_root/skills"
    mkdir -p "$_parent"
    if [ -e "$_parent/apastra" ] && [ ! -L "$_parent/apastra" ]; then
      echo "   ⚠️  Skip $_parent/apastra (exists and is not a symlink — remove or move it to retry)"
      continue
    fi
    ln -sfn "$_symlink_target_rel" "$_parent/apastra"
    echo "   → $_parent/apastra"
  done
fi

echo "✅ Apastra installed"
echo "   Skills:  .agent/skills/apastra/ (canonical)"
echo "   Scripts: .agent/scripts/apastra/"
echo "   CLI:     .agent/bin/apastra"
if [ "${APASTRA_INSTALL_AGENT_HOOKS:-}" = "1" ] && [ "${APASTRA_NO_AGENT_HOOKS:-}" != "1" ]; then
  echo "   Hooks:   .codex/ and .claude/settings.json"
else
  echo "   Hooks:   skipped (opt in with APASTRA_INSTALL_AGENT_HOOKS=1)"
fi
