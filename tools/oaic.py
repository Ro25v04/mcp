from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fetch_oaic_guidance(topic: str) -> str:
        """Fetch privacy guidance from oaic.gov.au."""
        # TODO: paste scraping logic from ComplyIQ backend/mcp_servers/oaic.py
        raise NotImplementedError("Paste scraping logic here")
