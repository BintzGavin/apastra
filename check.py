import sys, re

def check_unexecuted_plans():
    status_content = open('docs/status/EVALUATION.md', encoding='utf-8').read()

    import os
    plan_files = [f for f in os.listdir('.sys/plans') if f.startswith('2026-') and '-EVALUATION-' in f]

    unexecuted_plans = []

    for plan_file in plan_files:
        task_name = plan_file.split('-EVALUATION-')[1].replace('.md', '')
        # normalize task name
        norm_task_name = re.sub(r'^v\d+\.\d+\.\d+-', '', task_name)
        norm_task_name = re.sub(r'-v\d+\.\d+\.\d+$', '', norm_task_name)
        norm_task_name = re.sub(r'[^a-zA-Z0-9]', '', norm_task_name).lower()

        found = False
        for line in status_content.split('\n'):
            if line.startswith('[v') and 'Completed: ' in line:
                completed_task_name = line.split('Completed: ')[1].split(' - ')[0]
                norm_completed_task_name = re.sub(r'^v\d+\.\d+\.\d+-', '', completed_task_name)
                norm_completed_task_name = re.sub(r'-v\d+\.\d+\.\d+$', '', norm_completed_task_name)
                norm_completed_task_name = re.sub(r'[^a-zA-Z0-9]', '', norm_completed_task_name).lower()

                if norm_task_name == norm_completed_task_name:
                    found = True
                    break

        if not found:
            unexecuted_plans.append(plan_file)

    print(unexecuted_plans)

check_unexecuted_plans()
