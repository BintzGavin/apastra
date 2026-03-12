import subprocess
import yaml
import json
import re

def parse_version(v):
    # Remove 'v' prefix if present
    v = v.lstrip('v')
    m = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$', v)
    if m:
        major, minor, patch = map(int, m.groups()[:3])
        prerelease = m.group(4)
        return (major, minor, patch, prerelease)
    return None

def match_semver(tag, range_str):
    v = parse_version(tag)
    if not v:
        return False

    # We only match stable versions unless explicitly requested or handled
    if v[3] is not None:
        return False

    range_str = range_str.lstrip('v')

    if range_str.startswith('^'):
        target = parse_version(range_str[1:])
        if not target: return False
        if target[0] == 0:
            if target[1] == 0:
                return v[0] == 0 and v[1] == 0 and v[2] == target[2]
            return v[0] == 0 and v[1] == target[1] and v[2] >= target[2]
        else:
            return v[0] == target[0] and v[:3] >= target[:3]
    elif range_str.startswith('~'):
        target = parse_version(range_str[1:])
        if not target: return False
        return v[0] == target[0] and v[1] == target[1] and v[2] >= target[2]
    else:
        target = parse_version(range_str)
        if not target: return False
        return v[:3] == target[:3]

class GitRefResolver:
    def resolve(self, prompt_id, pin):
        """Resolves a prompt package from a git ref."""
        if pin.startswith("semver:"):
            range_str = pin.replace("semver:", "")
            result = subprocess.run(
                ["git", "tag", "--list"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                raise RuntimeError("Failed to execute git tag --list")

            tags = result.stdout.splitlines()
            valid_tags = [t for t in tags if match_semver(t, range_str)]
            if not valid_tags:
                raise RuntimeError(f"No matching semver tag found for '{range_str}'")

            # Sort tags by semver descending. We only care about the stable parts
            # (which match_semver already filters down to stable tags).
            valid_tags.sort(key=lambda x: parse_version(x)[:3], reverse=True)
            pin = valid_tags[0]

        try:
            # Try to resolve yaml first
            result = subprocess.run(
                ["git", "show", f"{pin}:promptops/prompts/{prompt_id}.yaml"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                return yaml.safe_load(result.stdout)

            # If yaml fails, try json
            result_json = subprocess.run(
                ["git", "show", f"{pin}:promptops/prompts/{prompt_id}.json"],
                capture_output=True,
                text=True,
                check=False
            )
            if result_json.returncode == 0:
                return json.loads(result_json.stdout)

            # If flat files fail, try directory yaml
            result_dir_yaml = subprocess.run(
                ["git", "show", f"{pin}:promptops/prompts/{prompt_id}/prompt.yaml"],
                capture_output=True,
                text=True,
                check=False
            )
            if result_dir_yaml.returncode == 0:
                return yaml.safe_load(result_dir_yaml.stdout)

            # If directory yaml fails, try directory json
            result_dir_json = subprocess.run(
                ["git", "show", f"{pin}:promptops/prompts/{prompt_id}/prompt.json"],
                capture_output=True,
                text=True,
                check=False
            )
            if result_dir_json.returncode == 0:
                return json.loads(result_dir_json.stdout)

            raise RuntimeError(f"Failed to resolve prompt '{prompt_id}' at git ref '{pin}'")

        except Exception as e:
            raise RuntimeError(f"Git ref resolution failed for prompt '{prompt_id}' at '{pin}': {str(e)}")
