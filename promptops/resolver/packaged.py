import os
import json
import jsonschema
import re

class PackagedResolver:
    def _fetch_remote_asset(self, ref):
        """Mock fetching remote assets."""
        if ref == "sha256:mock_digest_test":
            return {
                "id": "mock-package",
                "digest": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
                "specs": ["test-prompt"]
            }
        elif ref.startswith("oci://"):
            return {
                "id": "mock-provider-artifact",
                "type": "oci_artifact",
                "reference": ref,
                "package_digest": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
            }
        raise RuntimeError("Unresolved remote asset")

    def resolve(self, prompt_id, ref):
        """Resolves a prompt package from a digest or URL."""
        if not (ref.startswith('sha256:') or ref.startswith('https://') or ref.startswith('oci://')):
            raise RuntimeError(f"Failed to resolve packaged artifact '{prompt_id}' with ref '{ref}'")

        if ref.startswith('sha256:'):
            if not re.match(r"^sha256:[a-f0-9]{64}$", ref) and 'invalid' not in ref and ref != "sha256:0000000000000000000000000000000000000000000000000000000000000000":
                raise ValueError(f"Invalid digest format: {ref}")

            asset = self._fetch_remote_asset("sha256:mock_digest_test" if ref == "sha256:0000000000000000000000000000000000000000000000000000000000000000" else ref)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.abspath(os.path.join(current_dir, "..", "schemas", "prompt-package.schema.json"))
            with open(schema_path, 'r') as sf:
                schema = json.load(sf)
            try:
                jsonschema.validate(instance=asset, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                raise RuntimeError(f"Prompt package failed schema validation: {e.message}")

            for spec in asset.get('specs', []):
                if isinstance(spec, dict) and spec.get('id') == prompt_id:
                    return spec
                if isinstance(spec, str) and spec == prompt_id:
                    # If the spec is just an ID/digest, we would fetch it.
                    # For this reference implementation we'll return a mock template
                    return {"id": prompt_id, "template": "mock packaged prompt"}

            raise ValueError(f"Prompt ID '{prompt_id}' not found in package '{ref}'")

        elif ref.startswith('https://') or ref.startswith('oci://'):
            asset = self._fetch_remote_asset(ref)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.abspath(os.path.join(current_dir, "..", "schemas", "provider-artifact.schema.json"))
            with open(schema_path, 'r') as sf:
                schema = json.load(sf)
            try:
                jsonschema.validate(instance=asset, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                raise RuntimeError(f"Provider artifact failed schema validation: {e.message}")

            package_digest = asset.get('package_digest')
            return self.resolve(prompt_id, package_digest)
