import re

def fix_dashboards():
    with open('docs/dashboards/implementation-progress.md', 'r') as f:
        impl_progress = f.read()

    impl_progress = re.sub(r'last_verified: ".*?"', 'last_verified: "2026-03-29"', impl_progress)

    v13 = """
### DOCS v0.13.0
- ✅ Completed: Daily Documentation Review
  - Generated API docs for missing schemas
  - Refreshed cross-domain dashboards
  - Updated `.sys/llmdocs/context-docs.md`
"""

    # append to end of DOCS section
    match = re.search(r'## RUNTIME', impl_progress)
    if match:
        impl_progress = impl_progress[:match.start()] + v13 + "\n" + impl_progress[match.start():]

    with open('docs/dashboards/implementation-progress.md', 'w') as f:
        f.write(impl_progress)

fix_dashboards()
