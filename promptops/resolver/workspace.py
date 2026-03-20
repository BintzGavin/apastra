import os
import json
import yaml

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
