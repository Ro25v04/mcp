import os
from mcp.server.fastmcp import FastMCP
from tools import register_all

mcp = FastMCP("shared-tools")
register_all(mcp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)