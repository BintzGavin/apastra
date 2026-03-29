import os
import re
from datetime import datetime

def update_dashboards():
    today = datetime.now().strftime("%Y-%m-%d")

    # --- Update domain-status-overview.md ---
    with open('docs/dashboards/domain-status-overview.md', 'r') as f:
        status_overview = f.read()

    status_overview = re.sub(r'last_verified: ".*?"', f'last_verified: "{today}"', status_overview)

    status_dir = 'docs/status/'
    domains = [f.replace('.md', '') for f in os.listdir(status_dir) if f.endswith('.md')]

    for d in domains:
        with open(f"{status_dir}{d}.md", 'r') as f:
            content = f.read()

        version_match = re.search(r'\*\*Version\*\*: (\d+\.\d+\.\d+)', content)
        if version_match:
            v = version_match.group(1)

            # Find the section for this domain and update its version and recent commits
            lines = content.split('\n')
            recent_commits = []
            for line in lines:
                if line.startswith('[v'):
                    recent_commits.append(line)
                    if len(recent_commits) == 10:
                        break

            domain_section = f"## {d}\n\n**Version**: {v}\n" + "\n".join(recent_commits) + "\n"

            # Replace the old domain section
            status_overview = re.sub(rf'## {d}\n\n\*\*Version\*\*: .*?(?=\n\n## |\Z)', domain_section, status_overview, flags=re.DOTALL)

    with open('docs/dashboards/domain-status-overview.md', 'w') as f:
        f.write(status_overview)

    # --- Update implementation-progress.md ---
    with open('docs/dashboards/implementation-progress.md', 'r') as f:
        impl_progress = f.read()

    impl_progress = re.sub(r'last_verified: ".*?"', f'last_verified: "{today}"', impl_progress)

    progress_dir = 'docs/progress/'
    for d in domains:
        with open(f"{progress_dir}{d}.md", 'r') as f:
            content = f.read()

        # Insert the contents of the progress file into the corresponding section
        # Keep the format as a complete log
        match = re.search(rf'(## {d}\n\n).*?(?=\n## |\Z)', impl_progress, flags=re.DOTALL)
        if match:
            # remove the first ## domain heading and \n\n if present in the content
            content_to_insert = content
            if content_to_insert.startswith(f"## {d}"):
                 content_to_insert = content_to_insert.split('\n\n', 1)[1]

            # ensure no duplicated ## domain heading
            impl_progress = impl_progress[:match.start(1) + len(match.group(1))] + content_to_insert + "\n" + impl_progress[match.end():]

    with open('docs/dashboards/implementation-progress.md', 'w') as f:
        f.write(impl_progress)

update_dashboards()
