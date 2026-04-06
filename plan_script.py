import re
import os
import datetime

# Read vision
vision_content = open('docs/vision.md', 'r', encoding='utf-8').read()

# Check what we've already done
status_content = open('docs/status/GOVERNANCE.md', 'r', encoding='utf-8').read()
completed = set()
for match in re.finditer(r'✅ Completed:\s*(.*?)\s*-', status_content):
    completed.add(match.group(1).strip())

blocked = set()
for match in re.finditer(r'Blocked:\s*(.*?)\s*-', status_content):
    blocked.add(match.group(1).strip())

# Vision gaps to check:
# 1. Observability adapter delivery policies - Yes
# 2. Drift alert policies - Yes
# 3. Community prompt pack acceptance policies - Yes
# 4. Cost budget governance policies - Yes
# 5. Multi-model promotion policies - Yes

# Search for other things in vision:
print("Completed:", completed)
print("Blocked:", blocked)
