#### 1. Context & Goal
- **Objective**: Design the resolution logic to fetch prompt packages from GitHub Release assets.
- **Trigger**: The docs/vision.md and README.md explicitly promise support for GitHub Release assets as a governed release format, but promptops/resolver/packaged.py currently lacks a specific protocol handler for it.
- **Impact**: Unlocks governed distribution capabilities via GitHub Releases, allowing consumers to resolve prompts distributed as release assets securely and with optional immutability.

#### 2. File Inventory
- **Create**: None
- **Modify**: promptops/resolver/packaged.py
- **Read-Only**: docs/vision.md and README.md

#### 3. Implementation Spec
- **Resolver Architecture**: Extend the PackagedResolver._fetch_remote_asset method to handle a github-release: protocol. It will route to a GitHub API fetcher that downloads the release asset JSON payload and writes it to the local cache fallback directory.
- **Manifest Format**: Support pins formatted as github-release:owner/repo@tag.
- **Pseudo-Code**: If ref starts with github-release:, parse owner, repo, and tag. Use HTTP GET to fetch the GitHub Release API. Find the asset ending with .json. Download the asset, extract the JSON payload, and write it to the cache.
- **Harness Contract Interface**: N/A
- **Dependencies**: Depends on existing provider-artifact.schema.json from CONTRACTS.

#### 4. Test Plan
- **Verification**: Execute resolve('my-prompt', 'github-release:apastra/prompts@v1.0.0') using a mocked HTTP response and confirm it successfully renders the extracted artifact.
- **Success Criteria**: The PackagedResolver returns a valid parsed dictionary for github-release: protocols without raising a RuntimeError.
- **Edge Cases**: Missing release, missing asset in the release, API rate limits, registry downtime.
