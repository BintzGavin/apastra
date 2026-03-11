import json
import os
import yaml
import hashlib

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


def compute_digest(prompt_spec):
    if not isinstance(prompt_spec, dict):
        return None
    canonical_json = json.dumps(prompt_spec, separators=(',', ':'), sort_keys=True)
    digest = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    return f"sha256:{digest}"

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

            if isinstance(data, dict) and "prompts" in data and "version" in data:
                return ManifestWrapper(data)

            return OverrideManifest(ref_context)
        else:
            return PinManifest(ref_context)
    return ManifestWrapper()

def resolve(prompt_id, ref_context=None):
    manifest = load_manifest(ref_context)
    prompt_spec = ResolverChain().resolve(prompt_id, manifest)

    if not prompt_spec:
        raise RuntimeError(f"Failed to resolve prompt '{prompt_id}'")

    if isinstance(prompt_spec, str):
        prompt_spec = {"template": prompt_spec}

    metadata = {
        "prompt_digest": compute_digest(prompt_spec),
    }

    template = prompt_spec.get('template') if isinstance(prompt_spec, dict) else prompt_spec
    return template, metadata