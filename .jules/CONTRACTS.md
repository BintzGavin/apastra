## 0.6.0 - Content Digest Convention
**Learning:** `jq` does not parse yaml files out of the box, `yq` is needed to correctly convert yaml to json for canonicalization in `compute-digest.sh`.
**Action:** Use `yq .` prior to piping to `jq` for any `.yaml` or `.yml` files.