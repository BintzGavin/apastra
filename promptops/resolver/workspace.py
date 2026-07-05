import os
import json
import yaml
import glob
from pathlib import PurePosixPath

def load_prompt_package(path):
    if path.endswith('.yaml') or path.endswith('.yml'):
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif path.endswith('.json'):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def validate_prompt_id(prompt_id):
    if not isinstance(prompt_id, str) or not prompt_id.strip():
        raise ValueError("prompt_id must be a non-empty string")
    if "\\" in prompt_id:
        raise ValueError(f"Unsafe prompt_id: {prompt_id}")

    path = PurePosixPath(prompt_id)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"Unsafe prompt_id: {prompt_id}")
    return prompt_id

class WorkspaceResolver:
    def __init__(self):
        self.cache = {}

    def _detect_minimal_mode(self):
        prompt_files = (
            glob.glob('prompts/*.yaml')
            + glob.glob('prompts/*.json')
            + glob.glob('promptops/prompts/*.yaml')
            + glob.glob('promptops/prompts/*.json')
            + glob.glob('promptops/prompts/*/prompt.yaml')
            + glob.glob('promptops/prompts/*/prompt.json')
        )
        return len(prompt_files) <= 3

    def resolve(self, prompt_id):
        """Resolves a prompt package from a workspace path."""
        prompt_id = validate_prompt_id(prompt_id)

        paths_to_try = [
            (f"promptops/prompts/{prompt_id}.yaml", False),
            (f"promptops/prompts/{prompt_id}.json", False),
            (f"promptops/prompts/{prompt_id}/prompt.yaml", False),
            (f"promptops/prompts/{prompt_id}/prompt.json", False),
            (f"promptops/evals/{prompt_id}.yaml", True),
            (f"promptops/evals/{prompt_id}.json", True)
        ]

        if self._detect_minimal_mode():
            minimal_paths = [
                (f"prompts/{prompt_id}.yaml", False),
                (f"prompts/{prompt_id}.json", False),
                (f"evals/{prompt_id}.yaml", True),
                (f"evals/{prompt_id}.json", True)
            ]
            paths_to_try = minimal_paths + paths_to_try

        for path, is_quick_eval in paths_to_try:
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                if path in self.cache and self.cache[path]['mtime'] == mtime:
                    data = self.cache[path]['data']
                else:
                    data = load_prompt_package(path)
                    self.cache[path] = {'mtime': mtime, 'data': data}

                if is_quick_eval:
                    if data and "prompt" in data:
                        return {"id": prompt_id, "template": data["prompt"], "variables": {}}
                else:
                    return data
        return None
