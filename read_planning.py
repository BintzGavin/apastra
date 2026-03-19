import json

with open('.jules/prompts/planning-contracts.md', 'rb') as f:
    content = f.read().decode('utf-8')
    print(json.dumps(content))
