import re

status = """[v0.36.1] ✅ Completed: AnswerRelevanceAssertion - Minimal Plan Exception. Changes already present.
[v0.36.0] ✅ Completed: MCPIntegration - Implemented MCP Server adapter to expose evaluations as discoverable MCP tools
[v0.35.0] ✅ Completed: AuditCodebaseScanning - Implemented apastra-audit codebase scanning skill
[v0.34.0] ✅ Completed: RedTeamAdversarialGeneration - Implemented red-team adversarial generation skill
[v0.33.1] ✅ Completed: HarnessAdapterRunnerShim - Minimal Plan Exception. Changes already present.
[v0.33.0] ✅ Completed: RunRequestDigestValidation6 - Verified schema update"""

for line in status.split('\n'):
    if '✅ Completed:' in line:
        # Extract task name after "Completed:" and before "-"
        match = re.search(r'✅ Completed:\s*(.*?)(?:\s*-|$)', line)
        if match:
            task_name = match.group(1).strip()
            print(f"Matched: '{task_name}'")
            # Normalize
            normalized = re.sub(r'[^a-zA-Z0-9]', '', task_name).lower()
            print(f"Normalized: '{normalized}'")
