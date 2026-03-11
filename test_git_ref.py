from promptops.resolver.chain import ResolverChain

class Manifest:
    def get_rules(self, p):
        return {'pin': 'HEAD'}

try:
    ResolverChain().resolve('mock_id', Manifest())
except Exception as e:
    print(e)
