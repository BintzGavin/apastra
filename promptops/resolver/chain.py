from promptops.resolver.local import LocalResolver

class ResolverChain:
    def resolve(self, prompt_id, manifest):
        rules = manifest.get_rules(prompt_id)
        if rules and 'override' in rules:
            return LocalResolver().resolve(prompt_id, rules['override'])
        # ... fallback to workspace ...
        return None
