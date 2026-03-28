import subprocess

with open('lines.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    if not line or 'total' in line or 'docs/' in line or 'README' in line or '.jules/' in line:
        continue
    # skip the ones I already read
    if 'prompt-package' in line or 'provider-artifact' in line or 'namespace-claim' in line or 'approval-state' in line or 'provenance-attestation' in line or 'emergency-takedown' in line or 'harness-adapter' in line or 'policy-exception' in line or 'takedown-record' in line or 'delivery-target' in line or 'run-request' in line or 'consumption-manifest' in line or 'vulnerability-flag' in line or 'dataset-case' in line or 'scorecard.schema.json' in line or 'artifact-refs' in line or 'observability-adapter' in line or 'takedown-appeal' in line or 'moderation-decision' in line or 'baseline.schema.json' in line or 'automated-scan' in line:
        continue
    parts = line.split()
    if len(parts) == 2:
        count = int(parts[0])
        file_path = parts[1]
        start = 1
        while start <= count:
            end = min(start + 9, count)
            # Just read them
            print(f"Reading {file_path} {start}-{end}")
            subprocess.run(["sed", "-n", f"{start},{end}p", file_path], check=True)
            start += 10
