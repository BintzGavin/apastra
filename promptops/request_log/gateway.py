from __future__ import annotations

import http.client
import json
import os
import socket
import threading
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import SplitResult, urlsplit, urlunsplit

from .artifacts import RequestArtifactStore
from .config import RequestLogConfig, SUPPORTED_ADAPTERS, SUPPORTED_PROVIDERS


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-connection",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}


def _connection_header_tokens(headers) -> set[str]:
    tokens: set[str] = set()
    for name, value in headers:
        if name.lower() == "connection":
            tokens.update(token.strip().lower() for token in value.split(",") if token.strip())
    return tokens


@dataclass(frozen=True)
class GatewayRoute:
    provider: str
    adapter: str
    upstream_target: str
    log_path: str


def parse_gateway_route(target: str) -> GatewayRoute:
    parsed = urlsplit(target)
    segments = parsed.path.split("/")
    if len(segments) < 5 or segments[0] != "":
        raise ValueError("Request path must include provider, adapter, and API path")
    provider, adapter = segments[1], segments[2]
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unknown provider route: {provider}")
    if adapter not in SUPPORTED_ADAPTERS or provider not in SUPPORTED_ADAPTERS[adapter]:
        raise ValueError(f"Unsupported adapter route: {adapter}/{provider}")
    upstream_path = "/" + "/".join(segments[3:])
    upstream_target = urlunsplit(SplitResult("", "", upstream_path, parsed.query, ""))
    return GatewayRoute(provider, adapter, upstream_target, upstream_path)


class GatewayServer:
    def __init__(self, config: RequestLogConfig, store: RequestArtifactStore):
        self.config = config.normalized()
        self.config.validate()
        self.store = store
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        if self._server is None:
            raise RuntimeError("Gateway is not running")
        host, port = self._server.server_address[:2]
        display_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
        return f"http://{display_host}:{port}"

    def start(self) -> "GatewayServer":
        if self._server is not None:
            return self
        self.store.prune(
            retention_days=self.config.retention_days,
            max_bytes=self.config.max_bytes,
        )
        handler = _handler(self.config, self.store)
        self._server = ThreadingHTTPServer((self.config.bind_host, self.config.bind_port), handler)
        self._server.daemon_threads = True
        self._thread = threading.Thread(target=self._server.serve_forever, name="apastra-request-log", daemon=True)
        self._thread.start()
        return self

    def serve_forever(self) -> None:
        if self._server is None:
            self.store.prune(
                retention_days=self.config.retention_days,
                max_bytes=self.config.max_bytes,
            )
            self._server = ThreadingHTTPServer(
                (self.config.bind_host, self.config.bind_port),
                _handler(self.config, self.store),
            )
            self._server.daemon_threads = True
        self._server.serve_forever()

    def shutdown(self) -> None:
        if self._server is None:
            return
        self._server.shutdown()
        self._server.server_close()
        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join(timeout=5)
        self._server = None
        self._thread = None

    def __enter__(self) -> "GatewayServer":
        return self.start()

    def __exit__(self, *_args: Any) -> None:
        self.shutdown()


