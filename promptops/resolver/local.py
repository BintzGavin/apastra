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

class LocalResolver:
    def __init__(self):
        self.cache = {}

    def resolve(self, prompt_id, override_path):
        """Resolves a prompt package from a local path."""
        if not os.path.exists(override_path):
            raise FileNotFoundError(f"Local override path not found: {override_path}")

        mtime = os.path.getmtime(override_path)

        if override_path in self.cache and self.cache[override_path]['mtime'] == mtime:
            data = self.cache[override_path]['data']
        else:
            data = load_prompt_package(override_path)
            self.cache[override_path] = {'mtime': mtime, 'data': data}

        # Quick eval resolution
        if data and "prompt" in data:
            return {"id": prompt_id, "template": data["prompt"], "variables": {}}

        return data
