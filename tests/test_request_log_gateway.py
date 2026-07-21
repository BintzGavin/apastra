import http.client
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from promptops.request_log.artifacts import RequestArtifactStore
from promptops.request_log.config import RequestLogConfig
from promptops.request_log.gateway import GatewayServer, _connection_header_tokens, parse_gateway_route


class FakeProviderHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    requests = []
    response_status = 200
    default_response_body = b'data: {"type":"response.output_text.delta","delta":"hello"}\n\ndata: [DONE]\n\n'
    response_body = default_response_body

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.__class__.requests.append(
            {
                "path": self.path,
                "body": body,
                "authorization": self.headers.get("Authorization"),
                "api_key": self.headers.get("x-api-key"),
                "headers": {name.lower(): value for name, value in self.headers.items()},
                "header_names": [name.lower() for name, _value in self.headers.items()],
            }
        )
        self.send_response(self.__class__.response_status)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(self.__class__.response_body)))
        self.send_header("X-Request-Id", "provider-request-id")
        self.send_header("X-Upstream-Remove", "hop-by-hop-response")
        self.send_header("Proxy-Authenticate", "must-not-reach-client")
        self.send_header("Connection", "keep-alive, X-Upstream-Remove")
        self.end_headers()
        midpoint = len(self.__class__.response_body) // 2
        self.wfile.write(self.__class__.response_body[:midpoint])
        self.wfile.flush()
        time.sleep(0.01)
        self.wfile.write(self.__class__.response_body[midpoint:])
        self.wfile.flush()

    def log_message(self, _format, *_args):
        return


class FakeProvider:
    def __enter__(self):
        FakeProviderHandler.requests = []
        FakeProviderHandler.response_status = 200
        FakeProviderHandler.response_body = FakeProviderHandler.default_response_body
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeProviderHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address
        self.origin = f"http://{host}:{port}"
        return self

    def __exit__(self, *_args):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


def request(url, body, headers):
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.status, dict(response.headers.items()), response.read()


