from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fetch_legislation_tool(query: str) -> str:
        """Fetch Australian legislation summaries from legislation.gov.au."""
        # TODO: paste scraping logic from ComplyIQ backend/mcp_servers/legislation_au.py
        raise NotImplementedError("Paste scraping logic here")
