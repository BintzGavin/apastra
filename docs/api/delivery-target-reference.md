# Delivery Target Specification Reference

Schema for delivery target config across supported downstream sync mechanisms.

## Supported targets

- `github_pr`: requires `type`, `repo`, and `channel`.
- `npm`: requires `type`, `registry`, `channel`, and `credentials_ref`.
- `pypi`: requires `type`, `registry`, `channel`, and `credentials_ref`.
- `oci`: requires `type`, `registry`, `repository`, `channel`, and `credentials_ref`.
- `internal_api`: requires `type`, `endpoint`, and `payload_format`.
- `mcp_server`: requires `type` and `endpoint`.
- Legacy MCP target files may use `target_type: mcp_server` with `endpoint` and `channels`.
