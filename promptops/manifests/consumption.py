import json
import os
import jsonschema

def validate_manifest(manifest_content):
    if not isinstance(manifest_content, dict):
        return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.abspath(os.path.join(current_dir, "..", "schemas", "consumption-manifest.schema.json"))

    with open(schema_path, 'r') as sf:
        schema = json.load(sf)

    try:
        jsonschema.validate(instance=manifest_content, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise RuntimeError(f"Manifest schema validation failed: {e.message}")