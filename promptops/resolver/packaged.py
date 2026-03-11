class PackagedResolver:
    def resolve(self, prompt_id, ref):
        """Resolves a prompt package from a digest or URL."""
        # In a real implementation, this would download the package,
        # verify the digest, and extract the prompt.
        # For the reference implementation, we return a mock template
        # if it's a valid looking mock reference, otherwise raise an error.
        if ref.startswith('sha256:') and 'invalid' not in ref:
            return {"template": "mock packaged prompt"}
        elif ref.startswith('https://') or ref.startswith('oci://'):
            return {"template": "mock remote prompt"}
        else:
            raise RuntimeError(f"Failed to resolve packaged artifact '{prompt_id}' with ref '{ref}'")
