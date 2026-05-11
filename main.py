import os
from mcp.server.fastmcp import FastMCP
from tools.legislation_au import register as register_legislation
from tools.oaic import register as register_oaic

port = int(os.environ.get("PORT", 8001))

mcp = FastMCP("au-legislation-mcp", host="0.0.0.0", port=port)
register_legislation(mcp)
register_oaic(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse")
