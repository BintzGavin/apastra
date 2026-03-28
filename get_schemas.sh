for f in promptops/schemas/*.json; do
    echo "=== $f ==="
    jq -r '.properties | keys[]' "$f" 2>/dev/null || echo "No properties"
done
