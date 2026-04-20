#!/usr/bin/env bash
# npm postinstall — runs when someone does: npm install apastra
# Copies skills to .agent/skills/apastra/ and scripts to .agent/scripts/apastra/

set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(pwd)"

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
cp    "$PACKAGE_DIR/promptops/__init__.py" "$SCRIPTS_DEST/"

find "$SCRIPTS_DEST" -name "*.sh" -exec chmod +x {} \;

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

echo "✅ Apastra installed"
echo "   Skills:  .agent/skills/apastra/"
echo "   Scripts: .agent/scripts/apastra/"
