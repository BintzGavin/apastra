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
    def resolve(self, prompt_id, override_path):
        """Resolves a prompt package from a local path."""
        if not os.path.exists(override_path):
            raise FileNotFoundError(f"Local override path not found: {override_path}")

        data = load_prompt_package(override_path)

        # Quick eval resolution
        if data and "prompt" in data:
            return {"id": prompt_id, "template": data["prompt"], "variables": {}}

        return data
