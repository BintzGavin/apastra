"""Compatibility launcher for the supported MCP server."""
import importlib
from pathlib import Path
import sys

package = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(package.parent))
sys.modules.setdefault("promptops", importlib.import_module(package.name))

from promptops.runtime.mcp_server import start_mcp_server


if __name__ == "__main__":
    start_mcp_server()
