import os
import yaml
import json
import jsonschema

def emit_artifacts(output_dir):
    config_path = "promptops/delivery/observability.yaml"
    if not os.path.exists(config_path):
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas", "observability-adapter-config.schema.json")
    with open(schema_path, 'r') as sf:
        schema = json.load(sf)
    jsonschema.validate(instance=config, schema=schema)

    adapters = config.get("adapters", [])
    for adapter in adapters:
        adapter_type = adapter.get("type")
        endpoint = adapter.get("endpoint")
        emits = adapter.get("emit", [])

        for emit_file in emits:
            file_path = os.path.join(output_dir, f"{emit_file}.json")
            if os.path.exists(file_path):
                print(f"Observability adapter '{adapter_type}' mocking emission of '{emit_file}' to endpoint '{endpoint}'")
            else:
                print(f"Observability adapter '{adapter_type}' skipped '{emit_file}': file not found in output_dir")
