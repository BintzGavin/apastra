import os
import re

status_content = open('docs/status/GOVERNANCE.md', 'r', encoding='utf-8').read()

completed_tasks = set()
for match in re.finditer(r'✅ Completed:\s*(.*?)\s*-', status_content):
    completed_tasks.add(match.group(1).strip())

blocked_tasks = set()
for match in re.finditer(r'Blocked:\s*(.*?)\s*-', status_content):
    blocked_tasks.add(match.group(1).strip())

print("Completed tasks:")
print(completed_tasks)

print("\nBlocked tasks:")
print(blocked_tasks)

for plan_file in os.listdir('.sys/plans/'):
    if 'GOVERNANCE' in plan_file:
        # Extract plan name
        # Format: YYYY-MM-DD-GOVERNANCE-[TaskName].md
        match = re.search(r'\d{4}-\d{2}-\d{2}-GOVERNANCE-(.*)\.md', plan_file)
        if match:
            task_name = match.group(1)
            # Remove -vX.Y.Z
            task_name = re.sub(r'-v\d+\.\d+\.\d+$', '', task_name)

            if task_name not in completed_tasks and task_name not in blocked_tasks:
                print(f"UNEXECUTED PLAN FOUND: {plan_file} (Task: {task_name})")
