import re

vision_content = ""
with open("docs/vision.md", "r") as f:
    vision_content = f.read()

# I am looking for "Canary suite scheduling" mentioned in .jules/prompts/planning-runtime.md
import re
match = re.search(r'(Canary suite scheduling.*)', vision_content, re.IGNORECASE)
if match:
    print(f"Vision Match: {match.group(1)}")
