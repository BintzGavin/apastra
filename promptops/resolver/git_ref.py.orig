import subprocess
import yaml
import json
import re
import os
import tempfile
import shutil

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
    def __init__(self):
        self.cache = {}

    def _read_from_dir(self, directory, prompt_id):
        # Try flat yaml
        path = os.path.join(directory, "promptops", "prompts", f"{prompt_id}.yaml")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f)

        # Try flat json
        path = os.path.join(directory, "promptops", "prompts", f"{prompt_id}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)

        # Try directory yaml
        path = os.path.join(directory, "promptops", "prompts", prompt_id, "prompt.yaml")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f)

        # Try directory json
        path = os.path.join(directory, "promptops", "prompts", prompt_id, "prompt.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)

        # Try quick eval yaml
        path = os.path.join(directory, "promptops", "evals", f"{prompt_id}.yaml")
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if data and "prompt" in data:
                    return {"id": prompt_id, "template": data["prompt"], "variables": {}}

        # Try quick eval json
        path = os.path.join(directory, "promptops", "evals", f"{prompt_id}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                if data and "prompt" in data:
                    return {"id": prompt_id, "template": data["prompt"], "variables": {}}

        return None

    def resolve(self, prompt_id, pin):
        """Resolves a prompt package from a git ref."""
        cache_key = (prompt_id, pin)
        if cache_key in self.cache:
            return self.cache[cache_key]

        if pin.startswith('git+'):
            # Parse remote git URL and ref
            url_part, ref_part = pin[4:].split('#', 1)

            if ref_part.startswith('semver:'):
                range_str = ref_part.replace('semver:', '')
                result = subprocess.run(
                    ["git", "ls-remote", "--tags", url_part],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    raise RuntimeError(f"Failed to execute git ls-remote --tags {url_part}")

                tags = []
                for line in result.stdout.splitlines():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        tag = parts[1]
                        if tag.startswith('refs/tags/'):
                            tag = tag[len('refs/tags/'):]
                        if tag.endswith('^{}'):
                            tag = tag[:-3]
                        tags.append(tag)

                valid_tags = [t for t in set(tags) if match_semver(t, range_str)]
                if not valid_tags:
                    raise RuntimeError(f"No matching semver tag found for '{range_str}' on remote '{url_part}'")

                valid_tags.sort(key=lambda x: parse_version(x)[:3], reverse=True)
                ref_part = valid_tags[0]

            temp_dir = tempfile.mkdtemp()
            try:
                # Use git archive to extract specific files to a temp directory
                # First get the archive from the remote
                archive_p = subprocess.run(
                    ["git", "archive", f"--remote={url_part}", ref_part],
                    capture_output=True,
                    check=False
                )

                if archive_p.returncode == 0:
                    # Then tar it into temp_dir
                    tar_p = subprocess.run(
                        ["tar", "-x", "-C", temp_dir],
                        input=archive_p.stdout,
                        capture_output=True,
                        check=False
                    )

                    if tar_p.returncode != 0:
                        raise RuntimeError(f"Failed to tar remote git archive: {tar_p.stderr.decode('utf-8')}")
                else:
                    is_sha = len(ref_part) == 40 and all(c in '0123456789abcdefABCDEF' for c in ref_part)
                    if is_sha:
                        result = subprocess.run(["git", "clone", url_part, temp_dir], capture_output=True, check=False)
                        if result.returncode == 0:
                            result = subprocess.run(["git", "-C", temp_dir, "checkout", ref_part], capture_output=True, check=False)
                        if result.returncode != 0:
                            raise RuntimeError(f"Failed to fetch remote git repo: {result.stderr.decode('utf-8')}")
                    else:
                        # Fallback to shallow clone if git archive is disabled on the remote
                        clone_cmd = ["git", "clone", "--depth", "1", "--branch", ref_part, url_part, temp_dir]
                        result = subprocess.run(clone_cmd, capture_output=True, check=False)
                        if result.returncode != 0:
                            raise RuntimeError(f"Failed to fetch remote git repo: {result.stderr.decode('utf-8')}")

                # Read files from temp directory using existing fallback logic
                res = self._read_from_dir(temp_dir, prompt_id)
                if res is not None:
                    self.cache[cache_key] = res
                    return res
                else:
                    raise RuntimeError(f"Failed to resolve prompt '{prompt_id}' at remote git ref '{pin}'")
            finally:
                shutil.rmtree(temp_dir)

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
                res = yaml.safe_load(result.stdout)
                self.cache[cache_key] = res
                return res

            # If yaml fails, try json
            result_json = subprocess.run(
                ["git", "show", f"{pin}:promptops/prompts/{prompt_id}.json"],
                capture_output=True,
                text=True,
                check=False
            )
            if result_json.returncode == 0:
                res = json.loads(result_json.stdout)
                self.cache[cache_key] = res
                return res

            # If flat files fail, try directory yaml
            result_dir_yaml = subprocess.run(
                ["git", "show", f"{pin}:promptops/prompts/{prompt_id}/prompt.yaml"],
                capture_output=True,
                text=True,
                check=False
            )
            if result_dir_yaml.returncode == 0:
                res = yaml.safe_load(result_dir_yaml.stdout)
                self.cache[cache_key] = res
                return res

            # If directory yaml fails, try directory json
            result_dir_json = subprocess.run(
                ["git", "show", f"{pin}:promptops/prompts/{prompt_id}/prompt.json"],
                capture_output=True,
                text=True,
                check=False
            )
            if result_dir_json.returncode == 0:
                res = json.loads(result_dir_json.stdout)
                self.cache[cache_key] = res
                return res

            # Quick eval resolution
            result_eval_yaml = subprocess.run(
                ["git", "show", f"{pin}:promptops/evals/{prompt_id}.yaml"],
                capture_output=True, text=True, check=False
            )
            if result_eval_yaml.returncode == 0:
                data = yaml.safe_load(result_eval_yaml.stdout)
                if data and "prompt" in data:
                    res = {"id": prompt_id, "template": data["prompt"], "variables": {}}
                    self.cache[cache_key] = res
                    return res

            result_eval_json = subprocess.run(
                ["git", "show", f"{pin}:promptops/evals/{prompt_id}.json"],
                capture_output=True, text=True, check=False
            )
            if result_eval_json.returncode == 0:
                data = json.loads(result_eval_json.stdout)
                if data and "prompt" in data:
                    res = {"id": prompt_id, "template": data["prompt"], "variables": {}}
                    self.cache[cache_key] = res
                    return res

            raise RuntimeError(f"Failed to resolve prompt '{prompt_id}' at git ref '{pin}'")

        except Exception as e:
            raise RuntimeError(f"Git ref resolution failed for prompt '{prompt_id}' at '{pin}': {str(e)}")
