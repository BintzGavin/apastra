import os
import yaml

def load_project_config():
    cwd = os.getcwd()
    while True:
        for ext in ['.yaml', '.yml']:
            config_path = os.path.join(cwd, f"promptops.config{ext}")
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        return yaml.safe_load(f) or {}
                except Exception:
                    return {}
        parent = os.path.dirname(cwd)
        if parent == cwd:
            break
        cwd = parent
    return {}