def _handler(config: RequestLogConfig, store: RequestArtifactStore):
    class RequestLogHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self):
            if self.path == "/health":
                payload = json.dumps(
                    {
                        "status": "ok",
                        "pid": os.getpid(),
                        "save_dir": str(config.save_dir),
                    },
                    separators=(",", ":"),
                ).encode("utf-8") + b"\n"
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            self._forward()

        def do_POST(self):
            self._forward()

        def do_PUT(self):
            self._forward()

        def do_PATCH(self):
            self._forward()

        def do_DELETE(self):
            self._forward()

        def do_OPTIONS(self):
            self._forward()

        def _forward(self) -> None:
            try:
                route = parse_gateway_route(self.path)
            except ValueError as exc:
                self._local_error(404, "route_not_found", str(exc))
                return
            if not config.enabled or route.adapter not in config.adapters or route.provider not in config.adapters[route.adapter]:
                self._local_error(404, "route_not_enabled", "The provider/adapter route is not enabled")
                return

            try:
                body = self._read_request_body()
            except (OSError, ValueError) as exc:
                self._local_error(400, "invalid_request_body", str(exc))
                return

            started = time.monotonic()
            try:
                artifact = store.begin_request(
                    route.provider,
                    route.adapter,
                    self.command,
                    route.log_path,
                    self.headers.get("Content-Type", ""),
                    body,
                )
            except OSError:
                self._local_error(507, "log_write_failed", "The request could not be durably logged and was not forwarded")
                return
            except Exception:
                self._local_error(500, "log_write_failed", "The request could not be logged and was not forwarded")
                return

            upstream = urlsplit(config.upstreams[route.provider])
            connection: http.client.HTTPConnection | http.client.HTTPSConnection | None = None
            try:
                if upstream.scheme == "https":
                    connection = http.client.HTTPSConnection(upstream.hostname, upstream.port or 443, timeout=300)
                else:
                    connection = http.client.HTTPConnection(upstream.hostname, upstream.port or 80, timeout=300)
                request_headers = list(self.headers.items())
                request_hop_headers = HOP_BY_HOP_HEADERS | _connection_header_tokens(request_headers)
                headers = {
                    name: value
                    for name, value in request_headers
                    if name.lower() not in request_hop_headers | {"host", "content-length"}
                }
                if body or self.command in {"POST", "PUT", "PATCH"}:
                    headers["Content-Length"] = str(len(body))
                connection.request(self.command, route.upstream_target, body=body or None, headers=headers)
                response = connection.getresponse()
                self.send_response(response.status, response.reason)
                response_has_length = False
                response_headers = response.getheaders()
                response_hop_headers = HOP_BY_HOP_HEADERS | _connection_header_tokens(response_headers)
                for name, value in response_headers:
                    lowered = name.lower()
                    if lowered in response_hop_headers:
                        continue
                    if lowered == "content-length":
                        response_has_length = True
                    self.send_header(name, value)
                if not response_has_length:
                    self.send_header("Connection", "close")
                    self.close_connection = True
                self.end_headers()
                while True:
                    chunk = response.read(65536)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
                duration = max(0, round((time.monotonic() - started) * 1000))
                store.complete_request(artifact.request_id, response.status, duration)
                store.prune(retention_days=config.retention_days, max_bytes=config.max_bytes)
            except (BrokenPipeError, ConnectionResetError):
                duration = max(0, round((time.monotonic() - started) * 1000))
                store.fail_request(artifact.request_id, "client_disconnect", duration)
            except (OSError, http.client.HTTPException, socket.timeout):
                duration = max(0, round((time.monotonic() - started) * 1000))
                store.fail_request(artifact.request_id, "upstream_error", duration, 502)
                if not self.wfile.closed:
                    try:
                        self._local_error(502, "upstream_error", "The provider request failed")
                    except (BrokenPipeError, ConnectionResetError):
                        pass
            finally:
                if connection is not None:
                    connection.close()

        def _read_request_body(self) -> bytes:
            transfer_encoding = self.headers.get("Transfer-Encoding", "").lower()
            if transfer_encoding:
                if transfer_encoding != "chunked":
                    raise ValueError("Unsupported request transfer encoding")
                chunks: list[bytes] = []
                while True:
                    size_line = self.rfile.readline(128)
                    if not size_line:
                        raise ValueError("Unexpected end of chunked request")
                    size = int(size_line.split(b";", 1)[0].strip(), 16)
                    if size == 0:
                        while self.rfile.readline(8192) not in {b"\r\n", b"\n", b""}:
                            pass
                        return b"".join(chunks)
                    chunk = self.rfile.read(size)
                    if len(chunk) != size:
                        raise ValueError("Unexpected end of chunked request")
                    chunks.append(chunk)
                    if self.rfile.read(2) != b"\r\n":
                        raise ValueError("Malformed chunked request")
            length_text = self.headers.get("Content-Length")
            if not length_text:
                return b""
            length = int(length_text)
            if length < 0:
                raise ValueError("Invalid Content-Length")
            body = self.rfile.read(length)
            if len(body) != length:
                raise ValueError("Unexpected end of request body")
            return body

        def _local_error(self, status: int, code: str, message: str) -> None:
            payload = json.dumps({"error": {"type": code, "message": message}}, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(payload)
            self.close_connection = True

        def log_message(self, _format: str, *_args: Any) -> None:
            return

    return RequestLogHandler
