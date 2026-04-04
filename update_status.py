with open("docs/status/GOVERNANCE.md", "r") as f:
    lines = f.readlines()
lines.insert(1, "[v1.122.0] ✅ Completed: CapabilityTaggingPolicy - Create capability tagging policy\n")
with open("docs/status/GOVERNANCE.md", "w") as f:
    f.writelines(lines)
