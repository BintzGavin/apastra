import promptops.runtime
def patch_resolve(prompt_id, ref_context=None, variables=None, dataset_digest=None, harness_version=None, model_ids=None):
    from promptops.runtime.resolve import load_manifest, compute_digest_from_dict
    from promptops.resolver.chain import ResolverChain
    import jsonschema
    import json
    import os
    import sys
    from promptops.runtime.render import render_template

    manifest = load_manifest(ref_context)
    prompt_spec = ResolverChain().resolve(prompt_id, manifest)

    if not prompt_spec:
        raise RuntimeError(f"Failed to resolve prompt '{prompt_id}'")

    if isinstance(prompt_spec, str):
        prompt_spec = {"id": prompt_id, "variables": {}, "template": prompt_spec}

    current_dir = os.path.dirname(os.path.abspath(sys.modules['promptops.runtime.resolve'].__file__))
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
        model = rules.get('model', defaults.get('model'))
        if model:
            model_ids = [model]

    metadata = {
        "prompt_digest": compute_digest_from_dict(prompt_spec),
    }
    if model_ids:
        metadata["model_ids"] = model_ids
    if dataset_digest:
        metadata["dataset_digest"] = dataset_digest
    if harness_version:
        metadata["harness_version"] = harness_version

    template = prompt_spec.get('template') if isinstance(prompt_spec, dict) else prompt_spec
    rendered_prompt = render_template(template, variables or {})
    return rendered_prompt, metadata

print(patch_resolve('summarize', dataset_digest='abc', harness_version='v1', model_ids=['gpt-4']))
