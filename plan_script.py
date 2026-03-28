import re

vision_content = ""
with open("docs/vision.md", "r") as f:
    vision_content = f.read()

print("Vision features vs missing implementation:")
# The prompt mentions checking docs/status/RUNTIME.md for Blocked status.
status_content = ""
with open("docs/status/RUNTIME.md", "r") as f:
    status_content = f.read()
print(status_content[:150])

print("\nChecking block status:")
import re
match = re.search(r'Blocked:\s*(.*)', status_content)
if match:
    print(f"BLOCKED: {match.group(1)}")
else:
    print("NOT BLOCKED")
