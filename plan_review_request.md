1. **Create `promptops/runtime/config.py`**
   - Create a module with a `load_project_config()` function that traverses upwards from the current directory to find and load `promptops.config.yaml` or `promptops.config.yml`. It will parse the file using `yaml.safe_load()`.

2. **Update `promptops/runtime/resolve.py`**
   - Import `load_project_config` from `promptops.runtime.config`.
   - Call `load_project_config()` inside `resolve()`.
   - Update the model resolution logic to fallback to the project config if neither the prompt rule nor the manifest default provides a model.

3. **Verify the change**
   - `echo -e "defaults:\n  model: gpt-4o" > promptops.config.yaml`
   - `mkdir -p promptops/prompts/test-config`
   - `echo -e "id: test-config\ntemplate: hello" > promptops/prompts/test-config/prompt.yaml`
   - `python3 -c "from promptops.runtime.resolve import resolve; _, metadata = resolve('test-config'); assert metadata.get('model_ids') == ['gpt-4o'], 'Model not loaded from config'"`
   - Clean up the test files.

4. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done**
   - `./minimal.sh` or actual precommit execution if available.

5. **Submit the change**
   - Submit with title "✨ RUNTIME: ProjectConfigLoading".
