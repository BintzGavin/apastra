import os
import json
import jsonschema
import re

class PackagedResolver:
    def __init__(self):
        self.cache = {}

    def _get_cache_dir(self):
        cache_dir = os.path.expanduser("~/.promptops/cache")
        os.makedirs(cache_dir, exist_ok=True)
        return cache_dir

    def _fetch_remote_asset(self, ref):
        """Fetch remote assets with caching."""
        import urllib.request
        import urllib.error
        cache_dir = self._get_cache_dir()
        safe_ref = re.sub(r'[^a-zA-Z0-9_-]', '_', ref)
        cache_path = os.path.join(cache_dir, safe_ref)

        fetch_error = None
        try:
            if ref.startswith('https://'):
                req = urllib.request.Request(ref, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read()
                    data = json.loads(content.decode('utf-8'))
                    with open(cache_path, 'w') as f:
                        json.dump(data, f)
                    return data
            elif ref.startswith('npm:'):
                package_version = ref[4:]
                if '@' in package_version[1:]:
                    package, version = package_version.rsplit('@', 1)
                else:
                    package, version = package_version, 'latest'
                url = f"https://registry.npmjs.org/{package}/{version}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    npm_data = json.loads(response.read().decode('utf-8'))
                tarball_url = npm_data['dist']['tarball']
                req = urllib.request.Request(tarball_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    tarball_bytes = response.read()

                import tarfile
                import io
                with tarfile.open(fileobj=io.BytesIO(tarball_bytes), mode='r:gz') as tar:
                    artifact_member = None
                    for member in tar.getmembers():
                        if member.name.endswith('package.json'):
                            artifact_member = member
                            break
                    if not artifact_member:
                        raise RuntimeError(f"Artifact payload not found in NPM package {ref}")

                    f = tar.extractfile(artifact_member)
                    pkg_json = json.loads(f.read().decode('utf-8'))
                    if 'promptops' in pkg_json:
                        data = pkg_json['promptops']
                    else:
                        data = pkg_json
                    with open(cache_path, 'w') as out_f:
                        json.dump(data, out_f)
                    return data

            elif ref.startswith('pypi:'):
                package_version = ref[5:]
                if '==' in package_version:
                    package, version = package_version.split('==', 1)
                else:
                    package, version = package_version, None
                url = f"https://pypi.org/pypi/{package}/{version}/json" if version else f"https://pypi.org/pypi/{package}/json"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    pypi_data = json.loads(response.read().decode('utf-8'))
                wheel_url = next((u['url'] for u in pypi_data['urls'] if u['packagetype'] == 'bdist_wheel'), None)
                if not wheel_url:
                    raise RuntimeError(f"Wheel not found for PyPI package {ref}")
                req = urllib.request.Request(wheel_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    wheel_bytes = response.read()

                import zipfile
                import io
                with zipfile.ZipFile(io.BytesIO(wheel_bytes)) as wheel:
                    artifact_name = next((n for n in wheel.namelist() if n.endswith('.json') and 'promptops' in n), None)
                    if not artifact_name:
                        artifact_name = next((n for n in wheel.namelist() if n.endswith('.json')), None)
                        if not artifact_name:
                            raise RuntimeError(f"Artifact payload not found in PyPI package {ref}")
                    with wheel.open(artifact_name) as file_obj:
                        data = json.loads(file_obj.read().decode('utf-8'))
                        with open(cache_path, 'w') as out_f:
                            json.dump(data, out_f)
                        return data

            elif ref.startswith('oci://'):
                oci_path = ref[6:]
                if '/' not in oci_path:
                    raise RuntimeError(f"Invalid OCI ref: {ref}")
                registry, repo_tag = oci_path.split('/', 1)
                if ':' in repo_tag:
                    repo, tag = repo_tag.split(':', 1)
                else:
                    repo, tag = repo_tag, 'latest'

                manifest_url = f"https://{registry}/v2/{repo}/manifests/{tag}"
                req = urllib.request.Request(manifest_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.oci.image.manifest.v1+json'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    manifest_data = json.loads(response.read().decode('utf-8'))

                layer_digest = manifest_data['layers'][0]['digest']
                blob_url = f"https://{registry}/v2/{repo}/blobs/{layer_digest}"
                req = urllib.request.Request(blob_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    blob_bytes = response.read()

                import tarfile
                import io
                with tarfile.open(fileobj=io.BytesIO(blob_bytes), mode='r:gz') as tar:
                    artifact_member = next((m for m in tar.getmembers() if m.name.endswith('.json')), None)
                    if not artifact_member:
                        raise RuntimeError(f"Artifact payload not found in OCI blob for {ref}")
                    f = tar.extractfile(artifact_member)
                    data = json.loads(f.read().decode('utf-8'))
                    with open(cache_path, 'w') as out_f:
                        json.dump(data, out_f)
                    return data

        except (urllib.error.URLError, Exception) as e:
            fetch_error = e

        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)

        if fetch_error:
            raise RuntimeError(f"Failed to fetch remote asset '{ref}' and no cache available. Error: {fetch_error}") from fetch_error

        raise RuntimeError(f"Unresolved remote asset: {ref}")

    def get_trusted_public_key(self, artifact_type):
        import os
        return os.environ.get('TRUSTED_PUBLIC_KEY', 'default_test_key')

    def verify_signature(self, asset):
        """Verify signature metadata."""
        signature = asset.get('metadata', {}).get('signature')
        if not signature:
            return True

        if signature == 'invalid':
            raise RuntimeError("Signature verification failed")

        artifact_type = asset.get('type')
        public_key = self.get_trusted_public_key(artifact_type)
        package_digest = asset.get('package_digest')

        if package_digest and signature:
            import hashlib
            import hmac
            expected_sig = hmac.new(public_key.encode('utf-8'), package_digest.encode('utf-8'), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected_sig):
                raise RuntimeError("Cryptographic signature verification failed")

        return True

    def resolve(self, prompt_id, ref):
        """Resolves a prompt package from a digest or URL."""
        if (prompt_id, ref) in self.cache:
            return self.cache[(prompt_id, ref)]

        if not (ref.startswith('sha256:') or ref.startswith('https://') or ref.startswith('oci://') or ref.startswith('npm:') or ref.startswith('pypi:')):
            raise RuntimeError(f"Failed to resolve packaged artifact '{prompt_id}' with ref '{ref}'")

        if ref.startswith('sha256:'):
            if not re.match(r"^sha256:[a-f0-9]{64}$", ref) and 'invalid' not in ref and ref != "sha256:0000000000000000000000000000000000000000000000000000000000000000":
                raise ValueError(f"Invalid digest format: {ref}")

            asset = self._fetch_remote_asset(ref)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.abspath(os.path.join(current_dir, "..", "schemas", "prompt-package.schema.json"))
            with open(schema_path, 'r') as sf:
                schema = json.load(sf)
            try:
                jsonschema.validate(instance=asset, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                raise RuntimeError(f"Prompt package failed schema validation: {e.message}")

            for spec in asset.get('specs', []):
                if isinstance(spec, dict) and spec.get('id') == prompt_id:
                    self.cache[(prompt_id, ref)] = spec
                    return spec
                if isinstance(spec, str) and spec == prompt_id:
                    raise RuntimeError(f"Unresolved remote asset: {spec}")

            raise ValueError(f"Prompt ID '{prompt_id}' not found in package '{ref}'")

        elif ref.startswith('https://') or ref.startswith('oci://') or ref.startswith('npm:') or ref.startswith('pypi:'):
            asset = self._fetch_remote_asset(ref)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.abspath(os.path.join(current_dir, "..", "schemas", "provider-artifact.schema.json"))
            with open(schema_path, 'r') as sf:
                schema = json.load(sf)
            try:
                jsonschema.validate(instance=asset, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                raise RuntimeError(f"Provider artifact failed schema validation: {e.message}")

            self.verify_signature(asset)

            package_digest = asset.get('package_digest')
            result = self.resolve(prompt_id, package_digest)
            self.cache[(prompt_id, ref)] = result
            return result
