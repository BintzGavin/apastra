import os
import json
import yaml
import glob

def load_prompt_package(path):
    if path.endswith('.yaml') or path.endswith('.yml'):
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    elif path.endswith('.json'):
        with open(path, 'r') as f:
            return json.load(f)
    return None

class WorkspaceResolver:
    def __init__(self):
        self.cache = {}

    def _detect_minimal_mode(self):
        prompt_files = glob.glob('prompts/*.yaml') + glob.glob('prompts/*.json') +                        glob.glob('promptops/prompts/*.yaml') + glob.glob('promptops/prompts/*.json') +                        glob.glob('promptops/prompts/*/prompt.yaml') + glob.glob('promptops/prompts/*/prompt.json')
        return len(prompt_files) <= 3

    def resolve(self, prompt_id):
        """Resolves a prompt package from a workspace path."""
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
