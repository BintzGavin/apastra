"""MCP access to the same suite execution path used by the CLI."""

import json
import sys
import yaml

from promptops.runtime.digest import load_asset
from promptops.runtime.suite import UnsafeReferenceError, asset_directory, evaluate_suite

def list_suites() -> list:
    """List suite identities in this workspace."""
    result = []
    for path in sorted(asset_directory("suites").glob("*")):
        if path.suffix not in (".json", ".yaml", ".yml"):
            continue
        try:
            suite = load_asset(path)
            if isinstance(suite, dict) and "id" in suite:
                result.append({key: suite.get(key, "") for key in ("id", "name", "description")})
        except (OSError, ValueError, yaml.YAMLError):
            print(f"Invalid suite: {path.name}", file=sys.stderr)
    return result


def run_evaluation(suite_id: str, revision_ref: str = "workspace", adapter_config: str | None = None, output_dir: str | None = None) -> str:
    """Execute a declared harness; retain evidence and report its evaluation verdict."""
    try:
        result = evaluate_suite(suite_id, adapter_config, output_dir, revision_ref)
    except UnsafeReferenceError as error:
        result = {"status": "error", "reason": "unsafe_ref", "message": str(error)}
    except FileNotFoundError as error:
        result = {"status": "error", "reason": "suite_not_found" if "suites asset" in str(error) else "asset_not_found", "message": str(error)}
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        result = {"status": "error", "reason": "evaluation_invalid", "message": str(error)}
    return json.dumps(result, sort_keys=True, allow_nan=False)


def start_mcp_server():
    from promptops.runtime.mcp_launcher import main
    return main(sys.argv[2:])
