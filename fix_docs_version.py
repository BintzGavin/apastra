import re

def fix_docs_status():
    with open('docs/status/DOCS.md', 'r') as f:
        status = f.read()

    # Remove the duplicate v0.14.0 entry
    status = re.sub(r'\[v0.14.0\] ✅ Completed: Daily Documentation Review - Comprehensive daily review. Generated missing API docs, refreshed dashboards, and updated context-docs.md.\n\n', '', status)
    status = re.sub(r'\*\*Version\*\*: 0.14.0', '**Version**: 0.13.0', status)

    with open('docs/status/DOCS.md', 'w') as f:
        f.write(status)

def fix_docs_progress():
    with open('docs/progress/DOCS.md', 'r') as f:
        progress = f.read()

    # Remove the duplicate v0.14.0 entry
    progress = re.sub(r'### DOCS v0.14.0\n- ✅ Completed: Daily Documentation Review\n  - Generated API docs for missing schemas\n  - Refreshed cross-domain dashboards\n  - Updated \`\.sys/llmdocs/context-docs\.md\`\n', '', progress)

    with open('docs/progress/DOCS.md', 'w') as f:
        f.write(progress)

fix_docs_status()
fix_docs_progress()
