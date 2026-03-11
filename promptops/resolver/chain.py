from promptops.resolver.local import LocalResolver
from promptops.resolver.workspace import WorkspaceResolver
from promptops.resolver.git_ref import GitRefResolver

class ResolverChain:
    def resolve(self, prompt_id, manifest):
        rules = manifest.get_rules(prompt_id) if hasattr(manifest, 'get_rules') else {}
        if rules and 'override' in rules:
            return LocalResolver().resolve(prompt_id, rules['override'])

        workspace_result = WorkspaceResolver().resolve(prompt_id)
        if workspace_result is not None:
            return workspace_result

        if rules and 'pin' in rules:
            return GitRefResolver().resolve(prompt_id, rules['pin'])

        raise NotImplementedError("Resolution fallback not yet implemented")
