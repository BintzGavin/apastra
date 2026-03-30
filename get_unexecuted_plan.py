import os
import glob
import re

status_file = "docs/status/RUNTIME.md"
with open(status_file, "r") as f:
    status_content = f.read()

completed_tasks = []
for line in status_content.splitlines():
    match = re.search(r"\[v[0-9.]+\] ✅ Completed: (.*?) -", line)
    if match:
        completed_tasks.append(match.group(1).strip())

plan_files = glob.glob(".sys/plans/*-RUNTIME-*.md")
plan_files.sort()

unexecuted = []
for plan_file in plan_files:
    task_name = re.search(r"-RUNTIME-(.*?)\.md", plan_file).group(1)
    # Ignore if it contains version numbers or is clearly a duplicate already done
    if any(t in task_name for t in completed_tasks) or any(t.replace("-", "") in task_name.replace("-", "") for t in completed_tasks):
        continue
    # Special cases handling
    if "Directory-Resolver" in task_name and "DirectoryResolver" in completed_tasks:
        continue
    if "-v" in task_name:
        base_task = task_name.split("-v")[0]
        if any(base_task in t for t in completed_tasks):
            continue
    unexecuted.append((plan_file, task_name))

for f, t in unexecuted:
    print(f"Unexecuted: {f} (Task: {t})")
