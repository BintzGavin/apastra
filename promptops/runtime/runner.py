import sys
import os
import subprocess
import shlex
import yaml
import json
import jsonschema
from promptops.runtime.config import load_project_config, apply_config_defaults

def main():
    if len(sys.argv) != 4:
        print("Usage: python runner.py <run_request.json> <adapter_config.yaml> <output_dir>")
        sys.exit(1)

    request_path = sys.argv[1]
    adapter_path = sys.argv[2]
    output_dir = sys.argv[3]

    if not os.path.exists(request_path):
        print(f"Error: Run request file not found: {request_path}")
        sys.exit(1)


    if not os.path.exists(adapter_path):
        print(f"Error: Adapter config file not found: {adapter_path}")
        sys.exit(1)

    # Load and apply project config
    try:
        project_config = load_project_config()
        if project_config:
            with open(request_path, 'r') as f:
                run_request = json.load(f)

            run_request = apply_config_defaults(run_request, project_config)

            # Write the updated request to a temporary file to avoid mutating the original input
            import tempfile
            fd, temp_path = tempfile.mkstemp(suffix=".json")
            with os.fdopen(fd, 'w') as f:
                json.dump(run_request, f, indent=2)
            request_path = temp_path
    except Exception as e:
        print(f"Error processing project config: {e}")
        sys.exit(1)


    with open(adapter_path, 'r') as f:
        adapter_config = yaml.safe_load(f)

    entrypoint = adapter_config.get("entrypoint")
    if not entrypoint:
        print(f"Error: No entrypoint defined in {adapter_path}")
        sys.exit(1)

    # Required env vars
    env_vars = adapter_config.get("env_vars", [])
    for var in env_vars:
        if var not in os.environ:
            print(f"Warning: Required environment variable {var} not set.")

    # Execute
    cmd_args = shlex.split(entrypoint)
    cmd_args.extend([request_path, output_dir])
    print(f"Executing: {' '.join(cmd_args)}")

    result = subprocess.run(cmd_args)
    if result.returncode != 0:
        print(f"Error: Adapter execution failed with code {result.returncode}")
        sys.exit(result.returncode)

    # Validate output
    schema_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas")

    required_files = {
        "run_manifest.json": "run-manifest.schema.json",
        "scorecard.json": "scorecard.schema.json",
        "cases.jsonl": "run-case.schema.json",
        "artifact_refs.json": "artifact-refs.schema.json"
    }

    for filename, schema_file in required_files.items():
        filepath = os.path.join(output_dir, filename)
        schema_path = os.path.join(schema_dir, schema_file)

        if not os.path.exists(filepath):
            print(f"Error: Required output file not found: {filepath}")
            sys.exit(1)

        with open(schema_path, 'r') as sf:
            schema = json.load(sf)

        try:
            if filename.endswith(".jsonl"):
                with open(filepath, 'r') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                        instance = json.loads(line)
                        jsonschema.validate(instance=instance, schema=schema)
            else:
                with open(filepath, 'r') as f:
                    instance = json.load(f)
                jsonschema.validate(instance=instance, schema=schema)
        except jsonschema.ValidationError as e:
            print(f"Error: Schema validation failed for {filename}: {e.message}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {filename}: {str(e)}")
            sys.exit(1)

    # Optional failures.json
    failures_path = os.path.join(output_dir, "failures.json")
    if os.path.exists(failures_path):
        failures_schema_path = os.path.join(schema_dir, "run-failures.schema.json")
        with open(failures_schema_path, 'r') as sf:
            failures_schema = json.load(sf)
        try:
            with open(failures_path, 'r') as f:
                failures_instance = json.load(f)
            jsonschema.validate(instance=failures_instance, schema=failures_schema)
        except jsonschema.ValidationError as e:
            print(f"Error: Schema validation failed for failures.json: {e.message}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in failures.json: {str(e)}")
            sys.exit(1)

    from promptops.runtime.observability import emit_artifacts
    try:
        emit_artifacts(output_dir)
    except Exception as e:
        print(f"Warning: Failed to emit observability artifacts: {e}")

    print(f"Success: Run artifacts generated and validated at {output_dir}")

if __name__ == "__main__":
    main()
