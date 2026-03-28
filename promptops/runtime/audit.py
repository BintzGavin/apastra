import os
import re

def scan_codebase(directory="."):
    report = {
        "detected_prompts": 0,
        "debt_score": 0,
        "findings": []
    }

    ignore_dirs = {'.git', 'node_modules', 'venv', 'promptops'}

    heuristics = [
        re.compile(r'(?i)(you are a|act as a|translate this|summarize the following)'),
        re.compile(r'"""[\s\S]*?(you are|prompt|instruct)[\s\S]*?"""'),
        re.compile(r"'''[\s\S]*?(you are|prompt|instruct)[\s\S]*?'''")
    ]

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]

        for file in files:
            if not file.endswith(('.py', '.js', '.ts', '.java', '.go', '.rb', '.txt', '.md', '.json', '.yaml', '.yml')):
                continue

            filepath = os.path.join(root, file)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    for heuristic in heuristics:
                        for match in heuristic.finditer(content):
                            line_no = content.count('\n', 0, match.start()) + 1
                            snippet = match.group(0)[:100]
                            if len(match.group(0)) > 100:
                                snippet += "..."

                            report["findings"].append({
                                "file": filepath,
                                "line": line_no,
                                "snippet": snippet.strip(),
                                "versioned": False
                            })
                            report["detected_prompts"] += 1
                            report["debt_score"] += 10
            except Exception:
                pass

    return report
