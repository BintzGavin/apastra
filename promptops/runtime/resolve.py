import json
import os
import yaml

from promptops.resolver.chain import ResolverChain

class ManifestWrapper:
    def __init__(self, data=None):
        self.data = data or {}

    def get_rules(self, prompt_id):
        prompts = self.data.get("prompts", {})
        if prompt_id in prompts:
            return prompts[prompt_id]
        return {}

class OverrideManifest:
    def __init__(self, override_path):
        self.override_path = override_path

    def get_rules(self, p_id):
        return {"override": self.override_path}

class PinManifest:
    def __init__(self, pin_ref):
        self.pin_ref = pin_ref

    def get_rules(self, p_id):
        return {"pin": self.pin_ref}


from promptops.runtime.digest import compute_digest_from_dict

def load_manifest(ref_context):
    if not ref_context:
        return ManifestWrapper()

    if isinstance(ref_context, str):
        if os.path.exists(ref_context):
            with open(ref_context, 'r') as f:
                if ref_context.endswith('.yaml') or ref_context.endswith('.yml'):
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)

            if isinstance(data, dict) and ("prompts" in data or "version" in data):
                return ManifestWrapper(data)

            return OverrideManifest(ref_context)
        else:
            return PinManifest(ref_context)
    return ManifestWrapper()

from promptops.runtime.config import load_project_config

def resolve(prompt_id, ref_context=None, variables=None, dataset_digest=None, harness_version=None, model_ids=None):
    manifest = load_manifest(ref_context)
    project_config = load_project_config()
    project_defaults = project_config.get('defaults', {})
    prompt_spec = ResolverChain().resolve(prompt_id, manifest)

    if not prompt_spec:
        raise RuntimeError(f"Failed to resolve prompt '{prompt_id}'")

    if isinstance(prompt_spec, str):
        prompt_spec = {"id": prompt_id, "variables": {}, "template": prompt_spec}

    import jsonschema

    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.abspath(os.path.join(current_dir, "..", "schemas", "prompt-spec.schema.json"))

    with open(schema_path, 'r') as sf:
        schema = json.load(sf)

    try:
        jsonschema.validate(instance=prompt_spec, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise RuntimeError(f"Resolved prompt failed schema validation: {e.message}")

    rules = manifest.get_rules(prompt_id) if hasattr(manifest, 'get_rules') else {}
    defaults = manifest.data.get('defaults', {}) if hasattr(manifest, 'data') and isinstance(manifest.data, dict) else {}

    if model_ids is None:
        model = rules.get('model', defaults.get('model', project_defaults.get('model')))
        if model:
            model_ids = [model]

    metadata = {
        "prompt_digest": compute_digest_from_dict(prompt_spec),
        "verification": "unverified",
    }
    if model_ids:
        metadata["model_ids"] = model_ids
    if dataset_digest:
        metadata["dataset_digest"] = dataset_digest
    if harness_version:
        metadata["harness_version"] = harness_version
    provenance = None
    if isinstance(prompt_spec, dict) and "provenance" in prompt_spec:
        provenance = prompt_spec["provenance"]
    elif isinstance(rules, dict) and "provenance" in rules:
        provenance = rules["provenance"]

    if provenance:
        metadata["provenance"] = provenance

    template = prompt_spec.get('template') if isinstance(prompt_spec, dict) else prompt_spec

    from promptops.runtime.render import render_template
    rendered_prompt = render_template(template, variables or {})
    return rendered_prompt, metadata
