import os

def load_prompt_package(path):
    # Stub for loading a prompt package
    return f"Loaded prompt from {path}"

class LocalResolver:
    def resolve(self, prompt_id, override_path):
        """Resolves a prompt package from a local path."""
        if not os.path.exists(override_path):
            raise FileNotFoundError(f"Local override path not found: {override_path}")

        return load_prompt_package(override_path)
