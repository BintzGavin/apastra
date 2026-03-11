import subprocess
import yaml
import json

class GitRefResolver:
    def resolve(self, prompt_id, pin):
        """Resolves a prompt package from a git ref."""
        try:
            # Try to resolve yaml first
            result = subprocess.run(
                ["git", "show", f"{pin}:promptops/{prompt_id}.yaml"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                return yaml.safe_load(result.stdout)

            # If yaml fails, try json
            result_json = subprocess.run(
                ["git", "show", f"{pin}:promptops/{prompt_id}.json"],
                capture_output=True,
                text=True,
                check=False
            )
            if result_json.returncode == 0:
                return json.loads(result_json.stdout)

            raise RuntimeError(f"Failed to resolve prompt '{prompt_id}' at git ref '{pin}'")

        except Exception as e:
            raise RuntimeError(f"Git ref resolution failed for prompt '{prompt_id}' at '{pin}': {str(e)}")
