"""Authentication and actual MCP transport with ephemeral, in-memory test signing.

Only the generated PUBLIC key is written. No credentials are saved or printed.
"""
import asyncio
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest

import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

from tests.test_evaluation_contract import ROOT, make_workspace


class TransportTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace, self.adapter = make_workspace(temporary.name)
        self.signer = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public = self.workspace / "issuer-public.pem"
        self.public.write_bytes(self.signer.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
        self.issuer = "https://issuer.example.test"
        self.resource = "https://eval.example.test/mcp"
        self.args = [sys.executable, str(ROOT / "bin/apastra"), "mcp", "--workspace", str(self.workspace),
                     "--workspace-id", "isolated", "--adapter", "promptops/harnesses/local.json"]

    def credential(self, **overrides):
        claims = {"iss": self.issuer, "aud": self.resource, "sub": "test-owner", "scope": "apastra:evaluate",
                  "exp": int(time.time()) + 120, "iat": int(time.time())}
        claims.update(overrides)
        return jwt.encode(claims, self.signer, algorithm="RS256")

    async def test_verifier_rejects_wrong_owner_audience_issuer_expiry_and_signature(self):
        from promptops.runtime.mcp_auth import OwnerTokenVerifier
        verifier = OwnerTokenVerifier(self.public, self.issuer, self.resource, "test-owner")
        self.assertIsNotNone(await verifier.verify_token(self.credential()))
        for changes in ({"sub": "another-owner"}, {"aud": "https://other.test/mcp"}, {"iss": "https://other.test"},
                        {"exp": 1}, {"scope": "read"}):
            result = await verifier.verify_token(self.credential(**changes))
            self.assertTrue(result is None, "Invalid authorization was accepted")
        self.signer = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.assertTrue(await verifier.verify_token(self.credential()) is None)

    async def exercise(self, streams):
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            names = {tool.name for tool in (await session.list_tools()).tools}
            self.assertTrue({"workspace_info", "list_suites", "start_evaluation", "get_run", "compare_runs", "get_case"} <= names)
            async def call(name, args):
                response = await session.call_tool(name, args)
                self.assertFalse(response.isError, name)
                self.assertIsInstance(response.structuredContent, dict)
                return response.structuredContent
            self.assertEqual((await call("workspace_info", {}))["workspace_id"], "isolated")
            self.assertEqual((await call("list_suites", {}))["suites"][0]["id"], "demo")
            self.assertEqual((await call("start_evaluation", {"suite_id": "../private"}))["reason"], "unsafe_ref")
            self.assertEqual((await call("run_evaluation", {"suite_id": "demo", "adapter_config": "../private"}))["reason"], "server_owned_paths")
            results = []
            for _ in range(2):
                started = await call("start_evaluation", {"suite_id": "demo"})
                for _ in range(200):
                    result = await call("get_run", {"run_id": started["run_id"]})
                    if result["status"] not in ("queued", "running"):
                        break
                    await asyncio.sleep(.02)
                self.assertEqual(result["outcome"], "success", result)
                results.append(started["run_id"])
            report = await call("compare_runs", {"candidate_run_id": results[1], "baseline_run_id": results[0]})
            self.assertEqual(report["outcome"], "success")
            case = await call("get_case", {"run_id": results[1], "case_id": "one", "model_id": "local:uppercase"})
            self.assertEqual(case["case"]["output"], "HELLO")

    async def test_supported_stdio_launcher_roundtrip(self):
        with open(Path(self.workspace) / "stdio-diagnostics.txt", "w") as errors:
            async with stdio_client(StdioServerParameters(command=self.args[0], args=self.args[1:]), errlog=errors) as streams:
                await self.exercise(streams)

    async def test_authenticated_http_launcher_roundtrip_and_transport_protections(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        url = f"http://127.0.0.1:{port}/mcp"
        args = self.args + ["--transport", "streamable-http", "--port", str(port), "--auth-issuer", self.issuer,
                            "--resource-url", self.resource, "--auth-subject", "test-owner", "--auth-public-key", str(self.public)]
        process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        try:
            async with httpx.AsyncClient() as client:
                for _ in range(200):
                    try:
                        response = await client.post(url, json={})
                        break
                    except httpx.ConnectError:
                        if process.poll() is not None:
                            self.fail("Supported HTTP launcher exited before accepting requests")
                        await asyncio.sleep(.025)
                self.assertEqual(response.status_code, 401)
                headers = {"Authorization": "Bearer " + self.credential(), "Accept": "application/json, text/event-stream"}
                for override, expected in (({"Host": "attacker.test"}, 421), ({"Origin": "https://attacker.test"}, 403)):
                    response = await client.post(url, json={}, headers={**headers, **override})
                    self.assertEqual(response.status_code, expected)
                response = await client.get(f"http://127.0.0.1:{port}/.well-known/oauth-protected-resource/mcp")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["resource"], self.resource)
                async with httpx.AsyncClient(headers=headers) as authenticated:
                    async with streamable_http_client(url, http_client=authenticated) as streams:
                        await self.exercise(streams)
        finally:
            process.terminate()
            await asyncio.to_thread(process.wait, 10)

    def test_http_requires_explicit_auth_configuration_and_workspace(self):
        for args in (["mcp"], [*self.args[2:], "--transport", "streamable-http"]):
            result = subprocess.run([sys.executable, str(ROOT / "bin/apastra"), *args], capture_output=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
