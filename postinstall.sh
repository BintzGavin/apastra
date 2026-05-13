#!/usr/bin/env bash
# npm postinstall — runs when someone does: npm install apastra
# Copies skills to .agent/skills/apastra/, scripts to .agent/scripts/apastra/,
# and symlinks skills into .claude/skills/ and .agents/skills/ (unless APASTRA_NO_SKILL_SYMLINKS=1).
# Also installs Codex and Claude Code hooks unless APASTRA_NO_AGENT_HOOKS=1.

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
cp -r "$PACKAGE_DIR/promptops/runs"       "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/resolver"   "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/schemas"    "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/validators" "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/harnesses"  "$SCRIPTS_DEST/"
cp -r "$PACKAGE_DIR/promptops/hooks"      "$SCRIPTS_DEST/"
cp    "$PACKAGE_DIR/promptops/__init__.py" "$SCRIPTS_DEST/"

find "$SCRIPTS_DEST" -name "*.sh" -exec chmod +x {} \;
find "$SCRIPTS_DEST/hooks" -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

# Check Python dependencies
echo "📦 Checking Python dependencies..."
PY="$(command -v python3 || command -v python || true)"
PIP_DEPS_OK=0
if [ -n "$PY" ] && "$PY" -c "import yaml, jsonschema" &>/dev/null; then
  echo "   pyyaml + jsonschema already present."
  PIP_DEPS_OK=1
else
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
  echo "⚠️  Could not auto-install pyyaml + jsonschema."
  echo "   The apastra runtime scripts require both. Install manually via one of:"
  echo "     pipx install pyyaml && pipx install jsonschema"
  echo "     python3 -m venv .venv && source .venv/bin/activate && pip install pyyaml jsonschema"
  echo "     pip install --user pyyaml jsonschema"
  echo "     pip install --break-system-packages pyyaml jsonschema   # not recommended"
  echo ""
fi

if [ "${APASTRA_NO_AGENT_HOOKS:-}" != "1" ]; then
  if [ -n "$PY" ] && [ -f "$SCRIPTS_DEST/hooks/agent_hook.py" ]; then
    echo "🪝 Installing Codex and Claude Code hooks..."
    "$PY" "$SCRIPTS_DEST/hooks/agent_hook.py" --install-agent-configs "$PROJECT_ROOT" "$SCRIPTS_DEST/hooks/agent_hook.py"
  else
    echo "⚠️  Skipping agent hooks: python3 or agent_hook.py was not available."
  fi
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
if [ "${APASTRA_NO_AGENT_HOOKS:-}" != "1" ]; then
  echo "   Hooks:   .codex/ and .claude/settings.json"
fi
