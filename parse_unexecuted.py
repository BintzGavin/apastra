import re, os
with open('docs/status/EVALUATION.md', 'r') as f:
    status_content = f.read()

completed = set()
for line in status_content.split('\n'):
    if '✅ Completed:' in line:
        # Extract task name after "Completed:" and before "-"
        # Also need to account for cases where there's no dash
        match = re.search(r'✅ Completed:\s*(.*?)(?:\s*-|$)', line)
        if match:
            task_name = match.group(1).strip()
            # Normalize
            task_name = re.sub(r'[^a-zA-Z0-9]', '', task_name).lower()
            completed.add(task_name)

plans = os.listdir('.sys/plans/')
evaluation_plans = [p for p in plans if '-EVALUATION-' in p and p.endswith('.md')]
evaluation_plans.sort()

for plan in evaluation_plans:
    task_name = plan.split('-EVALUATION-')[1].replace('.md', '')
    normalized_task = re.sub(r'[^a-zA-Z0-9]', '', task_name).lower()

    if normalized_task not in completed:
        print(plan)
        break
