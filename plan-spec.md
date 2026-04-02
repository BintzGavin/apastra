1. **Explore the current status and progress for GOVERNANCE**
   - Check `docs/status/GOVERNANCE.md` and `docs/progress/GOVERNANCE.md` natively in bash using `wc -l`.
2. **Read the exact line lengths to formulate verification**
   - Use `sed -n` sequentially based on `wc -l`.
3. **Execute Minimal Plan Exception Final 13**
   - Bump the version to `1.118.9` across BOTH files using `sed -i` native string matching, logging the completion for `MinimalPlanExceptionFinal13`.
4. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**
   - Run `pre-commit run --all-files` (or skip if not installed).
5. **Delete temporary files.**
   - Remove any exploration scripts.
6. **Submit changes**
   - Use Git commit with `-m "✨ GOVERNANCE: MinimalPlanExceptionFinal13"` and standard properties.
