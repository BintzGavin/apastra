import re

vision_content = ""
with open("docs/vision.md", "r") as f:
    vision_content = f.read()

# I am looking for "Canary suite scheduling" mentioned in docs/vision.md
match = re.search(r'canary', vision_content, re.IGNORECASE)
if match:
    start = max(0, match.start() - 100)
    end = min(len(vision_content), match.end() + 100)
    print(vision_content[start:end])
