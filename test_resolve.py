import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

import promptops.runtime.resolve as resolve_mod

class MockResolverChain:
    def resolve(self, prompt_id, manifest):
        return {
            "id": prompt_id,
            "variables": {"name": {"type": "string"}},
            "template": "Hello {{name}}!"
        }

# monkey patch ResolverChain
import promptops.runtime.resolve
promptops.runtime.resolve.__globals__['ResolverChain'] = MockResolverChain

# test missing variables
rendered, metadata = promptops.runtime.resolve('test-prompt', None)
assert rendered == "Hello {{name}}!", "Failed missing variables"

# test variables
rendered, metadata = promptops.runtime.resolve('test-prompt', None, variables={"name": "Alice"})
assert rendered == "Hello Alice!", f"Failed variables: expected 'Hello Alice!', got '{rendered}'"

print("Tests passed")