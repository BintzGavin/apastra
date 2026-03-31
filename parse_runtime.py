import re, os, sys

domain = sys.argv[1]

with open(f'docs/status/{domain}.md', 'r') as f:
    status_content = f.read()

completed = set()
for line in status_content.split('\n'):
    if '✅ Completed:' in line:
        parts = line.split('✅ Completed:')
        if len(parts) > 1:
            rest = parts[1].strip()
            task_part = rest.split(' - ')[0].strip()

            # Remove any trailing vX.Y.Z
            task_part = re.sub(r'-v\d+\.\d+\.\d+$', '', task_part)

            task_name = re.sub(r'[^a-zA-Z0-9]', '', task_part).lower()
            completed.add(task_name)

plans = os.listdir('.sys/plans/')
domain_plans = [p for p in plans if f'-{domain}-' in p and p.endswith('.md')]
domain_plans.sort()

for plan in domain_plans:
    task_name = plan.split(f'-{domain}-')[1].replace('.md', '')

    # Remove any trailing vX.Y.Z
    task_name = re.sub(r'-v\d+\.\d+\.\d+$', '', task_name)

    normalized_task = re.sub(r'[^a-zA-Z0-9]', '', task_name).lower()

    if normalized_task not in completed:
        print(plan)
        break
