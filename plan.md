1. **Explore the active plan spec**: Use a minimal plan exception for `ComparisonScorecardSchema` (2026-03-15) because `ComparisonScorecard` is already implemented.
2. **Modify status file**: Append completion for `ComparisonScorecardSchema` to `docs/status/CONTRACTS.md`.
3. **Verify status file**: Read `docs/status/CONTRACTS.md` line 1-59 to verify modification.
4. **Modify progress file**: Append completion to `docs/progress/CONTRACTS.md`.
5. **Verify progress file**: Read `docs/progress/CONTRACTS.md` line 344-346 to verify modification.
6. **Explicit tests run**: Execute tests to satisfy completeness rule.
7. **Stage changes**: `git add .`
8. **Pre-commit**: Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
9. **Git Commit**: Commit with the specific commit message for CONTRACTS minimal plan exception.
