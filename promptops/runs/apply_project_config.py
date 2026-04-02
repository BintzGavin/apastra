#!/usr/bin/env python3
import sys
import json
import yaml
import os

def load_project_config(config_path="promptops.config.yaml"):
    if not os.path.exists(config_path):
        return {}
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading {config_path}: {e}", file=sys.stderr)
        return {}

def extract_defaults(config):
    return {
        "defaults": config.get("defaults", {}),
        "thresholds": config.get("thresholds", {})
    }

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "promptops.config.yaml"
    config = load_project_config(config_path)
    defaults = extract_defaults(config)
    print(json.dumps(defaults))