class GatewayRouteTests(unittest.TestCase):
    def test_connection_header_tokens_are_case_insensitive_trimmed_and_comma_separated(self):
        tokens = _connection_header_tokens(
            [
                ("cOnNeCtIoN", " keep-alive, X-Remove-Me "),
                ("X-Unrelated", "must-not-be-tokenized"),
            ]
        )

        self.assertEqual(tokens, {"keep-alive", "x-remove-me"})

    def test_route_keeps_forward_query_but_removes_it_from_log_path(self):
        route = parse_gateway_route("/openai/codex/v1/responses?api_key=forward-only")

        self.assertEqual(route.provider, "openai")
        self.assertEqual(route.adapter, "codex")
        self.assertEqual(route.upstream_target, "/v1/responses?api_key=forward-only")
        self.assertEqual(route.log_path, "/v1/responses")

    def test_unknown_provider_or_adapter_is_rejected(self):
        for path in ("/gemini/codex/v1/models", "/openai/cursor/v1/responses", "/openai/codex"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                parse_gateway_route(path)


class GatewayIntegrationTests(unittest.TestCase):
    def run_capture(self, provider, adapter, upstream_path, body):
        with tempfile.TemporaryDirectory() as temp_dir, FakeProvider() as upstream:
            root = Path(temp_dir)
            config = RequestLogConfig(
                enabled=True,
                adapters={adapter: [provider]},
                save_dir=root / "logs",
                activation_mode="session",
                retention_days=7,
                max_bytes=250 * 1024 * 1024,
                bind_port=0,
                upstreams={"openai": upstream.origin, "anthropic": upstream.origin},
            )
            store = RequestArtifactStore(config.save_dir)
            with GatewayServer(config, store) as gateway:
                url = f"{gateway.base_url}/{provider}/{adapter}{upstream_path}?trace=forwarded"
                parsed = urlsplit(url)
                connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=5)
                try:
                    connection.request(
                        "POST",
                        parsed.path + "?" + parsed.query,
                        body=body,
                        headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer openai-super-secret",
                        "x-api-key": "anthropic-super-secret",
                        "Cookie": "session=super-secret",
                        "Proxy-Authorization": "Basic super-secret",
                        "X-Remove-Me": "hop-by-hop-request",
                        "Host": "client-supplied.invalid",
                        "Connection": "keep-alive, X-Remove-Me",
                        },
                    )
                    response = connection.getresponse()
                    status = response.status
                    headers = dict(response.headers.items())
                    response_body = response.read()
                finally:
                    connection.close()

            self.assertEqual(status, 200)
            self.assertEqual(response_body, FakeProviderHandler.response_body)
            self.assertEqual(headers["X-Request-Id"], "provider-request-id")
            self.assertEqual(len(FakeProviderHandler.requests), 1)
            forwarded = FakeProviderHandler.requests[0]
            self.assertEqual(forwarded["path"], f"{upstream_path}?trace=forwarded")
            self.assertEqual(forwarded["body"], body)
            self.assertEqual(forwarded["authorization"], "Bearer openai-super-secret")
            self.assertEqual(forwarded["api_key"], "anthropic-super-secret")
            self.assertEqual(forwarded["headers"]["cookie"], "session=super-secret")
            self.assertNotEqual(forwarded["headers"]["host"], "client-supplied.invalid")
            self.assertNotIn("proxy-authorization", forwarded["headers"])
            self.assertNotIn("connection", forwarded["headers"])
            self.assertNotIn("x-remove-me", forwarded["headers"])
            self.assertEqual(forwarded["header_names"].count("content-length"), 1)
            self.assertEqual(forwarded["headers"]["content-length"], str(len(body)))
            self.assertNotIn("Proxy-Authenticate", headers)
            self.assertNotIn("Connection", headers)
            self.assertNotIn("X-Upstream-Remove", headers)

            artifacts = store.list_requests()
            self.assertEqual(len(artifacts), 1)
            shown = store.show_request(artifacts[0]["request_id"])
            self.assertEqual(shown["metadata"]["provider"], provider)
            self.assertEqual(shown["metadata"]["adapter"], adapter)
            self.assertEqual(shown["metadata"]["response_status"], 200)
            self.assertGreaterEqual(shown["metadata"]["duration_ms"], 1)
            self.assertIsNone(shown["metadata"]["error_class"])
            self.assertEqual(shown["raw_body"], body)
            persisted = b"\n".join(path.read_bytes() for path in root.rglob("*") if path.is_file())
            self.assertNotIn(b"openai-super-secret", persisted)
            self.assertNotIn(b"anthropic-super-secret", persisted)
            self.assertNotIn(b"session=super-secret", persisted)
            self.assertNotIn(FakeProviderHandler.response_body, persisted)

    def test_exact_openai_codex_request_and_streaming_response(self):
        body = b'{ "model":"gpt-test", "instructions":"system", "input":[{"role":"user","content":"hello"}], "tools":[{"type":"function","name":"shell"}], "reasoning":{"effort":"high"} }\n'
        self.run_capture("openai", "codex", "/v1/responses", body)

    def test_exact_anthropic_claude_code_request_and_streaming_response(self):
        body = b'{"model":"claude-test","system":[{"type":"text","text":"system"}],"messages":[{"role":"user","content":"hello"}],"tools":[{"name":"shell","input_schema":{"type":"object"}}],"max_tokens":1000}'
        self.run_capture("anthropic", "claude-code", "/v1/messages", body)

    def test_chunked_request_is_reassembled_and_logged_as_exact_bytes(self):
        with tempfile.TemporaryDirectory() as temp_dir, FakeProvider() as upstream:
            config = RequestLogConfig(
                enabled=True,
                adapters={"generic": ["openai"]},
                save_dir=Path(temp_dir) / "logs",
                bind_port=0,
                upstreams={"openai": upstream.origin, "anthropic": upstream.origin},
            )
            store = RequestArtifactStore(config.save_dir)
            chunks = [b'{"model":"gpt-test",', b'"input":"exact chunked body"}']
            with GatewayServer(config, store) as gateway:
                parsed = urlsplit(gateway.base_url)
                connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=5)
                try:
                    connection.request(
                        "POST",
                        "/openai/generic/v1/responses",
                        body=iter(chunks),
                        headers={"Content-Type": "application/json", "Authorization": "Bearer chunk-secret"},
                        encode_chunked=True,
                    )
                    response = connection.getresponse()
                    self.assertEqual(response.status, 200)
                    response.read()
                finally:
                    connection.close()

            expected = b"".join(chunks)
            self.assertEqual(FakeProviderHandler.requests[0]["body"], expected)
            row = store.list_requests()[0]
            self.assertEqual(store.show_request(row["request_id"])["raw_body"], expected)
            persisted = b"\n".join(path.read_bytes() for path in Path(temp_dir).rglob("*") if path.is_file())
            self.assertNotIn(b"chunk-secret", persisted)

    def test_empty_post_is_forwarded_and_logged_with_zero_length(self):
        with tempfile.TemporaryDirectory() as temp_dir, FakeProvider() as upstream:
            config = RequestLogConfig(
                enabled=True,
                adapters={"generic": ["openai"]},
                save_dir=Path(temp_dir) / "logs",
                bind_port=0,
                upstreams={"openai": upstream.origin, "anthropic": upstream.origin},
            )
            store = RequestArtifactStore(config.save_dir)
            with GatewayServer(config, store) as gateway:
                status, _headers, _response = request(
                    f"{gateway.base_url}/openai/generic/v1/responses",
                    b"",
                    {"Content-Type": "application/json"},
                )

            self.assertEqual(status, 200)
            self.assertEqual(FakeProviderHandler.requests[0]["body"], b"")
            self.assertEqual(FakeProviderHandler.requests[0]["headers"]["content-length"], "0")
            row = store.list_requests()[0]
            self.assertEqual(store.show_request(row["request_id"])["raw_body"], b"")

    def test_provider_error_status_and_body_reach_client_without_body_persistence(self):
        with tempfile.TemporaryDirectory() as temp_dir, FakeProvider() as upstream:
            FakeProviderHandler.response_status = 429
            FakeProviderHandler.response_body = b'{"error":{"message":"provider-only-response"}}'
            config = RequestLogConfig(
                enabled=True,
                adapters={"generic": ["openai"]},
                save_dir=Path(temp_dir) / "logs",
                bind_port=0,
                upstreams={"openai": upstream.origin, "anthropic": upstream.origin},
            )
            store = RequestArtifactStore(config.save_dir)
            with GatewayServer(config, store) as gateway:
                with self.assertRaises(urllib.error.HTTPError) as raised:
                    request(
                        f"{gateway.base_url}/openai/generic/v1/responses",
                        b'{"model":"gpt-test"}',
                        {"Content-Type": "application/json"},
                    )
                self.assertEqual(raised.exception.code, 429)
                self.assertEqual(raised.exception.read(), FakeProviderHandler.response_body)
                raised.exception.close()

            row = store.list_requests()[0]
            self.assertEqual(row["response_status"], 429)
            self.assertIsNone(row["error_class"])
            persisted = b"\n".join(path.read_bytes() for path in Path(temp_dir).rglob("*") if path.is_file())
            self.assertNotIn(b"provider-only-response", persisted)

    def test_unreachable_upstream_returns_502_and_records_coarse_failure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", 0))
                unavailable_origin = f"http://127.0.0.1:{probe.getsockname()[1]}"
            config = RequestLogConfig(
                enabled=True,
                adapters={"generic": ["openai"]},
                save_dir=Path(temp_dir) / "logs",
                bind_port=0,
                upstreams={"openai": unavailable_origin, "anthropic": unavailable_origin},
            )
            store = RequestArtifactStore(config.save_dir)
            with GatewayServer(config, store) as gateway:
                with self.assertRaises(urllib.error.HTTPError) as raised:
                    request(
                        f"{gateway.base_url}/openai/generic/v1/responses",
                        b'{"model":"gpt-test"}',
                        {"Content-Type": "application/json"},
                    )
                self.assertEqual(raised.exception.code, 502)
                self.assertIn(b"upstream_error", raised.exception.read())
                raised.exception.close()

            row = store.list_requests()[0]
            self.assertEqual(row["response_status"], 502)
            self.assertEqual(row["error_class"], "upstream_error")

    def test_unconfigured_route_never_reaches_upstream(self):
        with tempfile.TemporaryDirectory() as temp_dir, FakeProvider() as upstream:
            config = RequestLogConfig(
                enabled=True,
                adapters={"codex": ["openai"]},
                save_dir=Path(temp_dir) / "logs",
                upstreams={"openai": upstream.origin, "anthropic": upstream.origin},
                bind_port=0,
            )
            with GatewayServer(config, RequestArtifactStore(config.save_dir)) as gateway:
                with self.assertRaises(urllib.error.HTTPError) as raised:
                    request(f"{gateway.base_url}/anthropic/claude-code/v1/messages", b"{}", {"Content-Type": "application/json"})

            self.assertEqual(raised.exception.code, 404)
            raised.exception.close()
            self.assertEqual(FakeProviderHandler.requests, [])

    def test_logging_failure_is_fail_closed(self):
        class FailingStore:
            def prune(self, **_kwargs):
                return []

            def begin_request(self, *_args, **_kwargs):
                raise OSError("disk full")

        with tempfile.TemporaryDirectory() as temp_dir, FakeProvider() as upstream:
            config = RequestLogConfig(
                enabled=True,
                adapters={"codex": ["openai"]},
                save_dir=Path(temp_dir) / "logs",
                upstreams={"openai": upstream.origin, "anthropic": upstream.origin},
                bind_port=0,
            )
            with GatewayServer(config, FailingStore()) as gateway:
                with self.assertRaises(urllib.error.HTTPError) as raised:
                    request(f"{gateway.base_url}/openai/codex/v1/responses", b"{}", {"Content-Type": "application/json"})

            self.assertEqual(raised.exception.code, 507)
            raised.exception.close()
            self.assertEqual(FakeProviderHandler.requests, [])


if __name__ == "__main__":
    unittest.main()
