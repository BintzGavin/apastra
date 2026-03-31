import re

status_content = """[v1.22.0] ✅ Completed: NPM-PyPI-Resolver - Implemented npm and PyPI wrapper resolution in the PackagedResolver."""
match = re.search(r'✅ Completed:\s*(.*?)(?:\s*-|$)', status_content)
if match:
    task_name = match.group(1).strip()
    task_name = re.sub(r'[^a-zA-Z0-9]', '', task_name).lower()
    print("MATCH:", task_name)

