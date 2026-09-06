"""Provider-specific artifact delivery requires an implemented sink adapter."""


def emit_artifacts(output_dir):
    return {"status": "unsupported", "reason": "Observability delivery is not implemented; artifacts remain local.", "receipts": []}
