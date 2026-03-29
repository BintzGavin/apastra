import argparse
import json
import logging
import sys
import yaml
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_yaml(path):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load YAML {path}: {e}")
        return None

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON {path}: {e}")
        return None

def emit_to_endpoint(endpoint, payload, is_dry_run, system_name):
    if is_dry_run:
        logger.info(f"[Dry Run] Would send to {system_name} endpoint {endpoint} with payload size: {len(json.dumps(payload))} bytes")
        return

    logger.info(f"Sending to {system_name} endpoint {endpoint}")
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(endpoint, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            if response.status in (200, 201, 202):
                logger.info(f"Successfully sent artifacts to {system_name} endpoint {endpoint}")
            else:
                logger.warning(f"Unexpected status code {response.status} from {system_name} endpoint {endpoint}")
    except urllib.error.URLError as e:
        logger.error(f"Failed to connect to {system_name} endpoint {endpoint}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while sending to {system_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Emit evaluation artifacts to observability systems.")
    parser.add_argument("--config", required=True, help="Path to observability.yaml configuration file.")
    parser.add_argument("--scorecard", help="Path to scorecard.json.")
    parser.add_argument("--regression-report", help="Path to regression report JSON.")
    parser.add_argument("--run-manifest", help="Path to run manifest JSON.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without sending actual network requests.")
    args = parser.parse_args()

    config = load_yaml(args.config)
    if not config or "adapters" not in config:
        logger.error("Invalid observability configuration.")
        sys.exit(1)

    artifacts = {}
    if args.scorecard:
        data = load_json(args.scorecard)
        if data: artifacts["scorecard"] = data
    if args.regression_report:
        data = load_json(args.regression_report)
        if data: artifacts["regression_report"] = data
    if args.run_manifest:
        data = load_json(args.run_manifest)
        if data: artifacts["run_manifest"] = data

    if not artifacts:
        logger.warning("No artifacts loaded. Exiting.")
        sys.exit(0)

    for adapter in config.get("adapters", []):
        adapter_type = adapter.get("type")
        endpoint = adapter.get("endpoint")
        emit_types = adapter.get("emit", [])

        if not adapter_type or not endpoint:
            logger.warning("Skipping adapter due to missing type or endpoint.")
            continue

        selected_artifacts = {k: v for k, v in artifacts.items() if k in emit_types}

        if not selected_artifacts:
            logger.info(f"No specified artifacts found to emit for adapter {adapter_type}.")
            continue

        payload = {"source": "apastra", "artifacts": selected_artifacts}

        if adapter_type == "langfuse":
            emit_to_endpoint(endpoint, payload, args.dry_run, "Langfuse")
        elif adapter_type == "opentelemetry":
            emit_to_endpoint(endpoint, payload, args.dry_run, "OpenTelemetry")
        else:
            logger.warning(f"Unknown adapter type: {adapter_type}")

if __name__ == "__main__":
    main()
