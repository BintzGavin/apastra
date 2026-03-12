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
    def resolve(self, prompt_id):
        """Resolves a prompt package from a workspace path."""
        workspace_path_yaml = f"promptops/prompts/{prompt_id}.yaml"
        if os.path.exists(workspace_path_yaml):
            return load_prompt_package(workspace_path_yaml)

        workspace_path_json = f"promptops/prompts/{prompt_id}.json"
        if os.path.exists(workspace_path_json):
            return load_prompt_package(workspace_path_json)

        return None
