import sys
import os
import subprocess
import shlex
import yaml

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
    artifact_path = os.path.join(output_dir, "run_artifact.json")
    if not os.path.exists(artifact_path):
        print(f"Error: Expected run artifact not found at {artifact_path}")
        sys.exit(1)

    print(f"Success: Run artifact generated at {artifact_path}")

if __name__ == "__main__":
    main()
