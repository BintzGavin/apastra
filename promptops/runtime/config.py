import os
import yaml
import json
import jsonschema

def load_project_config():
    cwd = os.getcwd()
    while True:
        for ext in ['.yaml', '.yml']:
            config_path = os.path.join(cwd, f"promptops.config{ext}")
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config_data = yaml.safe_load(f) or {}
                    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas", "promptops-config.schema.json")
                    if os.path.exists(schema_path):
                        with open(schema_path, 'r') as sf:
                            schema = json.load(sf)
                        try:
                            jsonschema.validate(instance=config_data, schema=schema)
                        except jsonschema.exceptions.ValidationError as e:
                            raise ValueError(f"Config validation failed: {e.message}")
                    return config_data
                except ValueError:
                    raise
                except Exception:
                    return {}
        parent = os.path.dirname(cwd)
        if parent == cwd:
            break
        cwd = parent
    return {}

def apply_config_defaults(suite: dict, config: dict) -> dict:
    if not config:
        return suite
    if 'defaults' in config:
        defaults = config['defaults']
        if 'model' in defaults and 'model_matrix' not in suite:
            suite['model_matrix'] = [defaults['model']]

        if 'temperature' in defaults or 'max_tokens' in defaults:
            if 'sampling_config' not in suite:
                suite['sampling_config'] = {}
            if 'temperature' in defaults and 'temperature' not in suite['sampling_config']:
                suite['sampling_config']['temperature'] = defaults['temperature']
            if 'max_tokens' in defaults and 'max_tokens' not in suite['sampling_config']:
                suite['sampling_config']['max_tokens'] = defaults['max_tokens']

    if 'thresholds' in config:
        if 'thresholds' not in suite:
            suite['thresholds'] = config['thresholds']
        else:
            for k, v in config['thresholds'].items():
                if k not in suite['thresholds']:
                    suite['thresholds'][k] = v

    if 'baseline' in config:
        if 'baseline' not in suite:
            suite['baseline'] = config['baseline']
        else:
            for k, v in config['baseline'].items():
                if k not in suite['baseline']:
                    suite['baseline'][k] = v

    return suite
